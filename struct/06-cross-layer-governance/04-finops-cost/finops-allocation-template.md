# FinOps 四级成本分摊模型模板 (L1–L4 Allocation Model)

> **版本**: 2026-06-08
> **定位**: 将架构复用的共享成本按资产级、项目级、组织级、生态级进行透明化分摊
> **对齐来源**: [FinOps Foundation Framework 2026](https://www.finops.org/framework/), FinOps Foundation: Cost Allocation Capabilities, FOCUS 1.0
> **状态**: P2-T5 交付物

---

## 目录

- [FinOps 四级成本分摊模型模板 (L1–L4 Allocation Model)](#finops-四级成本分摊模型模板-l1l4-allocation-model)
  - [目录](#目录)
  - [1. 四级分摊模型总览](#1-四级分摊模型总览)
    - [1.1 L1 资产级 (Asset-Level)](#11-l1-资产级-asset-level)
    - [1.2 L2 项目级 (Project-Level)](#12-l2-项目级-project-level)
    - [1.3 L3 组织级 (Organizational-Level)](#13-l3-组织级-organizational-level)
    - [1.4 L4 生态级 (Ecosystem-Level)](#14-l4-生态级-ecosystem-level)
    - [1.5 FOCUS 1.0 与 Cloud Unit Economics 融入](#15-focus-10-与-cloud-unit-economics-融入)
    - [1.6 FinOps Framework 2026 能力映射](#16-finops-framework-2026-能力映射)
  - [2. 分摊公式](#2-分摊公式)
    - [2.1 直接成本公式](#21-直接成本公式)
    - [2.2 间接成本公式](#22-间接成本公式)
    - [2.3 风险成本公式](#23-风险成本公式)
    - [2.4 公式符号说明](#24-公式符号说明)
  - [3. 决策矩阵：何时分摊？何时不摊？](#3-决策矩阵何时分摊何时不摊)
  - [4. 计算案例：统一认证服务被 3 个项目复用](#4-计算案例统一认证服务被-3-个项目复用)
    - [4.1 假设数据](#41-假设数据)
    - [4.2 L1 资产级直接成本计算](#42-l1-资产级直接成本计算)
    - [4.3 L2 项目级使用量分摊](#43-l2-项目级使用量分摊)
    - [4.4 L3 组织级间接成本分摊](#44-l3-组织级间接成本分摊)
    - [4.5 L4 生态级风险成本分摊](#45-l4-生态级风险成本分摊)
    - [4.6 最终汇总](#46-最终汇总)
    - [4.7 洞察与建议](#47-洞察与建议)
    - [反模式：成本分摊沦为“政治博弈”](#反模式成本分摊沦为政治博弈)
  - [5. 配套工具](#5-配套工具)
    - [5.1 Excel 导出脚本](#51-excel-导出脚本)
    - [5.2 示例数据文件](#52-示例数据文件)
    - [5.3 预算与预测分析脚本](#53-预算与预测分析脚本)
    - [5.4 承诺折扣优化器](#54-承诺折扣优化器)
    - [5.5 成本异常检测器](#55-成本异常检测器)
    - [5.6 AI GPU 成本计算器](#56-ai-gpu-成本计算器)
  - [6. 实施检查清单](#6-实施检查清单)
    - [第 1–14 天：数据准备](#第-114-天数据准备)
    - [第 15–30 天：模型校准](#第-1530-天模型校准)
    - [第 31–60 天：试运行与 Showback](#第-3160-天试运行与-showback)
    - [第 61–90 天：正式运营与持续改进](#第-6190-天正式运营与持续改进)
  - [7. 权威来源](#7-权威来源)

---

## 1. 四级分摊模型总览

跨层复用成本分摊覆盖四层架构（业务→应用→组件→功能）的直接成本、间接成本和风险成本。
模型将成本划分为四个层级，从微观资产到宏观生态，确保每一分钱都有清晰的归属逻辑。

```text
L4 生态级 (Ecosystem)
├─ 开源依赖成本
├─ 供应链安全成本
└─ 许可证合规与 vendor lock-in 准备金

L3 组织级 (Organizational)
├─ 卓越中心 (CoE) 运营成本
├─ 平台工程团队成本
└─ 共享基础设施成本

L2 项目级 (Project)
├─ 项目A使用复用资产的分摊
├─ 项目B使用复用资产的分摊
└─ 项目C使用复用资产的分摊

L1 资产级 (Asset)
├─ 原始开发成本 (按 AAF 调整)
├─ 维护成本
└─ 部署/运营成本
```

### 1.1 L1 资产级 (Asset-Level)

**定义**: 单个复用组件/服务的直接成本，包含开发、维护、部署全生命周期的货币化度量。

| 成本子项 | 说明 | 数据来源 |
|---------|------|---------|
| **原始开发成本** | 资产首次构建的投入，按摊销期折算为月度成本 | COCOMO II 估算、实际人天记录 |
| **AAF (改编调整因子)** | Adaptation Adjustment Factor，反映资产为支持多场景复用所做的额外开发投资 | ISO/IEC 26564 复用度量标准 |
| **维护成本** | 月度 Bug 修复、安全补丁、版本升级投入 | 工单系统、Sprint 投入记录 |
| **部署成本** | 月度 CI/CD、发布、回滚、环境维护投入 | CI/CD 平台日志、运行时长 |

**关键原则**: 原始开发成本属于沉没成本，但通过 AAF 和摊销机制，可将其转化为各消费项目的"机会成本"基准——即若不复用，项目需自行投入的开发成本。

### 1.2 L2 项目级 (Project-Level)

**定义**: 项目使用复用资产的分摊，基于实际使用量按单位成本进行比例分配。

| 分摊维度 | 适用场景 | 计量单位 |
|---------|---------|---------|
| **调用量** | API/微服务复用 | 请求数 (requests) |
| **事务量** | 支付/交易组件复用 | 事务数 (transactions) |
| **消息量** | 通知/消息通道复用 | 消息数 (messages) |
| **查询量** | 分析/检索功能复用 | 查询数 (queries) |
| **存储量** | 共享存储/缓存复用 | GB / 对象数 |

**分摊逻辑**: 资产月度直接成本按各项目的实际使用量占总使用量的比例进行分配。未被任何项目使用的资产成本，由平台团队或 CoE 承担。

### 1.3 L3 组织级 (Organizational-Level)

**定义**: 卓越中心 (CoE)、平台团队、共享基础设施的间接成本，按项目的复用受益程度进行分摊。

| 成本池 | 说明 | 分摊驱动因子 |
|-------|------|------------|
| **CoE 运营成本** | 架构治理、标准制定、技术雷达、培训 | 项目复用资产数 |
| **平台团队成本** | 共享组件维护、Golden Path、CI/CD 平台 | 项目复用资产数 |
| **共享基础设施** | K8s 控制面、监控、日志、制品库 | 项目复用资产数 / 资源占用 |

**分摊逻辑**: 间接成本无法直接按单一使用量归属，因此采用"受益程度代理指标"——项目复用的资产数量越多，从平台和 CoE 获得的支撑越大，应承担更多间接成本。

### 1.4 L4 生态级 (Ecosystem-Level)

**定义**: 开源依赖、供应链安全、许可证合规、供应商锁定等外部性风险成本。

| 风险类别 | 说明 | 度量方式 |
|---------|------|---------|
| **供应链风险** | 开源组件 CVE、老旧依赖、维护者弃用 | 风险评分 (1–10) |
| **安全投入** | 为对冲供应链风险所需的持续安全投入 | 安全投入系数 (% of operational cost) |
| **许可证合规** | GPL 传染、商用许可证违规潜在罚金 | 月度准备金 |
| **供应商锁定** | 单一云厂商/技术栈的迁移风险对冲 | 月度准备金 |

**分摊逻辑**: 风险成本首先通过评分与系数计算为总体准备金，再按各项目的（直接+间接）成本比例分摊——成本规模越大的项目，风险暴露面越大。

### 1.5 FOCUS 1.0 与 Cloud Unit Economics 融入

**FOCUS 1.0**（FinOps Open Cost and Usage Specification）是 FinOps Foundation 主导的云成本数据开放标准，目标是把多云账单归一化为统一 Schema。将 FOCUS 1.0 融入本模型可实现：

| FOCUS 1.0 核心字段 | 本模型用法 | 收益 |
|:---|:---|:---|
| `BilledCost` / `EffectiveCost` | L1 资产直接成本、L2 项目分摊金额 | 消除云厂商账单格式差异 |
| `ResourceId` / `ResourceType` | 资产级成本归属与标签治理 | 精确追踪复用资产实例 |
| `Tags` / `Labels` | 项目归属、环境、成本中心 | 驱动 L2 使用量分摊与 Showback |
| `UsageQuantity` / `UsageUnit` | L2 计量单位（请求数、事务数、GB） | 支持按比例分摊 |
| `ChargePeriodStart` / `ChargePeriodEnd` | 月度摊销与预测校准 | 对齐财务结账周期 |

**Cloud Unit Economics** 将成本转化为业务可理解的单位指标。本模型推荐的单位经济学指标包括：

- **每次认证请求成本** = 资产月度总成本 ÷ 月度请求数
- **每事务成本** = 支付/交易组件月度总成本 ÷ 月度事务数
- **每 Token 成本** = AI 服务月度总成本 ÷ 输入/输出 Token 总数
- **每用户成本** = 共享平台月度总成本 ÷ 活跃用户数

这些指标可与 FinOps Foundation 的 **Unit Economics Capability** 对齐，用于跨项目、跨云厂商的 TCO 比较与投资决策。

### 1.6 FinOps Framework 2026 能力映射

| FinOps Framework 2026 能力 | 本模型对应层级 | 说明 |
|:---|:---|:---|
| **Allocation**（Understand Usage & Cost） | L2 项目级 + L1 资产级 | 将共享复用成本分配到责任方 |
| **Managing Shared Cost** | L3 组织级 + L4 生态级 | 平台、CoE、供应链风险成本分摊 |
| **Unit Economics**（Quantify Business Value） | 单位成本指标 | 把技术成本转化为业务单位成本 |
| **KPI & Benchmarking** | 复用率、成本透明度、摊销回收 | 持续度量成熟度与效率 |
| **Governance, Policy & Risk** | L4 风险成本 + 决策矩阵 | 建立分摊策略、合规与风险准备金 |
| **Executive Strategy Alignment** | Showback/Chargeback 报告 | 向高管呈现技术投资价值 |

---

## 2. 分摊公式

### 2.1 直接成本公式

**资产月度直接成本**:

$$
C_{asset}^{direct} = \frac{C_{dev} \times AAF}{T_{amortize}} + C_{maint} + C_{deploy}
$$

**项目分摊的直接成本**:

$$
C_{project}^{direct} = \sum_{i \in Assets} \left( C_{i}^{direct} \times \frac{U_{project,i}}{\sum_{p \in Projects} U_{p,i}} \right)
$$

### 2.2 间接成本公式

**总间接成本**:

$$
C^{indirect} = C_{CoE} + C_{platform} + C_{infra}
$$

**项目分摊的间接成本**:

$$
C_{project}^{indirect} = C^{indirect} \times \frac{N_{project}^{assets}}{\sum_{p \in Projects} N_{p}^{assets}}
$$

其中 $N_{project}^{assets}$ 为该项目实际复用的资产数量。

### 2.3 风险成本公式

**总风险成本**:

$$
C^{risk} = R_{license} + R_{vendor} + (C^{direct} + C^{indirect}) \times \frac{S_{supply}}{10} \times F_{security}
$$

**项目分摊的风险成本**:

$$
C_{project}^{risk} = C^{risk} \times \frac{C_{project}^{direct} + C_{project}^{indirect}}{\sum_{p \in Projects} (C_{p}^{direct} + C_{p}^{indirect})}
$$

### 2.4 公式符号说明

| 符号 | 含义 | 单位 |
|------|------|------|
| $C_{dev}$ | 原始开发成本 | USD |
| $AAF$ | 改编调整因子 (0–1) | 无量纲 |
| $T_{amortize}$ | 摊销月数 | 月 |
| $C_{maint}$ | 月度维护成本 | USD/月 |
| $C_{deploy}$ | 月度部署成本 | USD/月 |
| $U_{project,i}$ | 项目对资产 $i$ 的使用量 | 视资产而定 |
| $C_{CoE}$ | CoE 月度运营成本 | USD/月 |
| $C_{platform}$ | 平台团队月度成本 | USD/月 |
| $C_{infra}$ | 共享基础设施月度成本 | USD/月 |
| $S_{supply}$ | 供应链风险评分 (1–10) | 无量纲 |
| $F_{security}$ | 安全投入系数 | 无量纲 |
| $R_{license}$ | 许可证合规准备金 | USD/月 |
| $R_{vendor}$ | 供应商锁定准备金 | USD/月 |

---

## 3. 决策矩阵：何时分摊？何时不摊？

并非所有成本都适合纳入分摊模型。以下决策矩阵基于 FinOps Foundation 的共享成本治理最佳实践制定。

| 场景 | 是否分摊 | 分摊层级 | 理由 |
|------|---------|---------|------|
| **专属资源** (单一项目独占的 EC2/RDS) | ✅ 直接归属 | L1 | 可被唯一标签归属，不涉及分摊 |
| **共享微服务** (多项目 API 调用) | ✅ 使用量分摊 | L2 | 有明确的使用量信号 (请求数) |
| **共享平台** (K8s 控制面、监控) | ✅ 受益比例分摊 | L3 | 无单一使用量信号，按受益程度代理指标分摊 |
| **CoE 运营成本** | ✅ 受益比例分摊 | L3 | 组织级公共服务，按项目对平台依赖度分摊 |
| **开源供应链安全** | ✅ 风险比例分摊 | L4 | 外部性成本，按风险暴露面分摊 |
| **一次性探索性开发** (PoC/Spike) | ❌ 不分摊 | — | 成本归属于发起团队，不应转嫁 |
| **通用行政开销** (HR/财务系统) | ❌ 不分摊 | — | 属于 G&A，不应计入技术复用成本 |
| **未上线资产的预研成本** | ❌ 不分摊 | — | 未产生实际使用价值，待上线后再评估 |
| **< $100/月 的微量共享成本** | ⚠️ 可选不分摊 | — | 分摊管理成本高于收益，可计入平台开销 |
| **无使用量信号的共享存储** | ⚠️ 容量均摊 | L2/L3 |  fallback 为按存储容量或项目数均摊 |

**决策流程图**:

```text
成本项识别
    │
    ├─ 能否直接标签归属到单一项目？
    │       ├── 是 → 直接归属 (L1)，不走分摊
    │       └── 否 →
    │               ├─ 有可量化的使用信号？
    │               │       ├── 是 → 使用量分摊 (L2)
    │               │       └── 否 →
    │               │               ├─ 属于平台/CoE/基础设施？
    │               │               │       ├── 是 → 受益比例分摊 (L3)
    │               │               │       └── 否 →
    │               │               │               ├─ 属于供应链/安全/合规风险？
    │               │               │               │       ├── 是 → 风险比例分摊 (L4)
    │               │               │               │       └── 否 → 不计入复用分摊模型
    │               │               │
    │               │               └─ 金额 < $100/月？
    │                       ├── 是 → 计入平台统一开销
    │                       └── 否 → 建立 proxy 指标后分摊
```

---

## 4. 计算案例：统一认证服务被 3 个项目复用

本案例以 `svc-auth`（统一认证服务）为核心，演示一个微服务被 **电商平台**、**移动App**、**管理后台** 三个项目复用的完整四级分摊过程。

### 4.1 假设数据

**资产信息** (`svc-auth`):

| 属性 | 值 |
|------|-----|
| 原始开发成本 $C_{dev}$ | $120,000 |
| 改编调整因子 $AAF$ | 0.85 |
| 摊销月数 $T_{amortize}$ | 36 个月 |
| 月度维护 $C_{maint}$ | $2,000 |
| 月度部署 $C_{deploy}$ | $800 |
| 计量单位 | 认证请求数 (requests) |

**各项目月度使用量**:

| 项目 | 认证请求数 | 占比 |
|------|-----------|------|
| 电商平台 | 450,000 | 52.9% |
| 移动App | 320,000 | 37.6% |
| 管理后台 | 80,000 | 9.4% |
| **合计** | **850,000** | **100%** |

**组织级间接成本**:

| 成本池 | 月度金额 |
|-------|---------|
| CoE 运营成本 | $15,000 |
| 平台团队成本 | $25,000 |
| 共享基础设施 | $10,000 |
| **合计** | **$50,000** |

**风险配置**:

| 属性 | 值 |
|------|-----|
| 供应链风险评分 $S_{supply}$ | 7.5 / 10 |
| 安全投入系数 $F_{security}$ | 0.15 |
| 许可证合规准备金 $R_{license}$ | $2,000 |
| 供应商锁定准备金 $R_{vendor}$ | $1,000 |

### 4.2 L1 资产级直接成本计算

$$
C_{svc\text{-}auth}^{direct} = \frac{120{,}000 \times 0.85}{36} + 2{,}000 + 800 = 2{,}833.33 + 2{,}000 + 800 = \mathbf{\$5{,}633.33/月}
$$

| 成本子项 | 计算 | 金额 |
|---------|------|------|
| 摊销改编开发成本 | $120,000 × 0.85 ÷ 36 | $2,833.33 |
| 月度维护 | — | $2,000.00 |
| 月度部署 | — | $800.00 |
| **资产月度直接成本** | — | **$5,633.33** |

### 4.3 L2 项目级使用量分摊

| 项目 | 认证请求数 | 占比 | 分摊金额 |
|------|-----------|------|---------|
| 电商平台 | 450,000 | 52.9% | $5,633.33 × 52.9% = **$2,980.00** |
| 移动App | 320,000 | 37.6% | $5,633.33 × 37.6% = **$2,118.13** |
| 管理后台 | 80,000 | 9.4% | $5,633.33 × 9.4% = **$535.20** |
| **合计** | **850,000** | **100%** | **$5,633.33** |

> 注：取整后合计为 $5,633.33，实际系统保留精确小数。

### 4.4 L3 组织级间接成本分摊

三个项目均复用了 `svc-auth`，因此每项目的复用资产数 $N^{assets} = 1$。

$$
\sum N_{p}^{assets} = 1 + 1 + 1 = 3
$$

| 项目 | 复用资产数 | 占比 | 间接成本分摊 |
|------|-----------|------|------------|
| 电商平台 | 1 | 33.3% | $50,000 × 33.3% = **$16,666.67** |
| 移动App | 1 | 33.3% | $50,000 × 33.3% = **$16,666.67** |
| 管理后台 | 1 | 33.3% | $50,000 × 33.3% = **$16,666.67** |
| **合计** | **3** | **100%** | **$50,000.00** |

> 若项目间复用资产数不同（如电商平台复用 4 个，移动App复用 3 个，管理后台复用 1 个），则按 4:3:1 的比例分摊。

### 4.5 L4 生态级风险成本分摊

**步骤 1: 计算总风险成本**

$$
C^{risk} = 2{,}000 + 1{,}000 + (5{,}633.33 + 50{,}000) \times \frac{7.5}{10} \times 0.15 = 3{,}000 + 55{,}633.33 \times 0.1125 = \mathbf{\$9{,}258.75/月}
$$

**步骤 2: 按项目（直接+间接）成本比例分摊**

| 项目 | 直接成本 | 间接成本 | 直接+间接 | 占比 | 风险成本 |
|------|---------|---------|----------|------|---------|
| 电商平台 | $2,980.00 | $16,666.67 | $19,646.67 | 35.31% | **$3,269.27** |
| 移动App | $2,118.13 | $16,666.67 | $18,784.80 | 33.76% | **$3,125.76** |
| 管理后台 | $535.20 | $16,666.67 | $17,201.87 | 30.92% | **$2,863.72** |
| **合计** | **$5,633.33** | **$50,000.00** | **$55,633.33** | **100%** | **$9,258.75** |

### 4.6 最终汇总

| 项目 | 直接成本 (L2) | 间接成本 (L3) | 风险成本 (L4) | **总成本** | 占总成本比例 |
|------|-------------|-------------|-------------|-----------|------------|
| 电商平台 | $2,980.00 | $16,666.67 | $3,269.27 | **$22,915.94** | 41.2% |
| 移动App | $2,118.13 | $16,666.67 | $3,125.76 | **$21,910.56** | 39.4% |
| 管理后台 | $535.20 | $16,666.67 | $2,863.72 | **$20,065.59** | 36.1% |
| **合计** | **$5,633.33** | **$50,000.00** | **$9,258.75** | **$64,892.08** | — |

> 注：单个 `svc-auth` 微服务驱动了约 $64,892/月的全部分摊成本。其中间接成本占比最高 (77.0%)，这是因为组织级平台支撑是认证服务能够稳定运行的前提。

### 4.7 洞察与建议

1. **间接成本 dominance**: 间接成本 ($50,000) 远超资产直接成本 ($5,633)，表明平台团队和 CoE 的投入是复用体系的核心成本驱动力。建议定期审查 CoE 产出与项目实际受益的匹配度。

2. **管理后台的间接成本公平性**: 管理后台仅产生 9.4% 的认证请求，但承担了 33.3% 的间接成本。若该趋势在多资产分摊中持续，建议引入"服务等级权重"——核心业务系统 vs 内部系统的间接成本分摊可设置差异化系数。

3. **风险成本不可忽视**: 风险成本占总成本 14.3%，在供应链安全事件频发的背景下，该比例可能进一步上升。建议将风险准备金与实际 CVE 修复支出进行年度对账。

4. **单位经济学视角**: 每次认证请求的分摊成本 = $64,892.08 ÷ 850,000 = **$0.076/次**。该指标可用于与商业化身份认证服务（如 Auth0、AWS Cognito）进行 TCO 比对。

### 反模式：成本分摊沦为“政治博弈”

**背景**：某金融企业在实施 FinOps 分摊时，各业务线对“平台团队成本应由谁承担”争执不下。

**反模式表现**：

1. **分摊驱动因子不透明**：采用按项目数均摊，导致小微项目承担了与核心业务系统相同的平台成本；
2. **Showback 变 Chargeback 过早**：在未建立信任机制前直接扣费，引发业务线抵制；
3. **风险成本被忽视**：开源依赖许可证与 CVE 修复费用未纳入 L4，安全事件后被迫追加预算；
4. **缺乏 FOCUS 标准化**：多云账单字段不一致，财务团队无法复用分摊数据。

**后果**：分摊项目上线 6 个月后被业务线联合申诉，最终回退为“统一平台预算”，复用成本再次变得不可见。

**避免方法**：

- 先 Showback 透明化，再逐步过渡到 Chargeback；
- 使用基于使用量/受益程度的代理指标，而不是简单均摊；
- 将供应链风险、许可证合规纳入 L4 风险成本；
- 采用 FOCUS 1.0 统一多云成本数据 Schema。

---

## 5. 配套工具

### 5.1 Excel 导出脚本

**路径**: [`templates/finops-exporter.py`](./templates/finops-exporter.py)

功能：

- 读取 YAML/JSON 格式的成本数据
- 自动执行 L1–L4 四级分摊计算
- 优先使用 `openpyxl` 导出带 Excel 公式的 `.xlsx` 文件
- `openpyxl` 不可用时，自动生成可直接用 Excel/WPS 打开的 CSV 文件集

**CLI 用法**:

```bash
# 使用 YAML 示例数据生成 Excel 报告
python templates/finops-exporter.py --input templates/example-costs.yaml --output allocation.xlsx

# 强制使用 CSV 输出
python templates/finops-exporter.py --input templates/example-costs.yaml --output allocation.csv --format csv

# 使用 JSON 输入
python templates/finops-exporter.py --input costs.json --output report.xlsx
```

**输出结构** (Excel 模式):

| 工作表 | 内容 | 是否含公式 |
|--------|------|-----------|
| `摘要` | 周期、组织、总成本、风险配置 | 否 |
| `L1-资产级成本` | 各资产月度直接成本、AAF、摊销 | 否 |
| `L2-项目级分摊` | 项目 × 资产 分摊矩阵 | ✅ SUM 公式 |
| `L3-组织级间接成本` | 项目间接成本、复用资产数、占比 | 否 |
| `L4-风险成本` | 项目风险成本、直接+间接基数 | 否 |
| `最终报告` | 项目汇总：直接/间接/风险/总计 | ✅ SUM 公式 |

### 5.2 示例数据文件

**路径**: [`templates/example-costs.yaml`](./templates/example-costs.yaml)

包含完整示例：

- **5 个复用资产**: `svc-auth`, `svc-payment`, `svc-notification`, `svc-analytics`, `svc-search`
- **3 个项目**: `proj-ecommerce`, `proj-mobile`, `proj-admin`
- **组织级间接成本**: CoE $50K/月、平台团队 $80K/月、共享基础设施 $30K/月
- **风险评分**: 供应链风险 7.5/10、安全投入系数 0.15、合规与锁定准备金

### 5.3 预算与预测分析脚本

**路径**: [`templates/finops-budget-forecast.py`](./templates/finops-budget-forecast.py)

功能：

- 读取 YAML / JSON / CSV 格式的历史成本数据（至少 12 个月）
- 计算月度总成本、月度增长率 MoM、年度总成本
- 基于简单线性回归与移动平均生成下季度 / 下半年预测
- 计算预算偏差（Actual vs Budget）与预算执行率 / 运行率（Run Rate）
- 输出控制台表格、CSV 报告，或 Excel 报告（openpyxl 可用时）

**CLI 用法**:

```bash
# 控制台输出
python templates/finops-budget-forecast.py --input templates/example-budget.yaml --format console

# CSV 报告
python templates/finops-budget-forecast.py --input templates/example-budget.yaml --budget 500000 --format csv

# Excel 报告
python templates/finops-budget-forecast.py --input templates/example-budget.yaml --budget 500000 --output forecast.xlsx --format xlsx
```

**输出结构** (Excel 模式):

| 工作表 | 内容 |
|--------|------|
| `历史数据` | 月度成本、MoM 增长率 |
| `预测` | 线性回归下季度预测 + 3 个月移动平均下半年预测 |
| `预算偏差` | 年度总成本、预算、偏差、执行率、运行率 |

**对齐来源**: FinOps Foundation Forecasting Capability、FOCUS 1.0

**示例数据文件**: [`templates/example-budget.yaml`](./templates/example-budget.yaml)

### 5.4 承诺折扣优化器

**路径**: [`templates/finops-commitment-optimizer.py`](./templates/finops-commitment-optimizer.py)

功能：

- 读取 YAML / JSON 输入：按需成本、RI / Savings Plans / Spot 折扣率、工作负载可中断性
- 对比三种场景的年度总成本：全按需、RI/SP + Spot 最优组合、全 Spot（不可中断负载保留按需）
- 输出推荐方案、预计年节省金额、节省百分比、风险等级
- 支持控制台、CSV、Excel 三种输出（openpyxl / PyYAML 缺失时优雅降级）

**CLI 用法**:

```bash
# 控制台输出
python templates/finops-commitment-optimizer.py --input templates/example-commitment.yaml

# CSV 报告
python templates/finops-commitment-optimizer.py --input templates/example-commitment.yaml --csv commitment.csv

# Excel 报告
python templates/finops-commitment-optimizer.py --input templates/example-commitment.yaml --excel commitment.xlsx

# 覆盖风险胃口
python templates/finops-commitment-optimizer.py --input templates/example-commitment.yaml --risk-appetite low
```

**输出结构** (控制台 / Excel):

| 输出项 | 内容 |
|--------|------|
| `场景对比` | 全按需、RI/SP + Spot、全 Spot 的年度成本、节省、节省率、Spot 占比、风险 |
| `推荐方案` | 推荐类型、年度成本、节省、风险等级、推荐理由 |
| `工作负载细分` | 每个工作负载的可中断性、分配类型、折扣率、年度成本 |

**对齐来源**: FinOps Foundation Rate Optimization Capability; AWS / Azure / GCP RI、Savings Plans、Spot 文档

**示例数据文件**: [`templates/example-commitment.yaml`](./templates/example-commitment.yaml)

### 5.5 成本异常检测器

**路径**: [`templates/finops-anomaly-detector.py`](./templates/finops-anomaly-detector.py)

功能：

- 读取 YAML / JSON / CSV 格式的历史成本数据（按资源 / 服务 / 团队逐日或逐月）
- 实现两种异常检测算法：基于均值 + 3σ 的 Z-Score、基于环比增长率阈值（如 >30%）
- 输出异常列表：资源、服务、团队、日期、实际成本、预期成本、偏差百分比、异常类型
- 支持控制台、CSV、Excel 三种输出

**CLI 用法**:

```bash
# 同时使用 Z-Score 与增长率检测
python templates/finops-anomaly-detector.py --input templates/example-anomaly.yaml

# 仅使用 Z-Score，阈值 2.5
python templates/finops-anomaly-detector.py --input templates/example-anomaly.yaml --method zscore --threshold 2.5

# 仅使用增长率，阈值 30%
python templates/finops-anomaly-detector.py --input templates/example-anomaly.yaml --method growth --threshold 0.30

# 指定输出路径
python templates/finops-anomaly-detector.py --input templates/example-anomaly.yaml --output reports/anomaly.xlsx
```

**输出结构** (CSV / Excel):

| 字段 | 说明 |
|------|------|
| `Resource` | 异常资源 |
| `Service` | 服务类型 |
| `Team` | 所属团队 |
| `Date` | 异常日期 |
| `Actual` | 实际成本 |
| `Expected` | 预期成本 |
| `Deviation%` | 偏差百分比 |
| `Type` | 异常类型（zscore / growth_rate） |

**对齐来源**: FinOps Foundation Cost Anomaly Detection Capability、FOCUS 1.0

**示例数据文件**: [`templates/example-anomaly.yaml`](./templates/example-anomaly.yaml)

### 5.6 AI GPU 成本计算器

**路径**: [`templates/ai-gpu-cost-calculator.py`](./templates/ai-gpu-cost-calculator.py)

功能：

- 读取 YAML / JSON 输入，描述 AI 工作负载（GPU、Token、存储、网络、日志）
- 计算 GPU 总成本、Token 输入 / 输出 / 总量成本、附加成本
- 按团队 / 项目 / 模型分摊共享 GPU 与平台服务成本
- 输出每千次推理成本、每百万 token 成本、每 GPU 小时成本等单位经济学指标
- 支持控制台、CSV、Excel 三种输出

**CLI 用法**:

```bash
# 控制台 + CSV + Excel
python templates/ai-gpu-cost-calculator.py --input templates/example-ai-gpu-cost.yaml

# 仅 CSV
python templates/ai-gpu-cost-calculator.py --input templates/example-ai-gpu-cost.yaml --format csv

# 指定输出基础路径
python templates/ai-gpu-cost-calculator.py --input templates/example-ai-gpu-cost.yaml --output reports/ai-gpu-cost --format all
```

**输出结构** (控制台 / CSV / Excel):

| 输出项 | 内容 |
|--------|------|
| `汇总成本` | GPU 集群总成本、Token 成本、附加成本、平台服务分摊成本、总成本 |
| `单位经济学指标` | 每千次推理、每百万 token、每 GPU 小时、每千输入 / 输出 / 总 token 成本 |
| `Workload 明细` | 每个工作负载的 GPU、Token、附加、平台、总成本 |
| `按团队 / 项目 / 模型分摊` | 各维度成本金额与占比 |

**对齐来源**: FinOps Foundation AI Cost Management / Token Economics / Cost Allocation; GSF SCI for AI; 本项目 `ai-cost-allocation.md`、`unit-economics.md`

**示例数据文件**: [`templates/example-ai-gpu-cost.yaml`](./templates/example-ai-gpu-cost.yaml)

---

## 6. 实施检查清单

### 第 1–14 天：数据准备

- [ ] 梳理组织内所有复用资产清单（组件、服务、功能模块）
- [ ] 为每个资产采集：原始开发成本、月度维护/部署成本、AAF
- [ ] 建立项目-资产使用量采集机制（API Gateway 日志、APM 指标）
- [ ] 确认组织级间接成本池：CoE、平台团队、共享基础设施的月度成本
- [ ] 评估供应链风险评分，确定安全投入系数与准备金水平

### 第 15–30 天：模型校准

- [ ] 使用 `example-costs.yaml` 运行 `finops-exporter.py`，验证计算逻辑
- [ ] 与财务部门对齐摊销期、AAF 取值依据
- [ ] 召开项目代表评审会，确认使用量数据的准确性与完整性
- [ ] 处理异常：缺失使用量数据的项目，采用容量/用户数 proxy 指标

### 第 31–60 天：试运行与 Showback

- [ ] 生成首月 Showback 报告（非实际扣费，仅透明度展示）
- [ ] 收集各项目对分摊结果的反馈，校准受益比例代理指标
- [ ] 建立异常申诉流程：项目对分摊结果有异议时的复核机制
- [ ] 将 Showback 报告纳入月度技术治理会议议程

### 第 61–90 天：正式运营与持续改进

- [ ] 从 Showback 过渡到 Chargeback（如组织财务制度就绪）
- [ ] 将分摊结果纳入项目预算与绩效考核
- [ ] 建立季度复盘机制：审查 AAF、摊销期、风险评分是否仍然合理
- [ ] 发布首份《跨层复用成本透明度报告》

---

## 7. 权威来源

- **FinOps Foundation**: [FinOps Framework 2026](https://www.finops.org/insights/2026-finops-framework/) — 2026 框架更新、Executive Strategy Alignment 与跨技术类别治理能力
- **FinOps Foundation**: [FinOps Framework Capabilities](https://www.finops.org/framework/) — 成本分摊核心定义与共享成本治理
- **FinOps Foundation**: [Allocation Capability](https://www.finops.org/framework/capabilities/allocation/) — 分摊策略、标签与共享成本治理
- **FinOps Foundation**: [Unit Economics Capability](https://www.finops.org/framework/capabilities/unit-economics/) — 单位经济学指标定义
- **FinOps Foundation**: [FOCUS 1.0](https://focus.finops.org/) — 云成本数据标准化规范
- **FinOps Foundation**: [FOCUS Specification GitHub](https://github.com/FinOps-Open-Cost-And-Usage-Spec/FOCUS_Spec) — FOCUS 规范仓库
- **NASA SWE-148**: *Software Reuse Metrics* — 复用成本度量基准
- **ISO/IEC 26564:2022**: *Software Reuse — Measurement and Metrics* — AAF 与复用度量标准
- **COCOMO II**: *Model Definition Manual* — 原始开发成本估算方法

> **权威来源**：以上 FinOps Foundation、FOCUS 及 ISO/IEC 26564 等 URL 经人工核查，日期 2026-07-08。

> **交叉引用**:
>
> - FinOps 跨层成本分摊执行模板: [`cost-allocation-template.md`](./cost-allocation-template.md)
> - FinOps 单位经济学: [`finops-unit-economics-2026.md`](./finops-unit-economics-2026.md)
> - COCOMO II 2026 成本估算: [`struct/09-value-quantification/01-cocomo-ii-reuse/cocomo-2026-calibration.md`](../../09-value-quantification/01-cocomo-ii-reuse/cocomo-2026-calibration.md)
> - 成熟度评估: [`struct/06-cross-layer-governance/03-maturity-models/assessment-questionnaire.md`](../03-maturity-models/assessment-questionnaire.md)
> - 标准对齐矩阵: [`struct/01-meta-model-standards/01-iso-420xx-family/alignment-matrix.md`](../../01-meta-model-standards/01-iso-420xx-family/alignment-matrix.md)

> 最后更新：2026-07-08