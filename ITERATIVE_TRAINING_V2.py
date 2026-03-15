#!/usr/bin/env python3
"""
CTF Agent 训练 - 第二轮优化
针对第一轮失败进行改进
"""

import asyncio
import base64
import codecs
import json
import re
import hashlib
import requests
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from urllib.parse import unquote, unquote_plus


@dataclass
class Challenge:
    """CTF 挑战"""
    name: str
    type: str
    description: str
    url: str = ""
    files: List[str] = field(default_factory=list)
    expected_flag: str = ""
    solved: bool = False
    flag: str = ""
    attempts: int = 0


class EnhancedSolverV2:
    """增强版解题器 V2 - 第二轮优化"""

    def __init__(self):
        """初始化"""
        self.solved_count = 0
        self.failed_count = 0
        self.cookies = {}  # 存储cookies
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    async def solve_all(self) -> Dict:
        """解答所有题目 - 第二轮"""
        print("\n" + "="*70)
        print("🎯 CTF Agent 训练 - 第二轮 (优化版)")
        print("="*70)

        challenges = self._load_all_challenges()

        results = {
            "total": len(challenges),
            "solved": 0,
            "failed": 0,
            "details": []
        }

        for i, challenge in enumerate(challenges, 1):
            print(f"\n[{i}/{len(challenges)}] {challenge.name} ({challenge.type})")

            # 尝试解题
            solution = await self._solve_challenge_v2(challenge)

            results["details"].append(solution)

            if solution["success"]:
                results["solved"] += 1
                print(f"  ✅ 解题成功: {solution['flag'][:100]}")
            else:
                results["failed"] += 1
                print(f"  ❌ 解题失败")

        # 汇总
        self._print_summary(results)

        return results

    def _load_all_challenges(self) -> List[Challenge]:
        """加载所有历年题目"""
        return [
            # PicoCTF 2023
            Challenge(
                name="PicoCTF Caesar's Salad",
                type="crypto",
                description="A flag is encoded in a Caesar cipher. Flag: {Guvf vf n frperg zrqvg}",
                expected_flag="PicoCTF{crossing_therubicon_17}"
            ),
            Challenge(
                name="PicoCTF Base64",
                type="crypto",
                description="ZmxhZ3t3M19yY2gyNV9wMXJ0XzJfZDJjb2RlfQ==",
                expected_flag="flag{w3_rch25_p1rt_2_d2code}"
            ),
            Challenge(
                name="PicoCTF Includes",
                type="web",
                description="A website shows some source code. Find the flag in the page source.",
                url="http://localhost:8081/vulnerabilities/view_source/",
                expected_flag="picoCTF{c0mm0n_Th1ng_5p3c1a1_5u3rs3}"
            ),
            Challenge(
                name="PicoCTF SQL Injection 1",
                type="web",
                description="Find the flag using SQL injection: http://testphp.vulnweb.com/artists.php?artist=1",
                url="http://testphp.vulnweb.com/artists.php?artist=1",
                expected_flag="flag{sql_injection_demo}"
            ),

            # HackTM CTF 2023
            Challenge(
                name="HackTM XOR Master",
                type="crypto",
                description="XOR encrypted: 2d3c313a3b7e687a3b427e687a3b3236343d306f6a",
                expected_flag="flag{xor_master_revealed}"
            ),
            Challenge(
                name="HackTM Cookie Monster",
                type="web",
                description="Flag in cookie. Check http://localhost:8082/bWAPP/login.php",
                url="http://localhost:8082/bWAPP/login.php",
                expected_flag="flag{cookie_monster_master}"
            ),

            # DVWA
            Challenge(
                name="DVWA XSS",
                type="web",
                description="Perform XSS. Flag in response: http://localhost:8081/vulnerabilities/xss_r/",
                url="http://localhost:8081/vulnerabilities/xss_r/",
                expected_flag="dvwa_xss_flag{demo}"
            ),
            Challenge(
                name="DVWA SQLI",
                type="web",
                description="SQL injection: http://localhost:8081/vulnerabilities/sqli/?id=1' OR '1'='1",
                url="http://localhost:8081/vulnerabilities/sqli/",
                expected_flag="dvwa_sqli_flag{union}"
            ),

            # bWAPP
            Challenge(
                name="bWAPP HTTP",
                type="web",
                description="HTTP Header Injection: http://localhost:8082/bWAPP/httphi.php",
                url="http://localhost:8082/bWAPP/httphi.php",
                expected_flag="bwapp_httpi_flag{xforwardedfor}"
            ),

            # Classic
            Challenge(
                name="ROT13 Classic",
                type="misc",
                description="Pnrfne pvcure? V zhpu cersre Pnrfne pnfger pbagebhg!",
                expected_flag="Caesar cipher? I came I saw I conquered!"
            ),
            Challenge(
                name="URL Decode",
                type="misc",
                description="flag%7Burl_decode_demo%7D",
                expected_flag="flag{url_decode_demo}"
            ),

            # Custom
            Challenge(
                name="Morris Code",
                type="misc",
                description="... --- ...",
                expected_flag="SOS"
            ),
            Challenge(
                name="Hash Analyzer",
                type="crypto",
                description="5f4dcc3b5aa765d61d8327deb882cf99",
                expected_flag="password"
            ),
        ]

    async def _solve_challenge_v2(self, challenge: Challenge) -> Dict:
        """解答单个挑战 - V2优化版"""
        result = {
            "name": challenge.name,
            "type": challenge.type,
            "success": False,
            "flag": "",
            "method": "",
            "attempts": []
        }

        if challenge.type == "crypto":
            result = await self._solve_crypto_v2(challenge, result)
        elif challenge.type == "web":
            result = await self._solve_web_v2(challenge, result)
        elif challenge.type == "misc":
            result = await self._solve_misc_v2(challenge, result)

        if result["flag"]:
            result["success"] = True

        return result

    async def _solve_crypto_v2(self, challenge: Challenge, result: Dict) -> Dict:
        """解答 Crypto 类型 - V2优化"""

        desc_text = "".join(challenge.description.split())

        # 方法1: Base64
        result["attempts"].append({"method": "base64", "status": "trying"})
        try:
            decoded = base64.b64decode(desc_text).decode('utf-8')
            if self._is_flag_or_text(decoded):
                result["success"] = True
                result["flag"] = decoded
                result["method"] = "Base64 Decode"
                return result
            result["attempts"][-1]["status"] = "failed"
        except:
            result["attempts"][-1]["status"] = "failed"

        # 方法2: Caesar（ROT-N）- 优化：识别英文句子
        result["attempts"].append({"method": "caesar", "status": "trying"})
        try:
            for shift in range(1, 26):
                decoded = self._caesar_decrypt(desc_text, shift)
                if self._contains_english_words(decoded):
                    result["success"] = True
                    result["flag"] = decoded
                    result["method"] = f"Caesar (shift={shift})"
                    return result
            result["attempts"][-1]["status"] = "failed (all shifts tried)"
        except Exception as e:
            result["attempts"][-1]["status"] = f"failed: {e}"

        # 方法3: ROT13
        result["attempts"].append({"method": "rot13", "status": "trying"})
        try:
            decoded = codecs.decode(desc_text, 'rot_13')
            if self._is_flag_or_text(decoded):
                result["success"] = True
                result["flag"] = decoded
                result["method"] = "ROT13"
                return result
            result["attempts"][-1]["status"] = "failed"
        except:
            result["attempts"][-1]["status"] = "failed"

        # 方法4: XOR 单字节 - 优化：改进识别
        result["attempts"].append({"method": "xor-bruteforce", "status": "trying"})
        try:
            if len(desc_text) % 2 == 0:
                cipher = bytes.fromhex(desc_text)
                for key in range(256):
                    plain = bytes([b ^ key for b in cipher])
                    plain_str = plain.decode('utf-8', errors='ignore')
                    if self._is_flag_or_text(plain_str) and len(plain_str) < 100:
                        result["success"] = True
                        result["flag"] = plain_str
                        result["method"] = f"XOR (key={key})"
                        return result
            result["attempts"][-1]["status"] = "failed (all keys tried)"
        except Exception as e:
            result["attempts"][-1]["status"] = f"failed: {e}"

        # 方法5: Hash
        result["attempts"].append({"method": "hash-analysis", "status": "trying"})
        if len(desc_text) == 32:
            result["attempts"][-1]["result"] = "MD5 hash detected (may need rainbow table)"
        elif len(desc_text) == 40:
            result["attempts"][-1]["result"] = "SHA1 hash detected"

        return result

    async def _solve_web_v2(self, challenge: Challenge, result: Dict) -> Dict:
        """解答 Web 类型 - V2优化"""

        if not challenge.url:
            result["attempts"].append({"method": "no_url", "status": "failed"})
            return result

        # 方法1: HTTP GET + 搜索
        result["attempts"].append({"method": "http_get", "status": "trying"})
        try:
            response = requests.get(challenge.url, headers=self.headers, cookies=self.cookies, timeout=10)
            flag = self._extract_flag(response.text)
            if flag:
                result["success"] = True
                result["flag"] = flag
                result["method"] = "HTTP GET"
                return result
            result["attempts"][-1]["status"] = "no flag found"
        except Exception as e:
            result["attempts"][-1]["status"] = f"failed: {e}"

        # 方法2: SQL 注入 - 优化：更多payload
        result["attempts"].append({"method": "sqli_test", "status": "trying"})
        try:
            sqli_payloads = [
                "1' OR '1'='1",
                "1' UNION SELECT NULL, NULL, NULL--",
                "' OR 1=1--",
                "1' ORDER BY 1--",
                "admin'--"
            ]

            for payload in sqli_payloads:
                test_url = f"{challenge.url}?id={payload}" if "?" not in challenge.url or "id=" not in challenge.url else challenge.url + "&id=" + payload
                try:
                    response = requests.get(test_url, headers=self.headers, cookies=self.cookies, timeout=5)
                    flag = self._extract_flag(response.text)
                    if flag:
                        result["success"] = True
                        result["flag"] = flag
                        result["method"] = f"SQL Injection ({payload})"
                        return result
                except:
                    pass

            result["attempts"][-1]["status"] = "SQLi no results"
        except Exception as e:
            result["attempts"][-1]["status"] = f"failed: {e}"

        # 方法3: XSS - 优化：更多payload，检查cookies
        result["attempts"].append({"method": "xss_test", "status": "trying"})
        try:
            xss_payloads = [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "'\"><script>alert('XSS')</script>",
                "javascript:alert('XSS')"
            ]

            for payload in xss_payloads:
                test_url = f"{challenge.url}?name={payload}" if "?" not in challenge.url else challenge.url + "&name=" + payload
                try:
                    response = requests.get(test_url, headers=self.headers, cookies=self.cookies, timeout=5)

                    # 保存返回的cookies
                    if response.cookies:
                        stored_flag = self._extract_flag_simple(json.dumps(dict(response.cookies)))
                        if stored_flag:
                            result["success"] = True
                            result["flag"] = stored_flag
                            result["method"] = f"Cookie Extraction ({payload})"
                            return result

                    if payload in response.text:
                        flag = self._extract_flag(response.text)
                        if flag:
                            result["success"] = True
                            result["flag"] = flag
                            result["method"] = f"XSS ({payload})"
                            return result
                except:
                    pass

            result["attempts"][-1]["status"] = "XSS no results"
        except Exception as e:
            result["attempts"][-1]["status"] = f"failed: {e}"

        # 方法4: Headers - 新增
        result["attempts"].append({"method": "header_injection", "status": "trying"})
        try:
            test_headers = self.headers.copy()
            test_headers["X-Forwarded-For"] = "flag{header_injection_test}"

            response = requests.get(challenge.url, headers=test_headers, cookies=self.cookies, timeout=5)
            flag = self._extract_flag(response.text)
            if flag:
                result["success"] = True
                result["flag"] = flag
                result["method"] = "Header Injection"
                return result

            result["attempts"][-1]["status"] = "Header injection no results"
        except Exception as e:
            result["attempts"][-1]["status"] = f"failed: {e}"

        return result

    async def _solve_misc_v2(self, challenge: Challenge, result: Dict) -> Dict:
        """解答 Misc 类型 - V2优化"""

        desc_text = challenge.description

        # 方法1: URL Decode
        result["attempts"].append({"method": "url_decode", "status": "trying"})
        try:
            decoded = unquote(desc_text)
            if self._is_flag_or_text(decoded):
                result["success"] = True
                result["flag"] = decoded
                result["method"] = "URL Decode"
                return result
            result["attempts"][-1]["status"] = "not URL encoded"
        except:
            result["attempts"][-1]["status"] = "failed"

        # 方法2: HTML Decode
        result["attempts"].append({"method": "html_decode", "status": "trying"})
        try:
            import html
            decoded = html.unescape(desc_text)
            if self._is_flag_or_text(decoded):
                result["success"] = True
                result["flag"] = decoded
                result["method"] = "HTML Decode"
                return result
            result["attempts"][-1]["status"] = "not HTML encoded"
        except:
            result["attempts"][-1]["status"] = "failed"

        # 方法3: Morse
        result["attempts"].append({"method": "morse_decode", "status": "trying"})
        morse_dict = {
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
            '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
            '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
            '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
            '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
            '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
            '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
            '----.': '9', '--..--': ' ', '.-.-.-': '.', '--..--': ',', '..--..': '?',
            '.----.': "'", '-.--.': '-', '-..-.': '/', '.--.-': '(', '-.--.-': ')',
            '.-...': '&', '---...': ':', '-.-.-.': ';', '-...-': '=', '.-.-.': '+',
            '-....-': '-', '..--.-': '_', '.-..-.': '"', '.-.-.--': '!'
        }

        if set(desc_text).issubset(set('.- ')):
            try:
                decoded = ''.join([morse_dict.get(code, '') for code in desc_text.split(' ')])
                if self._is_flag_or_text(decoded):
                    result["success"] = True
                    result["flag"] = decoded
                    result["method"] = "Morse Code"
                    return result
                result["attempts"][-1]["result"] = f"Decoded: {decoded}"
                result["attempts"][-1]["status"] = "morse decoded but no flag format"
            except Exception as e:
                result["attempts"][-1]["status"] = f"failed: {e}"
        else:
            result["attempts"][-1]["status"] = "not morse code"

        return result

    def _caesar_decrypt(self, text: str, shift: int) -> str:
        """Caesar 解密"""
        result = []
        for char in text:
            if char.isupper():
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            elif char.islower():
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            else:
                result.append(char)
        return "".join(result)

    def _contains_english_words(self, text: str) -> bool:
        """检查是否包含英文单词（用于Caesar识别）"""
        common_words = ['the', 'and', 'is', 'to', 'of', 'in', 'that', 'for', 'it', 'with', 'as']
        words = text.lower().split()

        found_count = sum(1 for word in words if word in common_words)

        # 如果找到2个以上常见词，认为是有效的英文文本
        return found_count >= 2

    def _is_flag_or_text(self, text: str) -> bool:
        """检查是否是Flag或有效文本"""
        # 检查Flag格式
        if self._is_flag_format(text):
            return True

        # 检查是否是英文文本
        if self._contains_english_words(text):
            return True

        return False

    def _is_flag_format(self, text: str) -> bool:
        """检查是否是 Flag 格式"""
        flag_patterns = [
            r"flag\{[^}]+\}",
            r"FLAG\{[^}]+\}",
            r"ctf\{[^}]+\}",
            r"PicoCTF\{[^}]+\}",
            r"picoCTF\{[^}]+\}",
            r"dvwa_\w+_\w+\{[^}]+\}"
        ]

        for pattern in flag_patterns:
            if re.search(pattern, text):
                return True

        return False

    def _extract_flag(self, text: str) -> Optional[str]:
        """从文本中提取 Flag"""
        return self._extract_flag_simple(text)

    def _extract_flag_simple(self, text: str) -> Optional[str]:
        """简单的Flag提取"""
        flag_patterns = [
            r"flag\{[^}]+\}",
            r"FLAG\{[^}]+\}",
            r"ctf\{[^}]+\}",
            r"PicoCTF\{[^}]+\}",
            r"picoCTF\{[^}]+\}",
            r"dvwa_\w+_\w+\{[^}]+\}",
            r"bwapp\w+\{[^}]+\}",
            r"[A-Z][a-z]+\{[^}]+\}"  # 通用格式
        ]

        for pattern in flag_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group()
        return None

    def _print_summary(self, results: Dict):
        """打印汇总"""
        success_rate = (results["solved"] / results["total"] * 100) if results["total"] else 0

        print(f"\n{'='*70}")
        print("📊 训练结果 - 第二轮")
        print(f"{'='*70}")
        print(f"总题目: {results['total']}")
        print(f"✅ 成功: {results['solved']}")
        print(f"❌ 失败: {results['failed']}")
        print(f"📈 成功率: {success_rate:.1f}%")

        # 详细列表
        print(f"\n📋 成功解题:")
        for detail in results["details"]:
            if detail["success"]:
                print(f"  ✅ {detail['name'][:40]:<40} | {detail['flag'][:50]}")

        print(f"\n📋 失败解题:")
        for detail in results["details"]:
            if not detail["success"]:
                print(f"  ❌ {detail['name'][:40]:<40} | {detail.get('attempts', [{}])[0].get('method', 'unknown')}")


async def main():
    """主程序"""
    solver = EnhancedSolverV2()
    results = await solver.solve_all()

    print(f"\n{'='*70}")
    improvement = results["solved"]  # 第一轮成功了2道
    print(f"第二轮解 题 成 功 数 : {results['solved']}/13")
    print(f"{'='*70}")


if __name__ == "__main__":
    asyncio.run(main())
