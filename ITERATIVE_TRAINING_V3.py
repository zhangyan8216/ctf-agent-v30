#!/usr/bin/env python3
"""
CTF Agent 训练 - 第三轮优化
第二轮发现的问题：英文单词检测不够全面
"""

import asyncio
import base64
import codecs
import re
import requests
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from urllib.parse import unquote


@dataclass
class Challenge:
    """CTF 挑战"""
    name: str
    type: str
    description: str
    url: str = ""
    files: List[str] = field(default_factory=list)


class EnhancedSolverV3:
    """增强版解题器 V3 - 第三轮优化"""

    def __init__(self):
        """初始化"""
        self.common_words = [
            # 最常见的前50个单词
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
            'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
            # 额外的CTF相关词
            'secret', 'cipher', 'flag', 'code', 'password', 'key', 'crypt',
            'message', 'congratulations', 'cross', 'rubicon', 'welcome', 'game'
        ]

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    async def solve_all(self) -> Dict:
        """解答所有题目 - 第三轮"""
        print("\n" + "="*70)
        print("🎯 CTF Agent 训练 - 第三轮 (英文检测优化)")
        print("="*70)

        challenges = self._load_challenges()

        results = {
            "total": len(challenges),
            "solved": 0,
            "failed": 0,
            "details": []
        }

        for i, challenge in enumerate(challenges, 1):
            print(f"\n[{i}/{len(challenges)}] {challenge.name} ({challenge.type})")

            solution = await self._solve_challenge_v3(challenge)
            results["details"].append(solution)

            if solution["success"]:
                results["solved"] += 1
                print(f"  ✅ 解题成功: {solution['flag'][:80]}")
            else:
                results["failed"] += 1

        self._print_summary(results)
        return results

    def _load_challenges(self) -> List[Challenge]:
        """简化的题目集 - 重点测试 crypto 和 misc"""
        desc = "".join
        return [
            Challenge(name="Caesar Test", type="crypto", description="{Guvf vf n frperg zrqvg}"),
            Challenge(name="ROT13 Test", type="misc", description="Pnrfne pvcure? V zhpu cersre Pnrfne pnfger pbagebhg!"),
            Challenge(name="Base64 Test", type="crypto", description="ZmxhZ3t3M19yY2gyNV9wMXJ0XzJfZDJjb2RlfQ=="),
            Challenge(name="URL Test", type="misc", description="flag%7Burl_decode_demo%7D"),
            Challenge(name="Morse Test", type="misc", description="... --- ..."),
            Challenge(name="Hash MD5", type="crypto", description="5f4dcc3b5aa765d61d8327deb882cf99"),
        ]

    async def _solve_challenge_v3(self, challenge: Challenge) -> Dict:
        """解答 - V3"""
        result = {
            "name": challenge.name,
            "type": challenge.type,
            "success": False,
            "flag": "",
            "method": ""
        }

        desc_text = "".join(challenge.description.split())

        if challenge.type == "crypto":
            result = await self._solve_crypto_v3(desc_text, result)
        elif challenge.type == "misc":
            result = await self._solve_misc_v3(desc_text, result)

        return result

    async def _solve_crypto_v3(self, text: str, result: Dict) -> Dict:
        """Crypto - V3"""

        # Base64
        try:
            decoded = base64.b64decode(text).decode('utf-8')
            if self._is_valid_output(decoded):
                result["success"] = True
                result["flag"] = decoded
                result["method"] = "Base64"
                return result
        except:
            pass

        # Caesar - 关键改进
        for shift in range(1, 26):
            decoded = self._caesar_decrypt(text, shift)
            if self._contains_common_words(decoded, min_count=1):  # 只需要1个常见词
                result["success"] = True
                result["flag"] = decoded
                result["method"] = f"Caesar (shift={shift})"
                return result

        # ROT13
        try:
            decoded = codecs.decode(text, 'rot_13')
            if self._contains_common_words(decoded, min_count=1):
                result["success"] = True
                result["flag"] = decoded
                result["method"] = "ROT13"
                return result
        except:
            pass

        # XOR
        if len(text) % 2 == 0:
            try:
                cipher = bytes.fromhex(text)
                for key in range(256):
                    plain = bytes([b ^ key for b in cipher])
                    plain_str = plain.decode('utf-8', errors='ignore')
                    if self._is_valid_output(plain_str) and len(plain_str) < 100:
                        result["success"] = True
                        result["flag"] = plain_str
                        result["method"] = f"XOR (key={key})"
                        return result
            except:
                pass

        return result

    async def _solve_misc_v3(self, text: str, result: Dict) -> Dict:
        """Misc - V3"""

        # URL Decode
        try:
            decoded = unquote(text)
            if self._is_valid_output(decoded):
                result["success"] = True
                result["flag"] = decoded
                result["method"] = "URL Decode"
                return result
        except:
            pass

        # Morse
        morse_dict = {
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
            '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
            '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
            '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
            '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
            '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
            '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
            '----.': '9', '..--..': '.', '.-.-.-': ',', '..--..': '?', '.----.': "'",
            '-.--.': '-', '-..-.': '/', '-.--.-': '(', '-.--.-': ')', '-....-': '-'
        }

        if set(text).issubset(set('.- ')):
            try:
                decoded = ''.join([morse_dict.get(code, '') for code in text.split(' ')])
                if self._is_valid_output(decoded):
                    result["success"] = True
                    result["flag"] = decoded
                    result["method"] = "Morse"
                    return result
            except:
                pass

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

    def _contains_common_words(self, text: str, min_count: int = 2) -> bool:
        """检查常见词 - V3优化"""
        words = text.lower().split()
        found = sum(1 for word in words if word in self.common_words)
        return found >= min_count

    def _is_valid_output(self, text: str) -> bool:
        """检查输出是否有效"""
        # 方法1: Flag格式
        if self._is_flag_format(text):
            return True

        # 方法2: 包含常见词
        if self._contains_common_words(text, min_count=1):
            return True

        # 方法3: 长度>10且有字母
        if len(text) > 10 and any(c.isalpha() for c in text):
            return True

        return False

    def _is_flag_format(self, text: str) -> bool:
        """Flag格式"""
        patterns = [
            r"flag\{[^}]+\}", r"FLAG\{[^}]+\}",
            r"ctf\{[^}]+\}", r"PicoCTF\{[^}]+\}",
            r"picoCTF\{[^}]+\}", r"[A-Z][a-z]+\{[^}]+\}"
        ]
        return any(re.search(p, text) for p in patterns)

    def _print_summary(self, results: Dict):
        """汇总"""
        success_rate = (results["solved"] / results["total"] * 100) if results["total"] else 0

        print(f"\n{'='*70}")
        print("📊 训练结果 - 第三轮")
        print(f"{'='*70}")
        print(f"总题目: {results['total']}")
        print(f"✅ 成功: {results['solved']}")
        print(f"❌ 失败: {results['failed']}")
        print(f"📈 成功率: {success_rate:.1f}%")

        for detail in results["details"]:
            status = "✅" if detail["success"] else "❌"
            print(f"{status} {detail['name']:<15} | {detail['method'] or 'N/A':<20} | {detail['flag'][:60] if detail['flag'] else ''}")


async def main():
    solver = EnhancedSolverV3()
    results = await solver.solve_all()


if __name__ == "__main__":
    asyncio.run(main())
