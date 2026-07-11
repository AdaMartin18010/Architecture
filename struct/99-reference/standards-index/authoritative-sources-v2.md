# 国际标准与权威来源索引 v2.9

> **版本**: 2026-07-11 v2.9
> **定位**: 全项目引用的事实基准。所有 Markdown 文件引用标准、框架、协议时，应优先以本表为准。
> **维护节奏**: 每季度（3 月、6 月、9 月、12 月）对照官方来源复核一次。
> **上次复核**: 2026-07-11
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
| **ISO/IEC 21838** | -1:2021 / -2:2021（BFO）/ -3:2023（DOLCE）/ -4:2023（TUpper） | 已发布；-5（UFO）DIS 阶段 | <https://www.iso.org/standard/71954.html> | Top-Level Ontologies（TLO）；链接为 -1（Requirements，实测确认）；-4 TUpper = iso.org/standard/78928；-5 UFO = iso.org/standard/89915（2025-12 进入 DIS） |
| **ISO/IEC/IEEE 42010** | 2022 | 现行 | <https://www.iso.org/standard/74393.html> | 架构描述（Architecture Description）；URL 经 iso.org 直连实测确认（原误填 74296=ISO/IEC 22989） |
| **ISO/IEC/IEEE 42020** | 2019 | 现行；计划修订 | <https://www.iso.org/standard/68982.html> | 架构过程（Architecture Processes） |
| **ISO/IEC/IEEE 42030** | 2019 | 现行；AWI 修订中 | <https://www.iso.org/standard/73436.html> | 架构评估（Architecture Evaluation） |
| **ISO/IEC/IEEE AWI 42030** | — | 已注册工作项 | <https://www.iso.org/standard/93814.html> | 42030 修订项目 |
| **ISO/IEC/IEEE DIS 42024** | — | 草案；enquiry 2026-01-12 结束 | <https://www.iso.org/standard/87510.html> | 架构基础（Architecture Fundamentals） |
| **ISO/IEC/IEEE DIS 42042** | — | 草案；stage 40.60，enquiry 2026-01-30 结束 | <https://www.iso.org/standard/87310.html> | 参考架构（Reference Architectures） |
| **ISO/IEC/IEEE 12207** | **2026** | **已发布** | <https://www.iso.org/standard/90219.html> | 软件生命周期过程；2026-04-29 发布，取代 2017 版 |
| **ISO/IEC/IEEE 15288** | 2023 | 现行 | <https://www.iso.org/standard/81702.html> | 系统生命周期过程 |
| **ISO/IEC/IEEE 24765** | 2017 | 现行；计划修订 | <https://www.iso.org/standard/71952.html> | 系统与软件工程词汇 |
| **ISO/IEC 25010** | **2023** | 已发布 | <https://www.iso.org/standard/78176.html> | SQuaRE 产品质量模型；**注意：不存在 :2024 版**；URL 经 iso.org 直连实测确认（原误填 78175=ISO/IEC 25002:2024） |
| **ISO/IEC 25040** | 2024 | 已发布 | <https://www.iso.org/standard/83467.html> | 质量评估框架 |
| **ISO/IEC 26550** | 2015 | 现行 | <https://www.iso.org/standard/69529.html> | 产品线工程参考模型；**注意：不存在 2025 版** |
| **ISO/IEC 26564** | 2022 | 已发布 | <https://www.iso.org/standard/43123.html> | 产品线度量（product line measurement）；2022-12 首版；URL 经 iso.org 直连实测确认（原误填 81622=ISO/TS 24560-1）|
| **ISO/IEC 26565** | 2026 | 已发布 | <https://www.iso.org/standard/81436.html> | 产品线成熟度框架（product line maturity framework）；2026-05-29 发布；URL 经 iso.org 直连实测确认 |
| **ISO/IEC 26566** | 2026 | 已发布 | <https://www.iso.org/standard/81437.html> | 软件和系统工程 — 产品线纹理（product line texture）的方法与工具能力；定义纹理管理、操作化与支持的过程、方法能力和工具能力 |
| **ISO/IEC 26580** | 2021 | 已发布 | <https://www.iso.org/standard/43139.html> | 基于特征的产品线工程（feature-based PLE）；URL 经 iso.org 直连实测确认（原误填 71883=ISO 10204） |
| **ISO/IEC 33000 (SPICE)** | 系列 | 现行 | <https://www.iso.org/ics/35.080/x/> | 软件过程评估与能力确定 |
| **IEEE 1517** | 2010 | 现行 | <https://standards.ieee.org/ieee/1517/4603/> | 软件生命周期复用过程 |
| **OMG RAS** | v2.2 | 已发布 | <https://www.omg.org/spec/RAS/2.2/PDF> | 可复用资产规范（Reusable Asset Specification） |
| **FAIR4RS** | v1.0 | 已发布 | <https://archive.rd-alliance.org/sites/default/files/FAIR%20Principles%20for%20Research%20Software%20%28FAIR4RS%20Principles%29.pdf> | 研究软件可复用的 FAIR 原则 |
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
| **FEA** | 2.0 / BRM / ARM / SRM | 现行 | <https://obamawhitehouse.archives.gov/omb/e-gov/fea> | 美国联邦企业架构参考模型；原 whitehouse.gov 链接已迁移至国家档案馆归档页 |
| **BPMN** | 2.0 | 现行 | <https://www.omg.org/spec/BPMN/2.0> | 业务流程建模符号 |
| **DMN** | 1.5 | 2024 发布 | <https://www.omg.org/spec/DMN/1.5> | 决策模型与符号 |
| **OMG SysML v2** | v2 | 已发布 | <https://www.omg.org/spec/SysML/> | 系统建模语言第二版 |

