# 2026-Q2 前沿跟踪报告

> **报告周期**: 2026 年第二季度
> **编制日期**: 2026-06-12
> **核查日期**: 2026-07-09
> **状态**: 已审查

---

## 概念定义

**前沿跟踪（Frontier Tracking）**：对软件架构、标准、规范与生态工具的最新发布状态进行周期性监测、权威来源复核与影响评估的知识管理活动。其目标是在官方状态发生变化时，及时调整知识体系中的引用、结论与行动项。

---

## 1. 本季度新发布/变更的标准

| 标准/技术 | 变更前状态 | 变更后状态 | 权威来源 URL | 发现日期 |
|:---|:---|:---|:---|:---|
| **ArchiMate 4.0** | 厂商预发布/未获官方确认 | ✅ **已正式发布（2026-04-27，Document C260，白皮书 W262）** | <https://www.opengroup.org/The-Open-Group-Announces-ArchiMate%C2%AE-4-Specification> | 2026-06-12 |
| **ISO/IEC/IEEE 12207:2026** | 仍在制定中 | ✅ **已发布（2026-04-29）** | <https://www.iso.org/standard/90219.html> | 2026-06-12 |
| **ISO/IEC 30141:2024** | 被误审为“不存在 2024 版” | ✅ **已发布（2024-08）** | <https://www.iso.org/standard/88800.html> | 2026-06-12 |
| **ISO/IEC 25010** | 多处误写为 2024 版 | ✅ **正式版为 2023** | <https://www.iso.org/standard/78175.html> | 2026-06-12 |
| **NIST SSDF 1.2** | 正式版 | ⚠️ **Initial Public Draft（征求意见稿）** | <https://csrc.nist.gov/News/2025/draft-ssdf-version-1-2> | 2026-06-12 |
| **IEC 62443-4-2** | 误写为 2025 版 | ✅ **现行版为 2019** | <https://webstore.iec.ch/publication/67463> | 2026-06-12 |
| **ISO/IEC 5338** | 制定中 | ✅ **2023 版已发布** | <https://www.iso.org/standard/81118.html> | 2026-06-12 |
| **ISO/IEC 25040** | URL 指向 /standard/64768.html | ✅ **正确 URL 为 /standard/83467.html** | <https://www.iso.org/standard/83467.html> | 2026-06-12 |

### 1.1 权威来源核验摘要

| 标准/技术 | 官方来源 | 最新确认 URL | 状态 | 核查日期 |
|---|---|---|---|---|
| ArchiMate 4.0 | The Open Group | <https://www.opengroup.org/The-Open-Group-Announces-ArchiMate%C2%AE-4-Specification> | 已正式发布（2026-04-27） | 2026-07-09 |
| ISO/IEC/IEEE 12207:2026 | ISO | <https://www.iso.org/standard/90219.html> | 已发布（2026-04-29） | 2026-07-09 |
| ISO/IEC 30141:2024 | ISO | <https://www.iso.org/standard/88800.html> | 已发布（2024-08） | 2026-07-09 |
| ISO/IEC 25010:2023 | ISO | <https://www.iso.org/standard/78176.html> | 现行正式版 | 2026-07-09 |
| NIST SSDF 1.2 | NIST CSRC | <https://csrc.nist.gov/News/2025/draft-ssdf-version-1-2> | Initial Public Draft | 2026-07-09 |
| IEC 62443-4-2 | IEC Webstore | <https://webstore.iec.ch/publication/67463> | 现行版 2019 | 2026-07-09 |
| ISO/IEC 5338:2023 | ISO | <https://www.iso.org/standard/81118.html> | 已发布 | 2026-07-09 |
| ISO/IEC 25040:2024 | ISO | <https://www.iso.org/standard/83467.html> | 已发布 | 2026-07-09 |

> **核验原则**：每项标准状态必须来自 ISO/IEC、The Open Group、NIST、IEC 等官方发布渠道，避免依赖厂商博客或第三方百科的时效性信息。

---

## 2. 本季度确认保持不变的预期

| 标准/技术 | 当前状态 | 权威来源 | 备注 |
|:---|:---|:---|:---|
| **MCP 2025-11-25** | 现行稳定版 | modelcontextprotocol.io | 2026-07-28 RC 仍在预期中 |
| **A2A v1.0.0** | 已发布（2026-03-12） | a2aprotocol.io | 无变更 |
| **SLSA 1.2** | Build/Source Track 已发布；Build Environment Track / L4 仍在开发 | slsa.dev | 无变更 |
| **OPC UA FX Parts 80–84** | 已发布 | OPC Foundation | C2D/D2D 完善中 |
| **IEC 61508 Ed.3** | CDV 已完成，预计 2026 末–2027 初发布 | IEC | 无变更 |
| **ISO 26262 Ed.3** | 新工作项已注册（2026 初），目标 ~2029 | ISO | 无变更 |

---

## 3. 对本项目知识体系的潜在影响

