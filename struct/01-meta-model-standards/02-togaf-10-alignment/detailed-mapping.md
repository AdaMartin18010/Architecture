# TOGAF 10 ABB/SBB 与 ISO 42010:2022 的详细映射

> **版本**: 2026-06-06
> **对齐来源**: The Open Group TOGAF Standard, 10th Edition (2022/2025 Update); ISO/IEC/IEEE 42010:2022; The Open Group: "A Practitioners' Approach to Developing EA Following the TOGAF ADM" (Series Guide)
> **适用范围**: 软件工程架构复用知识体系 Track A — 01 元模型与标准对齐

---

## 1. 映射背景与方法论

### 1.1 为什么要做这个映射

ISO/IEC/IEEE 42010:2022 规定了架构描述（Architecture Description, AD）的通用结构与表达方式，其核心概念包括：

- **Entity of Interest (EoI)**: 架构描述的对象
- **Stakeholder / Concern**: 利益相关者及其关注点
- **Viewpoint / View / View Component**: 视点、视图与视图组件
- **Model Kind**: 模型种类
- **Correspondence / Correspondence Rule**: 对应关系与规则
- **Architecture Decision / Rationale**: 架构决策与依据

TOGAF 10 的架构开发方法（ADM）是一个迭代式、分阶段的企业架构开发过程。
每个阶段都会产生**架构构建块（Architecture Building Block, ABB）**和**解决方案构建块（Solution Building Block, SBB）**。
本映射的目标是将 ABB/SBB 的生命周期与 ISO 42010:2022 的架构描述元模型进行逐阶段对齐，从而在元模型层面打通"过程"与"描述"两个维度，为架构复用提供形式化基础。

### 1.2 映射原则

| 原则 | 说明 |
|------|------|
| **阶段全覆盖** | 覆盖 ADM 全部 10 个阶段（含预备阶段和需求管理） |
| **ABB/SBB 分离** | 区分逻辑构建块（ABB）与物理构建块（SBB）在 ISO 42010 中的不同映射 |
| **视点驱动** | 以 ISO 42010 的 Viewpoint-View-Model Kind 三层结构作为映射骨架 |
| **可验证性** | 每个映射均可追溯到 TOGAF 10 官方文档或 ISO 42010:2022 条款 |

---

## 2. 核心概念预映射

在展开逐阶段映射之前，先建立 TOGAF 10 与 ISO 42010:2022 的核心概念桥梁：

| ISO 42010:2022 概念 | TOGAF 10 概念 | 映射说明 |
|---------------------|---------------|----------|
| Entity of Interest (EoI) | Enterprise / Architecture Project | 架构工作的对象实体；TOGAF 中扩展为"企业"及其子系统 |
| Architecture Description (AD) | Architecture Deliverables / Catalogs | ADM 各阶段输出的架构交付物集合 |
| Architecture Description Framework (ADF) | TOGAF Content Framework + ADM | TOGAF 整体即是一个符合 ISO 42010 的 ADF |
| Stakeholder | Stakeholder Map | TOGAF 利益相关者映射 |
| Concern | Architecture Vision / Drivers / Requirements | 业务驱动力、架构原则、需求规格 |
| Viewpoint | View / Catalog / Matrix Definition | 视点定义，指导视图创建 |
| View | Architecture Artifact / View | 视图实例，如业务架构视图 |
| Model Kind | Artifact Type / Model Type | 模型种类，如业务流程模型、数据模型 |
| View Component | Model / Diagram / Catalog Entry | 视图组件，可复用的架构描述单元 |
| Correspondence Rule | Architecture Contract / Compliance Review | 对应规则与合规评估 |
| Architecture Decision | ADR (Architecture Decision Record) | 架构决策记录 |

在此基础上，**ABB 对应 ISO 42010 中的逻辑 View Component（模型化的架构元素），SBB 对应物理 View Component（实现化的架构元素）**。

---

## 3. 逐阶段详细映射

