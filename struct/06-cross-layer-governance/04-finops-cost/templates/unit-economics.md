# FinOps 单位经济学计算模板 (Unit Economics)

> **版本**: {{VERSION}}（示例: 2026-06-12）
> **适用范围**: {{SCOPE}}（示例: SaaS 产品、AI 平台、共享服务）
> **计算周期**: {{PERIOD}}（示例: 2026-05）
> **负责人**: {{OWNER}}（示例: FinOps 分析师 + 财务 FP&A）
> **对齐来源**: FinOps Foundation Framework 2026、Opslyft Cloud COGS Playbook、Unit Economics for Platform Engineering

---

## 目录

- [FinOps 单位经济学计算模板 (Unit Economics)](#finops-单位经济学计算模板-unit-economics)
  - [目录](#目录)
  - [1. 单位经济学目标](#1-单位经济学目标)
  - [2. 选择业务单位](#2-选择业务单位)
    - [2.1 单位选择原则](#21-单位选择原则)
    - [2.2 常见单位类型](#22-常见单位类型)
  - [3. Cloud COGS 构成](#3-cloud-cogs-构成)
    - [3.1 Cloud COGS 桥接流程](#31-cloud-cogs-桥接流程)
    - [3.2 Cloud COGS 分类](#32-cloud-cogs-分类)
    - [3.3 成本归集公式](#33-成本归集公式)
  - [4. 单位成本计算表](#4-单位成本计算表)
    - [4.1 每用户成本](#41-每用户成本)
    - [4.2 每交易/每请求成本](#42-每交易每请求成本)
    - [4.3 每 token 成本（AI 场景）](#43-每-token-成本ai-场景)
    - [4.4 每 GB 处理成本](#44-每-gb-处理成本)
  - [5. 分层毛利率计算](#5-分层毛利率计算)
    - [5.1 按客户层级](#51-按客户层级)
    - [5.2 按产品功能](#52-按产品功能)
  - [6. 计算示例](#6-计算示例)
    - [6.1 SaaS 产品示例](#61-saas-产品示例)
    - [6.2 AI 推理平台示例](#62-ai-推理平台示例)
  - [7. 数据质量要求](#7-数据质量要求)
  - [8. 实施检查清单](#8-实施检查清单)
    - [第 1–30 天：基线建立](#第-130-天基线建立)
    - [第 31–60 天：计算与报告](#第-3160-天计算与报告)
    - [第 61–90 天：运营化](#第-6190-天运营化)
  - [9. 参考索引](#9-参考索引)

---

## 1. 单位经济学目标

| 目标 | 说明 |
|------|------|
| 将云支出转化为业务可理解指标 | 从“上月 AWS 花费 $240K”到“每活跃用户 $0.42” |
| 支撑产品定价与毛利分析 | 将 Cloud COGS 纳入产品 P&L |
| 驱动架构优化决策 | 识别单位成本最高的功能/租户/模型 |
| 量化规模效应 | 随着用户增长，每单位成本是否下降 |
| 对齐财务报告 | 云成本可映射到 GAAP -ready 的销货成本 |

---

## 2. 选择业务单位

### 2.1 单位选择原则

| 原则 | 说明 |
|------|------|
| 与财务报告一致 | 单位应能被财务部门认可，便于纳入 P&L |
| 与产品价值挂钩 | 单位应反映用户/客户获得的价值 |
| 可稳定采集 | 单位数量必须有可靠、持续的数据源 |
| 避免过度细分 | 初期选择 1–3 个核心单位，逐步细化 |

### 2.2 常见单位类型

| 单位类型 | 适用场景 | 示例 |
|----------|---------|------|
| 每活跃用户（Monthly Active User, MAU）| 通用 SaaS | $/MAU |
| 每付费客户 | 订阅制/B2B SaaS | $/paying customer |
| 每交易 | 电商、支付、金融 | $/transaction |
| 每请求 | API 平台、微服务 | $/request |
| 每 GB 处理 | 数据平台、CDN、存储 | $/GB |
| 每千 token | LLM 应用 | $/1K tokens |
| 每 GPU 小时 | AI 训练/推理 | $/GPU hour |
| 每客户会话 | 客服、协作工具 | $/session |

---

## 3. Cloud COGS 构成

Cloud COGS 是将云账单转化为 GAAP-ready 销货成本的核心概念。

### 3.1 Cloud COGS 桥接流程

```text
原始云账单 ($2,400,000)
        ↓
成本分配 (95%+ 分配到团队/产品/租户)
        ↓
单位经济学 (每客户/每功能/每请求成本)
        ↓
Cloud COGS (GAAP 毛利率就绪)
```

### 3.2 Cloud COGS 分类

| 分类 | 说明 | 是否计入 COGS | 示例 |
|------|------|--------------|------|
| 生产环境资源 | 直接支撑客户服务的资源 | ✅ 计入 | 生产 EC2、RDS、负载均衡 |
| 客户支持工具 | 直接用于服务客户的 SaaS | ✅ 计入 | 客服系统、监控告警 |
| 共享平台分摊 | 按使用量/受益比例分摊到产品 | ✅ 计入 | K8s 平台、API 网关 |
| 开发/测试环境 | 不直接服务客户 | ❌ 计入 R&D | dev/staging 资源 |
| 内部管理工具 | 支撑内部运营 | ❌ 计入 G&A | HR、财务系统 |
| AI 推理成本 | 按 token/请求分摊到产品 | ✅ 计入 | LLM API、GPU 推理 |
| AI 研发实验 | 未上线模型的探索性支出 | ❌ 计入 R&D | PoC 训练任务 |

### 3.3 成本归集公式

```
产品 Cloud COGS = 该产品可直接归属成本
                + 该产品分摊的共享平台成本
                + 该产品分摊的风险成本
                + 该产品直接使用的 AI/SaaS 成本
```

---

## 4. 单位成本计算表

### 4.1 每用户成本

| 字段 | 公式/说明 | 值 |
|------|----------|-----|
| 周期 | 计算月份 | {{PERIOD}} |
| 产品/服务 | 计算对象 | {{PRODUCT_NAME}} |
| 可直接归属 Cloud COGS | 生产环境 + 客户支持 + 直接 AI 成本 | {{DIRECT_CLOUD_COGS}} |
| 分摊的共享平台成本 | 平台/基础设施按比例分摊 | {{ALLOCATED_PLATFORM_COST}} |
| 分摊的风险成本 | 安全/合规/供应链准备金 | {{ALLOCATED_RISK_COST}} |
| **总 Cloud COGS** | 直接 + 分摊平台 + 分摊风险 | {{TOTAL_CLOUD_COGS}} |
| 月活跃用户（MAU）| 活跃用户数 | {{MAU}} |
| 付费客户数 | 实际付费客户 | {{PAYING_CUSTOMERS}} |
| **每活跃用户 Cloud COGS** | 总 Cloud COGS / MAU | {{COST_PER_MAU}} |
| **每付费客户 Cloud COGS** | 总 Cloud COGS / 付费客户数 | {{COST_PER_PAYING_CUSTOMER}} |
| 每用户收入（ARPU）| 月收入 / 用户数 | {{ARPU}} |
| **Cloud COGS 占收入比** | 每用户 Cloud COGS / ARPU × 100% | {{CLOUD_COGS_TO_REVENUE}}% |

### 4.2 每交易/每请求成本

| 字段 | 公式/说明 | 值 |
|------|----------|-----|
| 相关服务成本 | 支撑该交易/请求的服务成本 | {{TRANSACTION_RELATED_COST}} |
| 交易/请求数量 | 周期内总交易/请求数 | {{TRANSACTION_COUNT}} / {{REQUEST_COUNT}} |
| **每交易成本** | 相关服务成本 / 交易数量 | {{COST_PER_TRANSACTION}} |
| **每请求成本** | 相关服务成本 / 请求数量 | {{COST_PER_REQUEST}} |
| 平均交易金额 | 收入 / 交易数量 | {{AVERAGE_TRANSACTION_VALUE}} |
| **交易毛利率** | （平均交易金额 - 每交易成本）/ 平均交易金额 × 100% | {{TRANSACTION_GROSS_MARGIN}}% |

### 4.3 每 token 成本（AI 场景）

| 字段 | 公式/说明 | 值 |
|------|----------|-----|
| LLM API 成本 | 输入 + 输出 token 费用 | {{LLM_API_COST}} |
| 自托管 GPU 推理成本 | GPU 实例 + 网络 + 存储 | {{SELF_HOSTED_GPU_COST}} |
| 嵌入/向量数据库成本 | Embedding + 检索费用 | {{EMBEDDING_RETRIEVAL_COST}} |
| 相关平台分摊 | AI 平台共享成本 | {{AI_PLATFORM_ALLOCATED_COST}} |
| **AI 总成本** | 以上之和 | {{TOTAL_AI_COST}} |
| 输入 token 数（千）| 输入 token / 1000 | {{INPUT_TOKENS_K}} |
| 输出 token 数（千）| 输出 token / 1000 | {{OUTPUT_TOKENS_K}} |
| 总 token 数（千）| 输入 + 输出 | {{TOTAL_TOKENS_K}} |
| **每千输入 token 成本** | LLM API 输入成本 / 输入 token（千）| {{COST_PER_1K_INPUT_TOKENS}} |
| **每千输出 token 成本** | LLM API 输出成本 / 输出 token（千）| {{COST_PER_1K_OUTPUT_TOKENS}} |
| **每千总 token 成本** | AI 总成本 / 总 token（千）| {{COST_PER_1K_TOTAL_TOKENS}} |

### 4.4 每 GB 处理成本

| 字段 | 公式/说明 | 值 |
|------|----------|-----|
| 数据存储成本 | 对象存储、文件存储、数据库存储 | {{STORAGE_COST}} |
| 数据处理成本 | ETL、计算、网络传输 | {{DATA_PROCESSING_COST}} |
| 相关平台分摊 | 数据平台共享成本 | {{DATA_PLATFORM_ALLOCATED_COST}} |
| **数据总成本** | 以上之和 | {{TOTAL_DATA_COST}} |
| 处理数据量（GB）| 周期内处理/存储的数据量 | {{DATA_GB}} |
| **每 GB 处理成本** | 数据总成本 / 处理数据量 | {{COST_PER_GB}} |

---

## 5. 分层毛利率计算

### 5.1 按客户层级

| 客户层级 | ARPU | 每客户 Cloud COGS | 毛利率 | 收入占比 |
|----------|------|------------------|--------|---------|
| Enterprise | {{ENTERPRISE_ARPU}} | {{ENTERPRISE_COST_PER_CUSTOMER}} | {{ENTERPRISE_GROSS_MARGIN}}% | {{ENTERPRISE_REVENUE_SHARE}}% |
| Mid-market | {{MID_MARKET_ARPU}} | {{MID_MARKET_COST_PER_CUSTOMER}} | {{MID_MARKET_GROSS_MARGIN}}% | {{MID_MARKET_REVENUE_SHARE}}% |
| Self-serve | {{SELF_SERVE_ARPU}} | {{SELF_SERVE_COST_PER_CUSTOMER}} | {{SELF_SERVE_GROSS_MARGIN}}% | {{SELF_SERVE_REVENUE_SHARE}}% |
| **合计/加权平均** | **{{WEIGHTED_ARPU}}** | **{{WEIGHTED_COST_PER_CUSTOMER}}** | **{{WEIGHTED_GROSS_MARGIN}}%** | **100%** |

> **洞察**: 聚合毛利率会隐藏亏损客户层级，建议按层级披露。

### 5.2 按产品功能

| 功能模块 | 模块收入 | 模块 Cloud COGS | 模块毛利率 | 优化优先级 |
|----------|---------|----------------|-----------|-----------|
| {{FEATURE_1}} | {{F1_REVENUE}} | {{F1_COGS}} | {{F1_GROSS_MARGIN}}% | P{{F1_PRIORITY}} |
| {{FEATURE_2}} | {{F2_REVENUE}} | {{F2_COGS}} | {{F2_GROSS_MARGIN}}% | P{{F2_PRIORITY}} |
| {{FEATURE_3}} | {{F3_REVENUE}} | {{F3_COGS}} | {{F3_GROSS_MARGIN}}% | P{{F3_PRIORITY}} |

---

## 6. 计算示例

### 6.1 SaaS 产品示例

**假设数据**:

| 字段 | 值 |
|------|-----|
| 月度总云支出 | $240,000 |
| 可直接归属 Cloud COGS（生产+支持） | $192,000 |
| 分摊的共享平台成本 | $38,000 |
| 分摊的风险成本 | $10,000 |
| 总 Cloud COGS | $240,000 |
| 月活跃用户（MAU） | 571,429 |
| 付费客户数 | 1,200 |
| 月度总收入 | $1,000,000 |

**计算结果**:

| 指标 | 计算 | 结果 |
|------|------|------|
| 每活跃用户 Cloud COGS | $240,000 / 571,429 | **$0.42 / MAU** |
| 每付费客户 Cloud COGS | $240,000 / 1,200 | **$200 / 付费客户** |
| ARPU（按 MAU） | $1,000,000 / 571,429 | **$1.75 / MAU** |
| Cloud COGS 占收入比 | $240,000 / $1,000,000 | **24%** |
| Cloud 毛利率 | ($1,000,000 - $240,000) / $1,000,000 | **76%** |

### 6.2 AI 推理平台示例

**假设数据**:

| 字段 | 值 |
|------|-----|
| LLM API 成本（输入+输出） | $18,000 |
| 自托管 GPU 推理成本 | $22,000 |
| 向量数据库成本 | $5,000 |
| AI 平台共享分摊 | $5,000 |
| AI 总成本 | $50,000 |
| 输入 token | 120,000,000 |
| 输出 token | 30,000,000 |
| 总 token | 150,000,000 |
| 总请求数 | 2,000,000 |

**计算结果**:

| 指标 | 计算 | 结果 |
|------|------|------|
| 每千输入 token 成本 | $18,000 × 40% / 120,000K | **$0.06 / 1K input tokens** |
| 每千输出 token 成本 | $18,000 × 60% / 30,000K | **$0.36 / 1K output tokens** |
| 每千总 token 成本 | $50,000 / 150,000K | **$0.333 / 1K tokens** |
| 每请求成本 | $50,000 / 2,000,000 | **$0.025 / request** |
| GPU 利用率 | — | **65%** |

> **洞察**: 输出 token 成本显著高于输入 token，建议优化提示词工程、减少输出长度或使用更小的模型处理简单任务。

---

## 7. 数据质量要求

| 要求 | 目标 | 验证方法 |
|------|------|---------|
| 分配准确率（AAI） | ≥ {{AAI_TARGET}}% | 直接归属成本 / 总基础设施成本 |
| 标签覆盖率 | ≥ {{TAG_COVERAGE_TARGET}}% | 含全部 Mandatory 标签资源占比 |
| 业务指标可用性 | 100% | 数据仓库每日刷新 |
| 成本分类准确性 | ≥ {{CLASSIFICATION_ACCURACY}}% | 财务抽样审计 |
| 分摊模型稳定性 | 无重大口径变更 | 月度对账 |

---

## 8. 实施检查清单

### 第 1–30 天：基线建立

- [ ] 与财务部门对齐 Cloud COGS 分类规则
- [ ] 选择 1–3 个核心单位（如 MAU、交易、token）
- [ ] 验证业务指标数据源与采集频率
- [ ] 评估当前 AAI 与标签覆盖率
- [ ] 建立 Cloud COGS 计算基线

### 第 31–60 天：计算与报告

- [ ] 实现 Cloud COGS 自动化计算
- [ ] 生成首份单位经济学报告
- [ ] 按客户层级/产品功能拆分毛利率
- [ ] 与产品团队核对单位成本合理性
- [ ] 识别 Top 5 高单位成本功能/租户

### 第 61–90 天：运营化

- [ ] 将单位经济学纳入月度 FinOps Review
- [ ] 设置单位成本异常告警
- [ ] 建立单位成本优化目标（如每 MAU 下降 10%）
- [ ] 将指标接入 Executive 仪表盘
- [ ] 发布《单位经济学运营手册》

---

## 9. 参考索引

- FinOps Foundation: [Unit Economics Capability](https://www.finops.org/framework/capabilities/unit-economics/)
- Opslyft (2026): *Cloud Unit Economics & Cloud COGS Playbook*
- FinOps Foundation: [Cost Allocation](https://www.finops.org/framework/capabilities/allocate/)
- DORA State of DevOps Report 2024

> **交叉引用**:
>
> - FinOps 云成本治理与价值量化: [`../finops-unit-economics-2026.md`](../finops-unit-economics-2026.md)
> - FinOps 跨层成本分摊执行模板: [`../cost-allocation-template.md`](../cost-allocation-template.md)
> - FinOps 四级成本分摊模型: [`../finops-allocation-template.md`](../finops-allocation-template.md)
> - AI 成本分摊模板: [`./ai-cost-allocation.md`](./ai-cost-allocation.md)

> 最后更新: {{LAST_UPDATED}}
