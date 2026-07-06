# 99 参考索引

> **版本**: 2026-06-06
> **定位**: 全知识库的参考索引、术语表、可视化资源与外部链接汇总

---

## 子目录导航

| 目录 | 内容 |
|------|------|
| `glossary/` | 术语表、同义词对照、跨标准术语映射、公理-定理推理树 |
| `visualizations/` | Mermaid 图、架构图、概念映射、标准族谱图 |
| `external-links/` | 外部权威资源链接（按主题分类） |
| `templates/` | 文档模板、快速参考卡、检查清单、评估问卷 |

---

## 快速参考

### 标准索引

| 标准 | 主题 | 状态 |
|------|------|------|
| ISO/IEC/IEEE 42010 | 01-元模型与标准对齐 | ✅ 已对齐 |
| ISO/IEC 25010 | 01-元模型与标准对齐 | ✅ 已对齐 |
| ISO/IEC 26550 | 01-元模型与标准对齐 | ✅ 已对齐 |
| TOGAF 10 | 01-元模型与标准对齐 | ✅ 已对齐 |
| ArchiMate 3.2/4.0 | 01-元模型与标准对齐 | ✅ 已对齐 |
| ISO/IEC 5962 (SPDX) | 10-供应链安全 | ✅ 已对齐 |
| SLSA 1.0 | 10-供应链安全 | ✅ 已对齐 |
| IEC 63278 (AAS) | 11-工业 IoT | ✅ 已对齐 |
| OPC UA FX 1.0 | 11-工业 IoT | ✅ 已对齐 |
| IEC 61508 / ISO 26262 | 11-工业 IoT | ✅ 已对齐 |
| TLA+, Alloy, Coq | 07-形式化验证 | ✅ 已对齐 |
| MCP 2025-11-25 | 12-AI 原生复用 | ✅ 已对齐 |
| A2A v1.0 | 12-AI 原生复用 | ✅ 已对齐 |

### 公理-定理索引

完整列表参见 [`glossary/axiom-theorem-tree.md`](./glossary/axiom-theorem-tree.md)。

### 关键外部资源

- [ISO 42010:2022](https://www.iso.org/standard/74296.html)
- [SLSA Specification](https://slsa.dev/spec/v1.0/)
- [CycloneDX Specification](https://cyclonedx.org/specification/overview/)
- [SPDX Specification](https://spdx.dev/use/specifications/)
- [OPC Foundation](https://opcfoundation.org/)
- [IDTA - AAS Specifications](https://industrialdigitaltwin.org/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [A2A Protocol](https://a2aprotocol.ai/)

---

## 维护规则

1. 每新增一个公理/定理，必须在 `glossary/axiom-theorem-tree.md` 中登记
2. 每新增一个外部标准引用，必须在本 README 的标准索引中更新
3. 每新增一个可视化图表，必须上传至 `visualizations/` 并在相关主题 README 中引用

## 当前状态

- [x] 术语查询脚本 (Python CLI) (`tools/terminology-query.py`)
- [x] 形式化验证 Docker 环境 (`tools/formal-verification-env/`)
- [x] 公理-定理推理树 (`glossary/axiom-theorem-tree.md`)
- [x] 跨主题综合索引 (`glossary/cross-topic-index.md`)

---

> 最后更新: 2026-06-08


---

## 补充说明：99 参考索引

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