### 3.1 Preliminary Phase — 架构能力预备

**TOGAF 10 活动**: 建立架构能力、定义架构原则、适配 ADM、设立治理框架。

| ISO 42010:2022 | TOGAF 10 ABB/SBB | 映射说明 |
|----------------|------------------|----------|
| **Stakeholder** | 架构组织、CIO、业务高管 | 识别对架构能力有决策权的利益相关者 |
| **Concern** | 架构原则、治理需求、合规要求 | 关注"如何规范地进行架构工作" |
| **Viewpoint** | *Architecture Capability Viewpoint* | 定义架构能力的观察角度 |
| **View** | Architecture Capability Catalog, Governance Log | 架构能力目录与治理日志视图 |
| **Model Kind** | Organization Model, Maturity Model | 组织模型、成熟度模型 |
| **ABB** | Architecture Governance Framework, Principles Catalog | 逻辑构建块：治理框架、原则目录 |
| **SBB** | EA Tool Platform, Repository Schema | 物理构建块：EA 工具平台、仓库 schema |
| **Correspondence** | Principles → Compliance Criteria | 原则与合规准则的对应 |

> **复用视角**: 本阶段产生的 ABB（如原则目录、治理框架）是跨项目复用的最高层级资产，属于企业连续体中的 Foundation 层级。

### 3.2 Phase A — Architecture Vision

**TOGAF 10 活动**: 定义架构愿景、识别利益相关者、确认业务目标、获得审批。

| ISO 42010:2022 | TOGAF 10 ABB/SBB | 映射说明 |
|----------------|------------------|----------|
| **Stakeholder** | 赞助者、业务负责人、最终用户 | 通过 Stakeholder Map 识别 |
| **Concern** | 业务目标、约束、风险、ROI | 架构愿景需要回应的核心关注点 |
| **Viewpoint** | *Stakeholder Requirements Viewpoint* | 利益相关者需求视点 |
| **View** | Architecture Vision Document, Statement of Architecture Work | 架构愿景文档作为高层视图 |
| **Model Kind** | Business Scenario Model, Goal Model | 业务场景模型、目标模型 |
| **ABB** | Target Business Scenario, High-Level Architecture Definition | 目标业务场景、高层架构定义 |
| **SBB** | Approved Project Charter, Budget Allocation | 已批准的项目章程与预算分配 |
| **Correspondence** | Vision → Business Goals Traceability | 愿景与业务目标的追溯矩阵 |

> **复用视角**: Architecture Vision 是复用的战略上下文。多个项目可共享同一愿景文档的 ABB，降低重复论证成本。

### 3.3 Phase B — Business Architecture

**TOGAF 10 活动**: 开发业务架构，包括组织单元、功能、流程、信息、能力地图。

| ISO 42010:2022 | TOGAF 10 ABB/SBB | 映射说明 |
|----------------|------------------|----------|
| **Stakeholder** | 业务分析师、流程Owner、产品经理 | 关注业务结构和能力 |
| **Concern** | 业务能力、流程效率、信息需求、组织一致性 | 业务架构的核心关注点 |
| **Viewpoint** | *Business Architecture Viewpoint* (TOGAF 内容框架定义) | 业务架构视点 |
| **View** | Business Architecture View, Organization/Actor Catalog, Location Catalog | 业务架构视图及目录 |
| **Model Kind** | Business Process Model, Business Function Model, Organization Decomposition Model | 业务流程/功能/组织分解模型 |
| **ABB** | Business Function, Business Process, Business Service, Business Object, Organization Unit | 业务功能、流程、服务、对象、组织单元 |
| **SBB** | CRM System, ERP Module, BPM Tool Configuration | 具体 CRM/ERP/BPM 工具及配置 |
| **Correspondence** | Function → Process → Service Realization | 功能-流程-服务实现对应规则 |

