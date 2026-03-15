#!/usr/bin/env python3
"""
JSON文件作用说明文档
解释仓库中各JSON文件的作用
"""

import json
import os

print("=" * 80)
print("📁 JSON文件作用说明")
print("=" * 80)

# 所有JSON文件列表
json_files = [
    ("training_data.json", "历年CTF题目数据（13题）"),
    ("real_world_ctf_training.json", "真实题目数据（6题 HackTheBox+CTFlearn）"),
    ("agent_training_final.json", "高级题目数据（14题）"),
    ("xctf_training.json", "XCTF 2022-2023题目（10题）"),
    ("bctf_training.json", "BCTF（蓝莲花）题目（9题）"),
    ("octf_training.json", "0CTF（零CTF）题目（5题）"),
    ("qwb_training.json", "QWB（强网杯）题目（4题）"),
    ("lilctf2025_training.json", "LILCTF2025最新题目（10题）"),
    ("advanced_ctf_training.json", "扩展题目数据（8题）"),
    ("expanded_ctf_training.json", "扩展平台（8题）"),
    ("cctf_training.json", "CCTF题目数据（10题）"),
    ("bytectf_training.json", "ByteCTF题目数据（6题）"),
    ("defcon_training.json", "DEFCON题目数据（5题）"),
    ("qwb_enhanced_training.json", "QWB增强版题目（6题）"),
    ("round6_data.json", "第6轮新数据（8题）"),
    ("round7_data.json", "第7轮新数据（6题）"),
    ("round8_data.json", "第8轮新数据（6题）"),
    ("round9_data.json", "第9轮新数据（6题）"),
]

# 按组分类
training_files = {
    "核心训练系统": ["training_data.json", "agent_training_final.json"],
    "真实题目系统": ["real_world_ctf_training.json", "cctf.json", "qwb.json", "bytectf.json"],
    "高级扩展": ["advanced_ctf_training.json", "expanded_ctf_training.json"],
    "第6-9轮迭代": ["round6_data.json", "round7_data.json", "round8_data.json", "round9_data.json"]
}

print("\n" + "=" * 80)
print("✅ 这些JSON文件是项目的核心功能数据！")
print("=" * 80)

# 详细说明
print("\n📊 基础训练系统（历年真题）")
print("  • training_data.json: 历年13道CTF真题数据（PicoCTF, HackTM等）")
print("  • 记录: 题目名称、难度、分数、flag格式、技术")

print("\n📊 真实题目系统（真实平台）")
print("  • real_world_ctf_training.json: HackTheBox+CTlearn 6题")
print("  • xctf.json: 中国CTF 16题")
print("  • bctf.json: 蓝莲花 9题")
print("  • qwb.json: 强网杯 4题")

print("\n📊 高级训练系统（Expert）")
print("  • agent_training_final.json: 高级题目14题（PicoCTF/CryptoHack/PortSwigger）")

print("\n✅ JSON文件的作用:")
print("  • 存储题目数据和元数据")
print("  • 记录解题结果和flag")
print("  • 支持脚本读取和生成")
print("  • 实现自动化训练和解题")
print("  • 提供可视化展示")

print("\n📂 核心工作流程:")
print("  1. 读取JSON训练数据 → 解析题目元数据")
print("  2. 匹配置规则/工具 → 生成解题方案")
print("  3. 执行解题脚本 → 保存结果到JSON")
print("  4. 读取结果JSON → 生成报告")

print("\n🎯 这些JSON文件让你的项目具备：")
print("  • 可溯源的结果记录")
print("  • 元数据驱动的系统")
print("  • 可扩展的训练框架")
print("  • 自动化能力")

print("\n💡 僡试性:")
print("  • JSON比硬编码灵活100倍")
print("  • 易于添加新题目和数据")
print("  • 支持版本管理（git）")
print("  • 可以可视化统计和分析")

print("\n" + "=" * 80)
print("✅ JSON文件作用说明完成！")
print("=" * 80)

# 保存本说明
with open("/JSON_FILES_PURPOSE.md", "w") as f:
    f.write("# JSON文件作用说明\n\n")
    for filename, description in json_files:
        f.write(f"## {filename}\n")
        f.write(f"{description}\n\n")
