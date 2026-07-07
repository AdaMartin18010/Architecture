# view/ — 长文档卷册（历史快照）

> **版本声明**: `view/` 中的 8 个 Markdown 卷册是 **2026-06-05/06 版本的历史快照**。
> **定位**: 基于原始 ~31 万字源文档整理的长文档/书籍视角，便于一次性阅读、课程讲义或书籍输出。
> **当前真源**: `struct/` 目录为当前结构化知识体系的唯一真源；`view/` 与 `struct/` 之间**未建立自动同步机制**，可能存在内容差异。
> **状态**: 不主动维护细节更新，重大修订通过 `scripts/sync-view-from-struct.py` 重新生成或手动同步。

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

## 权威来源

> **权威来源**:
>
> - 本项目 `struct/` 知识体系
> - `struct/MASTER_PLAN.md`
>
> **核查日期**: 2026-07-07
