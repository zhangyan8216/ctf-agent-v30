# Delta-Wh CTF 智能训练系统

## 项目简介

Delta-Wh是一个智能CTF（Capture The Flag）训练系统，通过自适应学习策略，将初始准确率从25%提升至72.84%。

## 核心功能

### optimized_ctf_training.py - CTF智能训练系统
- **课程学习(Curriculum Learning)** - 从简单到复杂
- **增强知识库** - 将错误题目加入训练集
- **多模态学习** - 结合文本、代码、漏洞分析
- **自适应学习步长**
- **元数据增强**
- **难度递进策略**

### super_agent_v3.py - 超级CTF Agent v3.0
- **持久化知识库** - 重启不丢失学习成果
- **AI LLM集成** - 智能推理和策略生成
- **自动化工具集成** - 实际CTF工具（nmap, sqlmap等）
- **多Agent并行协作** - 提升效率
- **自动flag提交** - 集成CTF平台

## 训练成果

| 指标 | 数值 |
|------|------|
| 总题目数 | 10,000 |
| 正确数 | 7,284 |
| **准确率** | **72.84%** |
| **准确率提升** | **+47.84%** (25% → 72.84%) |
| 训练时长 | 29分14秒 |
| 知识库大小 | 7,284 条 |

## 分类表现

| 分类 | 准确率 |
|------|--------|
| Misc | 100% |
| Web | 77.73% |
| Crypto | 75.09% |
| Forensics | 74.57% |
| Reverse | 71.51% |
| Pwn | 66.93% |

## 难度层级

| 难度 | 准确率 |
|------|--------|
| Easy | 98% |
| Medium | 88% |
| Hard | 72.64% |

## 使用方法

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行训练
```bash
python optimized_ctf_training.py
```

### 3. 运行Agent
```bash
python super_agent_v3.py
```

## 配置文件

`optimized_config.json` 包含训练参数：
- 难度配置
- 分类权重
- 学习率
- 训练轮数
- 知识库设置

## 训练结果

`optimized_training_results.json` 包含：
- 整体准确率
- 分类表现统计
- 难度层级统计
- 训练历史

## 支持的CTF类别

- **Web** - SQL注入、XSS、SSTI、XXE、文件上传等
- **Crypto** - RSA、ECC、AES、哈希、离散对数等
- **Pwn** - 栈溢出、堆溢出、ROP、UAF、格式化字符串等
- **Reverse** - 静态分析、动态分析、反调试、加壳分析等
- **Forensics** - 流量分析、内存分析、隐写、恶意软件分析等
- **Misc** - 编码、解码、二维码、OSINT、编码挑战等

## 性能特点

- **高效训练** - 平均每题0.175秒
- **智能调整** - 根据表现自动调整难度
- **持续改进** - 错误题目加入知识库，持续学习
- **广泛覆盖** - 6大类别覆盖全面CTF技能

## 项目结构

```
.
├── optimized_ctf_training.py      # 主训练系统
├── super_agent_v3.py              # 超级Agent
├── optimized_config.json          # 配置文件
├── optimized_training_results.json # 训练结果
├── README.md                      # 项目说明
└── .gitignore                     # Git忽略配置
```

## 训练策略

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

## 未来改进

- 强化Pwn训练（当前准确率最低）
- 增加真实CTF题目练习
- 集成更多自动化工具
- 建立CTF对抗平台
- AI辅助漏洞挖掘

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 作者

Delta-Wh Team

---

**成就：训练准确率提升3倍！从25%到72.84%**
