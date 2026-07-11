# 价值量化碳维度扩展：SCI 复用碳模型

> **版本**: 2026-07-09
> **定位**: 价值量化层 —— 软件架构复用决策中的碳成本量化与可持续性价值评估
> **对齐标准**: GSF SCI / ISO/IEC 21031:2024, GSF SCI for AI, COCOMO II, EU CSRD, Green Software Patterns, ISO 14040/14044
> **状态**: ✅ 已完成

---

## 目录

- [价值量化碳维度扩展：SCI 复用碳模型](#价值量化碳维度扩展sci-复用碳模型)
  - [目录](#目录)
  - [1. 复用决策的碳成本模型与核心概念](#1-复用决策的碳成本模型与核心概念)
    - [1.1 核心概念定义](#11-核心概念定义)
    - [1.2 SCI 基础公式（ISO/IEC 21031:2024）](#12-sci-基础公式isoiec-210312024)
    - [1.3 复用 vs 重建的碳比较](#13-复用-vs-重建的碳比较)
  - [2. GSF SCI for AI 与复用映射](#2-gsf-sci-for-ai-与复用映射)
  - [3. 碳成本与 COCOMO II 的整合](#3-碳成本与-cocomo-ii-的整合)
    - [3.1 扩展 COCOMO II](#31-扩展-cocomo-ii)
    - [3.2 复用调整因子（AAF）的碳扩展](#32-复用调整因子aaf的碳扩展)
  - [4. 可持续性 ROI](#4-可持续性-roi)
    - [4.1 绿色 ROI 公式](#41-绿色-roi-公式)
    - [4.2 碳价参考（2026）](#42-碳价参考2026)
  - [5. 碳预算驱动的复用策略](#5-碳预算驱动的复用策略)
    - [5.1 碳预算分配](#51-碳预算分配)
    - [5.2 碳预算超支的复用决策](#52-碳预算超支的复用决策)
  - [6. 计算示例：复用消息中间件的 SCI 对比](#6-计算示例复用消息中间件的-sci-对比)
  - [7. 正向示例](#7-正向示例)
  - [8. 反模式](#8-反模式)
  - [9. 交叉引用](#9-交叉引用)
  - [10. 分析与决策建议](#10-分析与决策建议)
  - [11. 权威来源](#11-权威来源)
  - [12. 可运行工具引用](#12-可运行工具引用)
  - [13. 版本记录](#13-版本记录)

---

## 1. 复用决策的碳成本模型与核心概念

### 1.1 核心概念定义

- **软件碳强度（Software Carbon Intensity, SCI）**：软件系统每完成一单位有用工作所造成的碳排放率，单位为 gCO₂e/R。该指标由 Green Software Foundation 提出，并于 2024 年 3 月成为国际标准 ISO/IEC 21031:2024。
- **复用碳成本**：将既有软件资产纳入新项目时，因运行、维护、硬件隐含碳及机会成本而产生的全生命周期碳排放。
- **碳预算**：组织基于科学碳目标（SBTi）为项目、部门或组件分配的年度碳排放上限。
- **功能单位（R）**：SCI 计算中用于度量的业务/技术单位，如一次 API 调用、一个 token、一次模型推理、一位活跃用户。

### 1.2 SCI 基础公式（ISO/IEC 21031:2024）

Green Software Foundation 的 Software Carbon Intensity（SCI）规范于 2024 年 3 月正式成为国际标准 **ISO/IEC 21031:2024**。该标准定义软件系统每单位有用工作的碳排放率：

```text
SCI = (C) per R
    = ((E × I) + M) / R
```

| 符号 | 含义 | 单位 |
|:---|:---|:---|
| **SCI** | 软件碳强度 | gCO₂e / R |
| **E** | 软件系统消耗的电能 | kWh |
| **I** | 电网碳强度（location-based，不含市场工具） | gCO₂e / kWh |
| **M** | 支撑软件运行的硬件隐含碳排放 | gCO₂e |
| **R** | 功能单位（functional unit），如一次 API 调用、一个 token、一次训练 | 单位 |
| **C** | 总碳排放 = 运行排放 (E×I) + 隐含排放 (M) | gCO₂e |

复用决策的碳成本可分解为：

```text
复用总碳成本 = 直接碳成本 + 间接碳成本 + 机会碳成本

其中：
- 直接碳成本 = 复用组件运行能耗(E) × 电网碳强度(I)
- 间接碳成本 = 复用组件供应链/硬件隐含碳足迹(M)
- 机会碳成本 = 因复用而放弃的更低碳替代方案的预期减排量
```

> **核心原则**：SCI 只承认“消除排放”的动作；碳抵消、REC、PPA 等市场工具不能降低 SCI 分数（ISO/IEC 21031:2024 第 12.2 条）。

### 1.3 复用 vs 重建的碳比较

| 成本项 | 复用 | 重建 |
|:---|:---|:---|
| 开发能耗 | 低（避免重复编码、测试、构建） | 高（全生命周期开发活动） |
| 运行能耗 | 中（可能因过度功能或旧架构导致能效偏低） | 低（可针对当前需求精确优化） |
| 硬件隐含碳 M | 中（使用现有基础设施，摊薄制造碳排） | 高（新硬件采购与部署） |
| 维护能耗 | 中（持续运行、升级、兼容性测试） | 低（精简维护，技术栈现代） |
| 数据/模型传输 | 中（共享组件跨网络调用） | 低（边界内本地调用） |

**决策规则**：当复用方案的 SCI_reuse < SCI_rebuild 且 AAF < AAF_ECONOMIC_FLOOR（0.7，canonical [0.0, 1.0]）时，复用同时具备经济与环境优势。

---

## 2. GSF SCI for AI 与复用映射

GSF 于 2025 年 12 月 ratified **SCI for AI** 规范（预计 2026 年提交 ISO），将 SCI 方法论扩展到 AI 系统全生命周期：数据准备、模型训练、部署、推理与退役。

| AI 复用场景 | 推荐功能单位 R | 复用价值 | 注意事项 |
|:---|:---|:---|:---|
| 复用预训练模型（Foundation Model） | per token / per inference | 避免从头训练的高能耗 | 需计入微调能耗与推理效率 |
| 复用特征库 / Embedding 服务 | per feature vector / per query | 减少重复数据工程与训练 | 需评估调用链路与缓存命中率 |
| 复用提示模板（Prompt Templates） | per generation / per task | 降低无效 token 生成 | 需监控 goodput 与重试率 |
| 复用推理优化组件（ONNX/TensorRT） | per inference | 提升能效，降低单位推理 SCI | 需验证精度损失与硬件兼容性 |

**AI 复用 SCI 计算示例**：

某团队决定复用开源 Embedding 模型而非自研：

```text
自研模型：
  训练能耗 E_train = 10,000 kWh
  推理 1 亿次，每次 E_inf = 0.0001 kWh
  总 E = 10,000 + 0.0001 × 100,000,000 = 20,000 kWh
  假设 I = 400 gCO₂e/kWh，M = 50,000 gCO₂e
  自研 SCI = (20,000 × 400 + 50,000) / 100,000,000 = 0.0805 gCO₂e/inference

复用预训练模型（仅微调）：
  微调能耗 E_finetune = 500 kWh
  推理 1 亿次，每次 E_inf = 0.0001 kWh
  总 E = 500 + 0.0001 × 100,000,000 = 10,500 kWh
  假设 I = 400 gCO₂e/kWh，M = 30,000 gCO₂e
  复用 SCI = (10,500 × 400 + 30,000) / 100,000,000 = 0.0423 gCO₂e/inference

碳强度下降 ≈ 47.5%
```

---

## 3. 碳成本与 COCOMO II 的整合

### 3.1 扩展 COCOMO II

将碳维度嵌入 COCOMO II 工作量估算：

```text
PM = A × (Size)^E × ∏(EM_i)

carbon_effort = PM × carbon_intensity_factor

carbon_intensity_factor = f(开发地点电网强度, 远程工作比例, 云供应商 PUE, 可再生能源比例)
```

| 参数 | 说明 | 典型取值 |
|:---|:---|:---|
| 开发地点电网强度 | 研发中心所在电网碳强度 | 50–700 gCO₂e/kWh |
| 远程工作比例 | 减少通勤与办公能耗 | 0–100% |
| 云供应商 PUE | 数据中心能效 | 1.05–1.6 |
| 可再生能源比例 | 直接/间接绿电占比 | 0–100% |

### 3.2 复用调整因子（AAF）的碳扩展

当复用组件能效低于新开发组件时，引入碳惩罚：

```text
AAF_carbon = AAF × (1 + carbon_penalty)

carbon_penalty = (E_reuse_per_R - E_new_per_R) / E_new_per_R
```

carbon_penalty 考虑：

- 复用组件的运行效率 vs 定制组件（如旧 JVM 版本、未使用 SIMD/AVX 优化）
- 复用引入的过度功能导致的额外能耗（over-provisioning）
- 跨服务调用带来的网络与序列化开销

---

## 4. 可持续性 ROI

### 4.1 绿色 ROI 公式

```text
Green ROI = (财务收益 + 碳减排价值 - 碳成本增加) / 总投资

其中：
  碳减排价值 = 减排吨数 × 碳价（ETS 价格或内部碳价）
  总投资 = 复用/改造投资 + 工具链投资 + 监测投资
```

### 4.2 碳价参考（2026）

| 碳市场 | 价格 | 说明 |
|:---|:---:|:---|
| EU ETS | ~80–100 EUR/吨 CO₂e | 欧盟碳排放交易体系 |
| 中国 ETS | ~60–80 CNY/吨 CO₂e | 全国碳市场 |
| 内部碳价（企业） | 20–200 USD/吨 CO₂e | 企业内部影子碳价 |
| SBTi 净零路径 | 按行业科学目标 | 长期碳预算约束 |

---

## 5. 碳预算驱动的复用策略

### 5.1 碳预算分配

```text
组织碳预算分配
├── 总碳预算（年度）
│   └── 基于科学碳目标（SBTi）
├── 部门碳预算
│   └── 按部门/项目分配
├── 项目碳预算
│   └── 复用决策必须在项目碳预算内
└── 复用组件碳配额
    └── 每个复用组件分配运行碳配额（SCI 上限）
```

### 5.2 碳预算超支的复用决策

当复用导致碳预算超支时：

```text
├── 选项 1: 寻找更低碳的替代组件
├── 选项 2: 优化复用组件的配置（降低资源占用、升级运行时）
├── 选项 3: 购买碳抵消（仅用于范围 1/2 库存报告，不能降低 SCI）
├── 选项 4: 申请额外碳预算（需提供业务理由与减排计划）
└── 选项 5: 拒绝复用，选择更低碳的重建方案
```

---

## 6. 计算示例：复用消息中间件的 SCI 对比

**场景**：某系统需集成消息中间件，评估复用既有 Kafka 封装层 vs 新开发精简组件。

**假设**：

- 月请求量 R = 1,000,000,000 次
- 电网碳强度 I = 350 gCO₂e/kWh
- 复用方案月能耗 E_reuse = 800 kWh，硬件隐含 M_reuse = 200,000 gCO₂e
- 新开发方案月能耗 E_new = 500 kWh，硬件隐含 M_new = 350,000 gCO₂e（需新采购服务器）

**计算**：

```text
SCI_reuse = (800 × 350 + 200,000) / 1,000,000,000
          = (280,000 + 200,000) / 1,000,000,000
          = 0.00048 gCO₂e/request

SCI_new = (500 × 350 + 350,000) / 1,000,000,000
        = (175,000 + 350,000) / 1,000,000,000
        = 0.000525 gCO₂e/request

结论：复用方案的 SCI 低 8.6%，但需确保 AAF < AAF_ECONOMIC_FLOOR（0.7）才能同时保证经济可行性。
```

---

## 7. 正向示例

### 示例 1：Rust 数据解析库复用

某云服务复用经能效优化的 Rust 数据解析库替代 Python 实现，CPU 利用率从 45% 降至 22%；按 SCI 公式，单位请求碳排下降约 48%。

### 示例 2：AI 预训练模型复用

某团队复用开源多语言 BERT 替代从头训练，训练能耗从约 10,000 kWh 降至约 500 kWh（微调），单位查询 SCI 下降约 47%。

---

## 8. 反例

### 反例 1：绿色清洗式复用

为追求“绿色”标签强行复用旧版本低能效组件，未考虑新硬件与新算法能效提升；整体碳排反而增加，且错失性能优化机会。

### 反例 2：忽视隐含碳 M

仅比较运行能耗 E，忽略复用组件所需老旧硬件的隐含碳；当硬件生命周期结束时，整体 SCI 可能高于新购高能效硬件。

### 反例 3：用碳抵消降低 SCI

购买 REC/碳抵消后宣称 SCI 下降，违反 ISO/IEC 21031:2024 第 12.2 条对市场工具的排除规定。

---

## 9. 交叉引用

- 与 [COCOMO II 复用模型深度解析](../01-cocomo-ii-reuse/cocomo-ii-reuse-model-deep-dive.md) 配合：将 AAF/RUSE 估算结果输入碳成本扩展。
- 与 [架构复用 ROI 框架](../02-roi-npv-models/roi-framework.md) 配合：将碳减排价值纳入 Green ROI 计算。
- 与 [成熟度经济学与复用价值曲线](../04-maturity-economics/maturity-value-curve.md) 配合：高成熟度资产通常具备更低 SCI。

---

## 10. 分析与决策建议

### 10.1 复用碳决策流程

1. **边界界定**：明确复用组件的软件边界，包含计算、存储、网络、监控、CI/CD 等支撑系统。
2. **功能单位选择**：选择与业务产出直接相关的 R（如 API 调用、token、交易）。
3. **基线测量**：测量当前方案 E、I、M，计算 SCI_base。
4. **复用方案估算**：估算复用后的 E'、I'、M'，计算 SCI_reuse。
5. **经济性校验**：同时校验 AAF < AAF_ECONOMIC_FLOOR（0.7）与 NPV > 0。
6. **持续监测**：将 SCI 纳入 FinOps/碳预算仪表盘，按季度校准。

### 10.2 关键结论

- 复用不一定降低 SCI；当复用组件能效显著低于新开发组件时，运行排放可能反超。
- 隐含碳 M 在短生命周期、高频使用场景中占比降低，但在长周期低利用率场景中不可忽视。
- ISO/IEC 21031:2024 排除市场工具，迫使组织通过真实能效改进降低 SCI。

---

## 11. 权威来源

| 来源 | URL | 核查日期 |
|:---|:---|:---|
| Green Software Foundation — SCI Specification | <https://sci.greensoftware.foundation/> | 2026-07-09 |
| ISO/IEC 21031:2024 — Software Carbon Intensity | <https://www.iso.org/standard/86612.html> | 2026-07-09 |
| GSF — SCI for AI | <https://sci-for-ai.greensoftware.foundation/> | 2026-07-09 |
| GSF — SCI CSRD Compliance White Paper | <https://greensoftware.foundation/policy/research/sci-csrd-compliance/> | 2026-07-09 |
| GSF — Green Software Patterns | <https://patterns.greensoftware.foundation/> | 2026-07-09 |
| USC COCOMO II | <https://cssed.usc.edu/research/research-sponsored-software/cocomo/cocomo-ii/> | 2026-07-09 |
| COCOMO II Model Definition Manual (PDF) | <https://athena.ecs.csus.edu/~buckley/CSc231_files/Cocomo_II_Manual.pdf> | 2026-07-09 |
| EU ETS | <https://climate.ec.europa.eu/eu-action/eu-emissions-trading-system-eu-ets_en> | 2026-07-09 |
| Science Based Targets (SBTi) | <https://sciencebasedtargets.org/> | 2026-07-09 |
| ISO 14040/14044 | <https://www.iso.org/iso-14040-environmental-management.html> | 2026-07-09 |

---

## 12. 可运行工具引用

- `struct/09-value-quantification/tools/cocomo-calculator.py`：将碳强度因子作为自定义 EM 输入，估算碳调整后的工作量。
- 外部工具：GSF [Impact Framework](https://if.greensoftware.foundation/) 用于 SCI 自动化计算；[Carbon Aware SDK](https://carbon-aware-sdk.greensoftware.foundation/) 用于碳感知调度。
- 外部数据：[Electricity Maps](https://app.electricitymaps.com/) 提供实时电网碳强度 I；[Boavizta](https://boavizta.org/) 提供硬件隐含碳 M 数据。

---

## 13. 版本记录

- 2026-07-09：对齐 ISO/IEC 21031:2024 与 GSF SCI for AI，补充完整 SCI 公式、AI 复用映射、计算示例、正向示例、反模式、交叉引用、分析建议与权威来源表格。
- 2026-06-10：初始版本，建立复用碳成本模型与绿色 ROI 框架。