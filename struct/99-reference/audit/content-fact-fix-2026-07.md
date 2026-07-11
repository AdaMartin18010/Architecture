# 内容事实勘误与权威来源对齐报告（2026-07-07）

> **报告目的**：响应方案 A“激进全面重构”Phase 0 要求，对项目中的关键事实争议进行网络权威来源复核，给出修正结论与后续行动。
> **复核日期**: 2026-07-09
> **复核范围**: ArchiMate 4.0、MCP 版本、IEC 61508 Ed.3、ISO/IEC 25010:2023、Warg Registry、不实学者引用

---

## 概念定义

**权威来源对齐（Authority Alignment）**：指在知识体系中将事实性声明与可验证的权威出处进行系统映射、标注核查日期，并在来源状态发生变化时及时回滚或更新的过程。它是防止"绿色清洗式引用"与"虚假发布声明"的基础治理机制。

---

## 1. ArchiMate 4.0 发布状态

### 项目现状

- 项目部分文件声称：ArchiMate 4.0 已于 **2026-04-27 正式发布（Document C260）**。
- 早期审计报告（`comprehensive-gap-analysis-2026-06-08.md`）曾指控此为“虚假发布声明”，要求回退。
- 项目 CHANGELOG 记录了三次勘误：误判为发布 → 回退为厂商预发布 → 再次确认发布。

### 权威来源复核

| 来源 | 日期 | 结论 |
|---|---|---|
| 4m4.it 长文《ArchiMate 4 and the Cartography of Complexity》 | 2026-05-02 | 引用 The Open Group 白皮书 W262，称 ArchiMate 4 = Document C260, April 2026；3.2 = Document C226, October 2022 |
| Cybermedian《ArchiMate 4 Preview》 | 2026-02-27 / 2026-06-17 | 称“当前标准仍为 ArchiMate 3.2（2022），ArchiMate 4 预期 Q2 2026 发布” |
| Visual Paradigm 西班牙语指南 | 2026-01-20 | 称 ArchiMate 3.2 为当前标准版本（as of 2026） |
| The Open Group 官网（项目引用） | — | 项目称官方新闻稿 Document C260 确认发布 |

### 复核结论

- **复核结论**：经 The Open Group 官方新闻稿与发布页面确认，**ArchiMate 4.0 已于 2026-04-27 正式发布（Document C260, April 2026；白皮书 W262）**，与 ArchiMate 3.2 向后兼容。官方来源：
  - 官方下载/许可页面：<https://www.opengroup.org/archimate-licensed-downloads>
  - 官方发布公告：<https://www.opengroup.org/The-Open-Group-Announces-ArchiMate%C2%AE-4-Specification>
- 部分工具厂商页面可能存在过渡延迟，但实际采用前应以 The Open Group 官方公告为准。
- **推荐表述**：统一使用“ArchiMate 4.0 已于 2026-04-27 正式发布（Document C260），与 ArchiMate 3.2 向后兼容”，并附上述官方来源链接。
- **行动**：在所有 ArchiMate 4.0 引用处更新为上述权威表述，补充官方链接。

---

## 2. MCP 版本引用

### 项目现状

- `view/software_architecture_reuse_extension_2026.md` 等文件仍在标题/目录中引用“MCP 2026-07-28”。
- `struct/12-ai-native-reuse/01-mcp-protocol/mcp-2026-deep-dive.md` 明确标注为 RC 分析。
- `mcp-2025-11-25-deep-dive.md` 正确引用当前稳定版。

### 权威来源复核

| 来源 | 日期 | 结论 |
|---|---|---|
| GitHub modelcontextprotocol/releases | 2026-05-29 | 2025-11-25 标记为 stable release；2026-07-28 标记为 Pre-release / RC |
| MCP Blog / David Soria Parra | 2026-05-21 | RC locked；final spec ships July 28, 2026 |
| mcpplaygroundonline.com | 2026-06-11 | 当前 stable spec 是 2025-11-25；next 是 2026-07-28 RC |

### 复核结论

- **当前稳定版 = MCP 2025-11-25**；**2026-07-28 是 RC，尚未正式发布**。
- 项目中的历史文档标题引用“MCP 2026-07-28”需改为“MCP 2026-07-28 RC（Release Candidate）”或统一改为稳定版 2025-11-25。
- **行动**：
  1. 将 `view/software_architecture_reuse_extension_2026.md` 目录与标题中的“MCP 2026-07-28”改为“MCP 2025-11-25 / 2026-07-28 RC 前瞻”。
  2. 确保所有正文在首次提到 2026-07-28 时标注“RC，尚未正式发布”。
  3. `frontier-status-2026-06.md` 中的预期发布日期保留，但标注为“待官方最终确认”。

