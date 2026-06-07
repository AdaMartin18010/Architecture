# 平台工程与内部开发者平台（IDP）复用
>
> 版本: 2026-06-06
> 对齐来源: CNCF Platforms White Paper、CNCF TAG App Delivery Maturity Model、Platform Engineering 2025 峰会、Team Topologies

## 1. 定义与演进

### 1.1 平台工程（Platform Engineering）

> "Platform engineering is a discipline focused on building and maintaining software development platforms that provide self-service for ..."
> — CNCF Blog, 2025-11-19

平台工程是 DevOps 的自然演进：

- **DevOps**：打破开发与运维壁垒，让团队自主拥有服务
- **平台工程**：将 DevOps 最佳实践打包为**托管内部产品**，使每位开发者无需从零实现基础设施

### 1.2 内部开发者平台（IDP）

IDP 是平台团队构建和维护的软件系统，为开发者提供：

- 基础设施自助配置
- CI/CD 流水线
- 可观测性
- 密钥管理
- 部署自动化

## 2. 关键概念

### 2.1 Golden Path（黄金路径）

- **定义**：针对常见工程任务的**有主见、预批准的工作流**
- **包含**：仓库结构、CI 流水线、K8s manifest/Helm Chart、监控告警、SLO、安全默认配置
- **原则**：非强制，但设计为最简单完整的路径，开发者自愿选择

### 2.2 最薄可行平台（Thinnest Viable Platform, TVP）

源自 *Team Topologies*（Skelton & Pais）：
> "A TVP is a careful balance between keeping the platform small and ensuring that the platform is helping to accelerate and simplify software delivery."

### 2.3 平台即产品（Platform as a Product）

2025 年的核心洞察：**"If you are not doing platform as a product, you're not really yet doing platform engineering."**

- 专职产品经理
- 完整文档与客户成功支持
- 新功能内部营销
- 用户调研与满意度追踪
- 发布说明与持续改进

## 3. CNCF 平台工程成熟度模型（5 级）

| 级别 | 名称 | 特征 |
|-----|------|------|
| **Level 1** | Reactive Operations | 无专职平台团队；资深工程师非正式承担基础设施；部署流程团队各异；入职需数周 |
| **Level 2** | Centralized Tooling | 小平台团队管理共享工具；体验非自助；仍需工单/Slack 请求；平台团队是瓶颈 |
| **Level 3** | Self-Service Paved Roads | 自助能力覆盖常见工作流；Golden Path 存在；入职时间降至天数 |
| **Level 4** | Product-Led Platform | 平台作为内部产品管理：路线图、SLA、用户研究、采用指标；认知负荷被测量并下降 |
| **Level 5** | Autonomous Delivery | 开发者每日多次持续部署；AI 辅助工具建议优化；成本/安全/合规嵌入开发工作流；平台成为竞争优势 |

> 大多数组织可在 **6–12 个月**内从 Level 1 升至 Level 3。

### 3.1 Level 3 详细特征

- **内在牵引（Intrinsic Pull）**：用户因平台价值自愿使用，而非外部强制
- **跨能力一致性**：使用一项能力后，用户预期其他能力体验一致
- **开放论坛与路线图**：用户反馈、共享路线图、开放对话
- **付费意愿**：应用/产品团队愿意通过 chargeback 为平台能力付费

## 4. 现代 IDP 组件架构

### 4.1 自助基础设施

- **实现**：Terraform / Pulumi / Crossplane 模板
- **原则**：不给开发者原始 Terraform，而是提供经过测试、体现组织标准的 opinionated 模块
- **效果**：环境配置从 3–5 天降至 15 分钟

### 4.2 GitOps 与持续交付

- ArgoCD / Flux 将声明式状态从 Git 同步到运行环境
- 每次生产变更 = Git commit，可审计、可回滚
- **合规优势**：审计员最清晰的控制演示路径

### 4.3 开发者门户（Developer Portal）

- **Backstage**：1400+ 组织采用，CNCF 孵化的开源标准
- **替代方案**：Port、Cortex
- **作用**：统一发现服务、创建新服务、查看部署状态、成本与性能数据、文档

### 4.4 可组合架构（Composable Architecture）

> "现代平台团队构建可组合平台：每项能力作为独立服务，通过清晰 API 交付。"

- CI 是一个服务；密钥管理是另一个；部署是另一个；可观测性是另一个
- 不同成熟度团队各取所需，无需妥协

## 5. 2025–2026 关键趋势

### 5.1 AI 成为平台的一部分

- AI 辅助代码审查：在人工审查前识别安全漏洞
- AI 成本建议：基于实际利用率推荐 right-sizing
- AI 生成流水线：从仓库上下文生成 CI/CD 配置
- AI 生成 Runbook：从服务遥测自动生成运维手册
- 智能告警：建议根因，而非仅触发原始告警

### 5.2 Crossplane 毕业（2025-11）

- CNCF 毕业项目：用 Kubernetes API 管理云基础设施的"控制平面构建框架"
- **案例**：American Family Insurance 用 Crossplane "将基础设施作为产品提供"
- **核心能力**：多云环境（AWS/GCP/Azure）统一 Kubernetes API 管理

### 5.3 Knative 毕业（2025-10）

- Kubernetes 上的 Serverless / 事件驱动应用层
- FaaS 自动扩缩容

### 5.4 Backstage 贡献量翻倍

- 开发者门户的 momentum 最强
- 成为内部平台的主要界面

## 6. 架构复用视角

### 6.1 平台能力作为可复用资产

| 能力层 | 复用资产 | 交付形式 |
|-------|---------|---------|
| 计算运行时 | 容器平台、Serverless 框架 | Cluster 模板、Knative Service |
| 数据层 | 数据库、消息队列、缓存 | Crossplane Composition |
| 可观测性 | 日志、指标、追踪、告警 | Grafana Dashboard as Code |
| 安全 | IAM、网络策略、密钥管理 | OPA Policy、Cert-Manager |
| 交付 | CI/CD、GitOps、部署策略 | Golden Path 模板 |

### 6.2 Golden Path 模板库

```text
Golden Path Library
├── backend-service/
│   ├── java-spring-boot/
│   ├── go-microservice/
│   └── rust-axum/
├── data-pipeline/
│   ├── kafka-streams/
│   └── spark-batch/
├── ml-inference/
│   ├── tensorflow-serving/
│   └── onnx-runtime/
└── edge-gateway/
    └── wasmcloud-component/
```

## 7. 实施路线图

| 阶段 | 时间 | 目标 |
|-----|------|------|
| Phase 1 | Weeks 1–4 | 发现摩擦点：观察开发者工作，识别等待和求助点 |
| Phase 2 | Months 1–3 | 构建最小可行平台：自动化最高摩擦工作流 |
| Phase 3 | Months 3–6 | 扩展 Golden Path：覆盖最常见工作负载，内置安全与可观测性 |
| Phase 4 | Months 4–8 | 添加门户层：Backstage 统一发现与操作界面 |
| Phase 5 | Ongoing | 度量与迭代：DORA 指标、开发者满意度、上线时间 |

## 8. 参考索引

- CNCF: "Platforms White Paper" (tag-app-delivery.cncf.io)
- CNCF TAG App Delivery: "Platform Engineering Maturity Model" (2024)
- Team Topologies: Skelton & Pais (2019, 2022 update)
- Evan Bottcher: "Platform Engineering" (ThoughtWorks, 2018)
- Platform Engineering 2025 Summit 资料
- Backstage: [backstage.io](https://backstage.io)
- Crossplane: [crossplane.io](https://crossplane.io)
