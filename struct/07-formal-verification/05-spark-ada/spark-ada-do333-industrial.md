# SPARK Ada 形式化验证与工业复用
>
> 版本: 2026-06-06
> 对齐来源: AdaCore 官方资料、DO-178C/DO-333 (ED-12C/ED-216)、Airbus/Dassault Aviation 工业经验、Military Embedded (2017/2025)

## 1. SPARK 语言与工具链

### 1.1 定位

SPARK 是 Ada 的子集/衍生语言，专为**高完整性系统**设计：

- **演绎式程序验证**（Deductive Program Verification）
- **模块化、可扩展**的系统和嵌入式程序验证
- **工业级**形式化方法（AdaCore SPARK Pro）

### 1.2 核心能力

| 能力 | 说明 |
|-----|------|
| 函数合同（Contracts） | Pre/Post 条件、数据依赖、流依赖 |
| 自动化证明 | 基于 SMT 求解器（Alt-Ergo, Z3, CVC5）|
| 运行时检查生成 | 合同可作为运行时断言编译 |
| 信息流分析 | 自动验证数据保密性与完整性 |
| 无运行时错误证明 | 消除溢出、除零、数组越界、未初始化读取 |

## 2. DO-178C / DO-333 合规路径

### 2.1 形式化方法补充件（FM Supplement）

DO-178C/ED-12C（2012 发布）及其补充件 DO-333/ED-216 定义了三种形式化方法类别：

1. **演绎方法（Deductive）**：SPARK、Frama-C
2. **模型检验（Model Checking）**：Spin, NuSMV
3. **抽象解释（Abstract Interpretation）**：Polyspace, Astrée

> **关键里程碑**：尽管 DO-333 已发布十余年，但 SPARK 证明替代测试的详细工业流程已获 FAA/EASA 认可。

### 2.2 SPARK 可替代的 DO-333 验证目标

#### 低级需求（LLR）相关目标（FM.A-4）

当 LLR 表达为 SPARK 合同时：

- **准确性（Accuracy）**：形式化记法保证 LLR 精确无歧义 → 目标 2, 4, 5
- **一致性（Consistency）**：不同函数的合同不会冲突 → 目标 2, 4, 5
- **可验证性（Verifiability）**：合同按设计语言标准设计 → 目标 2, 4, 5

#### 源代码相关目标（FM.A-5）

| 目标 | SPARK 覆盖方式 |
|-----|---------------|
| 源代码符合 LLR | 自动证明源代码满足函数合同 |
| 数据依赖性 | 合同中的 `Global`/`Depends` 子句 |
| 标准符合性 | SPARK 代码按设计语言标准可验证 |
| 可追溯性 | 函数合同隐式追溯至 LLR |
| 一致性 | 自动分析排除未初始化数据、溢出、运行时错误 |

#### 可执行目标代码（EOC）相关目标（FM.A-6）

EOC 合规性目标（目标 3, 4）可通过源代码对应目标实现，前提是证明**属性保持**（Property Preservation）：

- **方法**：集成测试中启用合同执行（contracts as assertions）
- **逻辑**：若编译器未保持语义，已证明的合同在集成测试中（极大概率）会失败
- **增强**：对比"有合同执行"与"无合同执行"的输出一致性，确认合同编译不影响代码编译

### 2.3 替代测试的额外目标（FM.A-7）

当使用 SPARK 替代单元测试时，DO-333 定义目标 5–8：

- 形式验证 + 评审可覆盖（Airbus 与 Dassault Aviation 工业经验）
- 利用数据依赖合同和不相交情况（disjoint cases）表达

## 3. 工业应用案例

### 3.1 航空电子

| 项目 | 组织 | SPARK 应用 |
|-----|------|-----------|
| C-130J 控制软件 | Lockheed Martin (1997) | 飞行控制软件开发 |
| C-130J 维护验证 | BAE Systems | 关键属性持续形式证明 |
| A380 低级需求验证 | Airbus (2002, Caveat→Frama-C) | 替代单元测试的形式证明 |
| 民用飞机软件 | Airbus / Dassault Aviation | DO-178C 形式验证替代测试 |
| MARS Rover 安全监控 | AdaCore 演示 (2025) | 自动证明自主模式安全性，发现遥控模式错误 |

### 3.2 Test & Proof 策略

```
Main_Program (Ada)
├── 集成测试（假设：Pre 被满足、输入非别名、输入已初始化）
Core_Service (SPARK)
├── 形式验证（Post 被满足、无副作用、输出已初始化）
Low_Level_Service (Ada)
└── 单元测试
```

**目标**：组合验证至少与单独测试一样好。
**关键**：从临时假设管理转向**工具辅助假设管理**。

## 4. SPARK 2024+ 演进

### 4.1 与生成式 AI 的协同

- **SPARK 是生成式 AI 的最佳目标语言之一**：
  - 合同作为形式化规范，AI 生成代码后可直接验证
  - 自动证明提供即时反馈循环
  - 消除 AI 生成代码常见的运行时错误

### 4.2 液体类型（Liquid Types）

- 将细化类型（refinement types）概念引入 Ada/SPARK 生态
- 增强合同表达能力，支持更复杂的不变量

## 5. 复用模式

### 5.1 合同级复用

- **通用合同模板**：为常见算法（排序、搜索、环形缓冲区）提供已验证的合同套件
- **抽象数据类型（ADT）**：已验证的栈、队列、映射实现，带完整合同

### 5.2 证明级复用

- **证明库（Proof Libraries）**：数学性质、位操作、定点运算的已证明引理
- **Ghost 代码复用**：辅助证明的不可执行代码片段

### 5.3 跨项目验证策略复用

| 策略 | 复用内容 |
|-----|---------|
| 逐级证明（Cascading Proof） | 同一行业项目的证明策略模板 |
| 假设管理框架 | Test & Proof 集成模式 |
| 工具资格包 | DO-333 工具资格证据复用 |

## 6. 参考索引

- DO-178C / ED-12C: "Software Considerations in Airborne Systems and Equipment Certification" (2012)
- DO-333 / ED-216: "Formal Methods Supplement to DO-178C and DO-278A" (2012)
- Moy et al.: "Testing or Formal Verification: DO-178C Alternatives and Industrial Experience", IEEE Software (2013)
- AdaCore: "Introduction to Formal Verification with SPARK" (Video, 2025)
- FOSDEM 2025: "Understanding liquid types, contracts and formal verification with Ada/SPARK"
- Military Embedded Systems: "Formal program verification in avionics certification" (2017/2025)
- SPARK 2014: "Formal Program Verification For All" (SOS-Vo)
