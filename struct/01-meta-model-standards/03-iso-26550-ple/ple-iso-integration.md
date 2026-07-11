# ISO 26550:2015 产品线工程参考模型与 ISO 42010/42020 的交叉映射

> **版本**: 2026-06-06
> **对齐来源**: ISO/IEC 26550:2015; ISO/IEC/IEEE 42010:2022; ISO/IEC/IEEE 42020:2019; ISO/IEC 26580:2021 (Feature-based PLE)
> **适用范围**: 软件工程架构复用知识体系 Track A — 01 元模型与标准对齐

---

## 1. 映射背景与方法论

### 1.1 为什么要做这个映射

ISO/IEC 26550:2015 定义了软件与系统产品线工程（Software and Systems Product Line Engineering, SSPL）的参考模型，
其核心特征在于**双轨生命周期**（Domain Engineering + Application Engineering）与**显式可变性定义**（Explicit Variability Definition）。
ISO/IEC/IEEE 42010:2022 规定了架构描述（Architecture Description）的通用元模型，
而 ISO/IEC/IEEE 42020:2019 则定义了架构过程（Architecture Processes）的六类核心过程。

本映射旨在回答三个关键问题：

1. 产品线工程的领域工程（Domain Engineering）和应用工程（Application Engineering）如何在 ISO/IEC/IEEE 42010:2022 的架构描述框架中被表达？
2. ISO/IEC/IEEE 42020:2019 的六大架构过程如何支撑产品线工程的双轨生命周期？
3. 产品线工程作为"系统化复用"的最高形式，如何在元模型层面与架构描述/过程标准形成闭环？

### 1.2 映射原则

| 原则 | 说明 |
|------|------|
| **双轨全覆盖** | 覆盖 Domain Engineering 和 Application Engineering 两条轨道的完整生命周期 |
| **variability 显性化** | 将 Variability Model 作为一等公民映射到 ISO 42010/42020 的核心概念 |
| **过程-描述协同** | 同时映射 ISO 42020（过程维度）与 ISO 42010（描述维度），避免"过程无描述"或"描述无过程" |
| **可追溯性** | 每个映射均可追溯到 ISO 26550、ISO 42010 或 ISO 42020 的具体条款 |

---

## 2. ISO 26550 核心概念与 ISO 42010/42020 的预映射

### 2.1 核心概念桥梁

ISO 26550:2015 将产品线工程与管理（Product Line Engineering and Management, PLEM）定义为包含五个主要组成部分的参考模型：
策略规划（Strategic Planning）、组织（Organization）、方法论（Methodology）、系统和组件集成（System and Component Integration）、配置管理（Configuration Management）。

在此基础上，以下建立与 ISO/IEC/IEEE 42010:2022/42020 的核心概念桥梁：

| ISO 26550:2015 概念 | ISO 42010:2022 对应 | ISO 42020:2019 对应 | 映射说明 |
|---------------------|---------------------|---------------------|----------|
| **Product Line** | Entity of Interest (EoI) — 产品线级 | Architecture Governance + Management | 产品线是被架构化的实体，其治理与管理由架构过程支撑 |
| **Domain Engineering** | Architecture Description (AD) — 领域层 | Architecture Conceptualization + Elaboration | 领域工程产出领域资产的架构描述，对应概念化与细化过程 |
| **Application Engineering** | Architecture Description (AD) — 应用层 | Architecture Evaluation + Enablement | 应用工程基于领域资产实例化具体产品，需要评估与使能支撑 |
| **Core Asset** | View Component (逻辑层/可复用层) | Architecture Enablement — Repository | 核心资产是架构描述中的可复用视图组件，由使能过程维护 |
| **Variability Model** | Concern — Variability Concern | Architecture Conceptualization | 可变性是利益相关者的特定关注点，在概念化过程中被识别与定义 |
| **Product (Member Product)** | Entity of Interest (EoI) — 产品级 | Architecture Management | 成员产品是产品线的实例化结果，由管理过程调度 |
| **Asset Repository** | Architecture Description Framework (ADF) 实例 | Architecture Enablement — Process Enablers | 资产库是架构描述框架的物理载体，属于使能过程的支撑能力 |
| **Scoping** | Stakeholder + Concern 识别 | Architecture Governance — 战略对齐 | 范围界定识别利益相关者及其关注点，确保与战略目标对齐 |