> **复用视角**: Phase B 的 ABB（如业务能力地图、流程模型）是业务架构复用的核心。它们以逻辑构建块形式存在，可在不同行业解决方案中通过 SBB 实现。

### 3.4 Phase C — Information Systems Architectures

**TOGAF 10 活动**: 开发数据架构和应用架构（通常并行或分步进行）。

#### 3.4.1 Data Architecture

| ISO 42010:2022 | TOGAF 10 ABB/SBB | 映射说明 |
|----------------|------------------|----------|
| **Stakeholder** | 数据架构师、合规官、数据治理委员会 | 关注数据一致性、质量、合规 |
| **Concern** | 数据实体、逻辑模型、治理规则、主数据管理 | 数据架构关注点 |
| **Viewpoint** | *Data Architecture Viewpoint* | 数据架构视点 |
| **View** | Data Architecture View, Data Entity Catalog, Data Lifecycle Diagram | 数据架构视图与目录 |
| **Model Kind** | Entity-Relationship Model, Data Flow Model, Canonical Data Model | ER 模型、数据流模型、规范数据模型 |
| **ABB** | Data Entity, Logical Data Model, Data Service, Data Quality Rule | 数据实体、逻辑数据模型、数据服务 |
| **SBB** | Database Schema (Oracle, PostgreSQL), Data Warehouse Platform, MDM Hub | 具体数据库 schema、数据仓库、MDM 平台 |
| **Correspondence** | Logical Data Model → Physical Schema Mapping | 逻辑-物理数据模型映射 |

#### 3.4.2 Application Architecture

| ISO 42010:2022 | TOGAF 10 ABB/SBB | 映射说明 |
|----------------|------------------|----------|
| **Stakeholder** | 应用架构师、开发团队、集成团队 | 关注应用组合与集成 |
| **Concern** | 应用组合、接口目录、集成模式、可替换性 | 应用架构关注点 |
| **Viewpoint** | *Application Architecture Viewpoint* | 应用架构视点 |
| **View** | Application Architecture View, Application Portfolio Catalog, Interface Catalog | 应用架构视图与目录 |
| **Model Kind** | Component Model, Interface Model, Integration Flow Model | 组件模型、接口模型、集成流模型 |
| **ABB** | Application Component, Application Service, Application Interface, Data Flow | 应用组件、服务、接口、数据流 |
| **SBB** | Microservice Instance, API Gateway (Kong, Apigee), ESB Configuration, SaaS Subscription | 微服务实例、API 网关、ESB、SaaS |
| **Correspondence** | ABB Interface → SBB API Contract (OpenAPI, AsyncAPI) | 逻辑接口与物理 API 契约的对应 |

> **复用视角**: Phase C 是应用架构复用的主战场。ABB（应用组件、接口定义）通过标准化接口契约，可在不同技术栈中以不同 SBB 实现，实现"换芯不换壳"。

### 3.5 Phase D — Technology Architecture

**TOGAF 10 活动**: 开发技术架构，定义平台、基础设施、中间件、网络、硬件标准。

| ISO 42010:2022 | TOGAF 10 ABB/SBB | 映射说明 |
|----------------|------------------|----------|
| **Stakeholder** | 基础设施架构师、运维团队、安全团队、采购部门 | 关注技术平台与标准 |
| **Concern** | 技术标准、平台蓝图、迁移路径、容量、可用性、安全基线 | 技术架构关注点 |
| **Viewpoint** | *Technology Architecture Viewpoint* | 技术架构视点 |
| **View** | Technology Architecture View, Technology Portfolio Catalog, Network/Hardware Diagram | 技术架构视图与设备目录 |
| **Model Kind** | Deployment Model, Network Topology Model, Technology Stack Model | 部署模型、网络拓扑、技术栈模型 |
| **ABB** | Technology Component, Technology Service, Platform Service, Network Service | 技术组件、技术服务、平台服务 |
| **SBB** | Kubernetes Cluster, Cloud VM (AWS EC2, Azure VM), CDN (Cloudflare), Load Balancer (F5, NGINX) | 具体云资源、容器平台、网络设备 |
| **Correspondence** | Technology Service → SBB Platform Mapping, SLAs → Monitoring Rules | 技术服务与平台映射、SLA 与监控规则 |

