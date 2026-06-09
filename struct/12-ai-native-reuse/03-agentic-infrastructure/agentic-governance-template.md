# P5-T2：Agentic Governance 组织设计模板

> **权威来源**：Microsoft Agent Governance Toolkit (AGT) GitHub、OWASP Agentic AI Top 10 (2025.12)、Google SAIF / Agent Gateway
> **版本**：2026-06
> **适用范围**：AI-Native 组织构建 Agent 卓越中心（CoE）及治理体系

---

## 1. Agentic Governance 框架综述

### 1.1 Microsoft AGT 7包体系映射

2026年4月2日，Microsoft 以 MIT 许可证开源 **Agent Governance Toolkit (AGT)**，提供覆盖 Agent 全生命周期的 7 包治理体系：

| 包名 | 核心职责 | 复用映射 |
|------|---------|---------|
| **Agent OS** | 策略引擎（决策延迟 <0.1ms）、实时授权判定 | 作为治理基础设施的"内核"，提供可复用的策略判定服务 |
| **Agent Mesh** | 分布式身份（DID/W3C）、Agent 间安全通信 | 复用身份凭证体系，避免每个 Agent 独立建设身份认证 |
| **Agent Runtime** | 四级特权环（Ring 0-3）、沙箱隔离 | 定义标准运行边界，作为安全复用的前提条件 |
| **Agent SRE** | 可观测性、混沌工程、容量管理 | 复用现有 SRE 体系，叠加 Agent 特有的轨迹追踪（Trace） |
| **Agent Compliance** | 审计日志、合规证据收集 | 与 GRC 平台集成，复用合规检查清单 |
| **Agent Marketplace** | Agent 发现、版本管理、信誉评分 | 作为组织级 Agent 资产目录，支撑复用度量 |
| **Agent Lightning** | 边缘部署、低延迟推理 | 定义边缘-云协同的部署模板 |

**复用原则**：AGT 7 包不是孤立系统，而是**Governance as Code 的分层实现**。Agent OS 的策略引擎和 Agent Runtime 的沙箱是"强制复用层"，所有 Agent 必须接入；Agent SRE 和 Agent Compliance 是"推荐复用层"，可对接现有平台；Agent Marketplace 是"生态复用层"，鼓励组织内共享。

### 1.2 OWASP Agentic AI Top 10 风险-缓解矩阵

2025年12月发布的 OWASP Agentic AI Top 10（ASI01-ASI10）为 Agent 治理提供了风险基线：

| 风险编号 | 风险描述 | 缓解策略 | 复用控制点 |
|----------|---------|---------|-----------|
| ASI01 | 提示注入（Prompt Injection） | 输入验证 + 语义过滤器 | Agent Runtime Ring 1 沙箱 |
| ASI02 | 敏感信息泄露 | 数据分类 + 最小权限 | Agent Mesh DID 属性凭证 |
| ASI03 | 供应链污染 | SBOM + 签名验证 | Agent Marketplace 信誉评分 |
| ASI04 | 权限提升 | 严格子集不变量 | Agent OS 策略引擎 |
| ASI05 | Agent 自主逃逸 | Kill Switch + 行为基线 | Agent SRE 轨迹异常检测 |
| ASI06 | 过度依赖工具调用 | 工具白名单 + 调用审计 | Agent Runtime Ring 2 工具网关 |
| ASI07 | 多 Agent 协作失控 | Mesh 级联策略 | Agent Mesh 通信协议 |
| ASI08 | 输出不可信 | 人类确认环（HITL） | 三层审批流程（见2.2节） |
| ASI09 | 训练数据投毒 | 数据溯源 + 清洗管道 | Agent Compliance 审计日志 |
| ASI10 | 模型窃取/滥用 | API 速率限制 + 水印 | Agent OS 授权判定 |

### 1.3 Google SAIF + Agent Gateway

Google 的 **Secure AI Framework (SAIF)** 强调六个核心原则：

1. **扩展安全基线到 AI 系统**（与现有安全控制对齐）
2. **扩大检测范围**（针对 AI 特有的攻击面）
3. **自动化防御**（利用 AI 对抗 AI 威胁）
4. **协调响应**（跨团队事件响应）
5. **闭环环境控制**（沙箱与数据隔离）
6. **持续适应性评估**

Google Agent Gateway 作为企业级 Agent 入口，提供统一的身份认证、流量管理和策略执行。其与 AGT 的映射关系为：**Agent Gateway ≈ Agent OS + Agent Mesh 的企业集成视图**。

---

## 2. 组织设计模板

### 2.1 Agent 卓越中心（Agent CoE）结构

