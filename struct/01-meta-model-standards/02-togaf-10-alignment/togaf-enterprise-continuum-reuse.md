# TOGAF 10 企业连续体与构建块复用
>
> 版本: 2026-06-06
> 对齐来源: The Open Group TOGAF Standard 10th Edition (2022/2025 Update), Visual Paradigm 2025, Sparx Systems, Barnes & Noble 2025 出版物

## 1. TOGAF 10 核心文档集

| 文档 | 内容 | 2025 更新 |
|-----|------|----------|
| **ADM** | 架构开发方法 — 迭代式企业架构开发 | 持续迭代优化 |
| **ADM Techniques** | 技术集合 — 应用于 TOGAF ADM | 新增敏捷/数字孪生适配 |
| **Applying the ADM** | ADM 适配指南 — 特定架构风格 | 扩展 AI/数据架构场景 |

## 2. 企业连续体（Enterprise Continuum）

### 2.1 虚拟仓库概念

> "The Enterprise Continuum is a 'virtual repository' of all the architecture assets that exist both within the enterprise and in the IT industry at large."

企业连续体包含两类资产：

- **企业内部资产**：以往架构工作的可交付物
- **IT 行业资产**：通用参考模型、架构模式、行业标准

### 2.2 架构连续体（Architecture Continuum）

架构连续体是**架构构建块（ABBs）**的结构化分类库：

| 层级 | 通用性 | 示例 |
|-----|--------|------|
| **基础架构（Foundation）** | 最通用 | TOGAF TRM、网络七层模型 |
| **通用系统架构（Common Systems）** | 跨行业 | Web 服务架构、安全管理框架 |
| **行业架构（Industry）** | 垂直领域 | eTOM（电信）、ARTS（零售）、POSC（石油）|
| **组织特定架构（Organization-Specific）** | 企业专属 | 某银行的客户数据管理原则 |

### 2.3 解决方案连续体（Solutions Continuum）

解决方案连续体是**解决方案构建块（SBBs）**的库，是 ABBs 的具体实现：

| 层级 | 对应 ABB 层级 | 示例 |
|-----|-------------|------|
| **基础解决方案** | 基础架构 | 操作系统、编程语言运行时 |
| **通用系统解决方案** | 通用系统架构 | CRM 套件、IAM 平台 |
| **行业解决方案** | 行业架构 | 电信计费系统、零售 POS |
| **组织特定解决方案** | 组织特定架构 | 定制开发的忠诚度计划系统 |

## 3. ABB 与 SBB 的复用关系

### 3.1 定义

| 维度 | Architecture Building Block (ABB) | Solution Building Block (SBB) |
|-----|-----------------------------------|-------------------------------|
| **抽象层级** | 逻辑/概念 | 物理/实现 |
| **内容** | 功能、接口、数据、行为定义 | 具体产品、软件、服务、硬件 |
| **复用方式** | 架构描述中引用，指导设计 | 直接集成、配置、定制 |
| **关系** | "需要什么能力" | "用什么实现该能力" |

### 3.2 映射示例

```
ABB: Customer Identity Management
├── 能力：注册、认证、授权、画像管理
├── 接口：REST API / SCIM / SAML / OIDC
└── 数据：身份图谱、同意记录

    ↓ 实现为

SBB: Keycloak + 定制扩展
├── 产品：Keycloak 22.x
├── 配置：Realm、Client、Flow 定义
├── 定制：同意管理插件、品牌主题
└── 集成：LDAP、CRM、营销自动化
```

## 4. 架构仓库（Architecture Repository）

### 4.1 分区结构

| 分区 | 内容 | 复用价值 |
|-----|------|---------|
| **架构元模型** | 企业使用的建模语言、记号、关系 | 保证全企业架构描述一致性 |
| **架构能力** | 当前架构组织的角色、技能、流程 | 评估与规划架构资源 |
| **架构景观** | 当前各层级架构的快照 | 影响分析、差距分析 |
| **标准信息库（SIB）** | 技术标准、产品标准、指南 | 采购决策、合规检查 |
| **参考库** | 外部参考模型、模式、框架 | 新项目启动加速器 |
| **治理日志** | 决策记录、合规评估、例外审批 | 审计、学习、争议解决 |

### 4.2 与 ArchiMate 模型库的集成

- TOGAF 架构仓库提供**物理存储和管理**
- ArchiMate 模型库提供**逻辑组织和导航**
- 两者结合实现跨工具、跨团队的架构资产复用

## 5. 架构交付物与制品（Deliverables & Artifacts）

### 5.1 核心交付物

| 交付物 | ADM 阶段 | 复用场景 |
|-------|---------|---------|
| **Architecture Vision** | Phase A | 多项目共享的战略上下文 |
| **Business Architecture** | Phase B | 业务能力地图、组织解构 |
| **Data Architecture** | Phase C | 数据实体、逻辑模型、治理规则 |
| **Application Architecture** | Phase C | 应用组合、接口目录、集成模式 |
| **Technology Architecture** | Phase D | 技术标准、平台蓝图、迁移路径 |
| **Architecture Roadmap** | Phase E/F | 跨项目的过渡架构规划 |
| **Architecture Contract** | Phase G | 实施团队与架构团队的契约模板 |

### 5.2 制品类型

- **模型（Models）**：业务流程模型、数据模型、技术模型
- **图表（Diagrams）**：数据流图、网络图、组件图
- **矩阵（Matrices）**：组件间关系与依赖矩阵
- **业务场景（Business Scenarios）**：架构如何支持特定业务目标的故事
- **用例（Use Cases）**：用户与系统交互表示

## 6. TOGAF 与 ISO 42010:2022 的映射

| ISO 42010:2022 | TOGAF 10 | 说明 |
|---------------|---------|------|
| Entity of Interest (EoI) | Enterprise / Architecture Project | 架构描述的对象 |
| Architecture Description (AD) | Architecture Deliverables | 架构工作产物 |
| Architecture Description Framework (ADF) | TOGAF Content Framework + ADM | 方法论框架 |
| Stakeholder | Stakeholder Map | 利益相关者识别 |
| Concern | Architecture Vision / Drivers | 关注点与驱动力 |
| Viewpoint | View / Catalog / Matrix | 视点定义 |
| View | Architecture Artifact | 视图实例 |
| Model | Architecture Model | 模型 |
| Correspondence Rule | Architecture Contract / Compliance Review | 对应规则与合规评估 |

## 7. 参考索引

- The Open Group: *TOGAF Standard, 10th Edition* (2022)
- The Open Group: *TOGAF Standard — Architecture Development Method — 2025 Update* (2025-06)
- Visual Paradigm: "Comprehensive Guide to the Enterprise Continuum in TOGAF" (2025-02)
- Paradigma Digital: "The 5 Key Components of TOGAF" (2025-03)
- Sparx Systems: Enterprise Architect User Guide — TOGAF Enterprise Continuum