> **复用视角**: 技术 ABB（如"容器编排服务"）可映射到多个 SBB（Kubernetes, Docker Swarm, ECS）。技术连续体的层级结构（基础→通用系统→行业→特定组织）在此阶段体现得最为明显。

### 3.6 Phase E — Opportunities & Solutions

**TOGAF 10 活动**: 评估实施目标，识别工作包，进行差距分析，确定过渡架构。

| ISO 42010:2022 | TOGAF 10 ABB/SBB | 映射说明 |
|----------------|------------------|----------|
| **Stakeholder** | 项目组合经理、业务负责人、架构委员会 | 关注实施可行性与优先级 |
| **Concern** | 差距、复用机会、工作包分组、过渡状态 | 机会与解决方案关注点 |
| **Viewpoint** | *Transition Architecture Viewpoint* | 过渡架构视点 |
| **View** | Gap Analysis Report, Consolidated Architecture Roadmap, Work Package Definition | 差距分析报告与路线图 |
| **Model Kind** | Gap Model, Transition Model, Dependency Model | 差距模型、过渡模型、依赖模型 |
| **ABB** | Gap Definition, Transition Architecture, Work Package (logical) | 差距定义、过渡架构、逻辑工作包 |
| **SBB** | Reusable COTS Component, SaaS Subscription Plan, Existing System Adapter | 可复用商业组件、SaaS 计划、存量系统适配器 |
| **Correspondence** | Gap → Work Package → Reusable Asset Mapping | 差距到工作包到可复用资产的映射 |

> **复用视角**: Phase E 是复用决策的关键节点。通过差距分析识别哪些差距可通过复用现有 ABB/SBB 弥合，哪些需要新建。企业连续体在此阶段被主动查询。

### 3.7 Phase F — Migration Planning

**TOGAF 10 活动**: 制定详细的迁移计划，排序项目，分配业务价值，确认路线图。

| ISO 42010:2022 | TOGAF 10 ABB/SBB | 映射说明 |
|----------------|------------------|----------|
| **Stakeholder** | PMO、项目组合经理、财务规划者 | 关注实施顺序与投资回报 |
| **Concern** | 迁移顺序、依赖关系、风险、成本、收益时间表 | 迁移规划关注点 |
| **Viewpoint** | *Implementation and Migration Viewpoint* | 实现与迁移视点 |
| **View** | Implementation and Migration Plan, Architecture Roadmap (confirmed), Transition Architecture (detailed) | 实施迁移计划与确认的路线图 |
| **Model Kind** | Migration Timeline Model, Dependency Network Model, Risk Model | 迁移时间线、依赖网络、风险模型 |
| **ABB** | Migration Project Definition, Transition State Definition, Value Stream Mapping | 迁移项目定义、过渡状态定义 |
| **SBB** | Project Schedule (MS Project, Jira Roadmap), Release Train Definition, Budget Spreadsheet | 具体项目计划、发布火车定义、预算表 |
| **Correspondence** | Project → ABB/SBB Delivery Mapping, Value → Cost Correspondence | 项目与构建块交付映射、价值-成本对应 |

> **复用视角**: 迁移计划中需要明确哪些 ABB/SBB 可在多个过渡状态中复用。例如，一个 IAM 平台的 SBB 可能在多个业务域的迁移项目中作为共享基础设施被复用。

### 3.8 Phase G — Implementation Governance

**TOGAF 10 活动**: 监督实施，确保架构合规，管理架构契约。

