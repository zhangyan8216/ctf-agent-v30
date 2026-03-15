#!/usr/bin/env python3
"""
高级 CTF 题目训练系统（真实世界高难度题目）
包含：Pwn, Reverse Engineering, Web Exploitation, Cryptography, Forensics
"""

import json
import os

# === 高难度真实 CTF 题目库 ===

ADVANCED_CTF_CHALLENGES = {
    "pwn_binary_exploitation": [
        {
            "name": "Buffer Overflow Basic",
            "category": "Pwn",
            "platform": "PicoCTF",
            "difficulty": "Medium",
            "description": "Exploit a buffer overflow vulnerability to read the flag from memory",
            "download_url": "https://github.com/picoCTF/2024-picoctf-writeups/tree/main/binary-exploitation/buffer-overflow-1",
            "points": 50,
            "flag_format": "picoCTF{...}",
            "techniques": ["buffer-overflow", "ret2win", "shellcode", "ROP"]
        },
        {
            "name": "Shellcode Injection",
            "category": "Pwn",
            "platform": "PicoCTF",
            "difficulty": "Medium",
            "description": "Inject shellcode into a vulnerable binary to spawn a shell",
            "download_url": "https://github.com/picoCTF/2024-picoctf-writeups/tree/main/binary-exploitation/shellcode",
            "points": 80,
            "flag_format": "picoCTF{...}",
            "techniques": ["shellcode", "injection", "no-exec-stack", "ret2libc"]
        },
        {
            "name": "Return to libc",
            "category": "Pwn",
            "platform": "PicoCTF",
            "difficulty": "Hard",
            "description": "Bypass NX protection using ROP chain with libc functions",
            "download_url": "https://github.com/picoCTF/2024-picoctf-writeups/tree/main/binary-exploitation/return-to-libc",
            "points": 100,
            "flag_format": "picoCTF{...}",
            "techniques": ["ROP", "ret2libc", "ASLR-bypass", "gadget-chaining"]
        }
    ],

    "reverse_engineering": [
        {
            "name": "Static Analysis",
            "category": "Reverse Engineering",
            "platform": "PicoCTF",
            "difficulty": "Medium",
            "description": "Analyze a stripped binary to extract the flag",
            "download_url": "https://github.com/picoCTF/2024-picoctf-writeups/tree/main/reverse-engineering/static-analysis",
            "points": 60,
            "flag_format": "picoCTF{...}",
            "techniques": ["Ghidra", "IDA", "objdump", "strace", "ltrace"]
        },
        {
            "name": "Dynamic Analysis",
            "category": "Reverse Engineering",
            "platform": "PicoCTF",
            "difficulty": "Hard",
            "description": "Debug a binary at runtime to bypass anti-debugging",
            "download_url": "https://github.com/picoCTF/2024-picoctf-writeups/tree/main/reverse-engineering/dynamic-analysis",
            "points": 90,
            "flag_format": "picoCTF{...}",
            "techniques": ["GDB", "ptrace", "anti-debug", "patching", "gdb-peda"]
        }
    ],

    "web_exploitation_advanced": [
        {
            "name": "SQL Injection Advanced",
            "category": "Web",
            "platform": "PicoCTF",
            "difficulty": "Medium",
            "description": "Advanced SQL injection with error-based, blind, and time-based techniques",
            "download_url": "https://github.com/picoCTF/2024-picoctf-writeups/tree/main/web/sqli-advanced",
            "points": 70,
            "flag_format": "picoCTF{...}",
            "techniques": ["union-based", "error-based", "blind-sqli", "time-based", "waf-bypass"]
        },
        {
            "name": "Server-Side Template Injection",
            "category": "Web",
            "platform": "PortSwigger Web Security Academy",
            "difficulty": "Hard",
            "description": "Exploit SSTI vulnerabilities in Jinja2 and Twig templates",
            "download_url": "https://portswigger.net/web-security/server-side-template-injection",
            "points": 120,
            "flag_format": "flag{...}",
            "techniques": ["SSTI", "Jinja2", "Twig", "template-injection", "RCE"]
        },
        {
            "name": "XXE Injection",
            "category": "Web",
            "platform": "PicoCTF",
            "difficulty": "Hard",
            "description": "Exploit XML External Entity injection to read files",
            "download_url": "https://github.com/picoCTF/2024-picoctf-writeups/tree/main/web/xxe",
            "points": 110,
            "flag_format": "picoCTF{...}",
            "techniques": ["XXE", "XML-parser", "file-read", "SSRF", "XXE-oob"]
        }
    ],

    "cryptography_advanced": [
        {
            "name": "RSA Padding Oracle",
            "category": "Cryptography",
            "platform": "CryptoHack",
            "difficulty": "Hard",
            "description": "Decrypt RSA ciphertext using padding oracle attack",
            "download_url": "https://cryptohack.org/challenges/padding_oracle",
            "points": 150,
            "flag_format": "crypto{...}",
            "techniques": ["RSA", "padding-oracle", "PKCS#1.5", "Bleichenbacher"]
        },
        {
            "name": "CBC Bit Flipping",
            "category": "Cryptography",
            "platform": "CryptoHack",
            "difficulty": "Medium",
            "description": "Manipulate CBC ciphertext to modify plaintext",
            "download_url": "https://cryptohack.org/challenges/cbc_bitflip",
            "points": 80,
            "flag_format": "crypto{...}",
            "techniques": ["AES-CBC", "bit-flipping", "IV-manipulation", "chosen-ciphertext"]
        },
        {
            "name": "ECC Curve Parameters",
            "category": "Cryptography",
            "platform": "CryptoHack",
            "difficulty": "Hard",
            "description": "Analyze elliptic curve parameters to recover private key",
            "download_url": "https://cryptohack.org/challenges/ecc_bad_parameters",
            "points": 140,
            "flag_format": "crypto{...}",
            "techniques": ["ECC", "curve-weakness", "private-key-recovery", "discrete-log"]
        }
    ],

    "forensics_advanced": [
        {
            "name": "Memory Forensics",
            "category": "Forensics",
            "platform": "PicoCTF",
            "difficulty": "Hard",
            "description": "Analyze a memory dump to extract hidden flag",
            "download_url": "https://github.com/picoCTF/2024-picoctf-writeups/tree/main/forensics/memory-forensics",
            "points": 130,
            "flag_format": "picoCTF{...}",
            "techniques": ["Volatility", "memory-dump", "process-injection", "kernel-structures"]
        },
        {
            "name": "PCAP Analysis",
            "category": "Forensics",
            "platform": "PicoCTF",
            "difficulty": "Medium",
            "description": "Extract flag from network packet capture file",
            "download_url": "https://github.com/picoCTF/2024-picoctf-writeups/tree/main/forensics/pcap-analysis",
            "points": 60,
            "flag_format": "picoCTF{...}",
            "techniques": ["Wireshark", "tshark", "packet-analysis", "network-protocols", "exfiltration"]
        },
        {
            "name": "Steganography Advanced",
            "category": "Forensics",
            "platform": "PicoCTF",
            "difficulty": "Hard",
            "description": "Hidden data in images using LSB and other advanced techniques",
            "download_url": "https://github.com/picoCTF/2024-picoctf-writeups/tree/main/forensics/steganography",
            "points": 100,
            "flag_format": "picoCTF{...}",
            "techniques": ["LSB", "EXIF", "image-stego", "polyglot-files", "metadata-analysis"]
        }
    ]
}

