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

## 跟踪原则

1. **权威来源优先**: 所有状态变更必须以官方机构（ISO、IEC、The Open Group、NIST、IEEE 等）发布的正式信息为准。
2. **区分“已发布”“征求意见稿”“草案”“预告”**: 避免将厂商预告、社区讨论或第三方预测误标为官方状态。
3. **保留历史认知**: 勘误记录保留在 `view/` 历史文档和 `struct/99-reference/CHANGELOG.md` 中，便于追溯。
4. **季度审查**: 每季度运行一次 `standards-version-audit.py`，生成报告并更新本索引。

---

## 当前活跃跟踪项（2026-Q3）

| 标准/技术 | 当前状态 | 权威来源 | 影响评估 | 跟踪负责人 |
|:---|:---|:---|:---|:---|
| **MCP** | 稳定版 **2025-11-25**；**RC 2026-07-28 已发布（2026-05-29）** | modelcontextprotocol.io / GitHub Releases | 功能层 AI 协议基线 | TBD |
| **A2A** | **v1.0.0** 已发布（2026-03-12） | a2aprotocol.io | Agent 互操作基线 | TBD |
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
└── templates/
    └── quarterly-frontier-template.md  # 季度报告模板
```

---

## 自动化工具

- **一致性扫描**: `struct/99-reference/tools/standards-version-audit.py`
- **P0 批量修复**: `struct/99-reference/tools/fix-p0-standards.py`
- **标准事实基准**: `struct/99-reference/standards-index/authoritative-sources-v2.md`

---

## 相关文档

- `struct/99-reference/frontier-tracking/2026-q3-frontier-report.md` —— 2026 年第三季度前沿跟踪报告
- `struct/99-reference/CHANGELOG.md` —— 历史勘误与重大更新
- `struct/99-reference/standards-index/authoritative-sources-v2.md` —— 全项目权威来源基准

---

> **最后更新**: 2026-07-08
> **维护者**: 软件工程架构复用知识体系项目组