### 2.2 产品线工程作为架构描述的生命周期

从 ISO/IEC/IEEE 42010:2022 的视角看，产品线工程本质上是一个**多层级架构描述生命周期**：

```text
Architecture Description (Product Line Level)
├── Viewpoint: Domain Engineering Viewpoint
│   └── View: Domain Architecture View
│       ├── Model Kind: Variability Model, Feature Model, Domain Model
│       └── View Component: Core Assets (ABB layer)
│           ├── Common Asset
│           └── Variable Asset (with Variation Point)
├── Viewpoint: Application Engineering Viewpoint
│   └── View: Application Architecture View
│       ├── Model Kind: Configuration Model, Binding Model
│       └── View Component: Product-Specific Instance (SBB layer)
│           └── Resolution of Variation Point
└── Correspondence Rule: Domain Asset ↔ Application Instance Binding Rule
```

---

## 3. 领域工程（Domain Engineering）与 ISO 42010/42020 的映射

### 3.1 领域工程概述

ISO 26550:2015 明确指出，领域工程的目标是"定义和实现产品线内成员产品共用的领域资产"（define and implement domain assets commonly used by member products within a product line）。
领域工程显式定义产品线的可变性（variability），反映不同市场和市场细分的特定需求。

### 3.2 领域工程 → ISO 42010:2022 映射

| ISO 42010:2022 概念 | 领域工程中的实例 | 映射说明 |
|---------------------|------------------|----------|
| **Stakeholder** | 领域专家、产品线经理、市场分析师、架构委员会 | 关注共性功能提取与可变性边界 |
| **Concern** | 可变性范围（Scope of Variability）、共性/变性比率、市场覆盖度 | "哪些可变、哪些不可变"是核心关注点 |
| **Viewpoint** | *Domain Engineering Viewpoint* | 观察领域资产的专用视点 |
| **View** | Domain Architecture View, Feature Model View, Variability Model View | 领域架构视图、特征模型视图、可变性模型视图 |
| **Model Kind** | Feature Model (FODA), Decision Model, Orthogonal Variability Model (OVM), Domain Model | 特征模型、决策模型、正交可变性模型、领域模型 |
| **View Component** | Core Asset — Common Part, Core Asset — Variable Part, Variation Point, Variant | 核心资产（共性部分/变性部分）、变化点、变体 |
| **Correspondence** | Feature → Asset → Variation Point Traceability | 特征到资产到变化点的追溯对应 |
| **Architecture Decision** | Variability Scoping Decision, Binding Time Decision (compile/runtime/deploy) | 可变性范围决策、绑定时间决策 |
| **Architecture Rationale** | Market Segmentation Analysis, ROI of Reuse | 市场细分分析、复用投资回报分析 |

### 3.3 领域工程 → ISO 42020:2019 映射

| ISO 42020:2019 过程 | 领域工程活动 | 映射说明 |
|---------------------|--------------|----------|
| **Architecture Governance** | 制定产品线策略、可变性治理原则、资产准入标准 | 确保领域资产与组织战略目标对齐 |
| **Architecture Management** | 领域资产版本管理、变更控制、发布计划 | 管理领域资产库的生命周期 |
| **Architecture Conceptualization** | 特征建模、可变性分析、领域范围界定（Scoping） | 识别并综合产品线的概念架构 |
| **Architecture Evaluation** | 领域资产可复用性评估、可变性覆盖率分析、技术债评估 | 评估领域架构是否充分满足多产品需求 |
| **Architecture Elaboration** | 领域设计细化、核心资产实现、接口契约定义 | 将概念架构细化为可交付的领域资产 |
| **Architecture Enablement** | 建立资产库（Asset Repository）、配置管理工具链、特征建模工具 | 提供支撑领域工程的基础设施与能力 |

