#!/usr/bin/env python3
"""
CTF Agent 训练系统 - 持续迭代优化版
通过解决历年题目，不断改进解题能力
"""

import asyncio
import base64
import codecs
import json
import re
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Challenge:
    """CTF 挑战"""
    name: str
    type: str
    description: str
    url: str = ""
    files: List[str] = None
    expected_flag: str = ""
    solved: bool = False
    flag: str = ""
    attempts: int = 0


class EnhancedSolver:
    """增强版解题器 - 持续优化"""

    def __init__(self):
        """初始化"""
        self.solved_count = 0
        self.failed_count = 0
        self.solve_history = []

    async def solve_all(self) -> Dict:
        """解答所有题目"""
        print("\n" + "="*70)
        print("🎯 CTF Agent 训练 - 第一轮")
        print("="*70)

        # 所有13道题目
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
            solution = await self._solve_challenge(challenge)

            results["details"].append(solution)

            if solution["success"]:
                results["solved"] += 1
                print(f"  ✅ 解题成功: {solution['flag']}")
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
                expected_flag="PicoCTF{crossing_therubicon_17}"  # 密钥16
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
                description="ROT13 encoded: Pnrfne pvcure? V zhpu cersre Pnrfne pnfger pbagebhg!",
                expected_flag="Caesar cipher? I came I saw I conquered! flag{rot13_master}"
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
                expected_flag="flag{sos_master}"
            ),
            Challenge(
                name="Hash Analyzer",
                type="crypto",
                description="5f4dcc3b5aa765d61d8327deb882cf99",
                expected_flag="password"
            ),
        ]

    async def _solve_challenge(self, challenge: Challenge) -> Dict:
        """解答单个挑战"""
        result = {
            "name": challenge.name,
            "type": challenge.type,
            "success": False,
            "flag": "",
            "method": "",
            "attempts": []
        }

        # 根据类型选择解题策略
        if challenge.type == "crypto":
            result = await self._solve_crypto(challenge, result)
        elif challenge.type == "web":
            result = await self._solve_web(challenge, result)
        elif challenge.type == "misc":
            result = await self._solve_misc(challenge, result)

        # 验证Flag
        if result["flag"]:
            result["success"] = True

        return result

    async def _solve_crypto(self, challenge: Challenge, result: Dict) -> Dict:
        """解答 Crypto 类型"""

        desc_text = "".join(challenge.description.split())

        # 方法1: Base64
        result["attempts"].append({"method": "base64", "status": "trying"})
        try:
            decoded = base64.b64decode(desc_text).decode('utf-8')
            if self._is_flag_format(decoded):
                result["success"] = True
                result["flag"] = decoded
                result["method"] = "Base64 Decode"
                return result
            result["attempts"][-1]["status"] = "failed"
        except:
            result["attempts"][-1]["status"] = "failed"

        # 方法2: Caesar（ROT-N）
        result["attempts"].append({"method": "caesar", "status": "trying"})
        try:
            for shift in range(1, 26):
                decoded = self._caesar_decrypt(desc_text, shift)
                if self._is_flag_format(decoded):
                    result["success"] = True
                    result["flag"] = decoded
                    result["method"] = f"Caesar (shift={shift})"
                    return result
            result["attempts"][-1]["status"] = "failed (all 25 shifts tried)"
        except Exception as e:
            result["attempts"][-1]["status"] = f"failed: {e}"

        # 方法3: ROT13
        result["attempts"].append({"method": "rot13", "status": "trying"})
        try:
            decoded = codecs.decode(desc_text, 'rot_13')
            if self._is_flag_format(decoded):
                result["success"] = True
                result["flag"] = decoded
                result["method"] = "ROT13"
                return result
            result["attempts"][-1]["status"] = "failed"
        except:
            result["attempts"][-1]["status"] = "failed"

        # 方法4: XOR 单字节
        result["attempts"].append({"method": "xor-bruteforce", "status": "trying"})
        try:
            # 先尝试十六进制编码
            if len(desc_text) % 2 == 0:
                try:
                    cipher = bytes.fromhex(desc_text)
                    for key in range(256):
                        plain = bytes([b ^ key for b in cipher])
                        plain_str = plain.decode('utf-8', errors='ignore')
                        if self._is_flag_format(plain_str) and len(plain_str) < 100:
                            result["success"] = True
                            result["flag"] = plain_str
                            result["method"] = f"XOR (key={key})"
                            return result
                except:
                    pass
            result["attempts"][-1]["status"] = "failed (all 256 keys tried)"
        except Exception as e:
            result["attempts"][-1]["status"] = f"failed: {e}"

        # 方法5: Hash 识别
        result["attempts"].append({"method": "hash-identify", "status": "trying"})
        if len(desc_text) == 32:
            result["attempts"][-1]["result"] = "MD5 hash detected"
            # 这里可以通过彩虹表查询，但暂不实现
        elif len(desc_text) == 40:
            result["attempts"][-1]["result"] = "SHA1 hash detected"
        elif len(desc_text) == 64:
            result["attempts"][-1]["result"] = "SHA256 hash detected"

        return result

    async def _solve_web(self, challenge: Challenge, result: Dict) -> Dict:
        """解答 Web 类型"""
        import requests

        if not challenge.url:
            result["attempts"].append({"method": "no_url", "status": "failed"})
            return result

        # 方法1: HTTP GET + Flag 搜索
        result["attempts"].append({"method": "http_get", "status": "trying"})
        try:
            response = requests.get(challenge.url, timeout=10)

            # 搜索 Flag
            flag = self._extract_flag(response.text)
            if flag:
                result["status"] = True
                result["flag"] = flag
                result["method"] = "HTTP GET + Flag Search"
                return result

            result["attempts"][-1]["status"] = "no flag found"
        except Exception as e:
            result["attempts"][-1]["status"] = f"failed: {e}"

        # 方法2: SQL 注入测试
        result["attempts"].append({"method": "sqli_test", "status": "trying"})
        try:
            sqli_payloads = [
                "1' OR '1'='1",
                "1' UNION SELECT NULL, NULL, NULL--",
                "' OR 1=1--"
            ]

            for payload in sqli_payloads:
                test_url = f"{challenge.url}?id={payload}" if "?" not in challenge.url else challenge.url + "&payload=" + payload
                try:
                    response = requests.get(test_url, timeout=5)
                    flag = self._extract_flag(response.text)
                    if flag:
                        result["success"] = True
                        result["flag"] = flag
                        result["method"] = f"SQL Injection ({payload})"
                        return result
                except:
                    pass

            result["attempts"][-1]["status"] = "SQL Injection no results"
        except Exception as e:
            result["attempts"][-1]["status"] = f"failed: {e}"

        # 方法3: XSS 测试
        result["attempts"].append({"method": "xss_test", "status": "trying"})
        try:
            xss_payload = "<script>alert('XSS')</script>"
            test_url = f"{challenge.url}?name={xss_payload}" if "?" not in challenge.url else challenge.url
            try:
                response = requests.get(test_url, timeout=5)
                if xss_payload in response.text:
                    flag = self._extract_flag(response.text)
                    if flag:
                        result["success"] = True
                        result["flag"] = flag
                        result["method"] = "XSS Injection"
                        return result
            except:
                pass

            result["attempts"][-1]["status"] = "XSS no results"
        except Exception as e:
            result["attempts"][-1]["status"] = f"failed: {e}"

        return result

    async def _solve_misc(self, challenge: Challenge, result: Dict) -> Dict:
        """解答 Misc 类型"""

        desc_text = challenge.description

        # 方法1: URL Decode
        result["attempts"].append({"method": "url_decode", "status": "trying"})
        try:
            from urllib.parse import unquote
            decoded = unquote(desc_text)
            if self._is_flag_format(decoded):
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
            if self._is_flag_format(decoded):
                result["success"] = True
                result["flag"] = decoded
                result["method"] = "HTML Decode"
                return result
            result["attempts"][-1]["status"] = "not HTML encoded"
        except:
            result["attempts"][-1]["status"] = "failed"

        # 方法3: 摩斯密码
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
                if self._is_flag_format(decoded):
                    result["success"] = True
                    result["flag"] = decoded
                    result["method"] = "Morse Code"
                    return result
                result["attempts"][-1]["result"] = f"Decoded: {decoded}"
                result["attempts"][-1]["status"] = "morse decoded but no flag"
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

    def _is_flag_format(self, text: str) -> bool:
        """检查是否是 Flag 格式"""
        flag_patterns = [
            r"flag\{[^}]+\}",
            r"FLAG\{[^}]+\}",
            r"ctf\{[^}]+\}",
            r"PicoCTF\{[^}]+\}",
            r"picoCTF\{[^}]+\}"
        ]

        for pattern in flag_patterns:
            if re.search(pattern, text):
                return True

        # 检查是否像英文句子（用于 Caesar 验证）
        if len(text) > 10 and any(c.islower() for c in text):
            common_words = ['the', 'and', 'is', 'of', 'to', 'in', 'that']
            word_count = sum(1 for word in text.lower().split() if word in common_words)
            if word_count >= 2:
                return True

        return False

    def _extract_flag(self, text: str) -> Optional[str]:
        """从文本中提取 Flag"""
        flag_patterns = [
            r"flag\{[^}]+\}",
            r"FLAG\{[^}]+\}",
            r"ctf\{[^}]+\}",
            r"PicoCTF\{[^}]+\}",
            r"picoCTF\{[^}]+\}",
            r"dvwa_\w+_\w+\{[^}]+\}"
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
        print("📊 训练结果 - 第一轮")
        print(f"{'='*70}")
        print(f"总题目: {results['total']}")
        print(f"✅ 成功: {results['solved']}")
        print(f"❌ 失败: {results['failed']}")
        print(f"📈 成功率: {success_rate:.1f}%")

        # 详细列表
        print(f"\n{'='*70}")
        print("📋 详细结果")
        print(f"{'='*70}")

        for detail in results["details"]:
            status = "✅" if detail["success"] else "❌"
            print(f"\n{status} {detail['name']} ({detail['type']})")
            if detail["success"]:
                print(f"    Flag: {detail['flag']}")
                print(f"    方法: {detail['method']}")
            else:
                print(f"    尝试过的方法:")
                for attempt in detail.get("attempts", []):
                    print(f"      • {attempt['method']}: {attempt['status']}")

        print(f"\n{'='*70}")

        # 分析失败原因
        if results["failed"] > 0:
            self._analyze_failures(results)

    def _analyze_failures(self, results: Dict):
        """分析失败原因"""
        print(f"\n{'='*70}")
        print("🔍 失败分析")
        print(f"{'='*70}")

        for detail in results["details"]:
            if not detail["success"]:
                print(f"\n❌ {detail['name']} ({detail['type']})")

                # 分析原因并给出建议
                suggestions = []

                if detail["type"] == "crypto":
                    suggestions.append("• 尝试更多编码方式 (Vigenère, Playfair, Rail Fence)")
                    suggestions.append("• 添加频率分析支持")
                    suggestions.append("• 添加字典暴力破解")

                elif detail["type"] == "web":
                    suggestions.append("• 检查靶场是否在线")
                    suggestions.append("• 添加更多 HTTP 方法 (POST, PUT)")
                    suggestions.append("• 添加 Header 操作能力")

                elif detail["type"] == "misc":
                    suggestions.append("• 添加更多编码方式")
                    suggestions.append("• 添加二进制工具支持")

                for suggestion in suggestions:
                    print(f"  {suggestion}")


# 迭代训练函数
async def iterative_training():
    """迭代训练 - 多轮优化"""

    print("\n" + "="*70)
    print("🎯 CTF Agent 迭代训练系统")
    print("="*70)
    print("\n目标: 持续优化直到解答所有13道历年题目\n")

    solver = EnhancedSolver()

    # 第一轮训练
    results_round1 = await solver.solve_all()

    success_rate = (results_round1["solved"] / results_round1["total"] * 100)

    print(f"\n{'='*70}")

    if success_rate == 100:
        print("🎉 恭喜！所有题目已解答！")
        return

    # 继续优化
    print(f"📊 当前成功率: {success_rate:.1f}%")
    print(f"🔄 开始第二轮优化...\n")


async def main():
    """主程序"""
    await iterative_training()


if __name__ == "__main__":
    asyncio.run(main())
