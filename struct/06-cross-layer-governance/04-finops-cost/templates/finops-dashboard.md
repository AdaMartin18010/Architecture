# FinOps 仪表盘指标与视图定义模板 (FinOps Dashboard)

> **版本**: {{VERSION}}（示例: 2026-06-12）
> **适用范围**: {{SCOPE}}（示例: 全组织多云 FinOps 治理）
> **仪表盘所有者**: {{DASHBOARD_OWNER}}（示例: FinOps CoE / 平台工程团队）
> **刷新频率**: {{REFRESH_FREQUENCY}}（示例: 账单数据每日、资源指标每小时）
> **对齐来源**: FinOps Foundation Framework 2026、FOCUS 1.0、Unit Economics for Platform Engineering

---

## 目录

- [FinOps 仪表盘指标与视图定义模板 (FinOps Dashboard)](#finops-仪表盘指标与视图定义模板-finops-dashboard)
  - [目录](#目录)
  - [1. 仪表盘设计原则](#1-仪表盘设计原则)
  - [2. 数据源清单](#2-数据源清单)
  - [3. 核心视图定义](#3-核心视图定义)
    - [3.1 Executive View（高管视图）](#31-executive-view高管视图)
    - [3.2 FinOps Team View（FinOps 团队视图）](#32-finops-team-viewfinops-团队视图)
    - [3.3 Engineering Team View（工程团队视图）](#33-engineering-team-view工程团队视图)
    - [3.4 Finance View（财务视图）](#34-finance-view财务视图)
    - [3.5 AI/GPU View（AI 成本视图）](#35-aigpu-viewai-成本视图)
  - [4. Showback / Chargeback 视图](#4-showback--chargeback-视图)
    - [4.1 Showback 视图（透明度展示，不实际扣费）](#41-showback-视图透明度展示不实际扣费)
    - [4.2 Chargeback 视图（实际内部结算）](#42-chargeback-视图实际内部结算)
  - [5. 单位成本视图](#5-单位成本视图)
    - [5.1 单位定义表](#51-单位定义表)
    - [5.2 单位成本下钻路径](#52-单位成本下钻路径)
  - [6. 异常检测视图](#6-异常检测视图)
    - [6.1 异常检测规则配置](#61-异常检测规则配置)
    - [6.2 异常事件仪表盘](#62-异常事件仪表盘)
  - [7. 指标字典](#7-指标字典)
  - [8. 权限与访问控制](#8-权限与访问控制)
  - [9. 实施检查清单](#9-实施检查清单)
    - [第 1–30 天：需求与数据源](#第-130-天需求与数据源)
    - [第 31–60 天：开发与集成](#第-3160-天开发与集成)
    - [第 61–90 天：试运行与推广](#第-6190-天试运行与推广)
  - [10. 参考索引](#10-参考索引)

---

## 1. 仪表盘设计原则

| 原则 | 说明 |
|------|------|
| **按受众分层** | 高管看趋势与单位经济学，工程师看资源利用率与优化机会，财务看预算与分摊 |
| **可行动** | 每个指标都应有明确的 Owner 与后续动作，避免“仅供参考” |
| **实时与准确平衡** | 账单数据允许 T+1，资源利用率尽量接近实时，异常告警需要实时/小时级 |
| **一致性** | 同一指标在不同视图中定义一致，避免口径冲突 |
| **可下钻** | 从总成本可下钻到业务单元 → 应用 → 组件 → 资源 |

---

## 2. 数据源清单

| 数据源 | 数据类型 | 刷新频率 | 接入方式 | 责任人 |
|--------|---------|---------|---------|--------|
| {{BILLING_SOURCE_1}}（如 AWS Cost & Usage Report） | 原始账单 | 每日 | S3 + ETL / API | {{BILLING_OWNER_1}} |
| {{BILLING_SOURCE_2}}（如 Azure Cost Management） | 原始账单 | 每日 | Exports + API | {{BILLING_OWNER_2}} |
| {{BILLING_SOURCE_3}}（如 GCP Billing Export） | 原始账单 | 每日 | BigQuery Export | {{BILLING_OWNER_3}} |
| {{SaaS_BILLING_SOURCE}}（如 Datadog、Snowflake） | SaaS 订阅与用量 | 每日/每周 | 账单邮件 / API | {{SAAS_BILLING_OWNER}} |
| {{AI_BILLING_SOURCE}}（如 OpenAI API、GPU 集群监控） | LLM token、GPU 时长 | 每小时/每日 | API / Prometheus | {{AI_BILLING_OWNER}} |
| {{RESOURCE_TAG_SOURCE}} | 资源标签与元数据 | 每小时 | 云厂商 API / CMDB | {{TAG_OWNER}} |
| {{USAGE_METRICS_SOURCE}} | CPU、内存、请求数、存储量 | 每小时 | CloudWatch / Azure Monitor / Prometheus | {{METRICS_OWNER}} |
| {{BUSINESS_METRICS_SOURCE}} | 用户数、交易量、收入 | 每日 | 数据仓库 / CRM | {{BUSINESS_METRICS_OWNER}} |

---

## 3. 核心视图定义

### 3.1 Executive View（高管视图）

**目标受众**: CEO/CFO/CTO、VP Engineering、FinOps 委员会
**更新频率**: 每日（展示 T+1）

| 指标/图表 | 说明 | 目标/阈值 | 数据源 |
|-----------|------|----------|--------|
| 月度总云支出 | 全组织云 + SaaS + AI 总成本 | ≤ 预算 | 各云厂商账单 |
| 预算达成率 | 实际支出 / 月度预算 × 100% | ≤ 100% | 账单 + 财务预算 |
| 年度累计支出趋势 | YTD 支出 vs YTD 预算 | 偏差 ≤ ±{{BUDGET_VARIANCE_THRESHOLD}}% | 账单 + 预算 |
| Cloud COGS | 可直接计入销货成本的云支出 | 趋势下降 | 分摊结果 |
| 毛利率 | （收入 - Cloud COGS）/ 收入 × 100% | ≥ {{GROSS_MARGIN_TARGET}}% | 财务 + 分摊 |
| 每用户云成本 | 云支出 / 活跃用户 | 环比下降 | 账单 + 业务指标 |
| 单位经济学成熟度 | Crawl / Walk / Run 阶段 | 向 Run 演进 | 治理评估 |

### 3.2 FinOps Team View（FinOps 团队视图）

**目标受众**: FinOps 分析师、FinOps 工程师
**更新频率**: 每日/每小时

| 指标/图表 | 说明 | 目标/阈值 | 数据源 |
|-----------|------|----------|--------|
| Allocation Accuracy Index（AAI） | 直接归属成本 / 总基础设施成本 | ≥ {{AAI_TARGET}}% | 账单 + 标签 |
| Resource Cost Shadowing Rate（RCSR） | 已追踪资源成本占比 | ≥ {{RCSR_TARGET}}% | 账单 + 标签 |
| 未分配成本金额 | 无法归属的成本 | ≤ {{UNALLOCATED_AMOUNT}} | 分摊引擎 |
| 标签覆盖率 | 含全部 Mandatory 标签的资源占比 | ≥ {{TAG_COVERAGE_TARGET}}% | 标签扫描 |
| 分摊模型健康度 | 各模型（Usage-Based、Layer-Based 等）运行状态 | 无错误 | 分摊引擎 |
| Showback/Chargeback 报告状态 | 上月报告生成与分发状态 | 100% 按时 | FinOps 平台 |
| 异常告警数量 | 待处理异常事件数 | ≤ {{OPEN_ANOMALIES_THRESHOLD}} | 异常检测 |

### 3.3 Engineering Team View（工程团队视图）

**目标受众**: 应用团队负责人、SRE、平台工程师
**更新频率**: 每小时/每日

| 指标/图表 | 说明 | 目标/阈值 | 数据源 |
|-----------|------|----------|--------|
| 团队月度成本 | 本团队直接 + 间接 + 风险成本 | 在预算内 | 分摊结果 |
| 资源利用率热力图 | CPU/内存/GPU 利用率分布 | 利用率 ≥ {{UTILIZATION_TARGET}}% | 监控指标 |
| 闲置资源清单 | 低利用率、未附加、长期未变更资源 | 0 高影响项 | 监控 + 账单 |
| 自动扩缩容效率 | 峰值/谷值资源调整效果 | 符合 SLO | APM / K8s |
| 优化机会列表 | Right-sizing、Spot 迁移、存储分层 | 按 ROI 排序 | FinOps 工具 |
| 团队单位成本 | 每请求/每用户/每事务成本 | 环比下降 | 分摊 + 业务指标 |

### 3.4 Finance View（财务视图）

**目标受众**: 财务规划与分析（FP&A）、会计、采购
**更新频率**: 每日/月度

| 指标/图表 | 说明 | 目标/阈值 | 数据源 |
|-----------|------|----------|--------|
| 实际 vs 预算（按 BU） | 各业务单元支出与预算对比 | 偏差 ≤ ±{{BU_BUDGET_VARIANCE}}% | 账单 + 预算 |
| 实际 vs 预测 | 滚动预测准确率 | 误差 ≤ ±{{FORECAST_ERROR}}% | 预测模型 |
| Cloud COGS 明细 | 按产品/客户的销货成本 | GAAP 就绪 | 分摊结果 |
| 承诺折扣利用率 | RI/Savings Plans 利用率 | ≥ {{COMMITMENT_UTILIZATION_TARGET}}% | 云厂商账单 |
| 预付 vs 按需比例 | 资本支出结构 | 符合财务策略 | 账单 |
| 发票对账状态 | 各厂商账单与内部记录一致性 | 100% 对账 | 账单系统 |

### 3.5 AI/GPU View（AI 成本视图）

**目标受众**: AI 平台团队、数据科学团队、产品负责人
**更新频率**: 每小时/每日

| 指标/图表 | 说明 | 目标/阈值 | 数据源 |
|-----------|------|----------|--------|
| LLM Token 成本 | 输入/输出 token 成本趋势 | 每千 token 成本下降 | AI API 账单 |
| GPU 集群利用率 | 训练/推理 GPU 利用率 | ≥ {{GPU_UTIL_TARGET}}% | GPU 监控 |
| 每模型调用成本 | 按模型版本/端点统计 | 按模型优化 | AI Gateway 日志 |
| RAG 检索成本 | 向量数据库查询与嵌入成本 | 每查询成本下降 | 向量 DB 账单 |
| 微调任务成本 | 每次 fine-tuning 任务成本 | 可追踪到租户 | GPU 调度系统 |
| AI 工作负载分摊 | 按 `ai-workload-type` 分摊的成本 | 100% 可追溯 | 标签 + 用量 |

---

## 4. Showback / Chargeback 视图

### 4.1 Showback 视图（透明度展示，不实际扣费）

| 维度 | 展示内容 | 受众 | 频率 |
|------|---------|------|------|
| 按业务单元 | 各 BU 成本、占比、环比 | BU Head | 每月 |
| 按项目/产品 | 项目直接/间接/风险成本 | 项目经理 | 每月 |
| 按应用/服务 | 应用级成本与单位成本 | 应用团队 | 每周/每月 |
| 按环境 | prod / staging / dev 成本分布 | SRE / 工程经理 | 每周 |
| 按云厂商 | AWS / Azure / GCP / SaaS / AI 支出 | FinOps / 采购 | 每月 |

### 4.2 Chargeback 视图（实际内部结算）

| 字段 | 说明 | 示例 |
|------|------|------|
| 成本中心 | 财务记账单元 | {{COST_CENTER}} |
| 计费周期 | 结算月份 | {{BILLING_PERIOD}} |
| 直接成本 | 可直接归属的成本 | {{DIRECT_COST}} |
| 间接成本分摊 | 平台/CoE/基础设施分摊 | {{INDIRECT_COST}} |
| 风险成本分摊 | 供应链/安全/合规准备金 | {{RISK_COST}} |
| 总成本 | 直接 + 间接 + 风险 | {{TOTAL_CHARGEBACK}} |
| 结算状态 | 已确认 / 待复核 / 有争议 | {{CHARGEBACK_STATUS}} |

---

## 5. 单位成本视图

### 5.1 单位定义表

| 单位 | 计算公式 | 适用场景 | 目标 |
|------|---------|---------|------|
| 每活跃用户成本 | 云总成本 / 月活跃用户（MAU）| SaaS 产品 | ≤ {{TARGET_COST_PER_MAU}} |
| 每付费客户成本 | Cloud COGS / 付费客户数 | 订阅制产品 | ≤ {{TARGET_COST_PER_PAYING_CUSTOMER}} |
| 每 API 请求成本 | API 相关成本 / API 请求数 | API 平台 | ≤ {{TARGET_COST_PER_API_REQUEST}} |
| 每事务成本 | 交易成本 / 事务数 | 电商/支付 | ≤ {{TARGET_COST_PER_TRANSACTION}} |
| 每 GB 处理成本 | 数据成本 / 处理 GB 数 | 数据平台 | ≤ {{TARGET_COST_PER_GB}} |
| 每千 token 成本 | AI 成本 / token 数（千）| LLM 应用 | ≤ {{TARGET_COST_PER_1K_TOKENS}} |
| 每 GPU 小时成本 | GPU 相关成本 / GPU 小时 | AI 训练/推理 | ≤ {{TARGET_COST_PER_GPU_HOUR}} |

### 5.2 单位成本下钻路径

```text
每用户云成本
├── 按业务单元拆分
│   └── 按应用拆分
│       ├── 直接资源成本
│       ├── 间接平台成本
│       └── 风险成本
└── 按单位类型拆分
    ├── 计算
    ├── 存储
    ├── 网络
    ├── 数据库
    ├── AI/GPU
    └── SaaS 订阅
```

---

## 6. 异常检测视图

### 6.1 异常检测规则配置

| 规则名称 | 检测对象 | 触发条件 | 严重级别 | 通知对象 |
|----------|---------|---------|---------|---------|
| 单日支出激增 | 总云支出 | 单日环比增长 ≥ {{DAILY_SPEND_SPIKE}}% | 高 | FinOps 团队 + 高管 |
| 预算偏差 | 团队/项目月度支出 | 月度预算达成率 ≥ {{BUDGET_ALERT_THRESHOLD}}% | 高 | 团队负责人 + 财务 |
| 资源利用率异常 | 计算资源 | CPU < {{LOW_CPU_THRESHOLD}}% 持续 {{LOW_CPU_DAYS}} 天 | 中 | 应用团队 |
| 闲置资源 | EBS/磁盘 | 未附加超过 {{UNATTACHED_DAYS}} 天 | 中 | 应用团队 |
| AI Token 激增 | LLM API | 单小时 token 量环比增长 ≥ {{TOKEN_SPIKE}}% | 高 | AI 平台团队 |
| GPU 空闲 | GPU 集群 | 利用率 < {{GPU_IDLE_THRESHOLD}}% 持续 {{GPU_IDLE_HOURS}} 小时 | 中 | AI 平台团队 |
| 预留实例利用率不足 | RI/Savings Plans | 利用率 < {{RI_UTIL_THRESHOLD}}% | 高 | FinOps 团队 |

### 6.2 异常事件仪表盘

| 异常 ID | 发生时间 | 资源/服务 | 规则 | 影响金额 | 状态 | Owner |
|---------|---------|----------|------|---------|------|-------|
| {{ANOMALY_ID_1}} | {{ANOMALY_TIME_1}} | {{ANOMALY_RESOURCE_1}} | {{ANOMALY_RULE_1}} | {{ANOMALY_IMPACT_1}} | 待处理/已确认/已关闭 | {{ANOMALY_OWNER_1}} |
| {{ANOMALY_ID_2}} | {{ANOMALY_TIME_2}} | {{ANOMALY_RESOURCE_2}} | {{ANOMALY_RULE_2}} | {{ANOMALY_IMPACT_2}} | 待处理/已确认/已关闭 | {{ANOMALY_OWNER_2}} |

---

## 7. 指标字典

| 指标 | 英文 | 计算公式 | 单位 | 采集频率 | 责任人 |
|------|------|---------|------|---------|--------|
| 分配准确率 | AAI | 直接归属成本 / 总基础设施成本 × 100% | % | 每月 | FinOps 分析师 |
| 资源成本覆盖率 | RCSR | 已分配/可追踪资源成本 / 总资源成本 × 100% | % | 每月 | FinOps 工程师 |
| 预算达成率 | Budget Attainment | 实际支出 / 预算 × 100% | % | 每日 | FP&A |
| 每用户成本 | Cost per User | 云总成本 / 用户数 | USD/用户 | 每月 | FinOps 分析师 |
| 每交易/请求成本 | Cost per Transaction/Request | 相关成本 / 交易或请求数 | USD/单位 | 每日 | 应用团队 |
| 预留覆盖率 | RI Coverage | RI 覆盖的计算小时 / 总计算小时 × 100% | % | 每日 | FinOps 工程师 |
| Spot 占比 | Spot Ratio | Spot 成本 / 计算总成本 × 100% | % | 每日 | 平台团队 |
| GPU 利用率 | GPU Utilization | GPU 平均利用率 | % | 每小时 | AI 平台团队 |
| 每千 token 成本 | Cost per 1K Tokens | AI 成本 / token 数（千）| USD/1K tokens | 每日 | AI 平台团队 |

---

## 8. 权限与访问控制

| 视图 | 可访问角色 | 权限级别 |
|------|-----------|---------|
| Executive View | C-level、VP、FinOps 委员会 | 只读 |
| FinOps Team View | FinOps 分析师/工程师 | 读写 |
| Engineering Team View | 应用团队负责人、SRE | 只读本团队 + 共享平台 |
| Finance View | FP&A、会计、采购 | 只读/导出 |
| AI/GPU View | AI 平台团队、数据科学团队 | 只读/读写 |
| 原始账单数据 | FinOps Lead、财务负责人 | 受限访问 |

---

## 9. 实施检查清单

### 第 1–30 天：需求与数据源

- [ ] 访谈各受众，确认每类用户的核心问题
- [ ] 梳理所有云厂商、SaaS、AI 数据源
- [ ] 建立指标字典，统一指标口径
- [ ] 设计 Executive / FinOps / Engineering / Finance / AI 五类视图
- [ ] 确定权限矩阵与数据安全策略

### 第 31–60 天：开发与集成

- [ ] 搭建 ETL Pipeline，导入账单与用量数据
- [ ] 实现分摊计算与单位经济学计算
- [ ] 配置异常检测规则与告警
- [ ] 开发各视图仪表盘（BI 工具或自研）
- [ ] 集成身份认证与权限控制

### 第 61–90 天：试运行与推广

- [ ] 小范围试点，收集反馈
- [ ] 校准异常检测阈值，降低误报
- [ ] 培训各受众使用仪表盘
- [ ] 建立数据质量监控与 SLA
- [ ] 正式发布并纳入 FinOps Review 流程

---

## 10. 参考索引

- FinOps Foundation: [FinOps Dashboard Best Practices](https://www.finops.org/framework/)
- FinOps Foundation: [Unit Economics](https://www.finops.org/framework/capabilities/unit-economics/)
- FinOps Foundation: [Anomaly Management](https://www.finops.org/framework/capabilities/anomalies/)
- FOCUS 1.0 Specification: <https://focus.finops.org/>

> **交叉引用**:
>
> - FinOps 审查会议模板: [`./finops-review.md`](./finops-review.md)
> - 单位经济学计算模板: [`./unit-economics.md`](./unit-economics.md)
> - AI 成本分摊模板: [`./ai-cost-allocation.md`](./ai-cost-allocation.md)
> - 标签治理策略模板: [`./tagging-policy.md`](./tagging-policy.md)

> 最后更新: {{LAST_UPDATED}}