> **复用视角**: 领域工程是"为复用而开发"（Development for Reuse）的最高形式。其产出的 Core Asset（以 ABB 形式存在）构成了企业连续体中的可复用基线。

---

## 4. 应用工程（Application Engineering）与 ISO 42010/42020 的映射

### 4.1 应用工程概述

ISO 26550:2015 指出，应用工程的目标是"通过利用领域资产（包括共性资产和变性资产）开发应用"。
在应用工程中，领域资产按照已定义的可变性模型进行部署，通过**绑定**（Binding）操作将变化点解析为具体变体，从而派生出成员产品。

### 4.2 应用工程 → ISO 42010:2022 映射

| ISO 42010:2022 概念 | 应用工程中的实例 | 映射说明 |
|---------------------|------------------|----------|
| **Stakeholder** | 产品负责人、客户、最终用户、合规审计员 | 关注具体产品的功能、质量、合规性 |
| **Concern** | 产品差异化需求、性能约束、合规要求、上市时间 | 应用工程关注"这个产品具体是什么" |
| **Viewpoint** | *Application Engineering Viewpoint* | 观察具体产品架构的视点 |
| **View** | Product Architecture View, Configuration View, Derivative View | 产品架构视图、配置视图、派生视图 |
| **Model Kind** | Configuration Model, Binding Model, Product Instance Model | 配置模型、绑定模型、产品实例模型 |
| **View Component** | Product Instance, Bound Variation Point, Resolved Variant, Product-Specific Extension | 产品实例、已绑定变化点、已解析变体、产品特有扩展 |
| **Correspondence** | Domain Asset → Product Instance Realization Correspondence | 领域资产到产品实例的实现对应 |
| **Architecture Decision** | Product Configuration Decision, Binding Time Selection, Extension vs. Core Trade-off | 产品配置决策、绑定时间选择、扩展与核心的权衡 |
| **Architecture Rationale** | Customer Requirement Coverage, Time-to-Market Constraint | 客户需求覆盖度、上市时间约束 |

### 4.3 应用工程 → ISO 42020:2019 映射

| ISO 42020:2019 过程 | 应用工程活动 | 映射说明 |
|---------------------|--------------|----------|
| **Architecture Governance** | 产品配置合规审查、衍生品与产品线策略一致性检查 | 确保派生产品符合产品线治理框架 |
| **Architecture Management** | 产品版本管理、衍生品生命周期管理、变更请求处理 | 管理具体产品的架构演进 |
| **Architecture Conceptualization** | 产品需求分析、特征选择（Feature Selection）、可变性解析 | 理解特定产品的架构目标并综合解决方案 |
| **Architecture Evaluation** | 产品架构评审、需求覆盖度验证、回归测试策略 | 评估产品架构是否满足该产品的特定关注点 |
| **Architecture Elaboration** | 产品详细设计、变性绑定、产品特有组件开发、集成测试 | 细化产品架构至可实施状态 |
| **Architecture Enablement** | 产品配置工具、自动派生工具链、回归测试平台 | 提供支撑应用工程自动化的基础设施 |

> **复用视角**: 应用工程是"基于复用而开发"（Development with Reuse）的典型场景。通过绑定领域资产中的变化点，应用工程将 ABB 级的 Core Asset 实例化为 SBB 级的具体产品，实现"一次开发、多次派生"。

---

## 5. 综合映射表：ISO 26550 核心概念 → ISO 42010/42020

