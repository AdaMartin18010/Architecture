# FAIR4RS 原则与软件复用对照

> **版本**: 2026-06-08
> **定位**: 将 FAIR4RS 原则纳入四层软件架构复用框架，建立可量化的实施检查清单与成熟度评分模型
> **对齐来源**: FAIR4RS Principles v1.0 (RDA, 2022), Chue Hong et al. (2022), ISO/IEC 25010:2024, OMG RAS v2.2, IEEE 1517-2010
> **状态**: ✅ 已完成
> **交叉引用**: [`../07-omg-ras/ras-alignment.md`](../07-omg-ras/ras-alignment.md), [`../01-iso-420xx-family/ieee-1517-reuse-processes.md`](../01-iso-420xx-family/ieee-1517-reuse-processes.md)

---

## 1. FAIR4RS 核心原则

FAIR4RS（FAIR Principles for Research Software）由 RDA、FORCE11 与 ReSA 于 2022 年联合发布，将 FAIR 数据原则适配至研究软件领域。与数据不同，软件具有**可执行性**与**组合性**，因此原则强调机器可操作与多粒度标识。

| 原则 | 核心要求 | 软件复用含义 |
|------|---------|-------------|
| **Findable** | 软件资产可被唯一标识和检索 | 全局持久 ID + 可搜索元数据索引 |
| **Accessible** | 协议标准化、元数据可获取 | 开放协议检索，认证授权不阻碍访问 |
| **Interoperable** | 使用标准格式和词汇表 | API/数据格式标准化，限定引用 |
| **Reusable** | 清晰的许可证、完善的文档、可验证的依赖 | 许可证合规 + 来源可审计 + 环境可复现 |

---

## 2. 与四层复用架构的对照映射

| FAIR4RS 原则 | 业务架构 | 应用架构 | 组件架构 | 功能架构 |
|-------------|---------|---------|---------|---------|
| **Findable** | 能力目录 (FEA BRM) | 服务注册表 (OpenAPI/UDDI) | 包管理索引 (npm/PyPI/Cargo) | 函数注册表 (MCP Tool Registry) |
| **Accessible** | BPMN/DMN 开放规范 | API 网关 + OpenAPI 文档 | 包仓库 (npm registry/Maven) | Protocol 端点 (stdio/SSE/HTTP) |
| **Interoperable** | ArchiMate 标准交换格式 | CNCF 标准 (gRPC/CloudEvents) | SPDX / SemVer 语义版本 | A2A / MCP 标准协议 |
| **Reusable** | 业务规则库 (DMN 决策表) | 微服务模板 (Helm/Dockerfile) | 开源许可证 (SPDX 标识符) | 概率契约 (Pact/MCP Schema) |

**映射说明**：
- **Findable** 在各层均要求可检索的目录机制：业务能力通过 FEA BRM 分类目录发现；应用服务通过 API 注册表发现；组件通过包管理器索引发现；AI 功能通过 MCP Tool Registry 发现。
- **Accessible** 要求分层协议透明：业务流程模型以开放标准（BPMN/DMN）发布；应用服务通过 API 网关暴露；组件通过包仓库分发；功能通过标准化端点调用。
- **Interoperable** 要求跨层格式统一：业务层使用 ArchiMate 交换；应用层使用 CNCF 接口标准；组件层使用 SPDX 描述和 SemVer 版本约束；功能层使用 A2A 或 MCP 协议实现互操作。
- **Reusable** 要求各层提供可验证的复用契约：业务规则库需配套决策逻辑说明；微服务模板需配套部署配置；组件需明确许可证和 SBOM；功能需声明输入输出 Schema 和概率契约。

---

## 3. 与供应链安全的结合

### 3.1 FAIR4RS + SBOM

| FAIR4RS 原则 | SBOM 映射 | 实践含义 |
|-------------|----------|---------|
| Findable | SBOM 存在性 | 每个发布版本附带 SPDX/CycloneDX SBOM，使组件可被机器发现 |
| Reusable | 许可证合规 | SBOM 中的 `licenseConcluded` 字段确保许可证清晰，支撑法律复用 |

### 3.2 FAIR4RS + SLSA

| FAIR4RS 原则 | SLSA 映射 | 实践含义 |
|-------------|----------|---------|
| Accessible | 构建来源可验证 | SLSA Level ≥ 2 要求构建过程使用托管构建平台，生成可验证的 provenance attestations，确保软件及其元数据的访问路径可信 |

### 3.3 FAIR4RS + MCP Tool 注册表

| FAIR4RS 原则 | MCP 映射 | 实践含义 |
|-------------|----------|---------|
| Findable | Tool Registry 索引 | 每个 MCP Server 在注册表中登记 `name`, `version`, `description` |
| Accessible | stdio / HTTP(S) with SSE | 标准传输层确保 AI 功能的访问不受厂商绑定 |

---

## 4. 实施检查清单

评分模型：**0 = 未实施, 1 = 部分实施, 2 = 基本实施, 3 = 完全实施**。总分 120 分。

| 编号 | Findable (F) 检查项 | 分值 |
|------|---------------------|------|
| F-01 | 软件资产分配全局唯一持久标识符 (DOI/SWHID/PURL) | 0–3 |
| F-02 | 不同粒度 (系统/模块/函数) 均有独立标识 | 0–3 |
| F-03 | 每个发布版本有独立持久标识 (SemVer + Git Tag) | 0–3 |
| F-04 | 元数据包含软件标识符且机器可读 | 0–3 |
| F-05 | 注册到至少一个可搜索公共目录或注册表 | 0–3 |
| F-06 | 提供 CodeMeta 或 CITATION.cff 元数据文件 | 0–3 |
| F-07 | 元数据本身可被搜索引擎索引 (sitemap/robots.txt) | 0–3 |
| F-08 | 使用标准化词汇描述软件领域与功能 | 0–3 |
| F-09 | 文档网站提供清晰的导航与检索功能 | 0–3 |
| F-10 | 架构决策记录 (ADR) 可被独立检索 | 0–3 |

| 编号 | Accessible (A) 检查项 | 分值 |
|------|----------------------|------|
| A-01 | 通过开放、免费、通用协议分发 (HTTPS/Git) | 0–3 |
| A-02 | 协议支持必要的认证与授权 (OIDC/OAuth2) | 0–3 |
| A-03 | 元数据在软件不可用时仍可访问 (Zenodo / SWH) | 0–3 |
| A-04 | 提供稳定的长期支持 (LTS) 版本下载路径 | 0–3 |
| A-05 | 源码与二进制制品均有可访问的归档 | 0–3 |
| A-06 | API 文档通过标准化接口暴露 (OpenAPI/GraphQL) | 0–3 |
| A-07 | 依赖包可通过公共仓库无阻碍获取 | 0–3 |
| A-08 | 容器镜像通过 OCI 标准注册表分发 | 0–3 |
| A-09 | 构建脚本与 CI/CD 配置公开可审计 | 0–3 |
| A-10 | 许可证全文随制品一同分发 | 0–3 |