---

## 安全与供应链

| 标准/框架 | 版本 | 状态 | 官方 URL | 备注 |
|-----------|------|------|----------|------|
| **SLSA** | 1.2 | 已发布 | <https://slsa.dev/spec/v1.2/> | Multi-Track；Build/Source Track 已发布；Build Environment Track / Build Level 4 仍在开发 |
| **NIST SSDF** | v1.2 | **Initial Public Draft（最终版预计 2026-Q3）** | <https://csrc.nist.gov/pubs/sp/800/218/r1/ipd> | SP 800-218 Rev. 1，2025-12-17 发布征求意见稿；**非最终版** |
| **OWASP Top 10 for Agentic AI** | 2026 | 已发布 | <https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/> | 自主 Agent 应用安全风险（ASI01–ASI10） |
| **OWASP MCP Top 10** | 2025/2026 | 已发布（Beta / v0.1） | <https://owasp.org/www-project-mcp-top-10/> | Model Context Protocol 专用安全风险 |
| **Microsoft Agent Governance Toolkit** | 1.0 | **2026-04-02 开源** | <https://github.com/microsoft/agent-governance-toolkit> | Agent 运行时治理、审计、策略执行；覆盖 OWASP Agentic Top 10 |
| **NIST SP 800-218** | v1.1 | 现行 | <https://csrc.nist.gov/publications/detail/sp/800-218/final> | SSDF v1.1 正式版 |
| **NIST SP 800-218A** | — | 已发布（2024-07；NIST 当前仅提供 IPD 页面） | <https://csrc.nist.gov/pubs/sp/800/218/a/ipd> | 生成式 AI 安全开发实践社区配置文件 |
| **OWASP Top 10** | 2025 | 已发布 | <https://owasp.org/www-project-top-ten/> | — |
| **OWASP ASVS** | 5.0.0 | 已发布 | <https://owasp.org/www-project-application-security-verification-standard/> | — |
| **OWASP SCVS** | 1.0 | 已发布 | <https://owasp.org/www-project-software-component-verification-standard/> | 软件组件验证标准 |
| **OpenSSF OSPS** | Baseline | 现行 | <https://baseline.openssf.org/> | 开源项目安全基线（OSPS Baseline）；源仓库 github.com/ossf/security-baseline |
| **OpenSSF Scorecard** | — | 现行 | <https://github.com/ossf/scorecard> | 开源安全健康度检查 |
| **SPDX** | 2.3 | 现行 | <https://spdx.dev/specifications/> | 软件物料清单标准 |
| **CycloneDX** | 1.6 | 现行 | <https://cyclonedx.org/specification/overview/> | 软件物料清单标准 |
| **EU CRA** | 2024/2847 | 已发布 | <https://eur-lex.europa.eu/eli/reg/2024/2847> | 欧盟网络弹性法案 |
| **NIST SP 800-161 Rev. 1** | — | 现行 | <https://csrc.nist.gov/publications/detail/sp/800-161/rev-1/final> | 供应链网络安全风险管理 |
| **NIST SP 800-204** | 系列 | 2025 更新 | <https://csrc.nist.gov/publications/detail/sp/800-204/final> | 微服务安全架构 |
| **IEC 62443-4-1** | 2018 | 现行 | <https://webstore.iec.ch/en/publication/33615> | IACS 安全产品开发生命周期要求 |
| **IEC 62443-4-2** | **2019** | 现行 | <https://webstore.iec.ch/en/publication/34421> | IACS 组件技术安全要求；**注意：不是 2025 版** |
| **IEC TS 62443-6-2** | 2025 | 已发布 | <https://webstore.iec.ch/en/publication/67463> | IACS 组件评估方法论 |

---

## 工业 IoT / OT-IT 融合

| 标准/框架 | 版本 | 状态 | 官方 URL | 备注 |
|-----------|------|------|----------|------|
| **ISA-95 / IEC 62264** | — | 现行 | <https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95> | 企业-控制系统集成 |
| **ISO/IEC 30141** | **2024** | **已发布** | <https://www.iso.org/standard/88800.html> | IoT 参考架构；**2024-08 发布，取代 2018 版** |
| **IEC 61508** | **Ed.3（CDV 投票完成，RVC 2026-05-15 发布：65A/1231~1234/RVC；IEC 官方 Fcst. Publ. Date 2026-07）** | **CDV 投票完成；TÜV Rheinland 等主要认证机构于 2026-06 起已可按 IEC 61508-3:2026 执行 SIL 2+ 认证** | <https://iec.ch/dyn/www/f?p=103:23:::::FSP_ORG_ID:1369> | 功能安全基础标准；需区分“认证机构按 61508-3:2026 执行”与“IEC 国际标准正式出版（官方预测 2026-07）” |
| **ISO 21448** | 2022 | Ed.2 修订中（ISO/AWI 21448，AWI 阶段） | <https://www.iso.org/standard/93071.html> | 预期功能安全 (SOTIF)；Ed.2 扩展覆盖 SAE L1-L5 驾驶自动化及远程用户操作/后台通信；发布时点未官宣 |
| **ISO 26262** | 2018 | 现行；Ed.3 新工作项注册（目标 ~2029） | <https://www.iso.org/standard/68383.html> | 道路车辆功能安全 |
| **IEC 63278-1** | 2023 | 已发布 | <https://webstore.iec.ch/en/publication/65628> | 资产管理壳（AAS）结构 |
| **OPC UA FX** | 1.0 (Parts 80–84) | 已发布 | <https://reference.opcfoundation.org/specs/OPC-10000-80> | 现场级通信；OPC Foundation 主站对自动化访问限制较严，规范参考页（Parts 80–84）可正常访问 |
| **IEC/IEEE 60802** | — | 草案/完善中 | <https://www.iec.ch/dyn/www/f?p=103:38:0::::::> | TSN 工业自动化配置文件 |
| **PLCopen Motion Control** | Part 1–4 + Safety | 现行 | <https://www.plcopen.org/standards/motion-control/> | 运动控制功能块 |
| **IEC 61511-1** | 2016 | 已发布（+AMD1:2017 合并版 CSV=61289；:2026 SER 系列合订=5527） | <https://webstore.iec.ch/en/publication/24241> | 过程工业安全仪表系统（SIS）功能安全 |
| **IEC 61511-2** | 2016 | 已发布 | <https://webstore.iec.ch/en/publication/25510> | IEC 61511-1 应用指南 |
| **IEC 61513** | 2011 | 已发布 | <https://webstore.iec.ch/en/publication/5532> | 核电厂安全重要仪表与控制 |
| **IEC 61131-3** | **2025** | **已发布（Ed.4，2025-05 发布，取代 2013 版）** | <https://webstore.iec.ch/en/publication/68533> | PLC 编程语言；Ed.4 纳入 UTF-8 字符串、移除 IL（指令表） |
| **IEC 62061** | 2021 | 已发布（Ed.2；另有 2021+AMD1:2024 CSV Ed.2.1） | <https://webstore.iec.ch/en/publication/59927> | 机械安全相关电气/电子/可编程控制系统功能安全 |
| **IEC 62304** | 2006 | 已发布（AMD1:2015=22790） | <https://webstore.iec.ch/en/publication/6792> | 医疗器械软件生命周期过程 |
| **IEC 61000-4-2** | 2008 | 已发布 | <https://webstore.iec.ch/en/publication/4189> | EMC 静电放电（ESD）抗扰度试验 |
| **IEC 61784-1** | 2019 | 已发布 | <https://webstore.iec.ch/en/publication/59887> | 工业通信网络配置文件 CPF 1（现场总线） |
| **IEC 61784-2** | 2019 | 已发布 | <https://webstore.iec.ch/en/publication/59888> | 工业通信网络配置文件 CPF 2（实时以太网） |
| **IEC 61499-1 / -2** | 2012 | 已发布 | <https://webstore.iec.ch/en/publication/5506> | 分布式工业过程测量与控制系统功能块（-2=5507） |
| **IEC 61360-1** | 2017 | 已发布（-7:2024=72956） | <https://webstore.iec.ch/en/publication/28560> | 部件数据元素类型规范（公共数据字典 CDD 基础） |
| **IEC 62682** | 2022 | 已发布（Ed.2） | <https://webstore.iec.ch/en/publication/65543> | 过程工业报警系统管理 |
| **IEC 63339** | 2024 | 已发布（2024-10，TC65） | <https://www.iso.org/standard/82374.html> | 智能制造统一参考模型（URMSM）；IEC 与 ISO 双标 |
| **IEC 63365** | **2022** | 已发布 | <https://webstore.iec.ch/en/publication/67436> | 数字铭牌（Digital Nameplate）；**年份订正 2024→2022** |
| **IEC 60870-5-104** | 2006 | 已发布（+AMD1:2016 CSV Ed.2.1，含 COR1:2023） | <https://webstore.iec.ch/en/publication/25035> | 电力远动传输 104 规约（TCP/IP 网络访问） |
| **IEC 60068-1** | 2013 | 已发布（Ed.7） | <https://webstore.iec.ch/en/publication/501> | 环境试验 第 1 部分：总则与指南 |

