# view/ — 卷册视图层

> **定位**: `view/` 是 `struct/` 的**派生卷册层**，不是内容真源。本目录包含 14 个现役聚合卷册（自动生成，禁止手改）与 `_HISTORICAL_/` 下的 8 个 2026-06 只读历史快照。
> **真源**: `struct/` 是当前结构化知识体系的唯一真源；本目录与 `struct/` 冲突时一律以 `struct/` 为准。
> **同步**: 现役卷册由 `scripts/sync-view-from-struct.py` 按**内容哈希**自动生成（当前 14/14 一致，差异见 `reports/view-diff-report.md`）。
> **核查日期**: 2026-07-12

---

## 1. 概念定义：什么是卷册视图

**卷册视图（Volume View）**是把 `struct/` 某一一级主题下的全部结构化文档，按原主题顺序聚合成一份长文档 `volume-NN-主题名.md`，用于一次性通读、讲义输出与书籍分卷。它与 `struct/` 的关系是"派生—真源"关系：卷册内容由脚本从 `struct/` 重新生成，因此卷册内不积累独立修订。

## 2. 目录构成与映射矩阵

| 区域 | 文件 | 性质 | 维护方式 |
| ---- | ---- | ---- | ---- |
| 现役卷册 | `volume-01-meta-model-standards.md` ~ `volume-13-emerging-trends.md` + `volume-99-reference.md`（共 14 个） | 生成物 | `scripts/sync-view-from-struct.py` 重新生成，**禁止手改** |
| 历史快照 | `_HISTORICAL_/` 下 8 个 `software_architecture_reuse_*_2026.md` | 只读归档 | 不维护；冲突以 `struct/` 为准 |

卷册 ↔ struct 主题一一对应：

| 卷册 | 对应 struct 主题 |
| ---- | ---- |
| `volume-01-meta-model-standards.md` | `struct/01-meta-model-standards/` |
| `volume-02-business-architecture-reuse.md` | `struct/02-business-architecture-reuse/` |
| `volume-03-application-architecture-reuse.md` | `struct/03-application-architecture-reuse/` |
| `volume-04-component-architecture-reuse.md` | `struct/04-component-architecture-reuse/` |
| `volume-05-functional-architecture-reuse.md` | `struct/05-functional-architecture-reuse/` |
| `volume-06-cross-layer-governance.md` | `struct/06-cross-layer-governance/` |
| `volume-07-formal-verification.md` | `struct/07-formal-verification/` |
| `volume-08-cognitive-architecture.md` | `struct/08-cognitive-architecture/` |
| `volume-09-value-quantification.md` | `struct/09-value-quantification/` |
| `volume-10-supply-chain-security.md` | `struct/10-supply-chain-security/` |
| `volume-11-industrial-iot-otit.md` | `struct/11-industrial-iot-otit/` |
| `volume-12-ai-native-reuse.md` | `struct/12-ai-native-reuse/` |
| `volume-13-emerging-trends.md` | `struct/13-emerging-trends/` |
| `volume-99-reference.md` | `struct/99-reference/` |

## 3. 同步机制分析

- **生成**：`scripts/sync-view-from-struct.py` 以内容哈希比对 struct 源文件与卷册段落，增量重写差异部分。
- **校验**：`python scripts/health-check.py` 将同步检查列为硬门禁；差异报告见 `reports/view-diff-report.md`。
- **链路**：`struct/`（真源）→ `view/`（卷册）→ `dist/book-volumes/`（交付分卷，由 `build-deliverables.py` 生成）。因此修改内容的正确入口永远是 `struct/`，详见根目录 `AGENTS.md` R2/R3。

## 4. 使用建议

- **通读**：按 `01 → 13 → 99` 顺序阅读现役卷册，获得完整叙事。
- **引用**：引用具体知识时优先链接 `struct/` 下的结构化文档（粒度更细、更新更快）；卷册适合做章节级引用。
- **追溯 2026-06 时点**：使用 `_HISTORICAL_/` 快照，并注明"历史快照，当前状态见对应 struct 主题"。
- **发现不一致**：不要直接改卷册；回到 `struct/` 修正后重新运行同步脚本。

### 示例：卷册的正确使用方式

例如，想了解 MCP 协议的完整论述：通读 `volume-12-ai-native-reuse.md` 获得全景，再深入 `struct/12-ai-native-reuse/01-mcp-protocol/` 核对当前稳定版表述；两份内容冲突时以 struct 为准。

### 反例：错误用法

- 直接在 `volume-*.md` 上改正错字——下次同步会被覆盖，应改 `struct/` 源文件。
- 以 `_HISTORICAL_/` 快照中的标准状态（如勘误前的 ArchiMate 版本表述）作为当前事实引用。
- 用卷册文件数评估项目当前规模——统计真源是 `reports/stats.json`。

## 5. 权威来源

> **权威来源**:
>
> - 本项目 `struct/` 知识体系（唯一内容真源）
> - `scripts/sync-view-from-struct.py`（同步机制真源）
> - `reports/view-diff-report.md`（同步状态真源）
>
> **核查日期**: 2026-07-12
