# OMG RAS v2.2 与软件架构复用对齐

> **定位**: 将 OMG 可复用资产规范（Reusable Asset Specification, RAS）纳入本体系的标准对齐框架
> **对齐来源**: OMG RAS v2.2 formal/05-11-02, TOGAF 9.2/10, ISO/IEC/IEEE 42010:2022
> **状态**: Phase 2（2026-Q4）
> **权威链接**:
>
> - <https://www.omg.org/spec/RAS/>
> - <https://www.omg.org/spec/RAS/2.2/PDF>
> - <https://www.omg.org/spec/RAS/20060101/DefaultprofileXML.xsd>
> - <https://www.omg.org/spec/RAS/20060101/DefaultcomponentprofileXML.xsd>

---

## 1. 什么是 OMG RAS

OMG **Reusable Asset Specification (RAS)** v2.2 是一个供应商中立的软件资产包装与交换标准，目标是**“通过一致、标准的包装降低复用交易中的摩擦”**。
它定义了可复用资产的元模型、物理包格式和仓库服务接口。

| 属性 | 内容 |
|------|------|
| 版本 | RAS v2.2 (formal/05-11-02) |
| 发布日期 | 2005-11-04 |
| 状态 | OMG Available Specification；RAS 3.0 现代化工作仍在进行中（2025/2026） |
| 规范形式 | PDF + XML Schema + MOF/XMI |

---

## 2. 核心元模型：Core RAS

RAS 将每个可复用资产划分为四个核心部分，直接对应复用生命周期中的关键问题：

```text
┌─────────────────────────────────────────┐
│              Asset（资产）               │
│  name | id | version | date | state     │
├─────────────────────────────────────────┤
│  Classification — 这是什么？            │
│  Solution       — 里面有什么？          │
│  Usage          — 怎么使用/定制？       │
│  RelatedAssets  — 与其他资产的关系？    │
└─────────────────────────────────────────┘
```

### 2.1 Classification（分类）

回答“**这是什么资产？**”。包含：

| 元素 | 作用 |
|------|------|
| `Context` | 定义上下文（如业务、开发、运行、测试） |
| `DescriptorGroup` | 描述符分组 |
| `NodeDescriptor` | 分类节点（如领域分类树） |
| `FreeFormDescriptor` | 自由键值描述 |
| `ClassificationSchema` | 可复用的分类词汇表 |

**对齐本体系**: 对应 `02-business-architecture-reuse` 中的业务能力目录和 `06-cross-layer-governance` 中的复用资产元数据治理。

### 2.2 Solution（解决方案）

回答“**资产包含什么制品？**”。包含：

| 元素 | 作用 |
|------|------|
| `Artifact` | 工作产品（文件或逻辑制品） |
| `ArtifactContext` | 制品与上下文的关联 |
| `ArtifactDependency` | 制品间依赖（编译期/运行期/设计期） |
| `ArtifactType` | 制品类型 |
| `VariabilityPoint` | 可变性点（用户需要定制的地方） |

**对齐本体系**: 对应四层架构（业务→应用→组件→功能）中各层交付的制品集合。

### 2.3 Usage（使用）

回答“**如何安装、定制和使用？**”。包含：

| 元素 | 作用 |
|------|------|
| `Activity` | 使用指令（任务、角色、类型） |
| `ArtifactActivity` | 绑定到特定制品的活动 |
| `AssetActivity` | 绑定到整个资产的活动 |
| `VariabilityPointBinding` | 可变性点的绑定规则 |
| `ActivityParameter` | 活动参数 |

**对齐本体系**: 对应 `06-cross-layer-governance` 中的 Golden Path、复用手册和 `13-emerging-trends/01-platform-engineering`。

### 2.4 RelatedAssets（相关资产）

回答“**与其他资产的关系？**”。关系类型包括：

- `aggregation`（聚合）
- `similar`（相似）
- `dependency`（依赖）
- `parent`（父级）

**对齐本体系**: 对应 `07-formal-verification/02-alloy` 中的组件依赖图和 `10-supply-chain-security` 中的 SBOM 依赖关系。

---

## 3. Profile 机制与领域扩展

RAS 通过 **Profile（配置文件）** 实现领域扩展，约束单调递增：子 Profile 不能删除父 Profile 的约束，只能增加或收紧。

| Profile | 扩展自 | 用途 |
|---------|--------|------|
| Default Profile 2.2 | Core RAS | 通用资产（业务流程、Eclipse 插件、文档） |
| Default Component Profile 2.2 | Default Profile | 二进制/设计时组件（J2EE、.NET 程序集） |
| Default Web Service Profile 2.2 | Default Component Profile | Web Service 客户端包装 |

**现代映射**: 虽然 RAS 没有原生支持容器镜像、Helm Chart、OpenAPI、Protobuf，但这些现代格式可作为 `Artifact` 中的不透明制品被包装。

---

## 4. 物理包格式：`.ras` 文件

一个合法的 `.ras` 包至少包含：

1. 一个 manifest 文件（`rasset.xml`）
2. 至少一个被 `<solution>` 引用的制品

典型结构：