```
┌─────────────────────────────────────────────┐
│          Agent Governance Board             │
│   (CIO/CTO + CISO + 法务 + 业务负责人)       │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│           Agent CoE 核心层                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │ 架构与标准 │ │ 安全与合规 │ │ 平台与工具 │   │
│  │ (Arch)   │ │ (Sec)    │ │ (Plat)   │   │
│  └──────────┘ └──────────┘ └──────────┘   │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│           Agent 交付团队（分布式）            │
│   业务域A Agent Squad │ 业务域B Agent Squad │
└─────────────────────────────────────────────┘
```

**角色定义**：

- **Agent Architect**：定义 WIT 接口标准、Agent 间契约、Golden Path
- **Agent Security Engineer**：实施 ASI01-ASI10 缓解控制、维护 RBAC 策略
- **Agent Platform Engineer**：运维 Agent Runtime、Marketplace、SRE 仪表盘
- **Agent Product Owner**：负责业务域 Agent 的路线图和价值度量

### 2.2 三层审批流程（人类→Agent→工具）

| 层级 | 审批主体 | 触发条件 | 最大延迟 |
|------|---------|---------|---------|
| **L1：人类审批（HITL）** | 业务负责人/安全官 | 高风险操作（资金转移、数据出境、模型变更） | 4 工作小时 |
| **L2：Agent 自治审批** | Agent OS 策略引擎 | 中风险操作（跨域数据访问、工具调用链 >3） | <100ms |
| **L3：工具级审批** | 工具网关 + 资源 ACL | 所有工具调用 | <10ms |

**流程设计原则**：

- **默认拒绝（Default Deny）**：未明确授权的操作一律拒绝
- **策略下沉**：L3 工具级审批在 Agent Runtime Ring 2 本地执行，不依赖网络调用
- **人类回环保留**：涉及不可逆操作（资金、法律承诺）必须保留人类确认环节

### 2.3 RBAC 策略模板

#### Cedar 策略示例（AWS 开源策略语言）

```cedar
// Agent 主体定义
entity Agent = {
  role: String,
  trustLevel: Int,
  domain: String,
  ephemeralId: String
};

// 资源定义
entity Document = {
  classification: String,  // public/internal/confidential/secret
  ownerDomain: String
};

// 动作定义
action "read", "write", "execute", "delegate" appliesTo {
  principal: Agent,
  resource: Document
};

// 策略：高信任度 Agent 可读取同域内部文档
permit(principal, action == "read", resource)
when {
  principal.trustLevel >= 3 &&
  principal.domain == resource.ownerDomain &&
  resource.classification == "internal"
};

// 策略：禁止 Agent 委托权限给跨域 Agent
forbid(principal, action == "delegate", resource)
when {
  principal.domain != resource.ownerDomain
};
```

#### OPA Rego 示例（Kubernetes + Agent 混合环境）

```rego
package agent.rbac

import future.keywords.if
import future.keywords.in

# 严格子集不变量：Agent 权限必须是人类创建者权限的严格子集
creator_subset(agent_perm, creator_perm) if {
    agent_perm.actions == subset(creator_perm.actions)
    agent_perm.resources == subset(creator_perm.resources)
    agent_perm.scopes == subset(creator_perm.scopes)
}

# 三层审批：检查操作是否已获取必要审批层级
required_approval(operation) = 1 if {
    operation.risk == "low"
}
required_approval(operation) = 2 if {
    operation.risk == "medium"
}
required_approval(operation) = 3 if {
    operation.risk == "high"
}

allow if {
    input.agent.trustLevel >= required_approval(input.operation)
    creator_subset(input.agent.permissions, input.creator.permissions)
    not input.agent.ephemeralId_expired
}
```

### 2.4 Kill Switch 和熔断器设计

| 机制 | 触发条件 | 动作 | 恢复策略 |
|------|---------|------|---------|
| **Agent Kill Switch** | 行为偏离基线 >3σ、检测到越狱尝试 | 立即终止 Agent 进程，吊销 Ephemeral Identity | 人工复核后重启 |
| **域级熔断器** | 跨域错误率 >20%（1分钟窗口） | 切断该域所有对外调用，进入降级模式 | 自动探测恢复（指数退避） |
| **模型级熔断器** | 输出毒性/幻觉率 >阈值 | 切换至备用模型，触发内容审查 | 自动恢复，记录异常 |
| **全局紧急停止** | CISO 或自动化响应系统触发 | 所有 Agent 进入只读模式，锁定工具调用 | 治理委员会手动解除 |

---

## 3. Golden Path for Agents