| 标准/技术 | 影响层级 | 影响描述 | 建议动作 | 优先级 |
|:---|:---|:---|:---|:---:|
| **ArchiMate 4.0** | 元模型层 | 已正式发布（2026-04-27，Document C260），与 3.2 向后兼容 | 已完成相关文档更新；持续跟踪官方页面 | 🟢 完成 |
| **ISO/IEC/IEEE 12207:2026** | 生命周期过程层 | 取代 2017 版，成为现行软件生命周期过程基准 | 更新 `01/01-iso-420xx-family/ieee-1517-reuse-processes.md`、`06/03-maturity-models/` 等引用 | 🔴 P0 |
| **ISO/IEC 30141:2024** | 工业 IoT 层 | 确认存在且为现行版，2018 版已被取代 | 强化 `11/01-isa-95-model/iso-30141-iot-ra-alignment.md` 与 2024 版第二版特性对齐 | 🔴 P0 |
| **NIST SSDF 1.2** | 供应链安全层 | 仍为征求意见稿，非正式版 | 修正 `10-supply-chain-security/` 中“正式版”表述；跟踪最终版发布 | 🔴 P0 |
| **ISO/IEC 25010:2023** | 质量模型层 | 官方正式版为 2023，不存在 2024 | 全项目回滚为 `:2023`；更新勘误说明 | 🔴 P0 |

因为标准状态的偏差会直接传递到架构决策与合规基线，所以季度跟踪必须基于官方来源进行交叉验证，并在发现误判时及时回滚或更新。

---

## 4. 下季度重点跟踪项

1. **MCP 2026-07-28 RC**: 关注是否按期发布及与 2025-11-25 的兼容性差异。
2. **NIST SSDF 1.2 最终版**: 跟踪 IPD 反馈期后是否进入正式版。
3. **IEC 61508 Ed.3**: 关注 2026 末–2027 初发布进展。
4. **ISO/IEC/IEEE DIS 42024 / DIS 42042**: 关注 DIS 投票结果及最终发布时间。
5. **WASI 1.0**: 跟踪 2026 底–2027 初发布计划。

---

## 5. 已执行动作

- [x] 运行 `standards-version-audit.py` 并修复误报
- [x] 更新 `authoritative-sources-v2.md`
- [x] 更新 `CHANGELOG.md` 并补充 ArchiMate 4.0 最终勘误说明
- [x] 修复 `fix-p0-standards.py` 使其幂等（dry-run 输出 0 变更）
- [x] 创建 `99-reference/frontier-tracking/` 索引与季度模板
- [x] 更新 `ieee-1517-reuse-processes.md` 12207 引用至 2026 版
- [x] 更新 `spice-rcmm-rise-mapping.md` 12207 引用至 2026 版
- [x] 更新 `iso-30141-iot-ra-alignment.md` 强化 2024 版第二版特性

---

## 6. 正向示例与反例

### 正向示例

**示例**：在 2026-Q2 跟踪中，团队通过 ISO 官网与 The Open Group 新闻稿交叉验证，确认 ArchiMate 4.0 已于 2026-04-27 正式发布（Document C260），并及时修正了早期审计报告中的"虚假发布"误判，避免了知识库回退到过时版本。

### 反例

**反例**：某季度报告仅依赖工具厂商页面判断 ArchiMate 4.0 未发布，未核对 The Open Group 官方公告，导致项目多处引用被错误标记为"需回退"，引发不必要的返工。

---

## 7. 权威来源

> 本报告中的标准状态以下列权威来源为准：
>
> - [The Open Group — ArchiMate 4.0 Specification](https://www.opengroup.org/The-Open-Group-Announces-ArchiMate%C2%AE-4-Specification)（核查日期：2026-07-09）
> - [The Open Group — TOGAF Standard, 10th Edition](https://www.opengroup.org/togaf)（核查日期：2026-07-09）
> - [ISO — ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html)（核查日期：2026-07-09）
> - [ISO — ISO/IEC/IEEE 12207:2026](https://www.iso.org/standard/90219.html)（核查日期：2026-07-09）
> - [ISO — ISO/IEC 30141:2024](https://www.iso.org/standard/88800.html)（核查日期：2026-07-09）
> - [ISO — ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html)（核查日期：2026-07-09）
> - [ISO — ISO/IEC 25040:2024](https://www.iso.org/standard/83467.html)（核查日期：2026-07-09）
> - [ISO — ISO/IEC 5338:2023](https://www.iso.org/standard/81118.html)（核查日期：2026-07-09）
> - [IEC — IEC 62443-4-2:2019](https://webstore.iec.ch/publication/67463)（核查日期：2026-07-09）
> - [NIST — SSDF 1.2 Initial Public Draft](https://csrc.nist.gov/News/2025/draft-ssdf-version-1-2)（核查日期：2026-07-09）
> - [NIST — AI Risk Management Framework 1.0](https://www.nist.gov/itl/ai-risk-management-framework)（核查日期：2026-07-09）

---

> **编制人**: 软件工程架构复用知识体系项目组
> **审查人**:
