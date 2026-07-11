# YYYY-QN 前沿跟踪报告模板

> **报告周期**: YYYY 年第 N 季度
> **编制日期**: YYYY-MM-DD
> **核查日期**: YYYY-MM-DD
> **状态**: 草稿 / 已审查

---

## 模板概念与用途

本模板是《季度前沿跟踪复核标准作业程序》（`templates/quarterly-sop.md`）步骤 5 的标准产出格式，用于记录一个季度内本项目所引用标准/协议的**官方状态变更**。其设计约束是：每一行记录都必须可由权威来源 URL 复核，因此模板将"权威来源 URL"设为表格的必填列，而不是可选备注。

### 反例：不应填入本模板的内容

- 未经官方机构确认的版本预测或路线图解读（应转入"下季度重点跟踪项"并标注为预期）；
- 与标准状态无关的内部工作汇报（属于 `99-reference/audit/` 范畴）；
- 缺少来源 URL 的状态声明（违反 `99-reference/templates/citation-standard.md` 的引用三元组规范）。

---

## 1. 本季度新发布/变更的标准

| 标准/技术 | 变更前状态 | 变更后状态 | 权威来源 URL | 发现日期 |
|:---|:---|:---|:---|:---|
| 示例：ISO/IEC XXXXX | 制定中 | 已发布 | <https://www.iso.org/standard/xxxxx.html> | YYYY-MM-DD |

---

## 2. 本季度确认保持不变的预期

| 标准/技术 | 当前状态 | 权威来源 | 备注 |
|:---|:---|:---|:---|
| 示例：MCP YYYY-MM-DD | 现行稳定版 | modelcontextprotocol.io | 无变更 |

---

## 3. 对本项目知识体系的潜在影响

| 标准/技术 | 影响层级 | 影响描述 | 建议动作 | 优先级 |
|:---|:---|:---|:---|:---:|
| 示例：ISO/IEC XXXXX | 元模型层 | 需要更新概念映射 | 更新 `01-meta-model-standards/` 相关文档 | 🔴 P0 |

---

## 4. 下季度重点跟踪项

1. **示例**: 跟踪 ISO/IEC XXXXX DIS 投票结果。
2. **示例**: 跟踪 MCP（Model Context Protocol） 新版本发布。

---

## 5. 已执行动作

- [ ] 运行 `standards-version-audit.py`
- [ ] 更新 `authoritative-sources-v2.md`
- [ ] 更新 `CHANGELOG.md`
- [ ] 通知相关主题负责人

---

> **编制人**:
> **审查人**:
