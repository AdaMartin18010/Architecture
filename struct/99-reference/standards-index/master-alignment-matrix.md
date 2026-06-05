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
| **应用** | FEA ARM/SRM | ISO 26550, C4 | TOGAF Phase C/D | ArchiMate Application | ISO 25010 | 42020/1517 | gRPC/REST | Service Mesh, WASM |
| **组件** | ISO 26566:2026 | IEEE 1517, C4 | arc42, C4 | UML Component | NASA RRL | 42020/12207 | FFI/WIT/Bindgen | WASM Component Model |
| **功能** | IEEE 1517 | ISO 25010 | Serverless, Temporal | 代码/流程图/决策表 | 复用率/覆盖率 | 12207/15504 | MCP/A2A | MCP 2026-07-28 |
| **治理** | ISO 26566:2026 | RiSE/RCMM | TOGAF ADM | 成熟度模型 | ISO 26564:2022 | 42030 | OPA/Gatekeeper | Agentic Governance |
| **安全** | SLSA 1.0 | NIST SSDF, OWASP SCVS | 零信任架构 | 攻击树、威胁模型 | CVSS/EPSS | ISO 27034 | Sigstore/cosign | SLSA L4 分布式构建 |
| **工业** | ISA-95 / IEC 62264 | IEC 61508, ISO 26262 | RAMI 4.0 | UML, IEC 63278 AAS | SIL/ASIL | IEC 61508 lifecycle | OPC UA FX, TSN | OPC UA FX 1.0 (2026) |

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
| **SLSA 1.0** | ☆☆☆☆☆ | ☆☆☆☆☆ | ☆☆☆☆☆ | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★☆☆ |
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
| MCP 2026-07-28 | RC | 2026-07-28 正式发布 | 功能层 AI 协议更新 | TBD |
| A2A v1.0.0 | 已发布 | v1.1 预计 2026 H2 | Agent 安全签名增强 | TBD |
| OPC UA FX 1.0 | 部分发布 | C2D/D2D 2026-2027 | 工业现场层复用 | TBD |
| SLSA 2.0 | 讨论中 | 预计 2027 | 供应链安全框架升级 | TBD |

---

## 使用说明

1. **设计时**: 查阅"矩阵 A"确定当前设计层次应使用的标准组合
2. **概念转换时**: 查阅"矩阵 C"进行跨标准术语翻译
3. **年度审查时**: 查阅"矩阵 D"更新标准状态
4. **评估时**: 查阅"矩阵 B"确定某标准在目标主题中的适用度

---

> 最后更新: 2026-06-06
