# 跨标准术语对照表

> **版本**: 2026-06-06
> **定位**: 建立不同标准/框架之间的术语映射，降低跨标准理解的摩擦

---

## ISO 42010 vs TOGAF 10

| ISO 42010:2022 | TOGAF 10 | 说明 |
|-----------|---------|------|
| Entity of Interest (EoI) | System of Interest | 2022 版新术语 |
| Architecture Description (AD) | Architecture Repository / Catalog | 架构描述的载体 |
| Stakeholder | Stakeholder | 利益相关者 |
| Concern | Concern / Architecture Requirement | 关注点/架构需求 |
| Viewpoint | Viewpoint | 视点 |
| View | View / Architecture View | 视图 |
| Architecture View Component | Model / Artifact | 视图组件（替代 Model） |
| Model Kind | Model / Artifact | 模型种类 |
| Correspondence | Relationship / Traceability | 对应关系 |
| Architecture Rationale | Architecture Decision / ADR | 架构依据 |
| Architecture Description Framework (ADF) | Architecture Framework | 2022 版新术语 |

## ArchiMate vs UML

| ArchiMate | UML | 说明 |
|-----------|-----|------|
| Business Actor | Actor | 业务参与者 |
| Business Role | Role | 业务角色 |
| Business Process | Activity Diagram | 业务流程 |
| Business Function | Package / Component | 业务功能 |
| Business Service | Interface | 业务服务 |
| Application Component | Component | 应用组件 |
| Application Service | Provided Interface | 应用服务 |
| Data Object | Class | 数据对象 |
| Node | Deployment Node | 节点 |
| Device | Node | 设备 |

## ISO 26550 vs 本体系

| ISO 26550 | 本体系对应主题 | 说明 |
|-----------|--------------|------|
| Domain Engineering | 01-元模型, 02-业务架构 | 领域工程产生可复用资产 |
| Application Engineering | 03-应用架构, 04-组件架构 | 应用工程使用可复用资产 |
| Product Line | 06-跨层治理 | 产品线管理复用资产 |
| Variability Model | 02-业务架构, 04-组件架构 | 变性模型 |
| Core Asset | 04-组件架构, 05-功能架构 | 核心资产 |

## SLSA vs NIST SSDF

| SLSA 1.2 | NIST SSDF 1.2 | 说明 |
|-----------|-----------|------|
| Build L1 Provenance | PO.1 Secure Software | 保护软件 |
| Build L2 Source-aware | PW.4 Reusable Code | 安全复用代码 |
| Build L3 Hardened | PW.6 Configure Compiler | 配置编译器 |
| Build L4 Reproducible | PW.8 Test Executable | 测试可执行文件 |
| Source L1 Version Control | PO.3.1 Store Code | 存储代码 |
| Source L3 Two-Person Review | PO.3.2 Review Code | 审查代码 |
| VEX | RV.1 / RV.2 | 漏洞可利用性 |
| SBOM | PW.7 / RV.2 | 软件物料清单 |

## Industrial Standards Crosswalk

| IEC 63278 (AAS) | OPC UA | ISA-95 | 说明 |
|-----------------|--------|--------|------|
| AssetAdministrationShell | Server / Object | Enterprise / Site / Area | 资产的管理壳 |
| Submodel | ObjectType / Folder | Work Unit / Cell | 子模型 |
| Property | Variable | Tag / Attribute | 属性 |
| Operation | Method | Operation / Phase | 操作 |
| ConceptDescription | VariableType | Data Structure | 概念描述 |
| AASX Package | - | - | 离线数据交换格式 |

## TSN 标准映射

| 标准 | 功能 | 应用场景 |
|------|------|---------|
| IEEE 802.1AS | 时间同步 | 所有 TSN 应用 |
| IEEE 802.1Qbv | 门控调度 | 硬实时流量 |
| IEEE 802.1Qbu/802.3br | 帧抢占 | 降低非实时流量对实时流量的影响 |
| IEEE 802.1CB | 帧复制和消除 | 高可靠性应用 |
| IEEE 802.1Qcc | 流预留 | 资源管理 |
| IEC/IEEE 60802 | TSN 工业自动化配置文件 | 工业 4.0 |

## AI Native Terminology

