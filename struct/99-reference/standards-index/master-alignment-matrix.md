# 国际标准对齐多维总矩阵

> **版本**: 2026-06-06
> **定位**: 全体系的国际标准、框架、建模语言、质量度量、过程标准的交叉映射总表
> **维护**: 每季度对照 ISO/OMG/IEEE 官网更新一次

---

## 矩阵 A：复用层次 × 标准族

| 复用层次 | 核心标准 | 辅助标准 | 架构框架 | 建模语言 | 质量度量 | 过程标准 | 协议/接口 | 2026 新增 |
|----------|----------|----------|----------|----------|----------|----------|-----------|-----------|
| **元模型** | ISO/IEC/IEEE 42010:2022 | ISO 24765, ISO 15288 | TOGAF 10, Zachman | ArchiMate 3.2+ | ISO 25010 | ISO/IEC/IEEE 42020 | N/A | DIS 42024/42042 |
| **业务** | FEA BRM 2.0 | ISO 15288, BPMN 2.0 | TOGAF Phase B | ArchiMate Business, BPMN | ISO 25010 | 42020 | REST/GraphQL | DMN 1.5 |
| **应用** | FEA ARM/SRM | ISO 26550, C4 | TOGAF Phase C/D | ArchiMate Application | ISO 25010 | 42020/1517 | gRPC/REST/Gateway API | Service Mesh, WASM, TOSCA v2.0 |
| **组件** | ISO 26566:2026 | IEEE 1517, C4, OWASP SCVS | arc42, C4 | UML Component | NASA RRL | 42020/12207 | FFI/WIT/Bindgen | WASM Component Model, WASI 0.3, SBOM |
| **功能** | IEEE 1517 | ISO 25010, COCOMO II | Serverless, Temporal | 代码/流程图/决策表/BPMN | 复用率/覆盖率 | 12207/15504 | MCP/A2A/DMN | MCP 2025-11-25, A2A v1.0, DMN 1.5 |
| **治理** | ISO 26566:2026 | RiSE/RCMM, FinOps, CMMI | TOGAF ADM | 成熟度模型 | ISO 26564:2022 | 42030 | OPA/Gatekeeper | Agentic Governance, Cloud Unit Economics |
| **安全** | SLSA 1.2 | NIST SSDF 1.2, OWASP SCVS | 零信任架构 | 攻击树、威胁模型 | CVSS/EPSS | ISO 27034, EU CRA | Sigstore/cosign | SLSA Multi-Track, Agentic AI Security |
| **工业** | ISA-95 / IEC 62264 | IEC 61508 Ed3, ISO 26262:2025 | RAMI 4.0 | UML, IEC 63278 AAS, PLCopen | SIL/ASIL | IEC 61508 lifecycle | OPC UA FX, TSN, Safe Motion | OPC UA FX 1.0, TinyML, Edge AI |

---

## 矩阵 B：标准 × 主题覆盖度

| 标准/框架 | 元模型 | 业务 | 应用 | 组件 | 功能 | 治理 | 安全 | 工业 |
|-----------|--------|------|------|------|------|------|------|------|
| **ISO 42010:2022** | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | ☆☆☆☆☆ | ★★☆☆☆ |
| **TOGAF 10** | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★☆☆ | ★★☆☆☆ | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ |
| **ArchiMate 3.2+** | ★★★☆☆ | ★★★★★ | ★★★★★ | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | ☆☆☆☆☆ | ★★★☆☆ |
| **ISO 26550:2015** | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | ★★★☆☆ | ★★★☆☆ | ☆☆☆☆☆ | ★★★☆☆ |
| **ISO 26566:2026** | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★★★★ | ☆☆☆☆☆ | ★★☆☆☆ |
| **IEEE 1517** | ★★☆☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | ★★★☆☆ | ☆☆☆☆☆ | ★★☆☆☆ |
| **FEA 2.0** | ★★★☆☆ | ★★★★★ | ★★★★☆ | ★★☆☆☆ | ☆☆☆☆☆ | ★★★☆☆ | ☆☆☆☆☆ | ☆☆☆☆☆ |
| **BPMN 2.0** | ★★☆☆☆ | ★★★★★ | ★★★☆☆ | ☆☆☆☆☆ | ★★★★☆ | ★★☆☆☆ | ☆☆☆☆☆ | ★★★☆☆ |
| **DMN 1.5** | ★★☆☆☆ | ★★★★☆ | ★★★☆☆ | ☆☆☆☆☆ | ★★★★★ | ★★☆☆☆ | ☆☆☆☆☆ | ★★☆☆☆ |
| **SLSA 1.2** | ☆☆☆☆☆ | ☆☆☆☆☆ | ☆☆☆☆☆ | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★☆☆ |
| **ISA-95 / IEC 62264** | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★★★ |
| **IEC 61508** | ★★☆☆☆ | ☆☆☆☆☆ | ★★☆☆☆ | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★★★ |

