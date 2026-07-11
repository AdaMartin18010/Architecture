# view/ — 长文档卷册（历史快照）

> **版本声明**: `view/` 中的 8 个 Markdown 卷册是 **2026-06-05/06 版本的历史快照**。
> **定位**: 基于原始 ~31 万字源文档整理的长文档/书籍视角，便于一次性阅读、课程讲义或书籍输出。
> **当前真源**: `struct/` 目录为当前结构化知识体系的唯一真源；`view/` 与 `struct/` 之间**未建立自动同步机制**，可能存在内容差异。
> **状态**: 不主动维护细节更新，重大修订通过 `scripts/sync-view-from-struct.py` 重新生成或手动同步。

---

## 概念定位：什么是历史快照

**历史快照（Historical Snapshot）** 在本目录中的定义是：2026-06-05/06 时点 `view/` 卷册的只读归档，保留该时点长文档的完整叙事以便追溯引用与版本对比。快照的效力规则只有一条：**当快照与 `struct/` 冲突时，一律以 `struct/` 为准**——因为 `struct/` 是唯一持续维护的真源，快照不接收细节修订。

### 示例：快照的正确使用方式

例如：研究者需要引用 2026-06-06 版《全面展开论证》卷中对 MCP 的原始论述时，应链接 `software_architecture_reuse_full_2026.md` 的对应章节，同时在引用处注明"历史快照，当前状态见 `struct/12-ai-native-reuse/01-mcp-protocol/`"——既保留可追溯性，又不传播过时状态。

### 反例：历史快照的错误用法

- 将快照中的标准状态（如 ArchiMate 4.0 勘误前的表述）当作当前事实引用；
- 在快照文件上直接提交内容更新（应改 `struct/` 后由 `scripts/sync-view-from-struct.py` 统一收口）；
- 以快照覆盖度评估项目当前完成度（快照不含 2026-06 之后的全部增量）。

因此，本目录只承诺"版本可追溯"，不承诺"内容最新"；任何内容层面的修正都必须回到 `struct/` 进行。

---

## 卷册清单

| 文件 | 主题/定位 | 对应 `struct/` 主题 | 版本日期 |
|---|---|---|---|
| `software_architecture_reuse_framework_2026.md` | 国际标准对齐与层次化提纲 | 01 + 02 + 03 + 04 + 05 + 06 | 2026-06-05 |
| `software_architecture_reuse_full_2026.md` | 全面展开论证 | 01–07 综合 | 2026-06-06 |
| `software_architecture_reuse_extension_2026.md` | 全面扩展卷（标准演进、BPMN/DMN、MCP/A2A、度量） | 01–06 + 12 + 13 | 2026-06-06 |
| `software_architecture_reuse_deep_extension_2026.md` | 深度扩展卷（形式化/认知/ROI） | 07 + 08 + 09 | 2026-06-06 |
| `software_architecture_reuse_technical_deep_2026.md` | 技术深度扩展卷（供应链/Rust/AI 概率） | 10 + 07(Rust) + 12(AI 概率) | 2026-06-06 |
| `software_architecture_reuse_industrial_2026.md` | 工业 IoT/OT-IT 融合扩展卷 | 11 | 2026-06-06 |
| `software_architecture_reuse_vol5_deep_2026.md` | 卷五深化卷（OPC UA FX/ISA-95/AAS/PLCopen/PIU） | 11（OPC UA FX/ISA-95/AAS/PLCopen/PIU） | 2026-06-06 |
| `software_architecture_reuse_vol469_deep_2026.md` | 卷六·卷九·卷四综合深化卷 | 07（安全关键）+ 金融核心 + 10/07 | 2026-06-06 |

## 使用建议

1. **系统学习**: 按卷册顺序阅读可获得从框架到深化的完整叙事。
2. **事实核查**: 若 `view/` 与 `struct/` 存在冲突，请以 `struct/` 为准。
3. **引用来源**: 卷册中的历史勘误段落（如 ArchiMate 4.0 三次勘误、MCP 2026-07-28 RC）已被 `struct/` 中的最终状态替代，引用时请注意版本。

## 同步机制

- 长期目标：通过 `scripts/sync-view-from-struct.py` 从 `struct/` 自动生成 `view/` 或差异报告。
- 当前状态：同步脚本尚未实现，`view/` 为只读历史快照。
- 参见：`struct/README.md`（当前真源入口）、`view/volume-01-meta-model-standards.md`（现役卷册示例）

## 权威来源

> **权威来源**:
>
> - 本项目 `struct/` 知识体系
> - `struct/MASTER_PLAN.md`
>
> **核查日期**: 2026-07-07
