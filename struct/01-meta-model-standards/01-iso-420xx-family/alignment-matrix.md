# 核心标准对齐矩阵

> **版本**: 2026-06-06
> **定位**: 将本知识体系的 13 个主题与权威国际标准对齐

---

## 1. 标准族谱

```text
ISO/IEC/IEEE 42010:2022 (架构描述)
        │
        ├── ISO/IEC/IEEE 42020:2019 (架构过程)
        ├── ISO/IEC/IEEE 42030:2019 (架构评估)
        ├── ISO/IEC 25010:2024 (产品质量模型)
        ├── ISO/IEC 26550:2015 (产品线工程)
        └── ISO/IEC/IEEE 15289:2019 (信息项)

TOGAF 10 (企业架构) ──→ ArchiMate 3.2/4.0 (架构建模语言)

SLSA 1.2 (供应链安全)
        │
        ├── SPDX ISO/IEC 5962
        ├── CycloneDX OWASP
        ├── SWID ISO/IEC 19770-2
        └── in-toto

IEC 63278 (AAS) 系列
        │
        ├── IEC 63278-1:2023 (AAS 结构)
        ├── IEC 63278-2 (元模型，开发中)
        ├── IEC 63278-3 (安全，开发中)
        ├── IEC 63278-4 (用例，开发中)
        ├── IEC 63278-5 (接口，规划中)
        └── OPC UA FX (Parts 80-84)

MCP 2025-11-25 / A2A v1.0 (AI 原生协议)
        │
        ├── Linux Foundation Agentic AI Foundation
        ├── OAuth 2.1 (RFC 9728, RFC 8707)
        └── OWASP LLM/MCP/Agentic AI Top 10
```

---

## 2. 主题-标准对齐矩阵

| 主题 | 核心标准 | 辅助标准 | 状态 |
|------|---------|---------|------|
| 01 元模型与标准 | ISO 42010:2022, ISO 25010:2024, ISO 26550 | TOGAF 10, ArchiMate, SWEBOK V4 | ✅ 已对齐 |
| 02 业务架构 | TOGAF 10, ArchiMate BPMN, DMN, FEA | ISO 42010, BRM | ✅ 已对齐 |
| 03 应用架构 | TOGAF 10, ArchiMate ISO 25010 | OpenAPI, AsyncAPI | ✅ 已对齐 |
| 04 组件架构 | ISO 26550, UML | GoF, SemVer, SBOM | ✅ 已对齐 |
| 05 功能架构 | ISO 25010, SWEBOK | BPMN, DMN | ✅ 已对齐 |
| 06 跨层治理 | COBIT, ITIL, ISO 330xx | FinOps, CMMI | ✅ 已对齐 |
| 07 形式化验证 | TLA+, Alloy, Coq, Isabelle | SPARK Ada, B Method, RustBelt | ✅ 已对齐 |
| 08 认知架构 | ACT-R, BDI, Cognitive Load Theory | AI 认知增强 | ✅ 已对齐 |
| 09 价值量化 | COCOMO II, ROI/NPV | FinOps, Strategic Value | ✅ 已对齐 |
| 10 供应链安全 | SLSA 1.2, NIST SSDF 1.2, EU CRA | SPDX, CycloneDX, SWID, in-toto | ✅ 已对齐 |
| 11 工业 IoT | IEC 63278, OPC UA FX, ISA-95 | IEC 61508, ISO 26262, IEC/IEEE 60802 | ✅ 已对齐 |
| 12 AI 原生复用 | MCP 2025-11-25, A2A v1.0 | OWASP LLM/MCP/Agentic AI | ✅ 已对齐 |
| 13 新兴趋势 | Platform Engineering, WebAssembly | RegTech AI, Rust Ecosystem | ✅ 已对齐 |

---

## 3. ISO 42010:2022 术语更新

> 2022 版关键术语变更：

| 2011 版 | 2022 版 | 说明 |
|---------|---------|------|
| System of Interest | **Entity of Interest (EoI)** | 扩展至非系统架构 |
| Architecture Framework | **Architecture Description Framework (ADF)** | 与评估框架区分 |
| Architecture Model | **Architecture View Component** | 更准确反映实践 |
| - | **Architecture Aspect** | 新增：架构方面 |
| - | **Stakeholder Perspective** | 新增：利益相关者视角 |
| - | **Architecture Description Element** | 新增：AD 元素 |

---

## 4. ISO 25010:2024 质量特性

| 特性 | 旧版名称 | 状态 |
|------|---------|------|
| Functional Suitability | 保持不变 | ✅ |
| Performance Efficiency | 保持不变 | ✅ |
| Compatibility | 保持不变 | ✅ |
| **Interaction Capability** | 替代 Usability | 🆕 |
| Reliability | 保持不变 | ✅ |
| Security | 保持不变 | ✅ |
| Maintainability | 保持不变 | ✅ |
| **Flexibility** | 替代 Portability | 🆕 |
| **Safety** | 新增 | 🆕 |

---

## 5. SLSA 1.2 轨道模型

| 轨道 | 等级 | 关键要求 |
|------|------|---------|
| Build Track | L1-L4 | Provenance → Hosted Build → Hardened → Reproducible |
| Source Track | L1-L3 | Version Control → Authenticated History → Two-Person Review |
| Attested Build Environments | L1+ | 构建环境认证 |

---

## 6. MCP 2025-11-25 vs A2A v1.0

| 维度 | MCP 2025-11-25 | A2A v1.0 |
|------|---------------|---------|
| 范围 | Agent ↔ Tool | Agent ↔ Agent |
| 关系 | Client-Server (Stateful) | Peer-to-Peer |
| 发现 | Server lists capabilities | Agent Card (/.well-known/agent.json) |
| 核心对象 | Tools, Resources, Prompts | Agent Card, Tasks, Messages, Artifacts |
| 流式 | Streamable HTTP / SSE | SSE |
| 认证 | OAuth 2.1 (RFC 9728/8707) | OAuth 2.1 + PKCE |
| 治理 | Linux Foundation AAIF | Linux Foundation |

---

> 最后更新: 2026-06-06
> 注意: 本矩阵将随标准更新持续维护。