---

## AI 原生与新兴协议

| 标准/框架 | 版本 | 状态 | 官方 URL | 备注 |
|-----------|------|------|----------|------|
| **MCP** | 2025-11-25 | **现行稳定版** | <https://modelcontextprotocol.io/specification/2025-11-25> | Model Context Protocol；已捐给 Linux Foundation Agentic AI Foundation |
| **MCP** | 2026-07-28 | **Release Candidate（RC）已发布（2026-05-29）；最终版预计 2026-07-28** | <https://github.com/modelcontextprotocol/modelcontextprotocol/releases> | 协议改为 stateless，新增 Extensions 框架、Tasks、MCP Apps；引用时必须标注 RC |
| **A2A** | **v1.0.0** | **已发布** | <https://a2a-protocol.org/latest/> | Agent-to-Agent Protocol；Google Cloud Next 2026-04 GA；Signed Agent Cards / AP2 |
| **NIST AI RMF** | 1.0 | 已发布 | <https://www.nist.gov/itl/ai-risk-management-framework> | AI 风险管理框架 |
| **NIST AI 600-1** | — | 已发布（2024-07 final；DOI 解析当前不稳定） | <https://airc.nist.gov/docs/NIST.AI.600-1.GenAI-Profile.ipd.pdf> | AI RMF Generative AI Profile（生成式 AI 风险管理）；IPD PDF 可稳定访问 |
| **WebAssembly Core** | 3.0 | 已发布 | <https://webassembly.org> | W3C WebAssembly 核心规范 |
| **WASM Component Model** | — | W3C Phase 1 | <https://component-model.bytecodealliance.org/> | 跨语言组件模型 |
| **WASI** | 0.3.0 | **2026-06-11 正式发布**；Wasmtime 43+ / jco 支持 | <https://github.com/WebAssembly/WASI> | 原生 async I/O（stream/future，wasi:io 并入 Canonical ABI）；WASI 1.0 目标 2026末/2027初 |
| **DMN** | 1.5 | 2024 发布 | <https://www.omg.org/spec/DMN/1.5> | 决策模型与符号 |
| **CloudEvents** | 1.0.2 | 已发布 | <https://cloudevents.io/> | 事件数据规范 |