| ISO 42010:2022 | TOGAF 10 ABB/SBB | 映射说明 |
|----------------|------------------|----------|
| **Stakeholder** | 实施团队、架构委员会、质量保证团队 | 关注合规与交付质量 |
| **Concern** | 架构合规、偏差管理、契约履行、合规评估 | 实施治理关注点 |
| **Viewpoint** | *Architecture Compliance Review Viewpoint* | 架构合规审查视点 |
| **View** | Architecture Contract, Compliance Assessment Report, Exception Log | 架构契约与合规评估报告 |
| **Model Kind** | Compliance Checklist Model, Deviation Model, Contract Model | 合规清单、偏差、契约模型 |
| **ABB** | Architecture Contract (logical terms), Compliance Criteria, Exception Policy | 架构契约条款、合规准则、例外策略 |
| **SBB** | Signed Vendor Contract, CI/CD Compliance Gate, Automated Policy Check (OPA, SonarQube) | 签署的合同、CI/CD 门禁、自动化策略检查 |
| **Correspondence** | ABB Contract → SBB Implementation Correspondence Rule | 契约条款与实现之间的对应规则验证 |

> **复用视角**: 架构契约是复用的法律与治理保障。通过标准化的架构契约模板（ABB），可快速适配到不同供应商和项目的具体合同（SBB）中。

### 3.9 Phase H — Architecture Change Management

**TOGAF 10 活动**: 管理架构变更请求，评估变更影响，更新架构基线。

| ISO 42010:2022 | TOGAF 10 ABB/SBB | 映射说明 |
|----------------|------------------|----------|
| **Stakeholder** | 变更请求者、架构委员会、运维团队 | 关注变更影响与持续演进 |
| **Concern** | 变更影响范围、基线一致性、回滚策略、技术债 | 变更管理关注点 |
| **Viewpoint** | *Change Management Viewpoint* | 变更管理视点 |
| **View** | Change Request Log, Updated Architecture Landscape, Impact Analysis Report | 变更请求日志与影响分析报告 |
| **Model Kind** | Impact Analysis Model, Baseline Diff Model, Lifecycle Model | 影响分析、基线差异、生命周期模型 |
| **ABB** | Change Request Definition, Updated ABB Definition, New Baseline Version | 变更请求定义、更新后的 ABB、新基线版本 |
| **SBB** | Patch/Release Package, Updated Configuration, Rollback Script | 补丁包、更新配置、回滚脚本 |
| **Correspondence** | Change Request → ABB/SBB Impact Correspondence | 变更请求与受影响构建块的追溯 |

> **复用视角**: 变更管理确保复用资产的演进受控。当某个 ABB 需要更新时，通过对应规则可快速定位所有依赖的 SBB 和视图组件。

### 3.10 Requirements Management

**TOGAF 10 活动**: 贯穿全生命周期的需求管理，确保需求变化被正确记录、评估和整合。

| ISO 42010:2022 | TOGAF 10 ABB/SBB | 映射说明 |
|----------------|------------------|----------|
| **Stakeholder** | 需求工程师、业务分析师、测试团队 | 关注需求可追溯性 |
| **Concern** | 需求完整性、一致性、可追溯性、优先级变化 | 需求管理关注点 |
| **Viewpoint** | *Requirements Engineering Viewpoint* | 需求工程视点 |
| **View** | Requirements Repository View, Traceability Matrix, Impact Analysis View | 需求库视图与追溯矩阵 |
| **Model Kind** | Requirements Model (Use Case, User Story), Traceability Model, Priority Model | 需求模型、追溯模型、优先级模型 |
| **ABB** | Requirement Definition (functional/non-functional), Constraint Definition, Assumption Catalog | 需求定义、约束定义、假设目录 |
| **SBB** | Jira Epic/Story, Azure DevOps Work Item, Test Case (TestRail, Xray) | 具体需求工单、测试用例 |
| **Correspondence** | Requirement → ABB → SBB Traceability Correspondence | 需求到 ABB 到 SBB 的完整追溯链 |

> **复用视角**: 需求管理是复用资产的"需求侧入口"。通过将需求与 ABB/SBB 建立追溯关系，可实现"需求变更 → 影响分析 → 复用资产更新"的闭环。