| MCP 2025-11-25 | A2A v1.0 | 通用含义 |
|----------|---------|---------|
| Server | Agent | 提供服务/能力的实体 |
| Tool | Skill | 可调用的具体能力 |
| Resource | Artifact | 可被访问的数据/内容 |
| Prompt | Message Part | 与 LLM 交互的单元 |
| Capability | Agent Card | 声明的能力集合 |
| Host-Client-Server | Peer-to-Peer | 架构关系 |

## 形式化验证术语映射

| TLA+ | Alloy | Coq/Isabelle | 通用含义 |
|------|-------|--------------|---------|
| State | Atom/Signature | Term/Type | 系统状态/元素 |
| Action | Predicate/Fact | Lemma/Theorem | 状态转移/性质 |
| Invariant | Assertion | Invariant | 不变量 |
| Liveness | Assertion (eventually) | Coinductive Proof | 活性性质 |
| MODULE | Module | Section/Module | 模块化单元 |
| VARIABLE | sig/field | Variable/Parameter | 状态变量 |
| Init | fact init | Definition init | 初始状态 |
| Next | pred step | Inductive step | 下一步关系 |

## 认知架构术语

| ACT-R | BDI | 双系统理论 | 通用含义 |
|-------|-----|-----------|---------|
| Chunk | Belief | Memory/Pattern | 知识单元 |
| Production | Desire-Intention | System 1 (Fast) | 行为规则 |
| Goal | Intention | System 2 (Slow) | 目标导向 |
| Retrieval | Belief Update | Recognition | 信息提取 |
| Cognitive Load | Cognitive Load | Cognitive Load | 认知负荷 |

## 平台工程与 WASM 术语

| 平台工程 | WASM | 通用含义 |
|---------|------|---------|
| IDP (Internal Developer Platform) | WASM Runtime | 内部开发者平台 / 运行时 |
| Golden Path | WIT (Wasm Interface Types) | 标准化路径 / 接口类型 |
| Software Catalog | Component Registry | 软件目录 / 组件注册表 |
| Self-Service | WASI | 自助服务 / 系统接口 |
| Platform Team | Component Producer | 平台团队 / 组件生产者 |

## 供应链安全术语

| SLSA | SBOM | 零信任 | 通用含义 |
|------|------|--------|---------|
| Provenance | SPDX Document | Identity Verification | 来源证明 |
| Attestation | CycloneDX BOM | Device Health | 证明/声明 |
| Build Integrity | Component Hash | Least Privilege | 构建完整性 |
| Reproducible Build | Dependency Tree | Continuous Verification | 可复现构建 |

---

## 质量标准版本对照

| 标准 | 旧版 | 新版 | 关键变化 |
|------|------|------|---------|
| ISO 42010 | 2011 | 2022 | EoI, ADF, View Component, Aspect, Perspective |
| ISO 25010 | 2011 | 2023 | 9 特性，新增 Safety/Flexibility/Interaction Capability |
| SLSA | v0.1 | v1.2 | Multi-Track: Build/Source/Environment |
| NIST SSDF | v1.1 (2022) | v1.2 (2026) | 供应链风险管理、VEX、SBOM |
| IEC 63278 | - | Part 1: 2023; Parts 2-5 开发中 | AAS 系列标准 |
| OPC UA FX | - | Parts 80-84 | C2C, Offline Engineering |
| MCP | 2024-11-05 | 2025-11-25 | Streamable HTTP, OAuth 2.1, schema 拆分 |
| A2A | v0.1 (2025-04) | v1.0 (2026-04) | Signed Agent Cards, gRPC, 多租户 |

---

> 最后更新: 2026-06-06


---

## 补充说明：跨标准术语对照表

## 示例

**示例**：维护 authoritative-sources.md 登记所有 ISO/IEC、IEEE、NIST、CNCF 来源 URL 与核查日期，确保全书引用可验证。

## 反例

**反例**：参考层链接长期不更新，术语表与正文定义冲突，读者无法确认内容准确性与时效性。

## 权威来源

> **权威来源**:
>
> - [ISO](https://www.iso.org)
> - [IEEE Standards](https://standards.ieee.org)
> - [NIST](https://www.nist.gov)
> - [CNCF](https://www.cncf.io)
> - 核查日期：2026-07-07

## 分析

**分析**：参考层的价值不在于内容本身，而在于建立知识之间的信任锚点；必须随标准演进定期审计与更新。
