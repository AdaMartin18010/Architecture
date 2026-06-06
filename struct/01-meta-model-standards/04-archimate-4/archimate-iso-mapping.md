# ArchiMate 3.2/4.0 元素与 ISO 42010:2022 的对照表

> **版本**: 2026-06-06
> **对齐来源**: The Open Group ArchiMate 3.2 Specification (2023); **ArchiMate 4 Specification (2026-04-27)**; ISO/IEC/IEEE 42010:2022; ArchiMate Forum, The Open Group
> **适用范围**: 软件工程架构复用知识体系 Track A — 01 元模型与标准对齐

> 📝 **状态更新**
>
> **ArchiMate 4 已于 2026-04-27 由 The Open Group 正式发布**。此前文档中将其标注为"厂商预告"属于**过渡期间的保守判断**，现予以纠正。
> ArchiMate 4 强调与 3.2 的向后兼容性，是当前活跃版本。详见官方发布：[`https://www.opengroup.org/press-releases`](https://www.opengroup.org/press-releases)

---

## 1. 背景与范围

ArchiMate 是 The Open Group 推出的企业架构建模语言，**当前版本为 ArchiMate 4（2026-04-27 发布）**，在 ArchiMate 3.2（2022-10）基础上进行了概念简化与扩展，强调向后兼容。ISO/IEC/IEEE 42010:2022 则规定了架构描述（Architecture Description）的通用元模型，包括视点（Viewpoint）、视图（View）、视图组件（View Component）、模型种类（Model Kind）等核心概念。

本文档建立 ArchiMate 3.2/4.0 核心元素与 ISO 42010:2022 概念之间的双向映射。ArchiMate 4.0 映射部分基于官方发布内容，具备标准合规效力。
ISO/IEC/IEEE 42010:2022 则规定了架构描述（Architecture Description）的通用元模型，包括视点（Viewpoint）、视图（View）、视图组件（View Component）、模型种类（Model Kind）等核心概念。

本文档建立 ArchiMate 3.2/4.0 核心元素与 ISO 42010:2022 概念之间的双向映射，覆盖以下四层：

- **业务层（Business Layer）**
- **应用层（Application Layer）**
- **技术层（Technology Layer）**
- **实现与迁移层（Implementation & Migration Layer）**

> **注**: ArchiMate 4 引入了**通用域（Common Domain）**、**策略域（Strategy Domain）**和**动机域（Motivation Domain）**的重大重构。
> 本文档在映射时标注 3.2 与 4.0 的差异，并以 4.0 为基准进行 ISO 42010 对齐。

---

## 2. 元模型级映射：ArchiMate 语言结构 vs ISO 42010

| ISO 42010:2022 概念 | ArchiMate 3.2/4.0 对应 | 映射说明 |
|---------------------|------------------------|----------|
| **Architecture Description (AD)** | ArchiMate Model / Repository | ArchiMate 模型库是 AD 的载体 |
| **Architecture Description Framework (ADF)** | ArchiMate Full Framework | ArchiMate 本身是一个符合 ISO 42010 的 ADF |
| **Architecture Description Language (ADL)** | ArchiMate Modeling Language | ArchiMate 是一种标准化的 ADL |
| **Viewpoint** | ArchiMate Viewpoint | ArchiMate 定义了 23+ 个标准视点 |
| **View** | ArchiMate Diagram / View | 从视点生成的具体图表或视图 |
| **View Component** | ArchiMate Element (in a View) | 视图中的元素实例 |
| **Model Kind** | Aspect × Layer 分类矩阵 | ArchiMate 的 Aspect（主动结构/行为/被动结构）与 Layer 的组合定义了 Model Kind |
| **Stakeholder** | Stakeholder (Motivation Domain) | ArchiMate 动机域中的利益相关者元素 |
| **Concern** | Driver, Assessment, Goal, Requirement | 动机域元素对应关注点 |
| **Correspondence** | Relationship (structural, dependency, dynamic) | ArchiMate 关系类型表达对应规则 |
| **Architecture Decision** | Plateau, Gap, Work Package (I&M Layer) | 实现与迁移元素记录架构决策与状态变化 |

---

## 3. 业务层（Business Layer）映射

### 3.1 业务层核心元素

ArchiMate 业务层描述企业的业务结构、行为和信息，与 TOGAF Phase B（Business Architecture）直接对应。

| ArchiMate 3.2 元素 | ArchiMate 4.0 元素 | 元素类别 | ISO 42010:2022 映射 | 说明 |
|---------------------|---------------------|----------|---------------------|------|
| Business Actor | Actor (Common Domain, 可标注为业务) | 主动结构 | Stakeholder / Active Structure View Component | 业务参与者 |
| Business Role | Role (Common Domain, 可标注为业务) | 主动结构 | Active Structure View Component | 业务角色 |
| Business Collaboration | Collaboration (Common Domain) | 主动结构 | Active Structure View Component | 跨主体协作 |
| Business Process | Process (Common Domain, 可标注为业务) | 行为 | Behavior View Component | 业务流程 |
| Business Function | Function (Common Domain, 可标注为业务) | 行为 | Behavior View Component | 业务功能 |
| Business Interaction | Process / Function (Common Domain) | 行为 | Behavior View Component | 4.0 中合并为通用行为 |
| Business Event | Event (Common Domain, 可标注为业务) | 行为 | Behavior View Component | 业务事件 |
| Business Service | Service (Common Domain, 可标注为业务) | 行为 | Behavior View Component | 对外业务服务 |
| Business Object | Business Object | 被动结构 | Passive Structure View Component | 业务对象/信息实体 |
| Product | Product | 被动结构 | Passive Structure View Component | 产品/服务组合 |
| Contract | Business Object (加契约语义标注) | 被动结构 | Passive Structure View Component | 4.0 移除 Contract，建议用标注实现 |
| Representation | Data Object / Artifact / Material | 被动结构 | Passive Structure View Component | 4.0 移除 Representation，映射到被动结构 |
| Meaning | Meaning | 动机 | Concern / Rationale | 业务含义 |
| Value | Value | 动机 | Concern / Rationale | 业务价值 |

### 3.2 业务层 → ISO 42010 Viewpoint 映射

| ArchiMate 业务层视点（示例） | ISO 42010:2022 Viewpoint | 包含的 Model Kind | 对应的 Concern |
|------------------------------|--------------------------|-------------------|----------------|
| Organization Viewpoint | Stakeholder Perspective Viewpoint | Organization Model | 组织责任、汇报线 |
| Business Process Viewpoint | Behavioral Viewpoint | Process Model (BPMN-like) | 流程效率、瓶颈 |
| Product Viewpoint | Structural Viewpoint | Product Composition Model | 产品构成、价值交付 |
| Service Realization Viewpoint | Realization Viewpoint | Service-Process Realization Model | 服务实现、能力映射 |

### 3.3 ABB/SBB 在业务层的体现

| 层级 | ArchiMate 表示 | 示例 |
|------|----------------|------|
| **ABB（逻辑）** | Business Process "Order-to-Cash" | 抽象业务流程定义 |
| **SBB（物理）** | SAP SD Module Workflow + Custom Extensions | SAP 销售分销模块工作流及定制 |

---

## 4. 应用层（Application Layer）映射

### 4.1 应用层核心元素

ArchiMate 应用层描述支持业务的信息系统与应用软件架构。

| ArchiMate 3.2 元素 | ArchiMate 4.0 元素 | 元素类别 | ISO 42010:2022 映射 | 说明 |
|---------------------|---------------------|----------|---------------------|------|
| Application Component | Application Component | 主动结构 | Active Structure View Component | 应用组件 |
| Application Collaboration | Collaboration (Common Domain) | 主动结构 | Active Structure View Component | 应用协作 |
| Application Interface | Interface (Common Domain, 可标注为应用) | 主动结构 | Active Structure View Component | 应用接口 |
| Application Process | Process (Common Domain, 可标注为应用) | 行为 | Behavior View Component | 4.0 合并为通用 Process |
| Application Function | Function (Common Domain, 可标注为应用) | 行为 | Behavior View Component | 4.0 合并为通用 Function |
| Application Interaction | Process / Function (Common Domain) | 行为 | Behavior View Component | 4.0 合并 |
| Application Event | Event (Common Domain, 可标注为应用) | 行为 | Behavior View Component | 应用事件 |
| Application Service | Service (Common Domain, 可标注为应用) | 行为 | Behavior View Component | 应用服务 |
| Data Object | Data Object | 被动结构 | Passive Structure View Component | 数据对象 |

### 4.2 应用层 → ISO 42010 Viewpoint 映射

| ArchiMate 应用层视点（示例） | ISO 42010:2022 Viewpoint | 包含的 Model Kind | 对应的 Concern |
|------------------------------|--------------------------|-------------------|----------------|
| Application Structure Viewpoint | Structural Viewpoint | Component Model | 应用组合、模块化 |
| Application Behavior Viewpoint | Behavioral Viewpoint | Process/Function Model | 应用行为、处理逻辑 |
| Application Usage Viewpoint | Usage Viewpoint | Usage Model | 业务-应用依赖关系 |
| Data Structure Viewpoint | Information Viewpoint | Data/Class Model | 数据一致性、实体关系 |

### 4.3 ABB/SBB 在应用层的体现

| 层级 | ArchiMate 表示 | 示例 |
|------|----------------|------|
| **ABB（逻辑）** | Application Component "Customer Service" + Application Interface "REST API" | 逻辑组件与接口定义 |
| **SBB（物理）** | Spring Boot Microservice (v3.2) + OpenAPI 3.0 Spec + Docker Image | 具体微服务、API 契约、容器镜像 |

---

## 5. 技术层（Technology Layer）映射

### 5.1 技术层核心元素

ArchiMate 技术层描述技术基础设施，包括 IT 和物理技术（ArchiMate 4 将 Physical Layer 并入 Technology Domain）。

| ArchiMate 3.2/3.1 元素 | ArchiMate 4.0 元素 | 元素类别 | ISO 42010:2022 映射 | 说明 |
|------------------------|---------------------|----------|---------------------|------|
| Node | Node | 主动结构 | Active Structure View Component | 计算节点 |
| Device | Device | 主动结构 | Active Structure View Component | 物理设备 |
| System Software | System Software | 主动结构 | Active Structure View Component | 系统软件 |
| Technology Collaboration | Collaboration (Common Domain) | 主动结构 | Active Structure View Component | 技术协作 |
| Technology Interface | Interface (Common Domain, 可标注为技术) | 主动结构 | Active Structure View Component | 技术接口 |
| Technology Process | Process (Common Domain, 可标注为技术) | 行为 | Behavior View Component | 4.0 合并为通用 Process |
| Technology Function | Function (Common Domain, 可标注为技术) | 行为 | Behavior View Component | 4.0 合并为通用 Function |
| Technology Service | Service (Common Domain, 可标注为技术) | 行为 | Behavior View Component | 技术服务 |
| Technology Event | Event (Common Domain, 可标注为技术) | 行为 | Behavior View Component | 技术事件 |
| Artifact | Artifact | 被动结构 | Passive Structure View Component | 可部署制品 |
| Communication Network | Communication Network | 主动结构 | Active Structure View Component | 通信网络 |
| Path (3.2 无，4.0 新增) | Path (Common Domain) | 主动/行为 | Active/Behavior View Component | 逻辑路径（数据/能量/物质） |
| Equipment (Physical) | Equipment (Technology Domain) | 主动结构 | Active Structure View Component | 物理设备/装备 |
| Facility (Physical) | Facility (Technology Domain) | 主动结构 | Active Structure View Component | 物理设施 |
| Distribution Network (Physical) | Distribution Network (Technology Domain) | 主动结构 | Active Structure View Component | 分配/传输网络 |
| Material (Physical) | Material (Technology Domain) | 被动结构 | Passive Structure View Component | 物质/材料 |

### 5.2 技术层 → ISO 42010 Viewpoint 映射

| ArchiMate 技术层视点（示例） | ISO 42010:2022 Viewpoint | 包含的 Model Kind | 对应的 Concern |
|------------------------------|--------------------------|-------------------|----------------|
| Infrastructure Viewpoint | Deployment Viewpoint | Deployment Model | 基础设施布局、容量 |
| Technology Usage Viewpoint | Dependency Viewpoint | Dependency Model | 应用-技术依赖关系 |
| Equipment Viewpoint (Physical) | Physical Viewpoint | Physical Layout Model | 物理设备布局、OT 安全 |
| Network Viewpoint | Connectivity Viewpoint | Network Topology Model | 网络拓扑、分段策略 |

### 5.3 ABB/SBB 在技术层的体现

| 层级 | ArchiMate 表示 | 示例 |
|------|----------------|------|
| **ABB（逻辑）** | Technology Service "Container Orchestration" + Node "Compute Cluster" | 逻辑技术服务与节点定义 |
| **SBB（物理）** | AWS EKS v1.29 + EC2 m6i.xlarge Instances + VPC CNI | 具体云服务、实例类型、网络插件 |

### 5.4 ArchiMate 4 的重要变化：Path 与 Realization

ArchiMate 4 引入了 **Path** 概念（位于 Common Domain），用于表达跨层的逻辑路径（数据路径、能源路径、物料路径）。Path 由下层技术元素 **realized by** 具体实现。这与 ISO 42010:2022 的 **Correspondence** 概念高度一致：Path 定义了逻辑对应规则，其实现元素定义了物理对应实例。

```
Path "Secure API Gateway Path" (Common Domain)
    └── realized by → Node "Kong Gateway" (Technology Domain)
        └── realized by → Device "AWS ALB" + System Software "Kong 3.5"
```

---

## 6. 实现与迁移层（Implementation & Migration Layer）映射

### 6.1 实现与迁移层核心元素

该层支持 TOGAF ADM Phase E/F/G 的实现规划与迁移管理。

| ArchiMate 3.2/3.1 元素 | ArchiMate 4.0 元素 | 元素类别 | ISO 42010:2022 映射 | 说明 |
|------------------------|---------------------|----------|---------------------|------|
| Work Package | Work Package | 实现元素 | Process/Activity View Component | 工作包 |
| Deliverable | Deliverable | 实现元素 | View Component / Information Part | 交付物 |
| Plateau | Plateau | 实现元素 | Baseline / State View Component | 架构基线/ plateau |
| Gap | Assessment 或 Deliverable (4.0 移除 Gap) | 实现元素 | Assessment View Component | 4.0 建议用 Assessment 或 Deliverable 替代 |
| Implementation Event | Event (Common Domain, 加标注) | 实现元素 | Event View Component | 4.0 合并为通用 Event |

### 6.2 实现与迁移层 → ISO 42010 Viewpoint 映射

| ArchiMate I&M 视点（示例） | ISO 42010:2022 Viewpoint | 包含的 Model Kind | 对应的 Concern |
|----------------------------|--------------------------|-------------------|----------------|
| Implementation and Migration Viewpoint | Transition Viewpoint | Migration/Transition Model | 迁移顺序、依赖、风险 |
| Project Viewpoint | Project Management Viewpoint | Work Breakdown Model | 工作包分解、资源分配 |
| Plateau & Gap Viewpoint (3.2) | Baseline Comparison Viewpoint | Diff/Baseline Model | 基线差异、差距分析 |

### 6.3 与 ISO 42010 架构决策的映射

ISO 42010:2022 要求 Architecture Description 必须包含 **Architecture Decision** 和 **Architecture Rationale**（Clause 6.10）。ArchiMate 的实现与迁移元素提供了决策的载体：

| ISO 42010:2022 | ArchiMate 4.0 映射 | 说明 |
|----------------|--------------------|------|
| Architecture Decision | Work Package + Deliverable | 工作包定义了"做什么决策"，交付物定义了"决策结果" |
| Architecture Rationale | Assessment + Goal + Outcome | 动机域的 Assessment 与 Goal 提供决策依据 |
| Decision Timeline | Plateau → Plateau Transition | Plateau 序列表达决策的时间线 |

---

## 7. 动机域（Motivation Domain）与策略域（Strategy Domain）映射

虽然动机域和策略域不属于传统四层，但它们是架构描述中"为什么"和"做什么"的关键部分，与 ISO 42010 的 Stakeholder/Concern/Decision 直接相关。

### 7.1 动机域元素映射

| ArchiMate 4.0 元素 | ISO 42010:2022 映射 | 说明 |
|--------------------|--------------------|------|
| Stakeholder | Stakeholder | 直接对应 |
| Driver | Concern (environmental influence) | 驱动因素是外部环境影响 |
| Assessment | Concern / Rationale input | 评估结果是决策输入 |
| Goal | Concern (objective) | 目标是具体的关注点 |
| Outcome | Concern (expected result) | 成果是期望状态 |
| Principle | Rationale / Decision constraint | 原则是决策约束 |
| Requirement | Concern / Specification | 需求是规格化的关注点 |
| Constraint | Requirement (stereotyped) | 4.0 中 Constraint 移除，建议用 Requirement 加标注 |
| Meaning | Concern (semantic) | 语义关注点 |
| Value | Concern (business value) | 价值关注点 |

### 7.2 策略域元素映射

| ArchiMate 4.0 元素 | ISO 42010:2022 映射 | 说明 |
|--------------------|--------------------|------|
| Resource | Active Structure View Component | 战略资源 |
| Capability | Behavior View Component | 业务能力 |
| Value Stream | Behavior View Component (sequence) | 价值流 |
| Course of Action | Decision / Process View Component | 行动路线 |

---

## 8. 综合对照矩阵：四层核心元素 vs ISO 42010

| 层面 | 主动结构 (Active Structure) | 行为 (Behavior) | 被动结构 (Passive Structure) | ISO 42010 Model Kind |
|------|----------------------------|-----------------|------------------------------|---------------------|
| **业务层** | Actor, Role, Collaboration | Process, Function, Service, Event | Business Object, Product | Business Model Kind |
| **应用层** | Application Component, Interface | Process, Function, Service, Event | Data Object | Application Model Kind |
| **技术层** | Node, Device, System Software, Network | Process, Function, Service, Event | Artifact, Material | Technology Model Kind |
| **实现层** | (通过分配关系关联) | Work Package, Event | Deliverable, Plateau | Implementation Model Kind |

---

## 9. ArchiMate 3.2 → 4.0 迁移对 ISO 42010 映射的影响

ArchiMate 4.0 的重大概念简化影响了 ISO 42010 映射方式：

| 变化项 | ArchiMate 3.2 | ArchiMate 4.0 | ISO 42010 映射影响 |
|--------|---------------|---------------|-------------------|
| 层特定行为元素 | Business Process, Application Process, Technology Process | 通用 Process (Common Domain) + 层标注 | Model Kind 的区分从元素类型转向标注/Profile，更符合 ISO 42010 的"Model Kind 是约定类别"的定义 |
| 层特定角色/协作 | Business Role, Business Collaboration, etc. | 通用 Role, Collaboration + 层标注 | 同上 |
| Constraint / Contract / Gap / Representation | 独立元素类型 | 移除或合并到通用元素 + 标注 | View Component 的粒度统一，Correspondence 通过关系而非元素类型表达 |
| Path | 无 | 新增 Common Domain 元素 | 直接支持 ISO 42010 的 Correspondence 概念，逻辑路径与物理实现的分离更清晰 |
| Implementation Event | 独立元素 | 通用 Event + 上下文标注 | 事件模型统一，通过 Viewpoint 区分生命周期阶段 |

---

## 10. 对齐验证

### 10.1 与 ArchiMate 官方规范的对齐

- **The Open Group: ArchiMate 3.2 Specification (2023)** — 定义了业务/应用/技术/物理/实现五层核心语言及动机扩展。[[来源](https://pubs.opengroup.org/architecture/archimate32-doc/)]
- **The Open Group: ArchiMate 4 Specification (2026-04-27)** — 引入 Common Domain、Strategy Domain、Path 概念，合并层特定行为/结构元素为通用元素。向后兼容 ArchiMate 3.2。[[来源](https://www.opengroup.org/press-releases)]
- **ArchiMate Forum, The Open Group (2025-2026)** — ArchiMate 4 的 Motivation White Paper 解释了 Path、Realization 模式与跨层治理的设计意图。

### 10.2 与 ISO 42010:2022 的对齐

- **ISO/IEC/IEEE 42010:2022, Clause 3** — 定义了 View Component 作为"separable portion of one or more architecture views"，ArchiMate 的 Element 在 View 中的实例即符合此定义。
- **ISO/IEC/IEEE 42010:2022, Clause 5.2.5** — 定义了 Model Kind 作为"category of model distinguished by its key characteristics and modelling conventions"。ArchiMate 的 Layer × Aspect 矩阵是 Model Kind 的典型实现。
- **ISO/IEC/IEEE 42010:2022, Clause 6.10** — 要求记录 Architecture Decision 和 Rationale。ArchiMate 4 的动机域（Goal, Principle, Assessment, Outcome）与实现域（Work Package, Deliverable, Plateau）共同支撑此要求。
- **ISO/IEC/IEEE 42010:2022, Annex F** — ArchiMate 被列为符合 ISO 42010 的 Architecture Description Language (ADL) 示例。

### 10.3 验证结论

1. **ArchiMate 的 Layer-Aspect 结构天然对应 ISO 42010 的 Model Kind-View Component 层次**。每层（业务/应用/技术/实现）结合每方面（主动结构/行为/被动结构）定义了一种独特的模型种类。
2. **ArchiMate 4 的通用化趋势与 ISO 42010:2022 的抽象层级理念一致**。通过将层特定元素合并为通用元素（Common Domain）并依赖标注/Profile 区分，ArchiMate 4 更接近 ISO 42010 "Viewpoint 决定观察角度" 的哲学。
3. **Path 与 Realization 机制的引入填补了 ArchiMate 在逻辑-物理分离方面的空白**，与 ISO 42010 的 Correspondence 概念形成精确映射。
4. **动机域和策略域完整覆盖了 ISO 42010 的 Stakeholder-Concern-Decision-Rationale 链条**，使 ArchiMate 成为少有的能完整表达 ISO 42010 全部概念的商业 ADL。

---

## 11. 参考索引

1. The Open Group. *ArchiMate 3.2 Specification*. 2023. <https://pubs.opengroup.org/architecture/archimate32-doc/>
2. The Open Group. *ArchiMate 4 Specification*. 2026-04-27. <https://www.opengroup.org/press-releases>
3. ISO/IEC/IEEE. *ISO/IEC/IEEE 42010:2022 — Software, systems and enterprise — Architecture description*. 2022. <https://www.iso.org/standard/74296.html>
4. 4m4.it. "ArchiMate 4 and the Cartography of Complexity". 2026. <https://4m4.it/longforms/archimate_4_and_the_cartography_of_complexity/>
5. LeanIX. "What is ArchiMate? Key Components & Comparisons". <https://www.leanix.net/en/wiki/ea/what-is-archimate>
6. Visual Paradigm. "ArchiMate Diagram Tutorial". <https://online.visual-paradigm.com/diagrams/tutorials/archimate-tutorial/>

---

> **最后更新**: 2026-06-06
> **维护者**: Track A — 01 元模型与标准对齐
> **状态**: Phase 2 交付物（T06 完成）
