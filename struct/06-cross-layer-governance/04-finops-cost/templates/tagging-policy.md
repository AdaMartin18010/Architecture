# FinOps 标签治理策略模板 (Tagging Policy)

> **版本**: {{VERSION}}（示例: 2026-06-12）
> **适用范围**: {{SCOPE}}（示例: 全组织云资源、SaaS 订阅、AI 推理服务）
> **所有者**: {{OWNER}}（示例: FinOps Center of Excellence）
> **审阅周期**: {{REVIEW_CYCLE}}（示例: 每季度）
> **对齐来源**: FinOps Foundation Framework 2026、AWS/Azure/GCP Tagging Best Practices、FOCUS 1.0

---

## 目录

- [FinOps 标签治理策略模板 (Tagging Policy)](#finops-标签治理策略模板-tagging-policy)
  - [目录](#目录)
  - [1. 治理目标](#1-治理目标)
  - [2. 标签分类与 Mandatory 级别](#2-标签分类与-mandatory-级别)
    - [2.1 Mandatory 标签（缺失即阻塞部署/触发告警）](#21-mandatory-标签缺失即阻塞部署触发告警)
    - [2.2 Recommended 标签（强烈建议，纳入月度审计）](#22-recommended-标签强烈建议纳入月度审计)
    - [2.3 Optional 标签（按需使用，团队自主决定）](#23-optional-标签按需使用团队自主决定)
  - [3. 命名规范](#3-命名规范)
    - [3.1 键名规范](#31-键名规范)
    - [3.2 值规范](#32-值规范)
    - [3.3 标签值受控词表示例](#33-标签值受控词表示例)
  - [4. 标签赋值责任矩阵](#4-标签赋值责任矩阵)
  - [5. 自动 Enforcement 机制](#5-自动-enforcement-机制)
    - [5.1 部署前拦截（Preventive）](#51-部署前拦截preventive)
    - [5.2 运行时检测与修复（Detective + Corrective）](#52-运行时检测与修复detective--corrective)
    - [5.3 Policy-as-Code 示例片段](#53-policy-as-code-示例片段)
  - [6. 缺失标签处理流程](#6-缺失标签处理流程)
    - [6.1 处理 SLA](#61-处理-sla)
  - [7. 合规检查与报告](#7-合规检查与报告)
    - [7.1 月度标签健康度报告](#71-月度标签健康度报告)
    - [7.2 报告受众与频率](#72-报告受众与频率)
  - [8. 例外管理](#8-例外管理)
  - [9. 实施检查清单](#9-实施检查清单)
    - [第 1–14 天：策略制定](#第-114-天策略制定)
    - [第 15–30 天：工具落地](#第-1530-天工具落地)
    - [第 31–60 天：试运行与修正](#第-3160-天试运行与修正)
    - [第 61–90 天：全面推广](#第-6190-天全面推广)
  - [10. 参考索引](#10-参考索引)
  - [补充说明：FinOps 标签治理策略模板 (Tagging Policy)](#补充说明finops-标签治理策略模板-tagging-policy)
  - [概念定义](#概念定义)
  - [反例](#反例)
  - [权威来源](#权威来源)
  - [分析](#分析)

---

## 1. 治理目标

| 目标 | 衡量指标 | 目标值 |
|------|---------|--------|
| 成本归属可追溯 | Allocation Accuracy Index（AAI）| ≥ {{AAI_TARGET}}%（建议 95%） |
| 资源可发现与治理 | 标签覆盖率 | ≥ {{COVERAGE_TARGET}}%（建议 98%） |
| 自动化审计可持续 | 未标签资源占比 | ≤ {{UNTAGGED_TARGET}}%（建议 2%） |
| 财务-工程对齐 | 按 cost-center 分类准确率 | ≥ {{COST_CENTER_ACCURACY}}%（建议 95%） |

---

## 2. 标签分类与 Mandatory 级别

### 2.1 Mandatory 标签（缺失即阻塞部署/触发告警）

| 标签键 | 英文键名 | 说明 | 示例值 | 适用资源 |
|--------|---------|------|--------|---------|
| 成本中心 | `cost-center` | 财务记账的最小成本单元 | `{{COST_CENTER}}`（如 CC-00123） | 全部 |
| 业务单元 | `business-unit` | 顶级业务线/事业部 | `{{BUSINESS_UNIT}}`（如 BU-Digital） | 全部 |
| 所有者 | `owner` | 资源技术负责人（工号/邮箱前缀） | `{{OWNER}}`（如 zhangsan） | 全部 |
| 环境 | `env` | 运行环境 | `prod` / `staging` / `dev` / `test` | 全部 |
| 应用系统 | `app` | 所属应用或服务名称 | `{{APP_NAME}}`（如 order-service） | 全部 |
| 项目 | `project` | 所属项目/产品代码 | `{{PROJECT_CODE}}`（如 PROJ-2026-AI） | 全部 |

### 2.2 Recommended 标签（强烈建议，纳入月度审计）

| 标签键 | 英文键名 | 说明 | 示例值 | 适用资源 |
|--------|---------|------|--------|---------|
| 数据分级 | `data-classification` | 数据敏感度等级 | `public` / `internal` / `confidential` / `restricted` | 存储、数据库、AI 训练数据 |
| 合规域 | `compliance-domain` | 需满足的合规要求 | `soc2` / `iso27001` / `gdpr` / `等保三级` | 全部 |
| 自动关停策略 | `auto-shutdown` | 是否允许非工作时间自动关停 | `true` / `false` / `weekend-only` | 开发/测试环境 |
| 备份策略 | `backup-policy` | 备份频率与保留期 | `daily-7d` / `weekly-30d` / `none` | 数据库、存储 |
| 架构层级 | `architecture-layer` | 业务/应用/组件/功能层 | `business` / `application` / `component` / `functional` | 全部 |
| 复用资产 ID | `reuse-asset-id` | 关联的内部复用组件/服务 ID | `{{REUSE_ASSET_ID}}`（如 svc-auth） | 共享服务 |

### 2.3 Optional 标签（按需使用，团队自主决定）

| 标签键 | 英文键名 | 说明 | 示例值 |
|--------|---------|------|--------|
| 生命周期 | `lifecycle` | 资源所处阶段 | `poc` / `pilot` / `production` / `deprecated` |
| 预算告警阈值 | `budget-alert-threshold` | 该资源/应用预算告警百分比 | `80` / `100` / `120` |
| 业务关键性 | `criticality` | 对业务的影响等级 | `tier1` / `tier2` / `tier3` |
| 区域/可用区 | `region` | 部署地域 | `cn-north-1` / `east-us-2` |
| AI 工作负载类型 | `ai-workload-type` | 用于 AI 成本分摊 | `llm-inference` / `embedding` / `rag-retrieval` / `fine-tuning` |

---

## 3. 命名规范

### 3.1 键名规范

- 全部小写，使用连字符 `-` 作为分词符，不使用下划线 `_`。
- 长度不超过 63 个字符。
- 不使用云厂商保留前缀（如 `aws:`、`azure:`、`gcp:`、`kubernetes.io/`）。
- 同一组织内标签键必须在全局标签仓库中注册，禁止随意新增。

### 3.2 值规范

| 规则 | 示例 | 反例 |
|------|------|------|
| 小写、无空格 | `order-service` | `Order Service` |
| 使用连字符分词 | `cost-center-001` | `cost_center_001` |
| 避免特殊字符 | `project-alpha` | `project@alpha#1` |
| 枚举值必须来自受控词表 | `prod` | `production`（若词表定义为 `prod`） |
| 未知值使用统一占位 | `unknown` | 留空 `""` |

### 3.3 标签值受控词表示例

```yaml
# 示例：受控词表片段
env:
  allowed: [dev, test, staging, prod]
  default: dev

business-unit:
  allowed: [BU-Digital, BU-Retail, BU-Finance, BU-AI]
  default: unknown

architecture-layer:
  allowed: [business, application, component, functional]
  default: application
```

---

## 4. 标签赋值责任矩阵

| 角色 | 责任 | 工具/入口 |
|------|------|----------|
| **平台工程团队** | 维护全局标签策略、受控词表、Policy-as-Code 规则 | Terraform / OPA / Cloud Custodian |
| **应用团队负责人** | 确保所属资源标签完整准确，处理团队告警 | 云厂商 Console / CI/CD Pipeline |
| **FinOps 分析师** | 月度标签覆盖率审计、AAI 计算、异常分析 | Cost Management / BI 仪表盘 |
| **安全与合规团队** | 审核 `data-classification`、`compliance-domain` 标签 | CSPM / 安全扫描平台 |
| **AI 平台团队** | 为 GPU/LLM 资源标注 `ai-workload-type` 与 `reuse-asset-id` | MLOps 平台 / K8s 标签注入 |

---

## 5. 自动 Enforcement 机制

### 5.1 部署前拦截（Preventive）

| 阶段 | 机制 | 工具示例 |
|------|------|---------|
| IaC 提交 | pre-commit hook 检查必填标签 | `pre-commit` + `terraform-validator` |
| CI/CD Pipeline | 静态扫描 Terraform/ARM/Bicep 模板 | Checkov / Terrascan / OPA Conftest |
| 资源创建 | 云厂商 Policy 阻止未标签资源创建 | AWS SCP / Azure Policy / GCP Organization Policy |
| API 调用 | 标签缺失时返回 `400 Bad Request` | 自定义 Admission Webhook |

### 5.2 运行时检测与修复（Detective + Corrective）

| 频率 | 动作 | 工具示例 |
|------|------|---------|
| 实时 | 资源创建事件触发标签校验，缺失则通知责任人 | Cloud Custodian / Azure Event Grid |
| 每日 | 扫描未标签资源，自动补全可推断标签 | Python 脚本 + 云厂商 API |
| 每周 | 生成标签合规报告，发送给团队负责人 | Cost Management + 邮件/企业微信 |
| 每月 | 纳入 FinOps Review 议程，审查覆盖率趋势 | FinOps Review 会议 |

### 5.3 Policy-as-Code 示例片段

```yaml
# Cloud Custodian 示例：标记缺失 mandatory 标签的 EC2 实例
policies:
  - name: ec2-mandatory-tags
    resource: aws.ec2
    filters:
      - or:
        - "tag:cost-center": absent
        - "tag:business-unit": absent
        - "tag:owner": absent
        - "tag:env": absent
        - "tag:app": absent
        - "tag:project": absent
    actions:
      - type: notify
        to:
          - resource-owner
        subject: "[FinOps] 资源标签缺失告警"
        template: default
```

---

## 6. 缺失标签处理流程

```text
资源被发现缺失 Mandatory 标签
        │
        ├─ 能否自动推断？（如从命名规范、所属 VPC、K8s namespace）
        │       ├── 是 → 自动补全并记录审计日志
        │       └── 否 →
        │               ├─ 是否在豁免清单？
        │               │       ├── 是 → 标记为豁免，记录理由与到期日
        │               │       └── 否 →
        │               │               ├─ 通知资源 Owner（24 小时内）
        │               │               ├─ Owner 在自助门户补全标签
        │               │               ├─ 第 3 天未修复：升级至团队负责人
        │               │               ├─ 第 7 天未修复：升级至部门负责人
        │               │               └─ 第 14 天未修复：触发资源自动关停或隔离
        │               │
        │               └─ 月度审计：统计未标签资源占比，纳入团队 KPI
```

### 6.1 处理 SLA

| 阶段 | 时间要求 | 责任方 | 输出 |
|------|---------|--------|------|
| 自动推断/补全 | 实时 | 自动化系统 | 审计日志 |
| 首次通知 | T+0 | FinOps 平台 | 告警邮件/工单 |
| Owner 修复 | T+3 | 资源 Owner | 标签补全 |
| 升级至团队负责人 | T+3 | FinOps 分析师 | 升级邮件 |
| 升级至部门负责人 | T+7 | FinOps CoE | 治理报告 |
| 自动关停/隔离 | T+14 | 自动化系统 | 资源状态变更记录 |

---

## 7. 合规检查与报告

### 7.1 月度标签健康度报告

| 指标 | 计算公式 | 目标 | 当前值 |
|------|---------|------|--------|
| Mandatory 标签覆盖率 | 含全部 Mandatory 标签的资源数 / 总资源数 × 100% | ≥ {{MANDATORY_COVERAGE_TARGET}}% | {{CURRENT_MANDATORY_COVERAGE}}% |
| 未标签资源占比 | 缺失任意 Mandatory 标签的资源数 / 总资源数 × 100% | ≤ {{UNTAGGED_TARGET}}% | {{CURRENT_UNTAGGED}}% |
| AAI | 可直接归属成本 / 总基础设施成本 × 100% | ≥ {{AAI_TARGET}}% | {{CURRENT_AAI}}% |
| 受控词表合规率 | 标签值符合受控词表的资源数 / 总带标签资源数 × 100% | ≥ {{CONTROLLED_VOCABULARY_TARGET}}% | {{CURRENT_CONTROLLED_VOCABULARY}}% |

### 7.2 报告受众与频率

| 受众 | 频率 | 内容重点 |
|------|------|---------|
| 工程团队 | 每周 | 本团队未标签资源清单、修复进度 |
| FinOps CoE | 每月 | 全组织覆盖率趋势、AAI、Top 10 问题团队 |
| 财务部门 | 每月 | 按 cost-center 的成本归属准确率 |
| 高级管理层 | 每季度 | 标签成熟度、成本透明度改进、ROI |

---

## 8. 例外管理

| 例外类型 | 批准人 | 有效期 | 记录位置 |
|----------|--------|--------|----------|
| 临时 PoC/Spike 资源 | 团队负责人 | ≤ 30 天 | 豁免清单（YAML/表格） |
| 第三方托管服务 | FinOps CoE | 按合同期 | 供应商清单 |
| 历史遗留资源 | 部门负责人 | ≤ 90 天 | 迁移计划 |
| 安全/合规特殊资源 | CISO 办公室 | 按审计周期 | 合规台账 |

**豁免申请模板**:

```markdown
- 资源 ID: {{RESOURCE_ID}}
- 资源类型: {{RESOURCE_TYPE}}
- 缺失标签: {{MISSING_TAGS}}
- 豁免理由: {{JUSTIFICATION}}
- 申请人: {{APPLICANT}}
- 批准人: {{APPROVER}}
- 有效期至: {{EXPIRATION_DATE}}
- 到期后续动作: {{FOLLOW_UP_ACTION}}
```

---

## 9. 实施检查清单

### 第 1–14 天：策略制定

- [ ] 组建标签治理工作组（FinOps + 平台工程 + 安全 + 财务）
- [ ] 定义 Mandatory / Recommended / Optional 标签集
- [ ] 建立受控词表并在全局标签仓库中注册
- [ ] 确定标签键名与值命名规范
- [ ] 制定缺失标签处理 SLA 与升级路径

### 第 15–30 天：工具落地

- [ ] 在 IaC Pipeline 中集成标签静态检查
- [ ] 配置云厂商 Policy 阻止未标签资源创建
- [ ] 部署运行时标签扫描与自动补全脚本
- [ ] 建立标签合规报告与告警机制
- [ ] 创建豁免申请与审批流程

### 第 31–60 天：试运行与修正

- [ ] 对非生产环境执行标签治理试点
- [ ] 收集团队反馈，修正受控词表与检查规则
- [ ] 生成首份月度标签健康度报告
- [ ] 处理历史未标签资源（补全、关停或豁免）

### 第 61–90 天：全面推广

- [ ] 将策略扩展至生产环境
- [ ] 将 AAI 与标签覆盖率纳入团队 KPI
- [ ] 建立季度策略复审机制
- [ ] 发布《标签治理运营手册》

---

## 10. 参考索引

- FinOps Foundation: [Tagging and Cost Allocation Best Practices](https://www.finops.org/framework/capabilities/allocate/)
- AWS: *Tagging AWS Resources*
- Azure: *Use tags to organize your Azure resources and management hierarchy*
- GCP: *Tagging resources*
- FOCUS 1.0 Specification: <https://focus.finops.org/>

> **交叉引用**:
>
> - FinOps 跨层成本分摊执行模板: [`../cost-allocation-template.md`](../cost-allocation-template.md)
> - FinOps 四级成本分摊模型: [`../finops-allocation-template.md`](../finops-allocation-template.md)
> - FinOps 仪表盘指标模板: [`./finops-dashboard.md`](./finops-dashboard.md)
> - AI 成本分摊模板: [`./ai-cost-allocation.md`](./ai-cost-allocation.md)

> 最后更新: {{LAST_UPDATED}}


---

## 补充说明：FinOps 标签治理策略模板 (Tagging Policy)

## 概念定义

**定义**：跨层复用治理是横跨业务、应用、组件与功能四层，通过过程、标准、度量与自动化手段确保复用资产可持续演进的体系。

## 反例

**反例**：资产库缺乏治理，任何人可随意发布资产，导致目录膨胀、质量参差、消费方难以找到可信资产。

## 权威来源

> **权威来源**:
>
> - [ISO/IEC/IEEE Standards](https://www.iso.org)
> - [FinOps Foundation](https://www.finops.org)
> - 核查日期：2026-07-07

## 分析

**分析**：无治理的复用会退化为克隆，无度量的治理会退化为形式；治理需要与价值量化紧密结合。