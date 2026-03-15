# 🎯 PWN专项训练系统

**针对PWN类别的强化训练 - 目标：从66.93%提升至85%+**

---

## 📊 当前状态

| 指标 | 当前数值 | 目标值 | 差距 |
|------|---------|--------|------|
| PWN准确率 | 66.93% | 85% | +18.07% |
| 总题目数 | 2,368 | 3,000 | +632题 |
| 正确数 | 1,585 | 2,550 | +965题 |

---

## 🚀 训练策略

### 1. 基础强化
- 栈溢出溢出基础
- 基础ROP链构造
- Shellcode编写
- 格式化字符串入门

### 2. 进阶训练
- 堆溢出漏洞
- Use-After-Free
- 堆喷射
- 堆风水技术

### 3. 高级技巧
- Heap Feng Shui
- Tcache Poisoning
- Fastbin Attack
- Unlink Exploitation
- IO_FILE Attack

### 4. 绕过技术
- Canary保护绕过
- NX/DEP绕过
- ASLR绕过
- PIE绕过
- 全保护绕过

---

## 📝 训练计划

| 阶段 | 主题 | 题目数 | 预计准确率 |
|------|------|--------|-----------|
| 第1阶段 | 基础栈溢出 | 200 | 75% |
| 第2阶段 | ROP与Shellcode | 300 | 78% |
| 第3阶段 | 堆溢出基础 | 300 | 80% |
| 第4阶段 | UAF与堆利用 | 300 | 82% |
| 第5阶段 | 高级堆技术 | 300 | 84% |
| 第6阶段 | 保护绕过 | 200 | 85% |
| **总计** | **完整PWN训练** | **1,600** | **85%** |

---

## 🎯 重点训练题型

### 栈溢出
- 简单栈溢出
- Canary保护Stack Smashing
- Return to plt
- Ret2csu
- Ret2syscall

### 堆利用
- Fastbin Attack
- Unsafe Unlink
- Unsorted Bin Attack
- House of Einherjar
- House of Spirit
- House of Force
- House of Lore

### UAF漏洞
- Double Free
- Use After Free
- Tcache Poisoning
- Tcache Dup

### 格式化字符串
- Print Information
- Write Arbitrary Address
- Overwrite GOT
- Overwrite Pointer

---

## 🛠️ 工具集

```bash
# 必备工具
pwntools        # PWN框架
pwndbg          # 调试器
Ropper/ROPgadget # ROP链生成
one_gadget      # 快速RCE
checksec        # 检查保护
```

---

## 📚 推荐资源

### 知识库
- Heap Exploitation (How2Heap)
- PWN入门到精通
- CTF Wiki PWN
- Bilibili PWN教程

## 🚦 快速开始

```bash
# 运行PWN专项训练
python specialized_pwn_training.py
```

---

## 💡 训练建议

1. **从简单开始** - 先掌握基础栈溢出
2. **调试习惯** - 必须使用pwndbg调试
3. **理解原理** - 不要只背套路
4. **多做练习** - 每种漏洞类型至少做20题
5. **记录总结** - 整理每个技巧的适用场景

---

**🎯 目标：PWN准确率从66.93%提升至85%+！**