| ISO 26550:2015 核心概念 | ISO 42010:2022 对应 | ISO 42020:2019 对应 | 双轨定位 |
|------------------------|---------------------|---------------------|----------|
| **Product Line** | Entity of Interest (Class of Systems) | Architecture Governance | 治理对象 |
| **Domain Engineering** | AD — Domain Layer Viewpoint | Conceptualization + Elaboration | 左轨：为复用而开发 |
| **Application Engineering** | AD — Application Layer Viewpoint | Evaluation + Enablement | 右轨：基于复用而开发 |
| **Core Asset** | View Component (Reusable, Logical) | Architecture Enablement — Repository | 左轨产出 |
| **Member Product** | Entity of Interest (Individual System) | Architecture Management | 右轨产出 |
| **Variability Model** | Concern + Model Kind (Variability) | Architecture Conceptualization | 双轨共享语言 |
| **Feature Model** | Model Kind — Feature Model | Conceptualization Activity | 领域工程核心 |
| **Variation Point** | View Component + Correspondence Anchor | Elaboration — Interface Definition | 变性注入点 |
| **Variant** | View Component (Alternative) | Conceptualization — Option Analysis | 可选项定义 |
| **Binding** | Correspondence Resolution | Elaboration — Configuration Activity | 右轨核心动作 |
| **Binding Time** | Architecture Decision (Temporal) | Governance — Policy Definition | 架构策略决策 |
| **Asset Repository** | ADF Instance / AD Repository | Enablement — Process Enabler | 使能基础设施 |
| **Scoping** | Stakeholder Concern Identification | Governance — Strategic Alignment | 起点活动 |
| **Product Line Management** | AD Lifecycle Management | Governance + Management | 贯穿双轨 |

---

## 6. 产品线工程作为"系统化复用"的最高形式

### 6.1 复用阶梯中的产品线工程

在软件工程架构复用知识体系中，复用存在清晰的阶梯层次：

| 复用层级 | 复用单元 | 对应标准/框架 | 与本体系主题对应 |
|----------|----------|---------------|------------------|
| **代码级复用** | 函数、类、模块 | 语言标准库、开源组件 | 04-组件架构复用 |
| **组件级复用** | 微服务、库、框架 | OSGi, Maven/npm, SPI | 04-组件架构复用 |
| **架构模式复用** | 设计模式、架构风格 | GoF, POSA, TOGAF Patterns | 05-功能架构复用 |
| **系统级复用** | 子系统、平台 | SOA, MSA, Platform Engineering | 03-应用架构复用 |
| **产品线级复用** | 领域资产、可变性模型 | **ISO 26550** | **02-业务架构复用 + 06-跨层治理** |

产品线工程位于复用阶梯的顶端，其独特价值在于：

1. **预规划复用**（Planned Reuse）：不同于机会主义复用（Opportunistic Reuse），产品线工程在领域工程阶段即系统性识别和设计复用单元；
2. **可变性驱动**（Variability-Driven）：通过显式的 Variability Model 管理"共性"与"差异"，使复用从"复制-修改"升级为"配置-绑定"；
3. **双轨闭环**（Two-Life-Cycle Loop）：领域工程持续沉淀资产，应用工程持续消耗并反馈资产缺口，形成资产演进的飞轮。

### 6.2 与 ISO 42020 架构过程的协同

ISO 42020:2019 的六大架构过程为产品线工程提供了过程骨架：

```text
┌─────────────────────────────────────────────────────────────┐
│                    ISO 42020 Architecture Governance        │
│  (产品线策略对齐、可变性治理原则、资产准入标准)                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    ISO 42020 Architecture Management        │
│  (资产库版本管理、变更控制、发布计划、产品生命周期)             │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│Conceptualization│ │  Evaluation   │  │  Elaboration  │
│   (概念化)     │  │   (评估)      │  │   (细化)      │
│特征建模/范围界定│  │可复用性评估   │  │资产实现/绑定  │
└───────────────┘  └───────────────┘  └───────────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    ISO 42020 Architecture Enablement        │
│  (资产库、特征建模工具、自动派生工具链、配置管理平台)            │
└─────────────────────────────────────────────────────────────┘
```

在此框架下，**Architecture Enablement** 是产品线工程区别于单系统架构的关键使能器。
它提供了特征建模工具（如 Gears、pure::variants、Capella Variability）、资产库（如 Git-based Asset Repository）和自动派生流水线（如 CI/CD for Product Derivation），将人工"复制-修改"升级为自动化"配置-生成"。

