# FinOps 月度/季度审查会议模板 (FinOps Review)

> **版本**: {{VERSION}}（示例: 2026-06-12）
> **会议类型**: {{MEETING_TYPE}}（月度审查 / 季度战略审查）
> **周期**: {{PERIOD}}（示例: 2026 年 5 月 / 2026 Q2）
> **主持人**: {{FACILITATOR}}（示例: FinOps Lead）
> **会议时间**: {{MEETING_DATE}} {{MEETING_TIME}}
> **参会人**: {{ATTENDEES}}（工程、财务、产品、平台团队代表）
> **对齐来源**: FinOps Foundation Framework 2026、FinOps Review Best Practices

---

## 目录

- [FinOps 月度/季度审查会议模板 (FinOps Review)](#finops-月度季度审查会议模板-finops-review)
  - [目录](#目录)
  - [1. 会议目标](#1-会议目标)
  - [2. 会前准备清单](#2-会前准备清单)
    - [2.1 数据准备（由 FinOps 分析师负责）](#21-数据准备由-finops-分析师负责)
    - [2.2 会议材料准备](#22-会议材料准备)
  - [3. 议程](#3-议程)
    - [3.1 月度审查议程（建议 60 分钟）](#31-月度审查议程建议-60-分钟)
    - [3.2 季度战略审查议程（建议 120 分钟）](#32-季度战略审查议程建议-120-分钟)
  - [4. 核心指标仪表盘](#4-核心指标仪表盘)
    - [4.1 财务健康度指标](#41-财务健康度指标)
    - [4.2 单位经济学指标](#42-单位经济学指标)
    - [4.3 团队/项目成本汇总](#43-团队项目成本汇总)
  - [5. 检查项清单](#5-检查项清单)
    - [5.1 数据质量检查](#51-数据质量检查)
    - [5.2 成本优化检查](#52-成本优化检查)
    - [5.3 治理与合规检查](#53-治理与合规检查)
  - [6. 异常与风险讨论](#6-异常与风险讨论)
    - [6.1 异常事件登记表](#61-异常事件登记表)
    - [6.2 风险登记](#62-风险登记)
  - [7. 优化机会登记](#7-优化机会登记)
    - [7.1 优化机会列表](#71-优化机会列表)
    - [7.2 优化决策矩阵](#72-优化决策矩阵)
  - [8. 行动项跟踪](#8-行动项跟踪)
  - [9. 会议纪要模板](#9-会议纪要模板)
  - [10. 参考索引](#10-参考索引)
  - [补充说明：FinOps 月度/季度审查会议模板 (FinOps Review)](#补充说明finops-月度季度审查会议模板-finops-review)
  - [概念定义](#概念定义)
  - [示例](#示例)
  - [反例](#反例)
  - [权威来源](#权威来源)

---

## 1. 会议目标

| 目标 | 说明 |
|------|------|
| **透明度** | 向所有利益相关方展示最新云成本与分摊结果 |
| **问责** | 确认各团队对成本异常与优化机会的 ownership |
| **优化** | 识别并排序 right-sizing、预留实例、Spot、AI 成本优化机会 |
| **预测** | 对比实际支出与预算/预测，调整下月/下季度 forecast |
| **协同** | 促进工程、财务、产品、平台团队之间的决策对齐 |

---

## 2. 会前准备清单

### 2.1 数据准备（由 FinOps 分析师负责）

- [ ] 上周期（{{PREVIOUS_PERIOD}}）完整云账单已导入成本管理平台
- [ ] 分摊结果（Showback / Chargeback）已按 cost-center / project / app 汇总
- [ ] 关键指标（AAI、RCSR、单位经济学）已计算并可视化
- [ ] 异常检测报告已生成（同比/环比波动、预算偏差）
- [ ] 上月/上季度行动项完成状态已更新
- [ ] 优化机会清单已初步筛选（按预计节省金额排序）

### 2.2 会议材料准备

| 材料 | 责任人 | 截止时间 |
|------|--------|----------|
| FinOps 仪表盘截图/PDF | {{DASHBOARD_OWNER}} | 会前 1 天 |
| 分摊报告（按团队/项目） | {{ALLOCATION_REPORT_OWNER}} | 会前 1 天 |
| 异常事件说明与根因分析 | {{ANOMALY_OWNER}} | 会前 1 天 |
| 优化机会 ROI 评估 | {{OPTIMIZATION_OWNER}} | 会前 1 天 |
| 预算 vs 实际对比表 | {{BUDGET_OWNER}} | 会前 1 天 |

---

## 3. 议程

### 3.1 月度审查议程（建议 60 分钟）

| 时间 | 议题 | 主讲人 | 输出 |
|------|------|--------|------|
| 0–5 min | 开场与行动项回顾 | {{FACILITATOR}} | 确认上期行动项状态 |
| 5–15 min | 核心指标回顾 | FinOps 分析师 | 指标趋势与异常点 |
| 15–30 min | 成本分摊 Showback/Chargeback 解读 | FinOps 分析师 | 团队成本变化说明 |
| 30–45 min | 异常与优化机会讨论 | 相关团队代表 | 根因与优化方案 |
| 45–55 min | 下月预算与预测校准 | 财务 + 工程 | Forecast 调整 |
| 55–60 min | 行动项确认与会议总结 | {{FACILITATOR}} | 新增/更新行动项 |

### 3.2 季度战略审查议程（建议 120 分钟）

| 时间 | 议题 | 主讲人 | 输出 |
|------|------|--------|------|
| 0–10 min | 季度目标回顾与成熟度评估 | FinOps Lead | 成熟度阶段判定 |
| 10–30 min | 季度成本趋势与单位经济学 | FinOps 分析师 | Cloud COGS、毛利率洞察 |
| 30–50 min | 架构复用成本透明度报告 | 平台工程负责人 | Golden Path 成本、共享服务利用率 |
| 50–70 min | AI 成本专题（如适用） | AI 平台负责人 | LLM/GPU 成本分摊与优化 |
| 70–90 min | 优化项目组合审查 | 各团队负责人 | 项目 ROI、优先级调整 |
| 90–110 min | 下季度预算与关键举措 | 财务 + 工程 VP | 预算分配、目标承诺 |
| 110–120 min | 行动项与会议纪要确认 | {{FACILITATOR}} | 季度行动项清单 |

---

## 4. 核心指标仪表盘

### 4.1 财务健康度指标

| 指标 | 英文缩写 | 本周期 | 上周期 | 环比 | 目标 | 状态 |
|------|---------|--------|--------|------|------|------|
| 总云支出 | Total Cloud Spend | {{CURRENT_SPEND}} | {{PREVIOUS_SPEND}} | {{SPEND_MOM}}% | ≤ {{SPEND_BUDGET}} | {{SPEND_STATUS}} |
| 预算达成率 | Budget Attainment | {{BUDGET_ATTAINMENT}}% | — | — | ≤ 100% | {{BUDGET_STATUS}} |
| 分配准确率 | AAI | {{CURRENT_AAI}}% | {{PREVIOUS_AAI}}% | {{AAI_MOM}}% | ≥ {{AAI_TARGET}}% | {{AAI_STATUS}} |
| 资源覆盖率 | RCSR | {{CURRENT_RCSR}}% | {{PREVIOUS_RCSR}}% | {{RCSR_MOM}}% | ≥ {{RCSR_TARGET}}% | {{RCSR_STATUS}} |
| 预留实例覆盖率 | RI Coverage | {{RI_COVERAGE}}% | — | — | ≥ {{RI_COVERAGE_TARGET}}% | {{RI_STATUS}} |
| Spot/Preemptible 占比 | Spot Ratio | {{SPOT_RATIO}}% | — | — | ≥ {{SPOT_RATIO_TARGET}}% | {{SPOT_STATUS}} |
| 单位成本（每用户） | Cost per User | {{COST_PER_USER}} | {{PREVIOUS_COST_PER_USER}} | {{CPU_MOM}}% | ≤ {{CPU_TARGET}} | {{CPU_STATUS}} |
| 单位成本（每交易） | Cost per Transaction | {{COST_PER_TXN}} | {{PREVIOUS_COST_PER_TXN}} | {{CPT_MOM}}% | ≤ {{CPT_TARGET}} | {{CPT_STATUS}} |

> **指标说明**:
>
> - **AAI** (Allocation Accuracy Index): 直接归属成本 / 总基础设施成本 × 100%
> - **RCSR** (Resource Cost Shadowing Rate): 已分配/可追踪资源成本占比，反映标签与分摊覆盖度
> - **预算达成率**: 实际支出 / 预算 × 100%

### 4.2 单位经济学指标

| 单位定义 | 本周期成本 | 单位数量 | 单位成本 | 上周期单位成本 | 趋势 |
|----------|-----------|---------|---------|---------------|------|
| 每活跃用户 | {{ACTIVE_USER_COST}} | {{ACTIVE_USERS}} | {{COST_PER_ACTIVE_USER}} | {{PREV_COST_PER_ACTIVE_USER}} | {{ACTIVE_USER_TREND}} |
| 每付费客户 | {{PAYING_CUSTOMER_COST}} | {{PAYING_CUSTOMERS}} | {{COST_PER_PAYING_CUSTOMER}} | {{PREV_COST_PER_PAYING_CUSTOMER}} | {{PAYING_CUSTOMER_TREND}} |
| 每 API 请求 | {{API_REQUEST_COST}} | {{API_REQUESTS}} | {{COST_PER_API_REQUEST}} | {{PREV_COST_PER_API_REQUEST}} | {{API_REQUEST_TREND}} |
| 每千 token（AI）| {{TOKEN_COST}} | {{TOKEN_COUNT_K}} | {{COST_PER_1K_TOKENS}} | {{PREV_COST_PER_1K_TOKENS}} | {{TOKEN_TREND}} |
| 每 GPU 小时 | {{GPU_HOUR_COST}} | {{GPU_HOURS}} | {{COST_PER_GPU_HOUR}} | {{PREV_COST_PER_GPU_HOUR}} | {{GPU_HOUR_TREND}} |

### 4.3 团队/项目成本汇总

| 团队/项目 | 直接成本 | 间接成本 | 风险成本 | 总成本 | 占总成本比例 | 环比 |
|-----------|---------|---------|---------|--------|------------|------|
| {{TEAM_1}} | {{T1_DIRECT}} | {{T1_INDIRECT}} | {{T1_RISK}} | {{T1_TOTAL}} | {{T1_RATIO}}% | {{T1_MOM}}% |
| {{TEAM_2}} | {{T2_DIRECT}} | {{T2_INDIRECT}} | {{T2_RISK}} | {{T2_TOTAL}} | {{T2_RATIO}}% | {{T2_MOM}}% |
| {{TEAM_3}} | {{T3_DIRECT}} | {{T3_INDIRECT}} | {{T3_RISK}} | {{T3_TOTAL}} | {{T3_RATIO}}% | {{T3_MOM}}% |
| **合计** | **{{TOTAL_DIRECT}}** | **{{TOTAL_INDIRECT}}** | **{{TOTAL_RISK}}** | **{{GRAND_TOTAL}}** | **100%** | **{{TOTAL_MOM}}%** |

---

## 5. 检查项清单

### 5.1 数据质量检查

- [ ] 账单数据已完整导入，无缺失厂商（AWS/Azure/GCP/SaaS/AI）
- [ ] 标签覆盖率 ≥ {{TAG_COVERAGE_TARGET}}%
- [ ] 未分配资源成本占比 ≤ {{UNALLOCATED_TARGET}}%
- [ ] 异常检测规则已运行并生成告警
- [ ] 财务分类（COGS/R&D/G&A）已核对

### 5.2 成本优化检查

- [ ] 是否存在持续低利用率的 EC2/VM/容器（CPU < {{LOW_UTIL_THRESHOLD}}% 连续 {{LOW_UTIL_DAYS}} 天）
- [ ] 是否存在未附加的磁盘/未使用的负载均衡器
- [ ] 是否有 RI/Savings Plans 即将到期或利用率不足
- [ ] AI/GPU 资源是否存在空闲窗口（夜间/周末）
- [ ] 开发/测试环境是否按策略自动关停

### 5.3 治理与合规检查

- [ ] 新增资源是否符合标签策略
- [ ] 是否有超出预算阈值的团队/项目
- [ ] 是否有异常支出事件需要根因分析
- [ ] 是否有新的共享服务需要纳入分摊模型
- [ ] 是否有供应商合同到期需要重新谈判

---

## 6. 异常与风险讨论

### 6.1 异常事件登记表

| 异常 ID | 发现时间 | 资源/服务 | 异常类型 | 影响金额 | 根因 | 状态 | 负责人 |
|---------|---------|----------|----------|---------|------|------|--------|
| {{ANOMALY_ID_1}} | {{ANOMALY_DATE_1}} | {{ANOMALY_RESOURCE_1}} | {{ANOMALY_TYPE_1}} | {{ANOMALY_IMPACT_1}} | {{ANOMALY_ROOT_CAUSE_1}} | {{ANOMALY_STATUS_1}} | {{ANOMALY_OWNER_1}} |
| {{ANOMALY_ID_2}} | {{ANOMALY_DATE_2}} | {{ANOMALY_RESOURCE_2}} | {{ANOMALY_TYPE_2}} | {{ANOMALY_IMPACT_2}} | {{ANOMALY_ROOT_CAUSE_2}} | {{ANOMALY_STATUS_2}} | {{ANOMALY_OWNER_2}} |

**常见异常类型**: 突发流量、配置漂移、资源泄漏、新服务上线、厂商定价变更、AI 调用量激增、预留实例到期。

### 6.2 风险登记

| 风险 | 可能性 | 影响 | 风险等级 | 缓解措施 | 负责人 |
|------|--------|------|---------|---------|--------|
| {{RISK_1}} | 高/中/低 | 高/中/低 | {{RISK_LEVEL_1}} | {{MITIGATION_1}} | {{RISK_OWNER_1}} |
| {{RISK_2}} | 高/中/低 | 高/中/低 | {{RISK_LEVEL_2}} | {{MITIGATION_2}} | {{RISK_OWNER_2}} |

---

## 7. 优化机会登记

### 7.1 优化机会列表

| ID | 优化项 | 类型 | 预计节省 | 实施成本 | ROI | 优先级 | 负责人 | 目标完成日期 |
|----|--------|------|---------|---------|-----|--------|--------|------------|
| {{OPP_ID_1}} | {{OPP_NAME_1}} | {{OPP_TYPE_1}} | {{OPP_SAVINGS_1}} | {{OPP_COST_1}} | {{OPP_ROI_1}} | P{{OPP_PRIORITY_1}} | {{OPP_OWNER_1}} | {{OPP_DUE_1}} |
| {{OPP_ID_2}} | {{OPP_NAME_2}} | {{OPP_TYPE_2}} | {{OPP_SAVINGS_2}} | {{OPP_COST_2}} | {{OPP_ROI_2}} | P{{OPP_PRIORITY_2}} | {{OPP_OWNER_2}} | {{OPP_DUE_2}} |

**优化类型**: Right-sizing、Reserved Instances、Savings Plans、Spot/Preemptible、自动扩缩容、存储分层、AI 模型蒸馏、缓存优化、许可优化。

### 7.2 优化决策矩阵

| 优化项 | 节省潜力 | 实施风险 | 工程投入 | 建议动作 |
|--------|---------|---------|---------|---------|
| {{OPT_1}} | 高/中/低 | 高/中/低 | 高/中/低 | 立即执行 / 列入计划 / 进一步评估 |
| {{OPT_2}} | 高/中/低 | 高/中/低 | 高/中/低 | 立即执行 / 列入计划 / 进一步评估 |

---

## 8. 行动项跟踪

| 行动项 ID | 行动项描述 | 负责人 | 截止日期 | 优先级 | 状态 | 验证标准 |
|-----------|-----------|--------|----------|--------|------|---------|
| {{ACTION_ID_1}} | {{ACTION_DESC_1}} | {{ACTION_OWNER_1}} | {{ACTION_DUE_1}} | P{{ACTION_PRIORITY_1}} | 待开始/进行中/已完成 | {{ACTION_VERIFY_1}} |
| {{ACTION_ID_2}} | {{ACTION_DESC_2}} | {{ACTION_OWNER_2}} | {{ACTION_DUE_2}} | P{{ACTION_PRIORITY_2}} | 待开始/进行中/已完成 | {{ACTION_VERIFY_2}} |
| {{ACTION_ID_3}} | {{ACTION_DESC_3}} | {{ACTION_OWNER_3}} | {{ACTION_DUE_3}} | P{{ACTION_PRIORITY_3}} | 待开始/进行中/已完成 | {{ACTION_VERIFY_3}} |

---

## 9. 会议纪要模板

```markdown
# FinOps Review 会议纪要

- **会议类型**: {{MEETING_TYPE}}
- **周期**: {{PERIOD}}
- **日期**: {{MEETING_DATE}}
- **主持人**: {{FACILITATOR}}
- **参会人**: {{ATTENDEES}}

## 关键结论

1. {{KEY_TAKEAWAY_1}}
2. {{KEY_TAKEAWAY_2}}
3. {{KEY_TAKEAWAY_3}}

## 通过的决议

- {{DECISION_1}}
- {{DECISION_2}}

## 行动项（详见第 8 节）

- {{ACTION_SUMMARY}}

## 下次会议

- **时间**: {{NEXT_MEETING_DATE}}
- **重点议题**: {{NEXT_MEETING_FOCUS}}
```

---

## 10. 参考索引

- FinOps Foundation: [FinOps Review Best Practices](https://www.finops.org/framework/)
- FinOps Foundation: [Forecasting & Budgeting Capabilities](https://www.finops.org/framework/capabilities/forecast/)
- FinOps Foundation: [Anomaly Management](https://www.finops.org/framework/capabilities/anomalies/)

> **交叉引用**:
>
> - FinOps 仪表盘指标模板: [`./finops-dashboard.md`](./finops-dashboard.md)
> - 单位经济学计算模板: [`./unit-economics.md`](./unit-economics.md)
> - 标签治理策略模板: [`./tagging-policy.md`](./tagging-policy.md)
> - 承诺折扣策略模板: [`./commitment-discount-policy.md`](./commitment-discount-policy.md)

> 最后更新: {{LAST_UPDATED}}


---

## 补充说明：FinOps 月度/季度审查会议模板 (FinOps Review)

## 概念定义

**定义**：FinOps 成本分摊治理是将云成本、平台成本与复用资产成本按业务价值归集到团队、产品与功能，实现成本透明与优化问责。

## 示例

**示例**：平台团队按“每活跃用户”“每千次请求”将共享服务成本分摊给消费方，并在仪表盘展示各产品的单位经济学指标。

## 反例

**反例**：共享平台成本由中央 IT 统一承担，消费方没有成本意识，导致资源浪费与利用率低下。

## 权威来源

> **权威来源**:
>
> - [FinOps Foundation](https://www.finops.org)
> - [CNCF](https://www.cncf.io)
> - 核查日期：2026-07-07