---

## 4. 综合映射矩阵

| ADM Phase | 主要 ISO 42010 Viewpoint | ABB (逻辑层) | SBB (物理层) | 关键 Correspondence Rule |
|-----------|-------------------------|--------------|--------------|--------------------------|
| **Preliminary** | Architecture Capability Viewpoint | Governance Framework, Principles Catalog | EA Tool, Repository Schema | Principles → Compliance Criteria |
| **Phase A** | Stakeholder Requirements Viewpoint | Architecture Vision, Business Scenario | Approved Charter, Budget | Vision → Goals Traceability |
| **Phase B** | Business Architecture Viewpoint | Business Function, Process, Service, Object | CRM, ERP, BPM Configuration | Function → Process → Service |
| **Phase C (Data)** | Data Architecture Viewpoint | Data Entity, Logical Data Model | DB Schema, MDM Hub, Data Warehouse | Logical → Physical Schema |
| **Phase C (App)** | Application Architecture Viewpoint | Application Component, Interface, Service | Microservice, API Gateway, SaaS | Interface → API Contract |
| **Phase D** | Technology Architecture Viewpoint | Technology Component, Platform Service | K8s, Cloud VM, CDN, Load Balancer | Service → Platform SLA |
| **Phase E** | Transition Architecture Viewpoint | Gap, Transition Architecture, Work Package | COTS Component, Existing Adapter | Gap → Work Package → Asset |
| **Phase F** | Implementation & Migration Viewpoint | Migration Project, Transition State | Project Schedule, Release Train | Project → ABB/SBB Delivery |
| **Phase G** | Compliance Review Viewpoint | Architecture Contract, Compliance Criteria | Signed Contract, CI/CD Gate | Contract → Implementation |
| **Phase H** | Change Management Viewpoint | Change Request, Updated ABB, Baseline | Patch, Config Update, Rollback Script | Change → Impact Correspondence |
| **Req Mgmt** | Requirements Engineering Viewpoint | Requirement, Constraint, Assumption | Jira Story, Test Case | Req → ABB → SBB Traceability |

---

## 5. ABB/SBB 在 ISO 42010 中的元模型定位

从 ISO 42010:2022 的内容模型来看，ABB 和 SBB 均属于 **Architecture View Component** 的范畴，但处于不同的抽象层级：

```
Architecture Description (AD)
├── Architecture Viewpoint
│   └── governs → Architecture View
│       └── contains → View Component
│           ├── Model Kind: Logical Model  → ABB (Architecture Building Block)
│           │   └── Example: "Customer Identity Management" (能力定义)
│           └── Model Kind: Physical Model → SBB (Solution Building Block)
│               └── Example: "Keycloak 22.x + Custom Plugins" (具体实现)
└── Correspondence Rule
    └── ABB ↔ SBB Realization Correspondence
```

ISO 42010:2022 引入的 **View Component** 概念（替代 2011 版的 Model）恰好容纳了 ABB/SBB 这种"同一视点下不同抽象层级"的情况。一个 View Component 可以是由 Model Kind 约束的模型化组件（ABB），也可以是由 Legend 说明的非模型化组件（SBB 的产品说明文档）。

---

## 6. 与 ArchiMate 的协同映射

TOGAF 10 的 ABB/SBB 可通过 ArchiMate 语言进行实例化描述：

| ArchiMate 元素 | ABB 映射 | SBB 映射 |
|----------------|----------|----------|
| Business Function / Process | 业务 ABB | BPM 工具中的工作流配置 |
| Application Component / Service | 应用 ABB | 部署的微服务/软件包 |
| Technology Service / Node | 技术 ABB | 具体的云实例/物理服务器 |
| Work Package / Deliverable | 过渡 ABB | 项目计划中的具体任务包 |

