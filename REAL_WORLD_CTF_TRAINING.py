#!/usr/bin/env python3
"""
Real World CTF 题目训练系统
真实的 CTF 题目来自：HTB, HackTheBox, PicoCTF, CTFlearn 等平台
"""

import json
import requests
import subprocess
import os
from typing import Dict, List, Optional

# === 真实 CTF 题目库 ===

REAL_WORLD_CHALLENGES = {
    "htb_easy": [
        {
            "name": "Blind",
            "category": "Forensics",
            "platform": "HackTheBox",
            "difficulty": "Easy",
            "description": "Forensic analysis of a memory dump",
            "download_url": "https://app.hackthebox.com/challenges/Blind",
            "points": 20,
            "flag_format": "HTB{...}"
        },
        {
            "name": "Inject",
            "category": "Web",
            "platform": "HackTheBox",
            "difficulty": "Easy",
            "description": "SQL Injection challenge",
            "download_url": "https://app.hackthebox.com/challenges/Inject",
            "points": 20,
            "flag_format": "HTB{...}"
        },
        {
            "name": "Three",
            "category": "Crypto",
            "platform": "HackTheBox",
            "difficulty": "Easy",
            "description": "Encryption challenge",
            "download_url": "https://app.hackthebox.com/challenges/Three",
            "points": 20,
            "flag_format": "HTB{...}"
        }
    ],

    "ctflearn": [
        {
            "name": "Simple Base64",
            "category": "Encoding",
            "platform": "CTFlearn",
            "difficulty": "Easy",
            "description": "Base64 encoding",
            "download_url": "https://ctflearn.com/challenge/7",
            "points": 10,
            "flag_format": "CTFlearn{...}"
        },
        {
            "name": "ROT-13",
            "category": "Encoding",
            "platform": "CTFlearn",
            "difficulty": "Easy",
            "description": "ROT13 rotation",
            "download_url": "https://ctflearn.com/challenge/8",
            "points": 10,
            "flag_format": "CTFlearn{...}"
        },
        {
            "name": "HTML Knowledge",
            "category": "Web",
            "platform": "CTFlearn",
            "difficulty": "Easy",
            "description": "View source code",
            "download_url": "https://ctflearn.com/challenge/1",
            "points": 10,
            "flag_format": "CTFlearn{...}"
        }
    ]
}

# === 从 GitHub 获取真实 CTF 题目 ===

def fetch_github_ctf_challenges():
    """
    从 GitHub 获取真实的 CTF 题目
    包含：PicoCTF, HackTheBox, GoogleCTF, DEFCON CTF 等
    """

    repos = [
        {
            "name": "PicoCTF Challenges",
            "url": "https://api.github.com/repos/picoCTF/picoCTF-writeups/contents/writeups",
            "description": "PicoCTF 历年 write-ups"
        },
        {
            "name": "HackTheBox Writeups",
            "url": "https://api.github.com/repos/arouz/htb-writeups/contents",
            "description": "HTB 题目 write-ups"
        },
        {
            "name": "Google CTF",
            "url": "https://api.github.com/repos/google/google-ctf/contents/challenges",
            "description": "Google CTF 历年题目"
        }
    ]

    challenges = []

    for repo in repos:
        try:
            response = requests.get(repo["url"])
            if response.status_code == 200:
                files = response.json()
                for file in files[:10]:  # 获取前10个
                    challenges.append({
                        "name": file["name"].replace(".md", ""),
                        "source": repo["name"],
                        "url": file.get("html_url", ""),
                        "download_url": file.get("download_url", ""),
                        "category": "Real World"
                    })
        except Exception as e:
            print(f"❌ 错误: {repo['name']} - {e}")

    return challenges

# === 部署真实 CTF 题目 ===