| 编号 | Interoperable (I) 检查项 | 分值 |
|------|-------------------------|------|
| I-01 | 数据交换采用领域社区标准格式 (JSON/XML/Protobuf) | 0–3 |
| I-02 | API 使用限定引用指向外部资源 (PURL/CPE) | 0–3 |
| I-03 | 组件接口遵循开放标准 (OpenAPI/gRPC/MQTT) | 0–3 |
| I-04 | 使用语义版本 (SemVer) 管理兼容性 | 0–3 |
| I-05 | 数据模型使用共享词汇表或本体 (Schema.org/ECLASS) | 0–3 |
| I-06 | 事件格式遵循 CloudEvents 或 CNCF 标准 | 0–3 |
| I-07 | 配置管理使用声明式标准 (YAML/TOML/JSON Schema) | 0–3 |
| I-08 | 跨语言绑定使用 IDL (Protobuf/Avro/Cap'n Proto) | 0–3 |
| I-09 | 错误码与日志格式遵循可解析标准 | 0–3 |
| I-10 | 协议端点支持内容协商 (Content Negotiation) | 0–3 |

| 编号 | Reusable (R) 检查项 | 分值 |
|------|---------------------|------|
| R-01 | 使用 SPDX 标识符明确声明许可证 | 0–3 |
| R-02 | 提供完整来源 provenance (作者/资助/项目) | 0–3 |
| R-03 | 包含 SBOM (SPDX/CycloneDX) 声明依赖 | 0–3 |
| R-04 | 提供 SLSA provenance 或 Sigstore 签名 | 0–3 |
| R-05 | README 包含安装、使用、贡献指南 | 0–3 |
| R-06 | 代码覆盖率达到可接受阈值 (≥ 60%) | 0–3 |
| R-07 | 架构决策记录 (ADR) 完整且可访问 | 0–3 |
| R-08 | 依赖更新策略清晰 (Renovate/Dependabot) | 0–3 |
| R-09 | 发布制品包含变更日志 (CHANGELOG) | 0–3 |
| R-10 | 提供可复现的构建环境 (Dockerfile/devcontainer) | 0–3 |

**等级划分**：
- **90–120 分**：优秀 (Excellent) — 资产完全 FAIR4RS 合规，可跨组织安全复用
- **60–89 分**：良好 (Good) — 核心原则已实施，存在局部改进空间
- **30–59 分**：及格 (Acceptable) — 基本可发现，但可访问性与可复现性不足
- **< 30 分**：需改进 (Needs Improvement) — 不满足可持续复用最低门槛

---

## 5. 与软件工程标准的映射

### 5.1 FAIR4RS ↔ ISO/IEC 25010:2024 Reusability

ISO/IEC 25010:2024 将 **Reusability** 定义为"软件资产可被用于构建其他软件资产的程度"。映射关系：

| ISO 25010:2024 子特性 | FAIR4RS 对应原则 | 对齐说明 |
|----------------------|-----------------|---------|
| Modularity | Interoperable | 模块化接口标准促进互操作 |
| Reusability (资产包装) | Findable + Accessible | RAS/SPDX 包装使资产可发现与获取 |
| Compatibility | Interoperable | 数据格式与 API 标准兼容性 |
| Maintainability | Reusable | 文档与来源 provenance 支撑长期维护 |

### 5.2 FAIR4RS ↔ OMG RAS v2.2 Classification/Usage

| RAS v2.2 核心部分 | FAIR4RS 原则 | 对齐说明 |
|------------------|-------------|---------|
| Classification | Findable | 分类信息回答"这是什么"，是发现的首要依据 |
| Solution | Accessible + Interoperable | 解决方案包含实际制品与可变性点 |
| Usage | Reusable | 使用指南回答"如何安装、定制、运行" |
| RelatedAssets | Interoperable | 相关资产引用实现限定依赖声明 |

### 5.3 FAIR4RS ↔ IEEE 1517 Reuse Process

IEEE 1517-2010 定义软件生命周期中的复用过程，包括领域工程与应用工程双轨。映射：

| IEEE 1517 过程域 | FAIR4RS 原则 | 对齐说明 |
|-----------------|-------------|---------|
| 领域工程 (Domain Engineering) | Findable + Interoperable | 构建可复用资产库，要求标准分类与接口 |
| 应用工程 (Application Engineering) | Accessible + Reusable | 从资产库检索、适配、集成到目标系统 |
| 复用管理 (Reuse Management) | Reusable | 资产成熟度评估、版本控制、许可证审计 |

---

## 6. 权威来源

- FAIR4RS Principles v1.0. Research Data Alliance, FORCE11, ReSA, 2022. <https://ardc.edu.au/resource/fair-principles-for-research-software-fair4rs/>
- Chue Hong, N.P., et al. (2022). "FAIR Principles for Research Software". *Nature Scientific Data*. <https://doi.org/10.1038/s41597-022-01710-x>
- Barker, M., et al. (2022). "Introducing the FAIR Principles for Research Software". *RDA*.
- ISO/IEC 25010:2024. *Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Quality model*.
- OMG RAS v2.2. *Reusable Asset Specification*. formal/05-11-02. <https://www.omg.org/spec/RAS/>
- IEEE 1517-2010. *IEEE Standard for Information Technology — System and Software Life Cycle Processes — Reuse Processes*.
- ReSA Actionable FAIR4RS Task Force (2024–2025). <https://www.researchsoft.org/tf-actionable-fair4rs/>