---

## 7. 对齐验证

### 7.1 与 ISO 26550:2015 的对齐

- **ISO/IEC 26550:2015, Clause 4.2** — 定义了产品线参考模型的五个组成部分（策略规划、组织、方法论、系统和组件集成、配置管理）。本映射将这五个组成部分分别映射到 ISO/IEC/IEEE 42010:2022 的架构描述元素和 ISO/IEC/IEEE 42020:2019 的架构过程。[[来源](https://www.iso.org/obp/ui/#iso:std:iso-iec:26550:ed-2:v1:en)]
- **ISO/IEC 26550:2015, Clause 5.3** — 明确了领域工程与应用工程的双轨生命周期，以及可变性在两条轨道之间的传递机制。本映射的第 3、4 节逐层展开了这一双轨机制与 ISO/IEC/IEEE 42010:2022/42020 的对应关系。
- **ISO/IEC 26580:2021** — 作为 ISO/IEC 26550:2015 的配套标准，提供了基于特征的产品线工程方法与工具指南，进一步细化了 Feature Model、Variation Point、Binding 等概念的操作定义。[[来源](https://www.iso.org/standard/71883.html)]

### 7.2 与 ISO 42010:2022 的对齐

- **ISO/IEC/IEEE 42010:2022, Clause 5.2** — 定义了架构描述的概念模型，包括 Entity of Interest、Stakeholder、Concern、Viewpoint、View、View Component、Model Kind、Correspondence 等。本映射将产品线（Product Line）和成员产品（Member Product）分别映射为不同粒度的 EoI，将 Core Asset 映射为可复用的 View Component。[[来源](https://www.iso.org/standard/74296.html)]
- **ISO/IEC/IEEE 42010:2022, Clause 6.8** — 引入 View Component 作为"one or more architecture views 的可分离部分"，恰好容纳了 Core Asset（共性/变性部分）作为跨视图复用单元的定位。
- **ISO/IEC/IEEE 42010:2022, Clause 6.10** — 要求记录 Architecture Decision 和 Architecture Rationale。本映射将 Binding Time Decision、Variability Scoping Decision 等关键决策纳入此框架。

### 7.3 与 ISO 42020:2019 的对齐

- **ISO/IEC/IEEE 42020:2019, Clause 6.2** — 定义了 Architecture Governance 过程，其目的是"确保架构集合与组织目标、政策和策略保持一致"。产品线工程中的策略规划和范围界定（Scoping）直接对应此过程的输出。[[来源](https://www.iso.org/standard/68982.html)]
- **ISO/IEC/IEEE 42020:2019, Clause 6.6** — 定义了 Architecture Enablement 过程，其目的是"为其他架构过程提供支持能力"。产品线工程中的资产库、特征建模工具、自动派生平台正是 Enablement 的典型实例。
- **ISO/IEC/IEEE 42020:2019, Annex A** — 明确指出本标准适用于"product lines"（产品线）的架构活动，为本映射提供了直接的标准依据。

### 7.4 验证结论

1. **产品线工程的双轨生命周期与 ISO/IEC/IEEE 42020:2019 的架构过程形成精确对应**：领域工程对应 Conceptualization + Elaboration（概念化与细化），应用工程对应 Evaluation + Enablement（评估与使能），而 Governance + Management（治理与管理）贯穿双轨。
2. **ISO/IEC 26550:2015 的 Core Asset / Variability Model 与 ISO/IEC/IEEE 42010:2022 的 View Component / Concern / Model Kind 形成精确对应**：产品线资产是可复用的架构描述组件，可变性是架构关注点的特殊化表达。
3. **产品线工程作为"系统化复用"的最高形式，其元模型基础已被 ISO/IEC/IEEE 42010:2022/42020 完整覆盖**：从战略治理到资产使能，从概念描述到过程执行，标准 trio（26550 + 42010 + 42020）共同构成了可复用架构的工程化基础。

---

## 8. 参考索引

1. ISO/IEC. *ISO/IEC 26550:2015 — Software and systems engineering — Reference model for product line engineering and management*. 2015. <https://www.iso.org/standard/69529.html>
2. ISO/IEC. *ISO/IEC 26580:2021 — Software and systems engineering — Methods and tools for the feature-based approach to software and systems product line engineering*. 2021. <https://www.iso.org/standard/71883.html>
3. ISO/IEC/IEEE. *ISO/IEC/IEEE 42010:2022 — Software, systems and enterprise — Architecture description*. 2022. <https://www.iso.org/standard/74296.html>
4. ISO/IEC/IEEE. *ISO/IEC/IEEE 42020:2019 — Software, systems and enterprise — Architecture processes*. 2019. <https://www.iso.org/standard/68982.html>
5. Pohl, K., Böckle, G., & van der Linden, F. *Software Product Line Engineering: Foundations, Principles and Techniques*. Springer, 2005.（ISO/IEC 26550:2015 的核心参考来源之一）
6. Clements, P. & Northrop, L. *Software Product Lines: Practices and Patterns*. Addison-Wesley, 2002.
7. Raatikainen, M., Tiihonen, J., & Männistö, T. "Software product lines and variability modeling." *The Journal of Systems and Software*, 149 (2019): 485-510.

---

> **最后更新**: 2026-06-06
> **维护者**: Track A — 01 元模型与标准对齐
> **状态**: Phase 1 交付物（T07 完成）


---

## 示例

某汽车电子企业将 ISO/IEC 26550:2015 的双轨生命周期落地为：

- **领域工程**：定义 ECU 软件平台及其 Variability Model，覆盖动力、底盘、信息娱乐三个产品族；
- **应用工程**：通过 Feature Selection 将平台资产绑定为具体车型 ECU。

对应 ISO/IEC/IEEE 42020:2019，领域工程由 Architecture Conceptualization（Clause 8）与 Elaboration（Clause 10）支撑，应用工程由 Evaluation（Clause 9）与 Enablement（Clause 11）支撑，资产库由 Management（Clause 7）维护。结果单车软件复用率从 45% 提升至 78%，且新车型上市周期缩短 30%。

## 反例

某 IoT 团队把产品线工程简化为“复制上一个项目后改配置”：

- 没有显式 Variability Model，导致共性代码与差异代码边界模糊；
- 未按 ISO/IEC 26550:2015 的 Domain/Application Engineering 分离职责，领域资产被具体项目直接修改；
- 三个月后同一平台出现 6 个分支，回归测试成本超过新建项目，复用体系名存实亡。

**避免建议**：在领域工程阶段显式定义 Feature Model、Variation Point 与 Binding Time，并由 Architecture Governance（ISO/IEC/IEEE 42020:2019 Clause 6）强制保护核心资产不被单个应用项目直接改写。

## 论证

因为 ISO/IEC 26550:2015 将显式 Variability Model 作为产品线工程区别于单系统工程的核心特征，所以若团队仅以“复制-修改”方式复用而不定义变化点，就无法形成受控的绑定规则，复用收益会被维护成本抵消。

## 权威来源与核查日期

> **权威来源**：
>
> - [ISO/IEC 26550:2015 — Product line engineering](https://www.iso.org/standard/69529.html)（核查日期：2026-07-08）
> - [ISO/IEC 26580:2021 — Feature-based PLE](https://www.iso.org/standard/71883.html)（核查日期：2026-07-08）
> - [ISO/IEC/IEEE 42010:2022 — Architecture description](https://www.iso.org/standard/74296.html)（核查日期：2026-07-08）
> - [ISO/IEC/IEEE 42020:2019 — Architecture processes](https://www.iso.org/standard/68982.html)（核查日期：2026-07-08）
> - [ISO/IEC/IEEE 42030:2019 — Architecture evaluation](https://www.iso.org/standard/73436.html)（核查日期：2026-07-08）
>
> **核查日期**：2026-07-08