### 3.1 Agent 开发→测试→部署→监控标准路径

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  设计   │ → │  开发   │ → │  测试   │ → │  部署   │ → │  监控   │
│(WIT+SDD)│   │(代码+策略)│   │(沙箱+红队)│   │(金丝雀) │   │(轨迹+指标)│
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
```

**各阶段复用资产**：

- **设计**：复用组织 WIT 接口目录、ASI 风险检查清单
- **开发**：复用 Agent Runtime SDK、Cedar/OPA 策略模板库
- **测试**：复用红队测试用例库（基于 OWASP ASI01-ASI10）、混沌实验模板
- **部署**：复用 GitOps 流水线（ArgoCD/Flux）、金丝雀发布模板
- **监控**：复用 OpenTelemetry 轨迹采集、Agent SRE 仪表盘

### 3.2 与现有 DevOps/GitOps 流程的集成

| 现有流程 | Agent 增强点 | 复用方式 |
|---------|------------|---------|
| CI 流水线 | 增加 Agent 策略编译（Cedar validate、Rego test） | 复用 Jenkins/GitHub Actions，新增 Agent 专用 Stage |
| CD 流水线 | 增加金丝雀健康检查（Agent 行为基线对比） | 复用 Argo Rollouts，注入 Agent 轨迹验证 |
| IaC | 增加 Agent Runtime 资源配置（Ring 级别、资源配额） | 复用 Terraform/Tofu，提供 Agent Runtime Module |
| 可观测性 | 增加 Agent 轨迹（Agent Trace）维度 | 复用 Grafana/Prometheus/Loki，新增 Agent 仪表盘 |
| 事件响应 | 增加 Agent 自主攻击面 | 复用 PagerDuty/OpsGenie，扩展 Runbook |

---

## 4. 合规映射

### 4.1 EU AI Act 高风险义务检查清单（2026年8月2日生效）

| 义务条款 | 要求 | AGT 映射 | 状态 |
|---------|------|---------|------|
| **Art. 8：风险管理系统** | 建立持续风险评估流程 | Agent Compliance 包 + 审计日志 | ☐ 待实施 |
| **Art. 9：数据治理** | 训练/测试/验证数据的质量管理 | Agent Marketplace SBOM + 数据溯源 | ☐ 待实施 |
| **Art. 10：技术文档** | 提供完整技术文档（SaaS/内部均需） | TechDocs 模板 + Agent 架构决策记录 | ☐ 待实施 |
| **Art. 13：透明度** | 向用户告知其正在与 AI 交互 | Agent Mesh DID 标识 + 交互水印 | ☐ 待实施 |
| **Art. 14：人类监督** | 确保有效人类监督机制 | 三层审批 L1 HITL | ☐ 待实施 |
| **Art. 15：准确性/鲁棒性/安全性** | 达到适当水平的准确性 | Agent SRE 基线监控 + 红队测试 | ☐ 待实施 |
| **Art. 52：深度伪造披露** | 深度伪造内容必须标注 | Agent Runtime 输出过滤器 | ☐ 待实施 |

### 4.2 FCA/SEC 监管要求对照

| 监管领域 | 核心要求 | Agent 治理映射 |
|---------|---------|---------------|
| **FCA AI 透明度** | 金融决策可解释、可审计 | Agent Trace 全链路记录 + 决策归因 |
| **SEC 投资顾问合规** | AI 生成的投资建议需人类复核 | 三层审批 L1 强制触发 |
| **SEC 网络安全规则** | 及时披露重大网络安全事件 | Agent SRE 异常检测 → 自动化事件上报 |
| **模型风险管理** | 模型验证、独立审核 | Agent CoE 架构与标准组独立审核 |

---

## 5. 实施路线图建议

| 阶段 | 时间 | 目标 | 关键交付 |
|------|------|------|---------|
| **Phase 1：基础治理** | 0-3月 | 建立 Agent CoE、部署 Agent OS 策略引擎 | RBAC 策略基线、Kill Switch 机制 |
| **Phase 2：规模化** | 3-6月 | 接入 AGT 7包、上线 Marketplace | Golden Path 模板、目录覆盖 >50% |
| **Phase 3：合规就绪** | 6-9月 | EU AI Act 高风险义务满足 | 审计证据链、技术文档模板 |
| **Phase 4：持续优化** | 9-12月 | 自动化红队、自适应策略 | 策略自优化闭环、ASI 覆盖率 100% |

---

## 参考文献

1. Microsoft Agent Governance Toolkit (AGT), GitHub, MIT License, 2026-04-02
2. OWASP Agentic AI Top 10, 2025-12, <https://owasp.org/www-project-agentic-ai/>
3. Google SAIF (Secure AI Framework), <https://saif.google>
4. Google Agent Gateway, Cloud Enterprise AI Infrastructure
5. EU AI Act Regulation (EU) 2024/1689, High-Risk System Obligations
6. FCA DP24/4: Artificial Intelligence and Machine Learning
7. SEC Release No. 34-100822: Predictive Data Analytics
