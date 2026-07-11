# COCOMO II 复用模型 2026 校准版

> **版本**: 2026-06-06
> **对齐来源**: USC COCOMO II Model Definition Manual (Boehm et al., 2000), GitHub Copilot Productivity Report 2025-2026, METR AI Developer Productivity Study (2025)
> **定位**: 将 COCOMO II 复用模型适配到 2026 年的 AI 辅助开发、Serverless、低代码环境

---

## 目录

- [COCOMO II 复用模型 2026 校准版](#cocomo-ii-复用模型-2026-校准版)
  - [目录](#目录)
  - [1. 原始 COCOMO II 复用公式](#1-原始-cocomo-ii-复用公式)
  - [2. 2026 校准动因](#2-2026-校准动因)
  - [3. 2026 校准参数](#3-2026-校准参数)
    - [3.1 AI 辅助开发调整](#31-ai-辅助开发调整)
    - [3.2 Serverless 调整](#32-serverless-调整)
    - [3.3 低代码平台调整](#33-低代码平台调整)
    - [3.4 复用成熟度 RUSE 调整](#34-复用成熟度-ruse-调整)
    - [3.5 2026 综合校准公式](#35-2026-综合校准公式)
  - [4. 完整计算示例](#4-完整计算示例)
    - [场景：电商订单系统的复用成本估算（2026 版）](#场景电商订单系统的复用成本估算2026-版)
  - [5. RUSE 乘数 2026 建议值](#5-ruse-乘数-2026-建议值)
  - [6. 行业对比分析](#6-行业对比分析)
    - [6.1 不同架构范式的 COCOMO II 2026 参数对比](#61-不同架构范式的-cocomo-ii-2026-参数对比)
    - [6.2 AI 辅助开发的权衡矩阵](#62-ai-辅助开发的权衡矩阵)
  - [7. 局限性声明](#7-局限性声明)
  - [参考索引与权威来源](#参考索引与权威来源)
  - [补充说明：COCOMO II 复用模型 2026 校准版](#补充说明cocomo-ii-复用模型-2026-校准版)
  - [概念定义](#概念定义)
  - [示例](#示例)
  - [反例](#反例)
  - [权威来源](#权威来源)

---

## 1. 原始 COCOMO II 复用公式

```text
开发工作量 (Person-Months):
    PM = A × (Size)^E × ∏(EMᵢ)

其中:
    A = 2.94 (校准常数，基于 1990-2000 年 161 个项目数据)
    Size = 千等效源代码行数 (KSLOC)
    E = B + 0.01 × Σ(SFⱼ)
    B = 0.91 (默认)
    SFⱼ = 5 个规模因子
    EMᵢ = 17 个工作量乘数

复用调整后的规模:
    ESLOC = ASLOC × (AAF) / 100

    AAF = 0.4 × (DM) + 0.3 × (CM) + 0.3 × (IM)

    DM = 设计修改百分比 [0-100%]
    CM = 代码修改百分比 [0-100%]
    IM = 集成工作量百分比 [0-100%]

若 AAF ≤ 50:
    ESLOC = ASLOC × [AA + AAF × (1 + 0.02 × SU × UNFM)] / 100

若 AAF > 50:
    ESLOC = ASLOC × [AA + AAF + (SU × UNFM)] / 100

    AA = 评估与同化百分比 (Assessment and Assimilation)
    SU = 软件理解增量 [10-50%]
    UNFM =  unfamiliarity 因子 [0.0-1.0]
```

---

## 2. 2026 校准动因

COCOMO II 的校准常数 A=2.94 基于 1990-2000 年的项目数据，对 2026 年的以下变化存在显著偏差：

| 变化 | 对 COCOMO II 的影响 | 校准方向 |
|------|-------------------|---------|
| AI 辅助编程 (Copilot/Cursor) | 编码速度提升 20-55%，但审查与返工成本增加 6.5-19% | 降低 CM 权重，增加 AI_review 因子 |
| Serverless/FaaS | 基础设施代码减少 70%，但配置代码 (IaC) 增加 | 重新定义 "代码行" 范围为等效功能单元 (EFU) |
| 低代码/无代码平台 | 可视化开发替代 40-70% 手写代码 | SLOC 不再适用，引入功能点-代码行混合换算 |
| 组件生态成熟 (npm/crates.io) | 依赖深度增加，但直接编写代码减少 | 调整 RUSE 乘数范围，引入供应链深度因子 |
| DevSecOps 流水线 | 自动化测试/扫描降低集成成本 15-25% | 降低 IM 基准值，增加安全审查因子 |
| 远程协作/全球化 | 沟通成本变化，协调时间增加 8% | 调整 TEAM 乘数基准 |

> **实证数据更新**（2025-2026 研究）：
>
> - GitHub 控制实验：Copilot 用户完成 HTTP 服务器任务速度提升 55%，平均耗时从 2h 41m 降至 1h 11m[^1]
> - METR / Xu et al. (2025)：AI 辅助代码需更多返工以满足仓库标准，核心开发者审查量增加 6.5%，原创代码生产率下降 19%[^2]
> - Song et al. (2024)：Copilot 使项目级代码贡献增加 5.9%，但协调时间增加 8%[^3]
> - Uplevel (2024)：Copilot 使用组引入 41% 更多 bug，对 cycle time 和 PR throughput 无显著改善[^4]

---

## 3. 2026 校准参数

### 3.1 AI 辅助开发调整

AI 辅助编码对 COCOMO II 的影响是**双向的**：编码效率提升被审查、返工和技术债务成本部分抵消。

**AI 辅助编码效率因子** (AI_Efficiency Factor, AEF)：

```text
CM_2026 = CM_original × AEF

AEF 取值:
├── 无 AI 辅助:                    1.00
├── 基础代码补全 (GitHub Copilot):  0.70  (编码效率提升 30%，CM 降低 30%)
├── 高级 Agent (Cursor, Claude Code): 0.55  (编码效率提升 45%)
├── 全栈 AI 生成 (vibe coding):     0.40  (编码效率提升 60%)
└── 安全关键领域调整:               +0.10 至 +0.15 (审查更严格)
```

**AI 审查与返工成本因子** (AI_Review Factor, ARF)：

```text
IM_2026 = IM_original × ARF

ARF 取值:
├── 非关键业务系统:                1.10  (审查成本增加 10%)
├── 一般企业系统:                  1.20  (审查成本增加 20%)
├── 金融/医疗合规系统:             1.35  (审查成本增加 35%)
└── 安全关键系统 (DO-178C, ISO 26262): 1.50  (审查成本增加 50%)
```

**AI 技术债务因子** (AI_TechDebt Factor, ATD)：

基于 METR (2025) 和 Uplevel (2024) 的实证发现，AI 生成代码的长期维护成本需增加调整：

```text
维护调整:
    Maintenance_Effort_2026 = Maintenance_Effort_original × ATD

ATD 取值:
├── 无 AI 辅助:                    1.00
├── 基础 Copilot (代码补全):       1.08  (技术债务增长约 8%)
├── 高级 Agent (多文件生成):       1.15  (技术债务增长约 15%)
└── 全栈 AI 生成:                  1.25  (技术债务增长约 25%)
```

**2026 年 AI 综合影响参数表**：

| AI 工具等级 | AEF (CM) | ARF (IM) | ATD (维护) | 综合净效应估算 |
|------------|----------|----------|-----------|--------------|
| 无 AI | 1.00 | 1.00 | 1.00 | 基准 1.00 |
| 基础补全 (Copilot) | 0.70 | 1.20 | 1.08 | **0.91** |
| 高级 Agent (Cursor) | 0.55 | 1.25 | 1.15 | **0.79** |
| 全栈生成 (vibe coding) | 0.40 | 1.35 | 1.25 | **0.68** |

> 综合净效应 = AEF × √(ARF) × ⁴√(ATD)，反映短期编码收益被中期审查和长期维护部分抵消后的近似结果。

### 3.2 Serverless 调整

Serverless 项目中，传统 SLOC 度量严重失真。2026 校准引入**等效功能单元 (Equivalent Functional Unit, EFU)**：

```text
Size_serverless = (SLOC_traditional × 0.30)
                + (SLOC_function_handlers × 1.00)
                + (Config_lines_IaC × 0.15)
                + (Event_rules × 8.0)
                + (IAM_policy_statements × 2.0)
```

**Serverless 规模换算系数说明**：

| 代码/配置类型 | 换算系数 | 说明 |
|-------------|---------|------|
| 传统业务逻辑 SLOC | 0.30 | 托管服务替代了 70% 传统基础设施代码 |
| Function handler SLOC | 1.00 | 函数入口代码是核心逻辑等效度量 |
| IaC 配置行 (YAML/Terraform) | 0.15 | 每行配置约等效 0.15 SLOC 复杂度 |
| Event 触发规则 | 8.0 | 每条 event rule 约等效 8 SLOC 的集成复杂度 |
| IAM 策略声明 | 2.0 | 每条 IAM statement 约等效 2 SLOC 的安全设计复杂度 |

**Serverless 架构成本驱动器调整**：

| 成本驱动器 | 原始定义 | 2026 Serverless 调整 |
|-----------|---------|-------------------|
| **TIME** (执行时间约束) | 新增：Serverless 冷启动对响应时间的约束 | 乘数 1.00-1.15 |
| **STOR** (存储约束) | 扩展至包含状态管理复杂度 | 乘数 1.00-1.10 |
| **PVOL** (平台变更) | Serverless 平台频繁更新带来的适配成本 | 乘数 1.05-1.25 |
| **TOOL** (工具成熟度) | Serverless 本地调试/测试工具链成熟度 | 乘数 0.90-1.20 |

### 3.3 低代码平台调整

低代码/无代码 (LCNC) 平台的开发模式根本性地改变了规模度量方式：

**混合规模度量公式**：

```text
Size_lcnc = (FP_visual × CF_visual) + (FP_integration × CF_integration) + (SLOC_custom × 1.0)

其中:
    FP_visual = 可视化配置的功能点计数
    CF_visual = 可视化功能点换算系数
    FP_integration = API/数据集成相关的功能点
    CF_integration = 集成复杂度换算系数
    SLOC_custom = 自定义代码（扩展/插件）的实际 SLOC
```

**低代码平台换算系数表**：

| 应用类型 | CF_visual (SLOC/FP) | CF_integration (SLOC/FP) | 典型 AI 辅助水平 |
|---------|-------------------|------------------------|---------------|
| 简单 CRUD / 审批流 | 15 | 30 | 高 (AI 生成 70%+) |
| 中等复杂度业务应用 | 25 | 45 | 中高 (AI 生成 50%+) |
| 复杂集成应用 (ERP/SAP 连接) | 35 | 65 | 中 (AI 生成 30%+) |
| 自定义扩展密集型应用 | 45 | 80 | 低 (AI 生成 <30%) |

**低代码平台专用成本驱动器**：

| 驱动器 | 评级 | 乘数 | 说明 |
|--------|------|------|------|
| **LCPL** (平台锁定风险) | 低 / 中 / 高 / 极高 | 0.95 / 1.00 / 1.15 / 1.30 | 平台迁移成本 |
| **LCUS** (可配置性利用率) | 高 / 中 / 低 | 0.85 / 1.00 / 1.25 | 使用原生配置 vs 自定义代码比例 |
| **LCIN** (集成复杂度) | 低 / 中 / 高 | 0.90 / 1.00 / 1.20 | 与遗留系统集成深度 |

### 3.4 复用成熟度 RUSE 调整

原始 RUSE 范围 0.65-1.00，2026 建议扩展至考虑 AI、平台工程、供应链安全因素：

| RUSE 等级 | 原始值 | 2026 建议值 | 复用场景 | 关键增强因素 |
|-----------|--------|------------|----------|-------------|
| **极低** | 1.00 | 1.00 | 无复用，全部自研 | 基准 |
| **很低** | 0.95 | 0.92 | 偶发复用，个人级 | +AI 搜索辅助 |
| **低** | 0.89 | 0.84 | 项目级复用，有管理 | +内部组件库 + IDP |
| **一般** | 0.84 | 0.78 | 组织级复用 + IDP | +AI 自动适配 + SBOM |
| **高** | 0.78 | 0.71 | 产品线级复用 + AI 辅助 | +Golden Path + 自动测试 |
| **很高** | 0.72 | 0.64 | 跨组织复用 + SLSA L3+ | +供应链 provenance |
| **极高** | 0.65 | 0.56 | 黑盒复用 + AI 自动集成 | +AI agent 自动适配 |

### 3.5 2026 综合校准公式

```text
PM_2026 = A_2026 × (Size_2026)^E × ∏(EMᵢ_2026)

其中:
    A_2026 = 2.20 （建议下调，反映工具链和开源生态成熟度）

    Size_2026 = KSLOC_2026（根据项目类型选择换算方式）:
        ├── 传统项目: 原始 KSLOC
        ├── Serverless: KSLOC_EFU / 1000
        └── 低代码: KFP_2026 × CF_avg / 1000

    EMᵢ_2026 包含关键调整:
        ├── RUSE_2026: 复用成熟度（见 3.4 节）
        ├── AEF: AI 编码效率因子 [0.40-1.00]
        ├── ARF: AI 审查返工因子 [1.10-1.50]
        ├── ATD: AI 技术债务因子 [1.00-1.25]
        ├── LCPL: 低代码平台锁定 [0.95-1.30]
        ├── PVOL_serverless: Serverless 平台变更 [1.05-1.25]
        └── 其他 11 个传统乘数（PERS, RCPX, PDIF, PREX 等）
```

---

## 4. 完整计算示例

### 场景：电商订单系统的复用成本估算（2026 版）

**项目参数**：

- 新开发订单系统预计需要 10,000 SLOC（传统架构）
- 组织内已有库存管理系统的订单处理模块，共 3,000 SLOC
- 计划复用该模块，需进行以下改编：
  - 设计修改 DM: 30%（适配新的数据库 Schema）
  - 代码修改 CM_original: 20%
  - 集成工作量 IM_original: 50%（新的消息队列集成）
- AI 工具: 高级 Agent (Cursor)，AEF = 0.55，ARF = 1.25
- AI 技术债务: ATD = 1.15
- AA = 10%（评估与同化）
- SU = 20%（软件理解）
- UNFM = 0.5
- 组织复用成熟度: 高（产品线级复用 + AI 辅助）→ RUSE_2026 = 0.71

**计算过程**：

```text
1. AI 调整后改编参数:
   CM_effective = 20% × 0.55 = 11%
   IM_effective = 50% × 1.25 = 62.5%

2. 改编调整因子:
   AAF = 0.4 × 30% + 0.3 × 11% + 0.3 × 62.5%
       = 0.12 + 0.033 + 0.1875 = 0.3405

3. 非线性调整 (AAF ≤ 0.5):
   ESLOC = 3,000 × [10 + 34.05 × (1 + 0.02 × 20 × 0.5)] / 100
         = 3,000 × [10 + 34.05 × 1.2] / 100
         = 3,000 × 50.86 / 100
         = 1,526 SLOC

4. 总项目规模:
   Size = (10,000 - 3,000) + 1,526 = 8,526 SLOC = 8.526 KSLOC

5. 规模因子评分:
   PREC = 4.0, FLEX = 3.0, RESL = 3.0, TEAM = 3.0, PMAT = 3.0
   Σ(SFⱼ) = 16.0
   E = 0.91 + 0.01 × 16.0 = 1.07

6. 工作量乘数（关键项）:
   RUSE_2026 = 0.71 (高复用)
   AEF       = 0.85 (AI 编码效率综合)
   ARF       = 1.25 (AI 审查成本)
   ATD       = 1.08 (技术债务 ⁴√1.15)
   ∏(EMᵢ) ≈ 0.71 × 0.85 × 1.25 × 1.08 ≈ 0.815

7. 开发工作量（2026 校准）:
   PM_2026 = 2.20 × (8.526)^1.07 × 0.815
           = 2.20 × 9.77 × 0.815
           ≈ 17.5 人月
```

**多情景对比分析**：

| 情景 | A 常数 | Size (KSLOC) | E | 综合乘数 | 工作量 (PM) | 相对基准 |
|------|--------|-------------|---|---------|------------|---------|
| **基准（无复用，无 AI，原始 COCOMO II）** | 2.94 | 10.0 | 1.07 | 1.00 | **34.5** | 100% |
| 有复用，无 AI（原始模型） | 2.94 | 7.99 | 1.07 | 0.78 | **20.9** | 60.6% |
| 有复用，基础 Copilot | 2.50 | 7.99 | 1.07 | 0.68 | **15.4** | 44.6% |
| **有复用，高级 Agent（2026 校准）** | **2.20** | **8.526** | **1.07** | **0.815** | **17.5** | **50.7%** |
| 有复用，全栈 AI 生成 | 2.20 | 8.526 | 1.07 | 0.69 | **14.8** | 42.9% |

**关键洞察**：

- 相对于无复用基准：节约 17.0 人月 (50.7%)
- 相对于传统复用（无 AI）：节约 3.4 人月 (16.3%)
- AI 的净效应约为 10-17% 的额外节约（而非表面上的 45-55%），因为审查成本和技术债务部分抵消了编码效率收益
- 若项目为安全关键系统（ARF = 1.50），2026 版工作量升至 **19.8 人月**，AI 净收益收窄至 42.6%

---

## 5. RUSE 乘数 2026 建议值

| RUSE 等级 | 描述 | 2026 建议值 | 复用场景 | 配套实践 |
|-----------|------|------------|----------|---------|
| **极低** | 无复用，全部自研 | 1.00 | 创新项目、无先例 | — |
| **很低** | 偶发复用，无系统管理 | 0.92 | 个人项目、临时复用 | AI 代码搜索 |
| **低** | 项目级复用，有管理 | 0.84 | 团队内共享代码 | 内部组件库 |
| **一般** | 组织级复用，标准化 + IDP | 0.78 | 企业级组件库 + Golden Path | SBOM + 自动化测试 |
| **高** | 产品线级复用 + AI 辅助 | 0.71 | 产品线工程 | AI 自动适配 + 变异测试 |
| **很高** | 跨组织复用 + SLSA L3+ | 0.64 | 行业级共享组件 | SLSA provenance + 签名验证 |
| **极高** | 黑盒复用 + AI 自动集成 | 0.56 | COTS/SaaS + AI 集成 | AI agent 自动 API 映射 |

---

## 6. 行业对比分析

### 6.1 不同架构范式的 COCOMO II 2026 参数对比

| 参数 | 传统单体 | 微服务 | Serverless | 低代码平台 |
|------|---------|--------|-----------|-----------|
| **A_2026** | 2.20 | 2.20 | 2.00 | 2.30 |
| **Size 度量** | KSLOC | KSLOC | KSLOC_EFU | KFP × CF |
| **RUSE 基线** | 0.84 | 0.78 | 0.71 | 0.80 |
| **AI 工具适用性** | 中 | 高 | 高 | 极高 |
| **AEF 典型值** | 0.65 | 0.55 | 0.50 | 0.40 |
| **ARF 典型值** | 1.20 | 1.25 | 1.20 | 1.15 |
| **PVOL** | 1.00 | 1.05 | 1.15 | 1.30 |
| **典型乘数积** | 0.75 | 0.68 | 0.62 | 0.72 |

### 6.2 AI 辅助开发的权衡矩阵

| 维度 | 短期收益 (0-6 月) | 中期成本 (6-18 月) | 长期影响 (18 月+) |
|------|-----------------|-------------------|------------------|
| 编码速度 | +30% 至 +55% | — | — |
| 代码审查 | — | +10% 至 +35% | — |
| 技术债务 | — | — | +8% 至 +25% |
| 缺陷密度 | -5% 至 +41%* | — | — |
| 协调开销 | — | +8% | — |
| 知识传递 | 不确定 | 不确定 | -15% 至 -30%** |

> \* Uplevel 研究显示 Copilot 组 bug 增加 41%；GitHub 研究显示新手 bug 减少。结果因使用模式和审查严格度而异。
> \*\* AI 生成代码的理解度下降可能导致长期知识传递成本增加（需更多实证研究验证）。

---

## 7. 局限性声明

> **公理 V.1** (Value Quantification Uncertainty): 复用的价值量化存在固有的不确定性。COCOMO II 的校准常数基于历史数据，对 AI 辅助开发、Serverless 架构、低代码平台的适用性存在偏差。任何量化结果应被视为"最佳估计"而非"精确真理"。
> **公理 V.2** (Strategic Value Non-Quantifiability): 复用的战略价值（上市时间优势、生态系统网络效应、组织能力进化）难以用货币精确量化，但不可因此忽略。
> **定理 V.1** (ROI Threshold): 复用项目的 ROI 为正的必要条件是：复用资产的改编调整因子 AAF < AAF_ECONOMIC_FLOOR（0.7，canonical [0.0, 1.0]）。若 AAF ≥ AAF_ECONOMIC_FLOOR，复用的直接经济价值消失，仅剩战略价值。
> **定理 V.2** (AI Net Benefit Ceiling): 在 2026 年的技术条件下，AI 辅助开发对 COCOMO II 估算的综合净收益上限约为 30-35%（相对于传统开发），远低于表面编码效率提升的 55%。组织在决策时应采用保守估算（净收益 15-25%）。

---

> 最后更新: 2026-06-06
> 下次更新: 基于更多 2026 年实际项目数据校准 A_2026 和 AEF/ARF 参数

---

## 参考索引与权威来源

| 来源 | URL | 核查日期 |
|:---|:---|:---|
| USC COCOMO II | <https://cssed.usc.edu/research/research-sponsored-software/cocomo/cocomo-ii/> | 2026-07-09 |
| COCOMO II Model Definition Manual (PDF) | <https://athena.ecs.csus.edu/~buckley/CSc231_files/Cocomo_II_Manual.pdf> | 2026-07-09 |
| NASA Reuse Readiness Levels (RRL) | <https://ntrs.nasa.gov/api/citations/20120010312/downloads/20120010312.pdf> | 2026-07-09 |
| NASA SWEHB — Software Reuse Catalog | <https://swehb.nasa.gov/display/SWEHBVD/SWE-148+-+Contribute+to+Agency+Software+Catalog> | 2026-07-09 |
| FinOps Foundation — Unit Economics | <https://www.finops.org/framework/capabilities/unit-economics/> | 2026-07-09 |
| CMMI Institute | <https://cmmiinstitute.com/> | 2026-07-09 |

文献：

- Boehm, B. et al.: *Software Cost Estimation with COCOMO II* (Prentice Hall, 2000)
- USC CSSE: *COCOMO II Model Definition Manual* (2000)
- COCOMO II.2000 Calibration Data (161 projects)
- GitHub / Vaithilingam et al. (2024): "Measuring GitHub Copilot's Impact on Productivity" (CACM)
- Xu, F. et al. (2025): "AI-Assisted Programming Decreases the Productivity of Experienced Developers..." (arXiv:2510.10165)
- Song, F. et al. (2024): "The Impact of Generative AI on Collaborative Open-Source Software Development" (arXiv:2410.02091)
- Uplevel (2024): "AI Won't Solve Your Developer Productivity Problems for You"
- CompaniesHistory (2026): "GitHub Copilot Statistics And User Trends In 2026"
- Jones, C.: *Applied Software Measurement* (SLOC/FP 转换表)
- IFPUG: *Function Point Counting Practices Manual* (1994+)

> **交叉引用**:
>
> - COCOMO II 深度解析: [`cocomo-ii-reuse-model-deep-dive.md`](./cocomo-ii-reuse-model-deep-dive.md)
> - 标准对齐矩阵: [`struct/01-meta-model-standards/01-iso-420xx-family/alignment-matrix.md`](../../01-meta-model-standards/01-iso-420xx-family/alignment-matrix.md)
> - 复用度量指标: [`struct/06-cross-layer-governance/05-metrics-kpi/metrics-framework.md`](../../06-cross-layer-governance/05-metrics-kpi/metrics-framework.md)
> - 可运行工具: [`../tools/cocomo-calculator.py`](../tools/cocomo-calculator.py)、[`../tools/cocomo-streamlit.py`](../tools/cocomo-streamlit.py)


---

## 补充说明：COCOMO II 复用模型 2026 校准版

## 概念定义

**定义**：COCOMO II（Constructive Cost Model II）通过规模、复用程度、人员能力、平台成熟度等因子预测软件成本；其复用模型（REVL、AA、SU 等）量化复用带来的生产率提升。

## 示例

**示例**：估算企业级消息中间件复用时，COCOMO II 将等效新代码行数按复用适配度从 100 KSLOC 降至 35 KSLOC，工期预测缩短 40%。

## 反例

**反例**：未计入文档、测试与治理成本，仅凭代码行复用率宣称“节省 80%”，上线后维护 overrun 30%。

## 权威来源

> **权威来源**:
>
> - [USC COCOMO II](https://cssed.usc.edu/research/research-sponsored-software/cocomo/cocomo-ii/)
> - [Barry Boehm - USC CSSE](https://cssed.usc.edu/)
> - 核查日期：2026-07-07