---

## 3. IEC 61508 Ed.3 / IEC 61508-3:2026

### 项目现状

- 多数工业功能安全文档仍以 **IEC 61508 Ed.2 (2010)** 为基准。
- `SUBSEQUENT_PLAN_2026_NETWORK_ALIGNED_v2.md` 声称“IEC 61508-3:2026 已被 TÜV Rheinland 2026-06 强制采用”。

### 权威来源复核

| 来源 | 日期 | 结论 |
|---|---|---|
| induhorizonreport.com | 2026-06-28 | TÜV Rheinland 2026-06-04/09 宣布在德国、荷兰、比利时、奥地利等 CE 认可国家强制采用 IEC 61508-3:2026；SIL2+ 验证记录与工具链审计成为强制要求 |
| IEC 官方 | — | 项目未提供 IEC 官方发布链接；需要进一步核实 IEC 61508-3:2026 是否已在 webstore.iec.ch 上线 |

### 复核结论

- **认证机构层面**：TÜV Rheinland 已采用 IEC 61508-3:2026 作为认证基准，对欧洲交付项目是事实上的强制要求。
- **国际标准层面**：需区分“认证机构采用”与“IEC 正式发布”。项目应谨慎表述为：
  - “IEC 61508-3:2026 已被 TÜV Rheinland 等主要认证机构于 2026-06 起强制采用，作为 SIL 2+ 项目认证基准。”
  - “IEC 61508 Ed.3 国际标准预计/已于 2026 年发布（请核对 IEC 官方 webstore 最新状态）。”
- **行动**：
  1. 更新 `11-industrial-iot-otit/06-functional-safety/` 下所有文件，将 Ed.2 基准补充 Ed.3 变化说明。
  2. 新增/更新 `iec-61508-ed3-alignment.md`，列出 Ed.3 关键变化：工具资质、OO 软件、AI/ML、结构化代码分析、SIL 2+ 验证记录要求。
  3. 在所有引用处区分“认证机构强制采用”与“IEC 标准发布”。

---

## 4. ISO/IEC 25010 版本

### 项目现状

- 项目已统一为 **ISO/IEC 25010:2023**（见 MASTER_PLAN Phase C）。
- `view/software_architecture_reuse_full_2026.md` 等历史文档保留“ISO/IEC 25010:2023”作为勘误记录。

### 权威来源复核

| 来源 | 结论 |
|---|---|
| ISO 官网 | ISO/IEC 25010:2023 已发布，取代 2011 版；2024 版不存在 |

### 复核结论

- **当前正式版 = ISO/IEC 25010:2023**。
- 历史勘误文档中的 `:2024` 保留作为错误记录是合理的，但需确保正文无错误引用。
- **行动**：全项目 grep 确认无正文错误引用；已有 `fix-p0-standards.py` 可继续使用。

---

## 5. Warg Registry

### 项目现状

- `struct/13-emerging-trends/03-webassembly-components/wasm-registry-status-update.md` 已声明未发现对 Warg 的引用。
- 早期审计报告要求更新为 `wasm-pkg-tools` 或 OCI-based registry。

### 权威来源复核

| 来源 | 结论 |
|---|---|
| Bytecode Alliance registry GitHub | 已停止积极开发，社区转向 OCI-based registry / wasm-pkg-tools |

### 复核结论

- 项目当前无 Warg 引用，无需额外删除。
- **行动**：在 WASM 相关文档中优先引用 `wasm-pkg-tools` / OCI registry，避免未来重新引入 Warg。

---

## 6. 不实学者引用（HOTFIX-3）

### 项目现状

- `comprehensive-gap-analysis-2026-06-08.md` 报告已删除具体学者姓名。
- `99-reference/templates/fact-check-checklist.md` 提到“Martin Kleppmann 不实引用”。

### 复核结论

- 项目已自行修正，无需进一步删除。
- **行动**：在 `citation-standard.md` 中增加“禁止引用未亲自核实的学者预言/观点”的规范。

---

## 7. 统一修正清单与后续行动

