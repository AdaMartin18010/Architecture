# 前沿跟踪索引（Frontier Tracking Index）

> **版本**: 2026-07-08
> **定位**: `99-reference/frontier-tracking/` —— 全项目新兴标准、技术动态与权威来源变更的季度跟踪入口
> **主要交付物**:
>
> - 季度前沿状态汇总
> - 标准版本变更预警
> - 对本项目知识体系的潜在影响评估
> - 下一步跟踪任务清单

---

## 概念定位：什么是前沿跟踪

**前沿跟踪（Frontier Tracking）** 是指对本知识体系所引用的国际标准、行业框架与技术协议（ISO/IEC/IEEE、The Open Group、NIST、W3C、Linux Foundation 等）的官方状态进行**周期性、来源可核查的监控**，并将确认后的变更同步到 `struct/99-reference/standards-index/authoritative-sources-v2.md` 与相关主题文档的过程。其范围仅限于"已发布/征求意见稿/草案/官方预告"四类官方状态；其产出是本目录下的季度报告与模板，以及全项目标准引用的事实基准更新。

前沿跟踪不等于"技术新闻汇总"：只有能改变本项目标准引用状态（版本号、发布状态、官方 URL）的事件才进入跟踪项。

---

## 跟踪原则

1. **权威来源优先**: 所有状态变更必须以官方机构（ISO、IEC、The Open Group、NIST、IEEE 等）发布的正式信息为准。
2. **区分“已发布”“征求意见稿”“草案”“预告”**: 避免将厂商预告、社区讨论或第三方预测误标为官方状态。
3. **保留历史认知**: 勘误记录保留在 `view/` 历史文档和 `struct/99-reference/CHANGELOG.md` 中，便于追溯。
4. **季度审查**: 每季度运行一次 `standards-version-audit.py`，生成报告并更新本索引。

---

### 示例：一条合格的前沿跟踪记录

例如：`2026-q3-frontier-report.md` 中对 ArchiMate 4.0 的跟踪条目，同时给出了变更前状态（3.2 为最新）、变更后状态（4.0 于 2026-04-27 正式发布）、官方来源（The Open Group Document C260 发布公告）与对本项目的影响评估（`01-meta-model-standards/04-archimate-4/` 映射需更新），四要素齐备，是合格的跟踪记录样例。

### 反例：不属于前沿跟踪的内容

- 厂商博客中的产品预告、社区论坛讨论、第三方媒体的版本预测（无官方机构背书）；
- 与本项目标准引用无关的技术新闻（如某框架的次要补丁版本）；
- 纯内部进度汇报（属于 `99-reference/audit/` 的统计报告范畴，而非前沿跟踪）。

因此，跟踪负责人在收录任一条目前必须先完成"官方来源可访问 + 状态可归入四分类"两项核查，否则不予收录。

---

## 当前活跃跟踪项（2026-Q3）

| 标准/技术 | 当前状态 | 权威来源 | 影响评估 | 跟踪负责人 |
|:---|:---|:---|:---|:---|
| **MCP** | 稳定版 **2025-11-25**；**RC 2026-07-28 已发布（2026-05-29）** | modelcontextprotocol.io / GitHub Releases | 功能层 AI 协议基线 | TBD |
| **A2A** | **v1.0.0** 已发布（2026-03-12） | <https://a2a-protocol.org/latest/> | Agent 互操作基线 | TBD |
| **ArchiMate 4.0** | ✅ **已正式发布（2026-04-27）** | The Open Group Document C260 / [官方发布公告](https://www.opengroup.org/The-Open-Group-Announces-ArchiMate%C2%AE-4-Specification) | 元模型层更新 | TBD |
| **ISO/IEC/IEEE 12207:2026** | ✅ **已发布（2026-04-29）** | ISO 90219 | 生命周期过程基准迁移 | TBD |
| **ISO/IEC 30141:2024** | ✅ **已发布（2024-08）** | ISO 88800 | IoT 参考架构对齐 | TBD |
| **NIST SSDF 1.2** | **Initial Public Draft**（征求意见稿） | NIST CSRC | 供应链安全基线待最终版 | TBD |
| **IEC 61508 Ed.3** | CDV 已完成，预计 2026 末–2027 初发布 | IEC | 功能安全跨域复用 | TBD |
| **ISO 26262 Ed.3** | 新工作项已注册（2026 初），目标 ~2029 | ISO | 汽车 SEooC 复用 | TBD |
| **WASI 1.0** | 预期 2026 底–2027 初；0.3 Preview 已可用 | WebAssembly 社区组 | WASM 组件复用 | TBD |

---

## 目录结构

```text
struct/99-reference/frontier-tracking/
├── README.md                    # 本索引
├── 2026-q2-frontier-report.md   # 2026 年第二季度前沿跟踪报告
├── 2026-q3-frontier-report.md   # 2026 年第三季度前沿跟踪报告
└── templates/
    ├── quarterly-frontier-template.md  # 季度报告模板
    └── quarterly-sop.md                # 季度复核标准作业程序
```

---

## 自动化工具

- **一致性扫描**: `struct/99-reference/tools/standards-version-audit.py`
- **P0 批量修复**: `struct/99-reference/tools/fix-p0-standards.py`
- **标准事实基准**: `struct/99-reference/standards-index/authoritative-sources-v2.md`

---

## 权威来源与核查依据

> **权威来源**（跟踪项状态判定所依据的官方机构页面）：
>
> - ISO 在线浏览平台（标准状态与版本）：<https://www.iso.org/standards.html>
> - The Open Group 标准库（TOGAF/ArchiMate）：<https://pubs.opengroup.org/togaf-standard/>
> - NIST CSRC 出版物目录（SSDF/SP 系列）：<https://csrc.nist.gov/publications/detail/sp/800-218/final>
> - MCP 官方规范：<https://modelcontextprotocol.io/specification/2025-11-25>
> - A2A 协议官方站点：<https://a2a-protocol.org/latest/>
>
> **核查日期**: 2026-07-08（每季度随 `standards-version-audit.py` 运行结果刷新）

---

## 相关文档

- `struct/99-reference/frontier-tracking/2026-q3-frontier-report.md` —— 2026 年第三季度前沿跟踪报告
- `struct/99-reference/CHANGELOG.md` —— 历史勘误与重大更新
- `struct/99-reference/standards-index/authoritative-sources-v2.md` —— 全项目权威来源基准

---

> **最后更新**: 2026-07-08
> **维护者**: 软件工程架构复用知识体系项目组
