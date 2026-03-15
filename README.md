# 🎯 Delta-Wh CTF 智能训练系统

**自适应学习CTF训练系统 - 准确率从25%提升至72.84%**

---

## 🎉 项目亮点

**✨ 47.84% 准确率提升！**

| 指标 | 训练前 | 训练后 | 提升 |
|------|--------|--------|------|
| **准确率** | 25% | **72.84%** | **+47.84%** |
| **总题目数** | - | 10,000 | - |
| **训练时长** | - | 29分14秒 | - |
| **知识库大小** | - | 7,284条 | - |

---

## 🚀 快速开始

```bash
# 1. 运行Delta-Wh训练系统
python optimized_ctf_training.py

# 2. 运行超级Agent
python super_agent_v3.py

# 3. 查看演示
python demo.py

# 4. 评估Agent
python CTF_AGENT_ASSESSMENT.py
```

---

## 📊 训练成果

### 整体表现
| 指标 | 数值 |
|------|------|
| 总题目数 | 10,000 |
| 正确数 | 7,284 |
| **准确率** | **72.84%** |
| **准确率提升** | **+47.84%** |
| 训练时长 | 29分14秒 |
| 知识库大小 | 7,284 条 |

### 难度层级表现
| 难度 | 正确/总数 | 准确率 |
|------|-----------|--------|
| Easy | 49/50 | **98%** |
| Medium | 44/50 | **88%** |
| Hard | 7,191/9,900 | **72.64%** |

### 分类表现
| 分类 | 正确/总数 | 准确率 |
|------|-----------|--------|
| Misc | 11/11 | **100%** |
| Web | 1,382/1,778 | **77.73%** |
| Crypto | 1,643/2,188 | **75.09%** |
| Forensics | 1,205/1,616 | **74.57%** |
| Reverse | 1,458/2,039 | **71.51%** |
| Pwn | 1,585/2,368 | **66.93%** |

---

## 🎮 核心功能

### ✅ 优化训练系统 (optimized_ctf_training.py)
- **课程学习(Curriculum Learning)** - 从简单到复杂
- **增强知识库** - 错误题目加入训练集
- **多模态学习** - 文本、代码、漏洞分析
- **自适应学习步长**
- **元数据增强**
- **难度递进策略**

### ✅ 超级Agent v3.0 (super_agent_v3.py)
- **持久化知识库** - 重启不丢失学习成果
- **AI LLM集成** - 智能推理和策略生成
- **自动化工具集成** - nmap, sqlmap等
- **多Agent并行协作**
- **自动flag提交**

### ✅ 专项训练系统
- BCTF_TRAINING.py - BCTF专项
- CCTF_TRAINING.py - CCTF专项
- BYTECTF_TRAINING.py - ByteCTF专项
- DEFCON_TRAINING.py - DEFCON专项
- LILCTF2025_TRAINING.py - LILCTF2025专项
- OCTF_TRA INING.py - OCTF专项
- QWB_TRAINING.py - QWB专项
- REAL_WORLD_CTF_TRAINING.py - 真实CTF训练
- XCTF_TRAINING.py - XCTF专项

---

## 📁 项目结构

```
ctf-agent-v30/
├── optimized_ctf_training.py      # Delta-Wh核心训练系统
├── optimized_config.json          # 训练配置
├── optimized_training_results.json # 训练结果报告
├── super_agent_v3.py             # 超级Agent v3.0
├── demo.py                       # 演示脚本
│
├── 专项训练/
│   ├── BCTF_TRAINING.py
│   ├── CCTF_TRAINING.py
│   ├── BYTECTF_TRAINING.py
│   ├── DEFCON_TRAINING.py
│   ├── LILCTF2025_TRAINING.py
│   ├── OCTF_TRAINING.py
│   ├── QWB_TRAINING.py
│   ├── REAL_WORLD_CTF_TRAINING.py
│   └── XCTF_TRAINING.py
│
├── 增强版本/
│   ├── ADVANCED_CTF_TRAINING.py
│   ├── ADVANCED_SOLVER.py
│   ├── SUPER_ENHANCED_AGENT.py
│   ├── ENHANCED_AGENT_SOLVER.py
│   └── advanced_reasoning.py
│
├── 迭代系统/
│   ├── ITERATIVE_TRAINING.py
│   ├── ITERATIVE_TRAINING_V2.py
│   ├── ITERATIVE_TRAINING_V3.py
│   ├── AGENT_ITERATION_MONITOR.py
│   └── TRAIN_ALL_CHALLENGES.py
│
└── 工具系统/
    ├── CTF_TRAINING.py
    ├── CTF_AGENT_ASSESSMENT.py
    ├── AUTO_DEMO.py
    ├── AUTO_EXPLOIT_GENERATOR.py
    ├── REAL_WORLD_SOLVER.py
    └── BATCH_ITERATION.py
```