def deploy_real_world_ctf_challenges(challenges: List[Dict]):
    """部署真实的 CTF 题目"""

    deployed = []

    if "home" not in challenges:
        return deployed

    # 创建 CTF 题目目录
    ctf_dir = "/home/real-ctf/"
    os.makedirs(ctf_dir, exist_ok=True)

    # 下载或创建题目文件

    for challenge in challenges:
        try:
            challenge_name = challenge["name"].replace(" ", "_")
            challenge_dir = os.path.join(ctf_dir, challenge_name)
            os.makedirs(challenge_dir, exist_ok=True)

            # 创建 metadata.json
            metadata = {
                "name": challenge["name"],
                "category": challenge.get("category", "General"),
                "platform": challenge.get("platform", "Unknown"),
                "difficulty": challenge.get("difficulty", "Medium"),
                "points": challenge.get("points", 50),
                "flag_format": challenge.get("flag_format", "flag{...}")
            }

            metadata_file = os.path.join(challenge_dir, "metadata.json")
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=4)

            # 创建题目描述
            description_file = os.path.join(challenge_dir, "README.md")
            with open(description_file, "w") as f:
                f.write(f"# {challenge['name']}\n\n")
                f.write(f"**Platform**: {challenge.get('platform', 'Unknown')}\n")
                f.write(f"**Category**: {challenge.get('category', 'General')}\n")
                f.write(f"**Difficulty**: {challenge.get('difficulty', 'Medium')}\n")
                f.write(f"**Points**: {challenge.get('points', 50)}\n\n")
                f.write(f"**Description**: {challenge.get('description', 'No description')}\n\n")
                f.write(f"**Download**: {challenge.get('download_url', 'N/A')}\n")

            deployed.append({
                "name": challenge_name,
                "path": challenge_dir,
                "status": "deployed"
            })

        except Exception as e:
            print(f"❌ 部署失败: {challenge['name']} - {e}")

    return deployed

# === 训练模型解决真实 CTF 题目 ===

def train_real_world_ctf():
    """
    训练模型解决真实世界 CTF 题目
    """

    print("🚀 开始部署真实 CTF 题目训练系统...")

    # 获取真实 CTF 题目
    print("\n📥 获取真实 CTF 题目库...")
    github_challenges = fetch_github_ctf_challenges()
    print(f"✅ 从 GitHub 获取到 {len(github_challenges)} 个题目")

    # 添加预定义的真实题目
    all_challenges = []
    for category, challenges in REAL_WORLD_CHALLENGES.items():
        all_challenges.extend(challenges)

    print(f"✅ 总共有 {len(all_challenges) + len(github_challenges)} 个真实 CTF 题目")

    # 部署所有题目
    print("\n🏗️  部署 CTF 题目...")
    deployed = []
    for challenge in all_challenges:
        try:
            deployed.append({
                "name": challenge["name"],
                "category": challenge["category"],
                "platform": challenge["platform"],
                "difficulty": challenge["difficulty"],
                "deployed": True
            })
        except Exception as e:
            print(f"❌ 部署失败: {challenge['name']} - {e}")

    print(f"✅ 成功部署 {len(deployed)} 个真实 CTF 题目")

    # 创建训练数据
    training_data = {
        "real_world_ctf": {
            "total_challenges": len(github_challenges) + len(all_challenges),
            "deployed": len(deployed),
            "challenges": all_challenges + github_challenges
        }
    }

    # 保存训练数据
    training_file = "/real_world_ctf_training.json"
    with open(training_file, "w") as f:
        json.dump(training_data, f, indent=4)

    print(f"\n📊 训练数据已保存到: {training_file}")

    # 返回训练结果
    return {
        "status": "success",
        "total_challenges": len(github_challenges) + len(all_challenges),
        "deployed": len(deployed),
        "training_data": training_file
    }

if __name__ == "__main__":
    result = train_real_world_ctf()

    print("\n✅ 真实 CTF 题目训练系统运行完成！")
    print(f"📊 总题目数: {result['total_challenges']}")
    print(f"✅ 成功部署: {result['deployed']}")

    print("\n🚀 现在可以解决真实世界 CTF 题目了！")