---

## 形式化方法与验证

| 标准/工具 | 版本 | 状态 | 官方 URL | 备注 |
|-----------|------|------|----------|------|
| **TLA+** | — | 现行 | <https://lamport.azurewebsites.net/tla/tla.html> | Leslie Lamport 时序逻辑规约 |
| **Alloy** | 6 | 现行 | <https://alloytools.org/> | MIT 约束求解建模 |
| **Coq** | — | 现行 | <https://coq.inria.fr> | 定理证明助手 |
| **Isabelle/HOL** | — | 现行 | <https://www.cl.cam.ac.uk/research/hvg/Isabelle> | 定理证明器 |
| **SPARK/Ada** | — | 现行 | <https://www.adacore.com/about-spark> | AdaCore 形式化验证工具 |
| **B Method** | — | 现行 | <https://www.atelierb.eu> | Clearsy 形式化方法 |
| **Rust** | — | 现行 | <https://www.rust-lang.org> | 类型系统内存安全 |
| **Kani** | — | 现行 | <https://github.com/model-checking/kani> | AWS Rust 模型检查器 |
| **Miri** | — | 现行 | <https://github.com/rust-lang/miri> | Rust UB 行为检测 |
| **IEEE 1012** | 2024 | 已发布 | <https://standards.ieee.org/ieee/1012/7324/> | 软件验证与确认 |

---

## 价值量化与可持续软件