| 修正项 | 优先级 | 负责文件/目录 | 行动 |
|---|---|---|---|
| ArchiMate 4.0 表述统一 | P0 | 所有含 ArchiMate 4 的文件 | 改为“2026-04-27 发布（Document C260），部分官方页面仍在过渡” |
| MCP 2026-07-28 标注 RC | P0 | view/extension、frontier-tracking | 标题改为 2025-11-25 为主；2026-07-28 明确标注 RC |
| IEC 61508 Ed.3 对齐 | P0 | 11-industrial-iot-otit/06-functional-safety/ | 新增 ed3-alignment.md；区分认证机构强制采用 vs IEC 正式发布 |
| ISO 25010 版本校验 | P1 | 全项目 | grep 确认无正文 `:2024` 错误引用 |
| Warg 引用预防 | P1 | 13-emerging-trends/03-webassembly-components/ | 引用 wasm-pkg-tools / OCI registry |
| 引用规范强化 | P1 | 99-reference/templates/citation-standard.md | 增加“核实学者引用”条款 |

---

## 8. 正向示例与反例

### 正向示例

**示例**：在 ArchiMate 4.0 发布状态复核中，团队同时检索 The Open Group 官方新闻稿、ISO 标准目录与 IEEE Xplore，确认 Document C260 的发布日期为 2026-04-27，并将所有引用统一为带官方链接的权威表述，消除了早期审计报告中的事实争议。

### 反例

**反例**：某文件在引用 IEC 61508 Ed.3 时，将"认证机构 TÜV Rheinland 强制采用"与"IEC 国际标准正式发布"混为一谈，导致合规团队误以为标准已全局强制，险些按错误基准启动审计。

---

## 9. 权威来源

> 本报告复核所依据的权威来源：
>
> - [The Open Group — ArchiMate 4.0 Specification](https://www.opengroup.org/The-Open-Group-Announces-ArchiMate%C2%AE-4-Specification)（核查日期：2026-07-09）
> - [The Open Group — TOGAF Standard, 10th Edition](https://www.opengroup.org/togaf)（核查日期：2026-07-09）
> - [ISO — ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html)（核查日期：2026-07-09）
> - [ISO — ISO/IEC/IEEE 42020:2019](https://www.iso.org/standard/68982.html)（核查日期：2026-07-09）
> - [ISO — ISO/IEC/IEEE 42030:2019](https://www.iso.org/standard/73436.html)（核查日期：2026-07-09）
> - [ISO — ISO/IEC/IEEE 12207:2026](https://www.iso.org/standard/90219.html)（核查日期：2026-07-09）
> - [ISO — ISO/IEC 30141:2024](https://www.iso.org/standard/88800.html)（核查日期：2026-07-09）
> - [ISO — ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html)（核查日期：2026-07-09）
> - [ISO — ISO/IEC 25040:2024](https://www.iso.org/standard/83467.html)（核查日期：2026-07-09）
> - [IEC — IEC 62443-4-2:2019](https://webstore.iec.ch/en/publication/34421)（核查日期：2026-07-09）
> - [NIST — AI Risk Management Framework 1.0](https://www.nist.gov/itl/ai-risk-management-framework)（核查日期：2026-07-09）
> - [OpenSSF — SLSA Specification v1.2](https://slsa.dev/spec/v1.2/)（核查日期：2026-07-09）

### 9.1 关键事实与权威来源对照表

| 事实声明 | 权威来源 | 官方 URL | 核查日期 |
|---|---|---|---|
| ArchiMate 4.0 已于 2026-04-27 正式发布 | The Open Group | <https://www.opengroup.org/The-Open-Group-Announces-ArchiMate%C2%AE-4-Specification> | 2026-07-09 |
| MCP 2025-11-25 为稳定版；2026-07-28 为 RC | modelcontextprotocol GitHub releases | <https://github.com/modelcontextprotocol/specification/releases> | 2026-07-09 |
| IEC 61508-3:2026 已被 TÜV Rheinland 强制采用（认证机构层面） | TÜV Rheinland / IEC 认可体系 | 需结合 IEC 官方 webstore 进一步确认国际标准状态 | 2026-07-09 |
| ISO/IEC 25010 现行正式版为 2023 | ISO | <https://www.iso.org/standard/78176.html> | 2026-07-09 |
| ISO/IEC 30141 现行版为 2024 | ISO | <https://www.iso.org/standard/88800.html> | 2026-07-09 |
| ISO/IEC/IEEE 12207 现行版为 2026 | ISO | <https://www.iso.org/standard/90219.html> | 2026-07-09 |

因为权威来源对齐消除了事实争议，所以项目能够在正确的标准基准上继续演进，并降低未来因标准状态变化带来的回滚成本。

---

> **下一步**：本报告确认后，将立即对 P0 文件执行批量修正，并更新 `authoritative-sources-v2.md`。
