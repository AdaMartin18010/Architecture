# 成熟度经济学与复用价值曲线

> **版本**: 2026-07-09
> **定位**: 价值量化层 —— 将组织/资产成熟度与经济回报、复用规模效应关联
> **对齐标准**: SEI CMMI, RiSE/RCMM, NASA RRL, ISO/IEC 26565/26566, COCOMO II
> **状态**: ✅ 已完成

---

## 目录

- [成熟度经济学与复用价值曲线](#成熟度经济学与复用价值曲线)
  - [目录](#目录)
  - [1. 核心概念](#1-核心概念)
  - [2. 成熟度模型对照](#2-成熟度模型对照)
    - [2.1 SEI CMMI 与复用成熟度](#21-sei-cmmi-与复用成熟度)
    - [2.2 RiSE/RCMM 复用能力成熟度](#22-risercmm-复用能力成熟度)
    - [2.3 NASA Reuse Readiness Levels (RRL)](#23-nasa-reuse-readiness-levels-rrl)
  - [3. 成熟度-价值曲线](#3-成熟度-价值曲线)
  - [4. 成熟度投资的 ROI 模型](#4-成熟度投资的-roi-模型)
  - [5. 正向示例](#5-正向示例)
    - [示例 1：从 Level 2 到 Level 3 的平台工程投资](#示例-1从-level-2-到-level-3-的平台工程投资)
    - [示例 2：RRL 9 资产的生态网络效应](#示例-2rrl-9-资产的生态网络效应)
  - [6. 反例](#6-反例)
    - [反例 1：跳过 Level 2 直接建设 Level 4 平台](#反例-1跳过-level-2-直接建设-level-4-平台)
    - [反例 2：成熟度目标脱离业务指标](#反例-2成熟度目标脱离业务指标)
    - [反例 3：忽视维护成本的指数增长](#反例-3忽视维护成本的指数增长)
  - [7. 交叉引用](#7-交叉引用)
  - [8. 计算示例与分析](#8-计算示例与分析)
  - [9. 权威来源](#9-权威来源)
  - [10. 可运行工具引用](#10-可运行工具引用)
  - [11. 版本记录](#11-版本记录)

---

## 1. 核心概念

**成熟度经济学**研究组织或资产在成熟度提升过程中，复用成本、收益与风险的变化规律。其核心假设是：

> 随着复用成熟度从“临时复用”向“系统化/产品线级复用”演进，单位资产的边际复用成本递减，但前期平台投资存在显著的沉没成本门槛。

| 概念 | 定义 |
|:---|:---|
| **成熟度价值曲线** | 描述成熟度等级与复用经济回报之间关系的 S 型或阶梯型曲线 |
| **复用临界点** | 单位资产收益开始超过单位资产总成本的最低成熟度等级 |
| **平台沉没成本** | 达到可规模化复用前必须投入的治理、工具、文档与认证成本 |
| **网络效应** | 复用资产越多，贡献者与消费者之间的正向反馈越强 |

---

## 2. 成熟度模型对照

### 2.1 SEI CMMI 与复用成熟度

CMMI（Capability Maturity Model Integration）由 SEI 提出，现由 CMMI Institute/ISACA 维护。其五级成熟度与复用实践的对应关系如下：

| CMMI 等级 | 特征 | 复用实践映射 |
|:---|:---|:---|
| Level 1 — Initial | 过程不可预测、依赖个人英雄 | 临时复用、复制粘贴、无管理 |
| Level 2 — Managed | 项目级计划与监控 | 项目内代码库、团队级组件目录 |
| Level 3 — Defined | 组织级标准过程 | 组织级组件库、Golden Path、IDP |
| Level 4 — Quantitatively Managed | 量化管理与统计控制 | 复用率、AAF、SCI 等指标驱动决策 |
| Level 5 — Optimizing | 持续优化与创新 | 产品线工程、AI 辅助复用、自动适配 |

CMMI 研究表明，从 Level 1 提升至 Level 3 通常带来 20–40% 的生产率提升；达到 Level 5 的组织在缺陷率与交付周期上显著优于低成熟度组织。

### 2.2 RiSE/RCMM 复用能力成熟度

RiSE（Reuse in Software Engineering）与 RCMM（Reuse Capability Maturity Model）是面向复用过程的专门成熟度模型，将复用能力分为 5 级：

| 等级 | 名称 | 关键特征 |
|:---|:---|:---|
| Level 1 | Ad hoc | 无复用过程，复用偶发 |
| Level 2 | Opportunistic | 项目级库支持，个人/团队复用 |
| Level 3 | Integrated | 复用与开发过程集成，组织级资产库 |
| Level 4 | Leveraged | 独立的产品线生命周期与专用过程 |
| Level 5 | Anticipating | 应用主动优化复用，生态网络效应显现 |

### 2.3 NASA Reuse Readiness Levels (RRL)

NASA ESDS Software Reuse Working Group 定义的 RRL 从 1 到 9 评估软件资产的可复用性：

| RRL | 等级描述 | 经济含义 |
|:---|:---|:---|
| RRL 1 | Limited reusability | 不建议复用 |
| RRL 2 | Initial reusability | 实际不可行 |
| RRL 3 | Basic reusability | 高成本、高风险 |
| RRL 4 | Reuse is possible | 可行但需显著投入 |
| RRL 5 | Reuse is practical | 经济可行 |
| RRL 6 | Software is reusable | 多数用户可复用 |
| RRL 7 | Highly reusable | 低成本、低风险 |
| RRL 8 | Demonstrated local reuse | 已本地验证 |
| RRL 9 | Demonstrated extensive reuse | 已跨系统广泛验证 |

> **经验法则**：RRL ≥ 5 的资产才建议进入规模化复用评估；RRL ≥ 7 的资产具备显著的经济杠杆效应。

---

## 3. 成熟度-价值曲线

成熟度-价值曲线通常呈现为 **S 型曲线**：

```text
价值 /
    |                                    ______ 平台化/生态化
    |                              ______/
    |                        ____/
    |                   ____/
    |              ____/
    |         ____/
    |    ____/
    |___/
    +-------------------------------------------------> 成熟度
       L1  L2  L3      L4              L5
```

| 阶段 | 成熟度 | 价值特征 | 管理重点 |
|:---|:---|:---|:---|
| 投入期 | L1–L2 | 成本高、收益低，甚至为负 | 控制范围、选择高价值试点 |
| 成长期 | L2–L3 | 收益快速增长 | 标准化、治理、工具链 |
| 成熟期 | L3–L4 | 规模经济显现，边际成本递减 | 量化管理、投资组合优化 |
| 平台期 | L4–L5 | 网络效应与生态价值 | 开放、外部贡献、持续创新 |

---

## 4. 成熟度投资的 ROI 模型

将成熟度提升视为投资组合，其 ROI 可建模为：

```text
ROI_maturity = (Σ NPV(复用项目_i) + 战略期权价值 - 平台投资总成本) / 平台投资总成本

或简化为：

V(M) = α × M^β - C × M^γ

其中：
  V(M) = 成熟度 M 下的净价值
  M = 成熟度等级（1–5 或 1–9）
  α = 单位成熟度带来的收益系数
  β = 收益弹性（通常 β > 1，体现网络效应）
  C = 成熟度提升的边际成本系数
  γ = 成本弹性（通常 γ > 1，体现越往后提升越难）
```

**最优成熟度条件**：

```text
dV/dM = α × β × M^(β-1) - C × γ × M^(γ-1) = 0

=> M* = (α × β / (C × γ))^(1/(γ-β))
```

---

## 5. 正向示例

### 示例 1：从 Level 2 到 Level 3 的平台工程投资

某企业将复用从项目级提升至组织级，建立内部开发者平台（IDP）：

- 平台投资：¥500 万
- 年均节省重复开发成本：¥300 万
- 折现率 10%，5 年 NPV ≈ ¥637 万
- 3 年 ROI ≈ 98%

### 示例 2：RRL 9 资产的生态网络效应

某开源日志处理组件达到 RRL 9，被数百个系统复用；每新增一个消费方，边际维护成本趋近于零，而社区贡献持续提升组件质量。

---

## 6. 反例

### 反例 1：跳过 Level 2 直接建设 Level 4 平台

缺乏项目级复用经验即投资大规模产品线工程，导致平台与实际需求脱节，采用率低于 20%，平台成为“白象”。

### 反例 2：成熟度目标脱离业务指标

为通过 CMMI 评级而批量生产文档，过程改进未与交付效率、缺陷率、复用率挂钩，认证后能力迅速回退。

### 反例 3：忽视维护成本的指数增长

高成熟度资产若缺乏退役机制，低价值老旧组件持续消耗维护资源，最终使平台总成本反超收益。

---

## 7. 交叉引用

- 与 [COCOMO II 复用模型深度解析](../01-cocomo-ii-reuse/cocomo-ii-reuse-model-deep-dive.md) 配合：RUSE 与 RRL 映射直接决定复用成本估算。
- 与 [架构复用 ROI 框架](../02-roi-npv-models/roi-framework.md) 配合：成熟度投资可视为平台工程投资，使用 NPV/IRR 评估。
- 与 [价值量化碳维度扩展：SCI 复用碳模型](../03-carbon-dimension/sci-reuse-value-extension.md) 配合：高成熟度资产通常因更好的文档、测试与优化而具备更低 SCI。

---

## 8. 计算示例与分析

**场景**：某企业评估将复用成熟度从 Level 2 提升至 Level 4 的投资。

**参数**：

- 当前成熟度 M₀ = 2
- 目标成熟度 M₁ = 4
- 平台投资 C_platform = ¥800 万
- 年均新增复用项目收益 = ¥250 万
- 折现率 r = 10%
- 项目周期 n = 5 年

**NPV 计算**：

```text
NPV = -800 + 250/(1.1)^1 + 250/(1.1)^2 + 250/(1.1)^3 + 250/(1.1)^4 + 250/(1.1)^5
    = -800 + 227.3 + 206.6 + 187.8 + 170.8 + 155.2
    = 147.7 万

结论：NPV > 0，投资 maturity 提升在经济上可行。
```

---

## 9. 权威来源

| 来源 | URL | 核查日期 |
|:---|:---|:---|
| CMMI Institute | <https://cmmiinstitute.com/> | 2026-07-09 |
| ISACA — CMMI Performance Solutions | <https://www.isaca.org/enterprise/cmmi-performance-solutions> | 2026-07-09 |
| SEI — Carnegie Mellon University | <https://www.sei.cmu.edu/> | 2026-07-09 |
| NASA — Reuse Readiness Levels (RRL) | <https://ntrs.nasa.gov/api/citations/20120010312/downloads/20120010312.pdf> | 2026-07-09 |
| NASA SWEHB — Software Reuse Catalog | <https://swehb.nasa.gov/display/SWEHBVD/SWE-148+-+Contribute+to+Agency+Software+Catalog> | 2026-07-09 |
| RiSE/RCMM 复用成熟度研究 | <https://hal.science/hal-03253865/document> | 2026-07-09 |
| ISO/IEC 26565 / 26566（DIS 阶段） | <https://www.iso.org/standard/86612.html> 系列 | 2026-07-09 |
| USC COCOMO II | <https://cssed.usc.edu/research/research-sponsored-software/cocomo/cocomo-ii/> | 2026-07-09 |

---

## 10. 可运行工具引用

- `struct/09-value-quantification/tools/cocomo-calculator.py`：估算不同 RUSE 等级（成熟度）下的工作量与成本。
- `struct/09-value-quantification/02-roi-npv-models/roi-framework.md`：将成熟度投资代入 NPV/IRR 计算。
- 外部参考：CMMI Institute [Model Viewer Plus](https://cmmiinstitute.com/) 用于 CMMI 实践区映射。

---

## 11. 版本记录

- 2026-07-09：创建文件，整合 SEI CMMI、RiSE/RCMM、NASA RRL 与 ISO/IEC 26565/26566，建立成熟度-价值曲线与 ROI 模型，补充示例、反模式、公式与权威来源。