ArchiMate 的 **realization** 关系可直接表达 ABB → SBB 的实现对应（Correspondence），而 ArchiMate 4 引入的 **Path** 概念进一步支持了跨层服务实现的逻辑-物理分离。

---

## 7. 对齐验证

### 7.1 与 TOGAF 10 官方来源的对齐

- **The Open Group: TOGAF Standard, 10th Edition (2022)** — 第 31 章（Building Blocks）明确定义了 ABB/SBB 的抽象层级差异；第 35-39 章详细描述了 ADM 各阶段的输入/步骤/输出。[[来源](https://www.opengroup.org/togaf)]
- **The Open Group: TOGAF Series Guide — A Practitioners' Approach to Developing EA Following the TOGAF ADM (2023)** — 提供了 ADM 各阶段与架构能力、治理的详细操作指南。[[PDF](https://governance.foundation/assets/frameworks/togaf/g186%20-%20A%20Practitioners%20Approach%20to%20Developing%20EA.pdf)]
- **The Open Group: TOGAF ADM and Architecture Content (2025 Update)** — 2025 年更新版扩展了敏捷/数字孪生场景下的 ABB/SBB 使用方式。

### 7.2 与 ISO 42010:2022 的对齐

- **ISO/IEC/IEEE 42010:2022, Clause 5.2** — 定义了架构描述的概念模型，包括 Stakeholder、Concern、Viewpoint、View、View Component、Model Kind、Correspondence 等核心元素。[[来源](https://www.iso.org/obp/ui/#iso:std:iso-iec-ieee:42010:ed-2:v1:en)]
- **ISO/IEC/IEEE 42010:2022, Clause 6.8** — 引入 View Component 作为"one or more architecture views 的可分离部分"，为 ABB/SBB 的层级化描述提供了标准术语。
- **ISO/IEC/IEEE 42010:2022, Annex F** — 列举了多个 ADF（Architecture Description Framework）的 conformance 示例，TOGAF 作为业界最广泛使用的 ADF 之一，其 ABB/SBB 机制与 ISO 42010 的 Viewpoint-View-Model Kind 结构高度一致。

### 7.3 验证结论

本映射覆盖了 TOGAF ADM 全部 10 个阶段，每个阶段均从 ISO 42010:2022 的 Stakeholder → Concern → Viewpoint → View → Model Kind → View Component (ABB/SBB) → Correspondence 链条进行了逐层展开。映射结果表明：

1. **ABB 本质上是逻辑 View Component**，由 Model Kind（如业务流程模型、组件模型）约束；
2. **SBB 本质上是物理 View Component**，可以是模型化的（如部署图）或非模型化的（如产品规格说明书）；
3. **ADM 的迭代过程本质上是 ISO 42010 架构描述生命周期的实例化**，每一轮 ADM 循环产生一组符合 ISO 42010 要求的 Architecture Description。

---

## 8. 参考索引

1. The Open Group. *TOGAF Standard, 10th Edition*. 2022. <https://www.opengroup.org/togaf>
2. The Open Group. *TOGAF Series Guide: A Practitioners' Approach to Developing Enterprise Architecture Following the TOGAF ADM*. 2023.
3. ISO/IEC/IEEE. *ISO/IEC/IEEE 42010:2022 — Software, systems and enterprise — Architecture description*. 2022. <https://www.iso.org/standard/74296.html>
4. ISO/IEC/IEEE. *ISO/IEC/IEEE 42010:2022, Annex F — Architecture description frameworks*. 2022.
5. Visual Paradigm. "Comprehensive Guide to the Enterprise Continuum in TOGAF". 2025. <https://www.visual-paradigm.com/guide/togaf/what-is-togaf/>
6. Ardoq. "What Is TOGAF? Definition and Uses of This EA Framework". 2024. <https://www.ardoq.com/knowledge-hub/togaf>

---

> **最后更新**: 2026-06-06
> **维护者**: Track A — 01 元模型与标准对齐
> **状态**: Phase 2 交付物（T05 完成）