# === 创建高级 CTF 题目数据集 ===

def create_advanced_ctf_training():
    """创建高级 CTF 题目训练数据集"""

    print("🚀 创建高级 CTF 题目训练系统...")
    print("=" * 80)

    # 合并所有类别的题目
    all_challenges = []
    total_challenges = 0
    total_points = 0

    for category, challenges in ADVANCED_CTF_CHALLENGES.items():
        all_challenges.extend(challenges)
        total_challenges += len(challenges)
        total_points += sum(c["points"] for c in challenges)
        print(f"\n📁 {category.upper().replace('_', ' ')}:")
        print(f"   题目数: {len(challenges)} | 总分: {sum(c['points'] for c in challenges)}")
        for challenge in challenges:
            print(f"   • {challenge['name']} ({challenge['difficulty']}, {challenge['points']}分)")

    # 创建训练数据
    training_data = {
        "metadata": {
            "system": "Advanced CTF Training System",
            "version": "2.0",
            "total_categories": len(ADVANCED_CTF_CHALLENGES),
            "total_challenges": total_challenges,
            "total_points": total_points,
            "difficulty_distribution": {
                "Medium": sum(1 for c in all_challenges if c["difficulty"] == "Medium"),
                "Hard": sum(1 for c in all_challenges if c["difficulty"] == "Hard")
            }
        },
        "platforms": {
            "PicoCTF": sum(1 for c in all_challenges if "PicoCTF" in c["platform"]),
            "PortSwigger": sum(1 for c in all_challenges if "PortSwigger" in c["platform"]),
            "CryptoHack": sum(1 for c in all_challenges if "CryptoHack" in c["platform"])
        },
        "categories": {
            cat: {
                "count": len(chals),
                "difficulty": {
                    "Medium": sum(1 for c in chals if c["difficulty"] == "Medium"),
                    "Hard": sum(1 for c in chals if c["difficulty"] == "Hard")
                },
                "challenges": chals
            }
            for cat, chals in ADVANCED_CTF_CHALLENGES.items()
        }
    }

    # 保存训练数据
    training_file = "/advanced_ctf_training.json"
    with open(training_file, "w") as f:
        json.dump(training_data, f, indent=4)

    print("\n" + "=" * 80)
    print("📊 高级 CTF 题目训练系统创建完成！")
    print("=" * 80)
    print(f"📁 总类别: {len(ADVANCED_CTF_CHALLENGES)}")
    print(f"📊 总题目: {total_challenges}")
    print(f"🏆 总分: {total_points}")
    print(f"💾 数据已保存到: {training_file}")

    # 打印分类统计
    print("\n📈 难度分布:")
    print(f"   Medium: {training_data['metadata']['difficulty_distribution']['Medium']} 题")
    print(f"   Hard: {training_data['metadata']['difficulty_distribution']['Hard']} 题")

    print("\n🔗 平台分布:")
    for platform, count in training_data["platforms"].items():
        print(f"   • {platform}: {count} 题")

    print("=" * 80)

    return training_data

if __name__ == "__main__":
    result = create_advanced_ctf_training()

    print("\n✅ 高级 CTF 题目训练系统部署完成！")
    print("\n🎯 下一步:")
    print("1. 使用 REAL_WORLD_SOLVER.py 解决这些题目")
    print("2. 针对 Pwn、Reverse、Web Exploit 等高级类型进行训练")
    print("3. 实现自动 exploit 生成和利用")