---

## 🔧 环境要求

- Python 3.8+
- Linux / macOS / Windows
- 1GB磁盘空间

### 依赖安装
```bash
pip install requests beautifulsoup4 pwntools cryptography
```

---

## 📈 训练策略

### 1. 课程学习
- 从Easy开始，建立信心和基础
- 逐步提升到Medium，加强技能
- 最后挑战Hard，磨练高级技能

### 2. 知识库增强
- 正确答案存入知识库
- 错误答案分析原因
- 定期回顾错误题目

### 3. 自适应调整
- 准确率高时提升难度
- 准确率低时降低难度
- 动态调整类别权重

---

## 🌍 支持的CTF类别

### Web (1,382/1,778, 77.73%)
- SQL注入、XSS、SSTI、XXE、文件上传
- CSRF、JWT、SSRF、RCE、模板注入

### Crypto (1,643/2,188, 75.09%)
- RSA、ECC、AES、DES
- 哈希、离散对数、CBC位翻转
- Padding Oracle、编码解码

### Pwn (1,585/2,368, 66.93%)
- 栈溢出、堆溢出、UAF
- ROP、格式化字符串、Shellcode
- Ret2libc、Heap Spray

### Reverse (1,458/2,039, 71.51%)
- 静态分析、动态分析
- 反调试、加壳分析
- 调试、Patch

### Forensics (1,205/1,616, 74.57%)
- 流量分析、内存分析
- 隐写、文件恢复
- 恶意软件分析

### Misc (11/11, 100%)
- 编码、解码、二维码
- OSINT、编程挑战

---

## 📚 文档

- [部署指南](DEPLOYMENT_AND_IMPLEMENTATION.md)
- [演示指南](FINAL_DEMO_GUIDE.md)
- [项目索引](PROJECT_INDEX.md)
- [准确率报告](ACCURACY_REPORT.md)
- [完成报告](COMPLETION_REPORT.md)
- [迭代报告](AGENT_ITERATION_REPORT.md)
- [JSON文件说明](JSON_FILES_PURPOSE.md)
- [交付清单](PROJECT_DELIVERY_CHECKLIST.md)

---

## 💡 未来改进

- ✅ **强化Pwn训练**（当前准确率最低66.93%）
- ✅ 增加真实CTF题目练习
- ✅ 集成更多自动化工具
- ✅ 建立CTF对抗平台
- ✅ AI辅助漏洞挖掘

---

## 🏆 成就

- ✅ 训练10,000道题
- ✅ 准确率提升47.84%（25% → 72.84%）
- ✅ 覆盖6大CTF类别
- ✅ 支持Easy/Medium/Hard三级难度
- ✅ 知识库积累7,284条
- ✅ 训练时长29分14秒
- ✅ 平均每题0.175秒

---

## 📦 Git仓库

- **地址**: https://github.com/zhangyan8216/ctf-agent-v30
- **文件数**: 50+ 个
- **代码行数**: 100,000+ 行
- **分支**: main
- **状态**: ✅ 已完整推送

---

## 🤝 贡献

欢迎提交Issues和Pull Requests！

---

## 📞 支持

查看文档或提交Issues

---

**🎉 Delta-Wh系统训练准确率提升3倍！从25%到72.84%！**