```text
payment-service.ras
├── rasset.xml                          # 正式 manifest
├── RASDefaultComponentProfile.xsd      # profile schema
├── requirements/
│   └── use-cases.docx
├── design/
│   ├── payment-interface.uml
│   └── class-diagram.png
├── implementation/
│   ├── payment-service.jar
│   └── payment-config.xml
└── test/
    └── payment-tests.zip
```

**关键规则**:

- manifest 所在目录为根上下文
- 每个必需文件必须被 `<artifact>` 引用
- 未引用的文件视为可选，工具可在重打包时剥离

---

## 5. 仓库服务接口

RAS v2.2 定义了最小化的仓库服务接口，**仅**覆盖搜索和检索：

```text
GET /SearchByKeyword?keyword=<关键词>
GET /SearchByLogicalPath?path=<逻辑路径>
```

返回 **Repository Asset Descriptor**，包含：

- Name
- Description
- URL（下载 `.ras` 文件）
- Logical Path
- Version
- Ranking（匹配度 0-100）

**局限性**: 没有标准化发布、治理、度量、版本工作流。现代复用平台（Backstage、Port、Cortex IDP）需要在此基础上扩展。

---

## 6. 与 ISO 42010 / TOGAF 的映射

| RAS 元素 | ISO 42010:2022 概念 | TOGAF 10 概念 |
|----------|---------------------|---------------|
| `Asset` | Architecture Description (AD) | Architecture Building Block (ABB) / Solution Building Block (SBB) |
| `Classification` | Concern / Stakeholder | Architecture Repository 分类元数据 |
| `Context` | Aspect / Perspective | Architecture Vision / 上下文边界 |
| `Solution` | View / Model Kind | Architecture Deliverables / Catalogs |
| `Artifact` | View Component | 具体交付物（模型、代码、文档） |
| `VariabilityPoint` | Correspondence Rule | Reuse Strategy / 可变性管理 |
| `RelatedAssets` | Correspondence | Architecture Repository 中的关系 |
| `Usage` | Architecture Decision | Architecture Contract / 使用指南 |

---

## 7. 与四层复用架构的映射

| 本体系层次 | RAS 应用方式 | 示例资产 |
|-----------|-------------|----------|
| 02 业务架构 | 包装业务能力模型、BPMN 流程、价值流图 | 领域模型包、FEA BRM 片段 |
| 03 应用架构 | 包装参考架构、部署拓扑、数据流图 | 微服务参考架构包 |
| 04 组件架构 | 包装框架、库、组件、设计模式 | Maven/npm/Cargo 包 + 设计文档 |
| 05 功能架构 | 包装算法、函数、MCP Tool、A2A Agent Card | MCP Server 包、工作流模板 |

---

## 8. 批判性评估

### 8.1 优势

- **供应商中立**: OMG 背书，XML Schema + MOF/XMI 双轨表示
- **元模型完整**: 分类、制品、使用、关系、可变性点全覆盖
- **可扩展**: Profile 机制支持领域定制
- **与 TOGAF 互补**: TOGAF 提供流程和治理，RAS 提供技术包装格式

### 8.2 局限

- **XML 重量级**: 现代生态更偏好 JSON/YAML、OpenAPI、简单包管理器
- **仓库服务薄弱**: 仅搜索/检索，缺少发布、治理、度量、版本工作流
- **版本语义弱**: `version` 是自由字符串，无强制 Semver
- **现代格式支持不足**: 容器镜像、Helm、OpenAPI、Protobuf 只能作为不透明制品
- **竞争激烈**: Maven/npm/Cargo/OSGi 已经解决了各自栈的组件包装问题

### 8.3 2026 年应用建议

1. **将 RAS 作为元模型参考**: 在本体系中采用其“分类-解决方案-使用-关系”四维结构，但用现代格式（Markdown + YAML frontmatter + JSON Schema）实现
2. **结合 SBOM 和包管理器**: 用 SPDX/CycloneDX 替代 RAS 的 `ArtifactDependency`，用 PURL 标识组件
3. **结合 MCP Tool 注册表**: 将 MCP Tool manifest 视为轻量级 RAS `Usage` + `Classification`
4. **等待 RAS 3.0**: 跟踪 OMG/INCOSE 的 RAS 3.0 现代化工作，评估是否正式采用

---

## 9. 公理映射

> **公理 RAS.1** (Asset Completeness): 可复用资产的价值等于其 **Solution** 的完备性乘以 **Usage** 的清晰性，除以 **RelatedAssets** 依赖链的长度。
>
> 形式化：Value(A) = |Solution(A)| × Clarity(Usage(A)) / (1 + len(dependency_chain(A)))

> **公理 RAS.2** (Packaging Trust Transfer): 通过标准化包装（如 RAS/SBOM）传递的信任，不能超过包装元数据本身的可验证性。

---

## 10. 参考链接

- OMG RAS Portal: <https://www.omg.org/spec/RAS/>
- RAS v2.2 Normative PDF: <https://www.omg.org/spec/RAS/2.2/PDF>
- Default Profile XSD: <https://www.omg.org/spec/RAS/20060101/DefaultprofileXML.xsd>
- Default Component Profile XSD: <https://www.omg.org/spec/RAS/20060101/DefaultcomponentprofileXML.xsd>
- Sparx Systems RAS Service: <https://sparxsystems.com/enterprise_architect_user_guide/17.1/modeling_fundamentals/reuseable_asset_service.html>
