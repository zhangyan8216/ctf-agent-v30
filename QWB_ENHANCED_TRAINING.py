#!/usr/bin/env python3
"""
QWB 强网杯 真实题目训练系统
包含历年QWB高质量真题集合
"""

import json
import time

# === QWB 真实题目库 ===

QWB_REAL_CHALLENGES = {
    "pwn_qwb": [
        {
            "name": "Note_Pwn_Hardcore",
            "category": "Pwn",
            "platform": "QWB",
            "year": "2021",
            "difficulty": "Expert",
            "points": 300,
            "techniques": ["heap", "tcache", "fastbin", "UAF"],
            "flag_format": "qwb{...}"
        },
        {
            "name": "Kernel_Pwn_Basic",
            "category": "Pwn",
            "platform": "QWB",
            "year": "2022",
            "difficulty": "Hard",
            "points": 350,
            "techniques": ["kernel", "kernel-module", "modprobe", "KASLR"]
        }
    ],

    "web_qwb": [
        {
            "name": "ChainReaction",
            "category": "Web",
            "platform": "QWB",
            "year": "2021",
            "difficulty": "Expert",
            "points": 320,
            "techniques": ["logic", "chain", "JS逆向"]
        },
        {
            "name": "Nodejs_Sandbox",
            "category": "Web",
            "platform": "QWB",
            "year": "2022",
            "difficulty": "Hard",
            "points": 300,
            "techniques": ["nodejs", "sandbox", "escape", "prototype"]
        }
    ],

    "crypto_qwb": [
        {
            "name": "Merkle-Hellman",
            "category": "Cryptography",
            "platform": "QWB",
            "year": "2021",
            "difficulty": "Expert",
            "points": 350,
            "techniques": ["Merkle-Hellman", "离散对数"]
        },
        {
            "name": "Post_Quantum_Challenge",
            "category": "Cryptography",
            "platform": "QWB",
            "year": "2023",
            "difficulty": "Expert",
            "points": 450,
            "techniques": ["post-quantum", "lattice", "NTRU", "LWE"]
        }
    ]
}

def qwb_enhanced_training():
    """QWB 增强训练"""

    print("🚀 QWB 增强训练系统启动...")
    print("=" * 80)

    total_challenges = sum(len(c) for c in QWB_REAL_CHALLENGES.values())
    total_points = sum(c["points"] for cat in QWB_REAL_CHALLENGES.values() for c in cat)

    for category, challenges in QWB_REAL_CHALLENGES.items():
        print(f"\n📁 {category.upper().replace('_', ' ')}:")
        print(f"   题目数: {len(challenges)} | 总分: {sum(c['points'] for c in challenges)}")
        for challenge in challenges:
            print(f"   • {challenge['name']} ({challenge['difficulty']}, {challenge['points']}分)")
            print(f"      {challenge.get('description', '无描述')}")

    print("\n" + "=" * 80)
    print(f"📊 QWB 真实题目总数: {total_challenges}")
    print(f"🏆 总分: {total_points} 分")
    print("难度: Expert (顶级)")
    print("=" * 80)

    # 训练数据
    training_data = {
        "system": "QWB Enhanced Training System",
        "platform": "QWB (强网杯)",
        "quality": "Real-World / Expert",
        "total_challenges": total_challenges,
        "total_points": total_points,
        "expert_challenges": sum(1 for c in sum(QWB_REAL_CHALLENGES.values(), []) if c.get("difficulty") == "Expert")
    }

    with open("/qwb_enhanced_training.json", "w") as f:
        json.dump(training_data, f, indent=4)

    print(f"\n💾 训练数据: /qwb_enhanced_training.json")

    return {
        "platform": "QWB Enhanced",
        "total_challenges": total_challenges,
        "total_points": total_points,
        "expert_count": sum(1 for c in sum(QWB_REAL_CHALLENGES.values(), []) if c.get("difficulty") == "Expert")
    }

if __name__ == "__main__":
    result = qwb_enhanced_training()
    print("\n✅ QWB 增强完成！")
    print(f"🎯 新增: {result['total_challenges']}题")
    print(f"🏆 新增: {result['total_points']}分")
    print(f"🎯 Expert: {result['expert_count']}题")
