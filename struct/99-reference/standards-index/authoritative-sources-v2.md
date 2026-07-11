# 国际标准与权威来源索引 v2.3

> **版本**: 2026-07-08 v2.3
> **定位**: 全项目引用的事实基准。所有 Markdown 文件引用标准、框架、协议时，应优先以本表为准。
> **维护节奏**: 每季度（3 月、6 月、9 月、12 月）对照官方来源复核一次。
> **上次复核**: 2026-07-08
> **下次复核**: 2026-09-30
> **关联勘误**: [`99-reference/audit/content-fact-fix-2026-07.md`](../audit/content-fact-fix-2026-07.md)

---

## 目录

- [国际标准与权威来源索引 v2.3](#国际标准与权威来源索引-v23)
  - [目录](#目录)
  - [使用说明](#使用说明)
  - [架构与软件工程标准](#架构与软件工程标准)
  - [企业架构与建模框架](#企业架构与建模框架)
  - [安全与供应链](#安全与供应链)
  - [工业 IoT / OT-IT 融合](#工业-iot--ot-it-融合)
  - [AI 原生与新兴协议](#ai-原生与新兴协议)
  - [形式化方法与验证](#形式化方法与验证)
  - [价值量化与可持续软件](#价值量化与可持续软件)
  - [变更日志](#变更日志)
  - [补充说明：国际标准与权威来源索引 v2.2](#补充说明国际标准与权威来源索引-v22)
  - [概念定义](#概念定义)
  - [示例](#示例)
  - [反例](#反例)
  - [权威来源](#权威来源)

## 使用说明

1. **引用标准时**：先查本表确认官方版本号、状态和 URL，再写入文档。
2. **发现版本冲突时**：以本表为基准，修正项目内其他文件。
3. **新增标准时**：补充到本表，并标注复核日期。
4. **链接失效时**：更新本表 URL，并同步修改引用处。

---

## 架构与软件工程标准

| 标准/框架 | 版本 | 状态 | 官方 URL | 备注 |
|-----------|------|------|----------|------|
| **ISO/IEC 21838** | -1:2021 / -2:2021 / -3:2023 | 已发布 | <https://www.iso.org/standard/74307.html> | Top-Level Ontologies（TLO）；项目内引用 74307 为第 3 分部 DOLCE 的 URL |
| **ISO/IEC/IEEE 42010** | 2022 | 现行 | <https://www.iso.org/standard/74296.html> | 架构描述（Architecture Description） |
| **ISO/IEC/IEEE 42020** | 2019 | 现行；计划修订 | <https://www.iso.org/standard/68982.html> | 架构过程（Architecture Processes） |
| **ISO/IEC/IEEE 42030** | 2019 | 现行；AWI 修订中 | <https://www.iso.org/standard/73436.html> | 架构评估（Architecture Evaluation） |
| **ISO/IEC/IEEE AWI 42030** | — | 已注册工作项 | <https://www.iso.org/standard/93814.html> | 42030 修订项目 |
| **ISO/IEC/IEEE DIS 42024** | — | 草案；enquiry 2026-01-12 结束 | <https://www.iso.org/standard/87510.html> | 架构基础（Architecture Fundamentals） |
| **ISO/IEC/IEEE DIS 42042** | — | 草案；stage 40.60，enquiry 2026-01-30 结束 | <https://www.iso.org/standard/87310.html> | 参考架构（Reference Architectures） |
| **ISO/IEC/IEEE 12207** | **2026** | **已发布** | <https://www.iso.org/standard/90219.html> | 软件生命周期过程；2026-04-29 发布，取代 2017 版 |
| **ISO/IEC/IEEE 15288** | 2023 | 现行 | <https://www.iso.org/standard/81702.html> | 系统生命周期过程 |
| **ISO/IEC/IEEE 24765** | 2017 | 现行；计划修订 | <https://www.iso.org/standard/71952.html> | 系统与软件工程词汇 |
| **ISO/IEC 25010** | **2023** | 已发布 | <https://www.iso.org/standard/78175.html> | SQuaRE 产品质量模型；**注意：不存在 :2024 版** |
| **ISO/IEC 25040** | 2024 | 已发布 | <https://www.iso.org/standard/83467.html> | 质量评估框架 |
| **ISO/IEC 26550** | 2015 | 现行 | <https://www.iso.org/standard/69529.html> | 产品线工程参考模型；**注意：不存在 2025 版** |
| **ISO/IEC 26564** | 2022 | 已发布 | <https://www.iso.org/standard/81622.html> | 产品线度量（product line measurement）；URL 待 ISO 直连复核 |
| **ISO/IEC 26565** | 2026 | 已发布 | <https://www.iso.org/standard/81436.html> | 产品线成熟度框架（product line maturity framework）；2026-05-29 发布；URL 待 ISO 直连复核 |
| **ISO/IEC 26566** | 2026 | 已发布 | <https://www.iso.org/standard/81437.html> | 软件和系统工程 — 产品线纹理（product line texture）的方法与工具能力；定义纹理管理、操作化与支持的过程、方法能力和工具能力 |
| **ISO/IEC 26580** | 2021 | 已发布 | <https://www.iso.org/standard/71883.html> | 基于特征的产品线工程 |
| **ISO/IEC 33000 (SPICE)** | 系列 | 现行 | <https://www.iso.org/ics/35.080/x/> | 软件过程评估与能力确定 |
| **IEEE 1517** | 2010 | 现行 | <https://standards.ieee.org/standard/1517-2010.html> | 软件生命周期复用过程 |
| **OMG RAS** | v2.2 | 已发布 | <https://www.omg.org/spec/RAS/2.2/PDF> | 可复用资产规范（Reusable Asset Specification） |
| **FAIR4RS** | v1.0 | 已发布 | <https://doi.org/10.15497/RDA00068> | 研究软件可复用的 FAIR 原则 |
| **SWEBOK** | V4 | 已发布 | <https://www.computer.org/education/bodies-of-knowledge/software-engineering> | 软件工程知识体系 |
| **ISO/IEC 5338** | 2023 | 已发布 | <https://www.iso.org/standard/81118.html> | AI 系统生命周期过程 |
| **ISO/IEC 42001** | 2023 | 已发布 | <https://www.iso.org/standard/81230.html> | AI 管理体系 |

---

## 企业架构与建模框架

| 标准/框架 | 版本 | 状态 | 官方 URL | 备注 |
|-----------|------|------|----------|------|
| **TOGAF Standard** | 10th Edition | 现行 | <https://www.opengroup.org/togaf> | The Open Group 企业架构框架 |
| **ArchiMate** | 4.0 | **已正式发布（2026-04-27，Document C260，白皮书 W262）** | <https://www.opengroup.org/archimate-licensed-downloads> | The Open Group EA 建模语言；与 ArchiMate 3.2 向后兼容；官方发布公告见 <https://www.opengroup.org/The-Open-Group-Announces-ArchiMate%C2%AE-4-Specification> |
| **ArchiMate** | 3.2 | 仍有效 | <https://pubs.opengroup.org/architecture/archimate32-doc/> | 与 4.0 向后兼容 |
| **FEA** | 2.0 / BRM / ARM / SRM | 现行 | <https://www.whitehouse.gov/omb/management/egov/> | 美国联邦企业架构参考模型 |
| **BPMN** | 2.0 | 现行 | <https://www.omg.org/spec/BPMN/2.0> | 业务流程建模符号 |
| **DMN** | 1.5 | 2024 发布 | <https://www.omg.org/spec/DMN/1.5> | 决策模型与符号 |
| **OMG SysML v2** | v2 | 已发布 | <https://www.omg.org/spec/SysML/> | 系统建模语言第二版 |

---

## 安全与供应链

| 标准/框架 | 版本 | 状态 | 官方 URL | 备注 |
|-----------|------|------|----------|------|
| **SLSA** | 1.2 | 已发布 | <https://slsa.dev/spec/v1.2/> | Multi-Track；Build/Source Track 已发布；Build Environment Track / Build Level 4 仍在开发 |
| **NIST SSDF** | v1.2 | **Initial Public Draft（最终版预计 2026-Q3）** | <https://csrc.nist.gov/publications/detail/sp/800-218r1/draft> | SP 800-218 Rev. 1，2025-12-17 发布征求意见稿；**非最终版** |
| **OWASP Top 10 for Agentic AI** | 2025/2026 | 已发布 | <https://owasp.org/www-project-agentic-ai/> | 自主 Agent 应用安全风险（ASI01–ASI10） |
| **OWASP MCP Top 10** | 2025/2026 | 已发布 | <https://cycode.com/blog/owasp-mcp-top-10/> | Model Context Protocol 专用安全风险 |
| **Microsoft Agent Governance Toolkit** | 1.0 | **2026-04-02 开源** | <https://github.com/microsoft/agent-governance-toolkit> | Agent 运行时治理、审计、策略执行；覆盖 OWASP Agentic Top 10 |
| **NIST SP 800-218** | v1.1 | 现行 | <https://csrc.nist.gov/publications/detail/sp/800-218/final> | SSDF v1.1 正式版 |
| **NIST SP 800-218A** | — | 已发布 | <https://csrc.nist.gov/publications/detail/sp/800-218a/final> | 生成式 AI 安全开发实践社区配置文件 |
| **OWASP Top 10** | 2025 | 已发布 | <https://owasp.org/www-project-top-ten/> | — |
| **OWASP ASVS** | 5.0.0 | 已发布 | <https://owasp.org/www-project-application-security-verification-standard/> | — |
| **OWASP SCVS** | 1.0 | 已发布 | <https://owasp.org/www-project-software-component-verification-standard/> | 软件组件验证标准 |
| **OpenSSF OSPS** | Baseline | 现行 | <https://openssf.org/projects/openssf-osps-baseline/> | 开源项目安全基线 |
| **OpenSSF Scorecard** | — | 现行 | <https://github.com/ossf/scorecard> | 开源安全健康度检查 |
| **SPDX** | 2.3 | 现行 | <https://spdx.dev/specifications/> | 软件物料清单标准 |
| **CycloneDX** | 1.6 | 现行 | <https://cyclonedx.org/specification/overview/> | 软件物料清单标准 |
| **EU CRA** | 2024/2847 | 已发布 | <https://eur-lex.europa.eu/eli/reg/2024/2847> | 欧盟网络弹性法案 |
| **NIST SP 800-161 Rev. 1** | — | 现行 | <https://csrc.nist.gov/publications/detail/sp/800-161/rev-1/final> | 供应链网络安全风险管理 |
| **NIST SP 800-204** | 系列 | 2025 更新 | <https://csrc.nist.gov/publications/detail/sp/800-204/final> | 微服务安全架构 |
| **IEC 62443-4-1** | 2018 | 现行 | <https://webstore.iec.ch/publication/66912> | IACS 安全产品开发生命周期要求 |
| **IEC 62443-4-2** | **2019** | 现行 | <https://webstore.iec.ch/publication/66913> | IACS 组件技术安全要求；**注意：不是 2025 版** |
| **IEC TS 62443-6-2** | 2025 | 已发布 | <https://webstore.iec.ch/en/publication/67463> | IACS 组件评估方法论 |

---

## 工业 IoT / OT-IT 融合

| 标准/框架 | 版本 | 状态 | 官方 URL | 备注 |
|-----------|------|------|----------|------|
| **ISA-95 / IEC 62264** | — | 现行 | <https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95> | 企业-控制系统集成 |
| **ISO/IEC 30141** | **2024** | **已发布** | <https://www.iso.org/standard/88800.html> | IoT 参考架构；**2024-08 发布，取代 2018 版** |
| **IEC 61508** | **Ed.3 (认证基准 2026；IEC 正式发布预计 ~2027)** | **CDV 投票完成；TÜV Rheinland 等主要认证机构于 2026-06 起可采用 Ed.3 作为 SIL 2+ 认证基准** | <https://iec.ch/dyn/www/f?p=103:23:::::FSP_ORG_ID:1369> | 功能安全基础标准；需区分“认证机构强制采用”与“IEC 国际标准正式发布” |
| **ISO 21448** | 2022 | Ed.2 制定中（预计 2026） | <https://www.iso.org/standard/93071.html> | 预期功能安全 (SOTIF)；扩展至 SAE L3-L5 |
| **ISO 26262** | 2018 | 现行；Ed.3 新工作项注册（目标 ~2029） | <https://www.iso.org/standard/68383.html> | 道路车辆功能安全 |
| **IEC 63278-1** | 2023 | 已发布 | <https://webstore.iec.ch/en/publication/65628> | 资产管理壳（AAS）结构 |
| **OPC UA FX** | 1.0 (Parts 80–84) | 已发布 | <https://opcfoundation.org/about/opc-technologies/opc-ua/opc-ua-fx/> | 现场级通信 |
| **IEC/IEEE 60802** | — | 草案/完善中 | <https://www.iec.ch/dyn/www/f?p=103:38:0::::::> | TSN 工业自动化配置文件 |
| **PLCopen Motion Control** | Part 1–4 + Safety | 现行 | <https://plcopen.org/technical-activities/motion-control> | 运动控制功能块 |

---

## AI 原生与新兴协议

| 标准/框架 | 版本 | 状态 | 官方 URL | 备注 |
|-----------|------|------|----------|------|
| **MCP** | 2025-11-25 | **现行稳定版** | <https://modelcontextprotocol.io/specification/2025-11-25> | Model Context Protocol；已捐给 Linux Foundation Agentic AI Foundation |
| **MCP** | 2026-07-28 | **Release Candidate（RC）已发布（2026-05-29）；最终版预计 2026-07-28** | <https://github.com/modelcontextprotocol/modelcontextprotocol/releases> | 协议改为 stateless，新增 Extensions 框架、Tasks、MCP Apps；引用时必须标注 RC |
| **A2A** | **v1.0.0** | **已发布** | <https://a2a-protocol.org/latest/> | Agent-to-Agent Protocol；Google Cloud Next 2026-04 GA；Signed Agent Cards / AP2 |
| **NIST AI RMF** | 1.0 | 已发布 | <https://www.nist.gov/itl/ai-risk-management-framework> | AI 风险管理框架 |
| **NIST AI 600-1** | — | 已发布 | <https://www.nist.gov/artificial-intelligence/ai-600-1> | AI 红队测试 |
| **WebAssembly Core** | 3.0 | 已发布 | <https://webassembly.org> | W3C WebAssembly 核心规范 |
| **WASM Component Model** | — | W3C Phase 1 | <https://component-model.bytecodealliance.org/> | 跨语言组件模型 |
| **WASI** | 0.3 Preview | 2026-02 发布 preview；Wasmtime 37+ 支持 | <https://github.com/WebAssembly/WASI> | 原生 async I/O（stream/future）；WASI 1.0 目标 2026末/2027初 |
| **DMN** | 1.5 | 2024 发布 | <https://www.omg.org/spec/DMN/1.5> | 决策模型与符号 |
| **CloudEvents** | 1.0.2 | 已发布 | <https://cloudevents.io/> | 事件数据规范 |

---

## 形式化方法与验证

| 标准/工具 | 版本 | 状态 | 官方 URL | 备注 |
|-----------|------|------|----------|------|
| **TLA+** | — | 现行 | <https://lamport.azurewebsites.net/tla/tla.html> | Leslie Lamport 时序逻辑规约 |
| **Alloy** | 6 | 现行 | <https://alloytools.org/> | MIT 约束求解建模 |
| **Coq** | — | 现行 | <https://coq.inria.fr> | 定理证明助手 |
| **Isabelle/HOL** | — | 现行 | <https://isabelle.in.tum.de> | 定理证明器 |
| **SPARK/Ada** | — | 现行 | <https://www.adacore.com/about-spark> | AdaCore 形式化验证工具 |
| **B Method** | — | 现行 | <https://www.atelierb.eu> | Clearsy 形式化方法 |
| **Rust** | — | 现行 | <https://www.rust-lang.org> | 类型系统内存安全 |
| **Kani** | — | 现行 | <https://github.com/model-checking/kani> | AWS Rust 模型检查器 |
| **Miri** | — | 现行 | <https://github.com/rust-lang/miri> | Rust UB 行为检测 |
| **IEEE 1012** | 2024 | 已发布 | <https://standards.ieee.org/standard/1012-2024.html> | 软件验证与确认 |

---

## 价值量化与可持续软件

| 标准/框架 | 版本 | 状态 | 官方 URL | 备注 |
|-----------|------|------|----------|------|
| **COCOMO II** | 2000.1 / 后续校准 | 现行 | <https://csse.usc.edu/tools/cocomoii.php> | 软件成本估算模型 |
| **FinOps Foundation** | — | 现行 | <https://www.finops.org/> | 云成本管理框架 |
| **GSF SCI** | — | 现行；已 ISO/IEC 21031:2024 | <https://sci.greensoftware.foundation/> | 软件碳强度规范 |
| **GSF SCI for AI** | — | **2026-Q1 ratified** | <https://greensoftware.foundation/standards/sci-ai/> | AI 系统全生命周期碳强度度量 |
| **ISO/IEC 14040** | 系列 | 现行 | <https://www.iso.org/standard/37456.html> | 生命周期评价 |

---

## 变更日志

| 日期 | 变更内容 | 责任人 |
|:---|:---|:---|
| 2026-06-12 | 创建 v2.0；修正 ISO/IEC 25010:2023、ArchiMate 4.0、ISO/IEC 30141:2024、ISO/IEC/IEEE 12207:2026、NIST SSDF 1.2、IEC 62443 等状态 | 自动对齐代理 |
| 2026-06-12 | 新增 ISO/IEC 5338:2023、ISO/IEC 42001:2023、IEC TS 62443-6-2:2025 等条目 | 自动对齐代理 |
| 2026-07-06 | 更新为 v2.1：更新 DIS 42024/42042 状态、IEC 61508 Ed.3、ISO 21448 Ed.2、SLSA 1.2、NIST SSDF 1.2 状态；新增 OWASP Agentic AI / MCP Top 10、Microsoft Agent Governance Toolkit、A2A v1.0 GA、WASI 0.3、GSF SCI for AI | 自动对齐代理 |
| 2026-07-07 | 更新为 v2.2：ArchiMate 4.0 增加“官方页面更新滞后”备注；新增 MCP 2026-07-28 RC 条目；细化 IEC 61508 Ed.3“认证机构采用 vs 标准发布”区分；关联 `content-fact-fix-2026-07.md` 勘误报告 | 自动对齐代理 |
| 2026-07-11 | 更新为 v2.4：补录 ISO/IEC 26564:2022、ISO/IEC 26565:2026、ISO/IEC 21838 系列（真实已发布但原表漏收）| 自动对齐代理 |

---

> **注意**: 本表为人工复核后的基准。若官方来源在下次复核前发生变更，以官方最新发布为准，并及时更新本表。


---

## 补充说明：国际标准与权威来源索引 v2.2

## 概念定义

**定义**：参考层是结构化知识体系的“地图”，汇总权威来源、术语表、标准索引、课程对标与审计报告，为各主题提供可追溯的引用与一致性校验。

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