| 标准/框架 | 版本 | 状态 | 官方 URL | 备注 |
|-----------|------|------|----------|------|
| **COCOMO II** | 2000.1 / 后续校准 | 现行 | <https://boehmcsse.org/tools/cocomo-models/> | 软件成本估算模型；原 USC csse.usc.edu 域名已无法解析，现改用 Boehm CSSE 官方页面 |
| **FinOps Foundation** | — | 现行 | <https://www.finops.org/> | 云成本管理框架 |
| **GSF SCI** | — | 现行；已 ISO/IEC 21031:2024 | <https://sci.greensoftware.foundation/> | 软件碳强度规范 |
| **GSF SCI for AI** | — | **2025-12 ratified**（GSF 公告 2025-12-17；SCI 方法论首个 AI 扩展规范，基于 ISO/IEC 21031:2024） | <https://greensoftware.foundation/standards/sci-ai/> | AI 系统全生命周期碳强度度量；provider/consumer 双边界责任模型 |
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
| 2026-07-11 | 更新为 v2.5（联网核对）：IEC 61508 Ed.3 状态订正为“CDV 投票完成、RVC 2026-05-15（65A/1231~1234/RVC）、IEC 官方 Fcst. Publ. Date 2026-07”，取代旧表述“预计 ~2027”；复核 DIS 42024/42042（Close of voting 40.60）、SSDF 1.2（IPD，意见截止 2026-01-30，仍 Draft）、ArchiMate 4.0（C260/W262，2026-04 发布）、MCP 2026-07-28 RC（2026-05-21 锁定，稳定版仍 2025-11-25）均与表内一致 | 自动对齐代理 |
| 2026-07-11 | 更新为 v2.6（联网核对）：ISO 21448 Ed.2 订正为“ISO/AWI 21448（AWI 阶段），现行 2022 版，发布时点未官宣”（iso.org/standard/93071），取代“预计 2026 发布”；WASI 0.3.0 订正为“已发布（2026-06-11，Preview 3）”，取代“2026-02 preview”；复核 IEC/IEEE 60802:2026（2026-06 发布）、IEC 63278-2 CDV（65/1193，投票截止 2026-08-07）、ISO/IEC 26566:2026（81437，2026-05 发布）、SysML v2.0/KerML 1.0（OMG formal/2026-03，已提交 ISO）、EU CRA 2024/2847（2026-09-11 漏洞报告义务生效、2027-12-11 全面适用）、OWASP Top 10 for Agentic Applications 2026（2025-12-09 发布）与 OWASP MCP Top 10（MCP01:2025–MCP10:2025，Phase 3 Beta）均与表内一致 | 自动对齐代理 |
| 2026-07-11 | 更新为 v2.7（联网核对）：GSF SCI for AI 订正为 2025-12 ratified（GSF 公告 2025-12-17，基于 ISO/IEC 21031:2024）；ISO/IEC 21838 系列补全为 -1:2021/-2:2021(BFO)/-3:2023(DOLCE)/-4:2023(TUpper)，-5(UFO) 2025-12 进入 DIS；复核 OMG RAS v2.2（2005-11）、FAIR4RS v1.0（2022-06 RDA 批准）、CNCF Platform Engineering Maturity Model（2023-11 首版，无 v1.0 编号）、Microsoft Agent Governance Toolkit（2026-04-02 开源）、OSPS Baseline v2026.02.19、OPC UA FX Part 80-84 v1.00.03（2026-05-23）、ISO/IEC/IEEE 12207:2026（2026-04-29 发布）、ISO/IEC 25010:2023（现行）均一致 | 自动对齐代理 |
| 2026-07-11 | 更新为 v2.8（iso.org 全表链接实测复核，Mozilla UA 直连成功，23 条中 4 条纠错）：ISO/IEC 21838 链接 74307（实为 ISO 17889-2 瓷砖）→ 71954（-1:2021）；ISO/IEC/IEEE 42010 链接 74296（实为 ISO/IEC 22989:2022）→ 74393；ISO/IEC 25010 链接 78175（实为 ISO/IEC 25002:2024）→ 78176；ISO/IEC 26580 链接 71883（实为 ISO 10204 铁矿石）→ 43139；ISO/IEC 26564 链接 81622（实为 ISO/TS 24560-1 医疗）→ 43123；ISO/IEC 26565/26566（81436/81437）、26550（69529）复核确认 | 自动对齐代理 |
| 2026-07-11 | 更新为 v2.9（IEC webstore 直连实测，16 条工业自动化标准补全 publication 号，全部经 `<title>` 实测确认）：IEC 61511-1:2016=24241（+AMD1:2017 CSV=61289、-2:2016=25510、:2026 SER 系列合订=5527）、IEC 61513:2011=5532、IEC 61131-3:2025 Ed.4=68533（2025-05 发布，UTF-8 字符串纳入、IL 移除，取代 2013 版）、IEC 62061:2021=59927、IEC 62304:2006=6792（AMD1:2015=22790）、IEC 61000-4-2:2008=4189、IEC 61784-1/-2:2019=59887/59888、IEC 61499-1/-2:2012=5506/5507、IEC 61360-1:2017=28560（-7:2024=72956）、IEC 62682:2022=65543、IEC 63339:2024=iso.org/standard/82374、IEC 63365 年份订正 2024→2022（=67436）、IEC 60870-5-104:2006+AMD1:2016 CSV=25035、IEC 60068-1:2013=501 | 自动对齐代理 |

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