---

## 矩阵 C：术语映射（跨标准概念对齐）

| 本体系概念 | ISO 42010:2022 | TOGAF 10 | ArchiMate 3.2+ | ISO 26550:2015 | ISA-95 |
|-----------|---------------|----------|----------------|----------------|--------|
| **架构描述** | Architecture Description (AD) | Architecture Repository / ADM 产物 | Architecture View / Model | Product Line Asset Documentation | Operations Definition |
| **视点** | Viewpoint | Architecture Viewpoint | Viewpoint | Stakeholder Concern View | Functional Hierarchy |
| **视图** | View | Architecture View | View | Architecture Description View | Operations Schedule |
| **复用单元** | Model (in Model Library) | Building Block (ABB/SBB) | Element / Building Block | Domain Asset / Core Asset | Segment / Resource |
| **共性/变性** | Concern / Viewpoint customization | Architecture Continuum variability | Element specialization | Commonality / Variability | Product Segment / Master Recipe |
| **接口契约** | Correspondence Rule | Interface Catalog | Relationship / Serving | Asset Interface | Exchange Framework |
| **生命周期** | Architecture Description lifecycle | ADM Cycle | Architecture Development Cycle | Domain Engineering + Application Engineering | Operations Lifecycle |

---

## 矩阵 D：2026 标准更新追踪

| 标准 | 当前状态 | 预期更新 | 对体系的影响 | 跟踪责任人 |
|------|---------|---------|-------------|-----------|
| ISO/IEC/IEEE DIS 42024 | 草案 | 预计 2026-2027 发布 | 元模型层定义需更新 | TBD |
| ISO/IEC/IEEE DIS 42042 | 草案 | 预计 2026-2027 发布 | 参考架构规范补充 | TBD |
| ArchiMate 4.0 Snapshot 1 | 快照 | 预计 2026 Q2 发布 | Dynamic Connection, AI 资产类别 | TBD |
| MCP 2025-11-25 | 稳定版 | Linux Foundation 管理 | 功能层 AI 协议基线 | TBD |
| A2A v1.0 | 已发布 (Cloud Next 2026-04) | v1.1 预计 2026 H2 | Agent 安全签名增强 | TBD |
| OPC UA FX 1.0 | Parts 80-84 发布 | C2D/D2D 完善中 | 工业现场层复用 | TBD |
| SLSA 2.0 | 讨论中 | 预计 2027 | 供应链安全框架升级 | TBD |
| WASI 1.0 | 预期 2026 底–2027 初 | WASI 0.3 2026-02 | WASM 跨平台组件复用 | TBD |
| PLCopen Motion Part 4 | 2025 发布 | Coordinated Motion 完善 | 机器人-PLC 统一控制 | TBD |
| ISO 26262:2025 | 草案/已发布 | ML/V2X/车云协同 | 汽车软件 SEooC 复用 | TBD |
| IEC 61508 Ed3 | 预期发布 | 与 ISO 26262 对齐 | 功能安全跨域复用 | TBD |
| OASIS TOSCA v2.0 | 2025-09 OASIS 标准 | IoT/边缘/过程自动化扩展 | 应用拓扑跨域编排 | TBD |
| Gateway API / GAMMA | 稳定 / SIG Network | 替代 Ingress 与服务网格 API | K8s 原生流量管理复用 | TBD |
| DMN 1.5 | 2024 OMG 发布 | 与 BPMN 深度集成 | 业务决策服务化复用 | TBD |
| NIST SP 800-161r1 | 现行 | 供应链风险管理 | 开源组件安全治理 | TBD |
| NIST SP 800-204 系列 | 2025 更新 | DevSecOps + 供应链集成 | 微服务安全架构复用 | TBD |

---

## 使用说明

1. **设计时**: 查阅"矩阵 A"确定当前设计层次应使用的标准组合
2. **概念转换时**: 查阅"矩阵 C"进行跨标准术语翻译
3. **年度审查时**: 查阅"矩阵 D"更新标准状态
4. **评估时**: 查阅"矩阵 B"确定某标准在目标主题中的适用度

---

> 最后更新: 2026-06-06
