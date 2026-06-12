# NIST SP 800-204 微服务安全策略与架构复用
>
> 版本: 2026-06-06
> 对齐来源: NIST SP 800-204/204A/204B/204C/204D (2025-02 更新), Tetrate 技术博客, PCI DSS 4.0 参考

## 1. NIST SP 800-204 系列概览

| 出版物 | 主题 | 核心贡献 |
|-------|------|---------|
| **SP 800-204** | 微服务安全策略 | 技术背景、威胁分析、核心安全特性 |
| **SP 800-204A** | 服务网格架构 | Kubernetes + Istio 参考平台、数据平面/控制平面 |
| **SP 800-204B** | ABAC 访问控制 | 基于属性的细粒度授权、NGAC 模型 |
| **SP 800-204C** | DevSecOps 实施 | 五种代码类型、C-ATO 持续授权 |
| **SP 800-204D** | 供应链安全集成 | CI/CD 流水线中的软件供应链安全 |
| **SP 800-233** | 服务网格代理模型 | 云原生应用代理架构 |

## 2. 微服务设计驱动因素与安全原则

### 2.1 四大设计驱动

1. **单一功能（Single Function）**：每个微服务在限定上下文内运行单一功能
2. **生命周期独立（Lifecycle Independence）**：服务间解耦，独立开发部署
3. **容忍持续故障与恢复（Constant Failure & Recovery）**：面向状态lessness 设计
4. **复用可信的状态管理服务（Reuse Trusted Services for State）**

### 2.2 衍生的设计原则

| 原则 | 复用含义 |
|-----|---------|
| **自治（Autonomy）** | 服务独立演进，内部实现可替换 |
| **可发现性（Discoverability）** | 服务注册中心支持动态复用 |
| **容错（Fault Tolerance）** | 熔断器、重试、超时模式复用 |
| **可复用性（Reusability）** | 核心服务（认证、日志、配置）跨应用复用 |
| **可组合性（Composability）** | 微服务编排为更高阶业务能力 |
| **松耦合（Loose Coupling）** | 接口契约稳定，实现细节隐藏 |
| **API 与业务流程对齐** | 领域驱动设计（DDD）的边界上下文 |

## 3. 核心安全特性（MS-SS 系列策略）

### 3.1 认证（MS-SS-1）

- **禁止单独使用 API Key**：认证令牌必须数字签名或由权威源验证
- **令牌类型**：Handle-based、Signed、HMAC 保护
- **API Key 范围限制**：范围与应用和 API 集合匹配，与保证级别相称
- **无状态令牌**：过期时间尽可能短；密钥为动态环境变量，存储于数据保险箱（Data Vault）

### 3.2 访问管理（MS-SS-2）

- 策略定义于**访问服务器**，边缘网关执行粗粒度策略，靠近微服务处执行细粒度策略
- 缓存策略数据仅在访问服务器不可用时使用，需设置合适过期策略
- 访问决策通过**标准化令牌**（OAuth 2.0）以**平台无关格式**（JSON）传递
- 内部授权令牌遵循**最小权限原则**

### 3.3 服务发现（MS-SS-3）

- 服务注册功能应在专用服务器或服务网格上运行
- 服务注册网络需高可用和弹性
- 注册通信必须安全
- **禁止服务自注册/自注销**：采用第三方注册模式，注册更新依赖健康检查
- 大型应用使用分布式注册时需确保数据一致性

### 3.4 安全通信（MS-SS-4）

- 外部客户端入站调用通过**网关 URL** 路由，不直接访问单个微服务
- 服务间通信默认使用 **mTLS**

### 3.5 可用性与弹性（MS-SS-5 ~ MS-SS-7）

- 负载均衡、限流、熔断器模式
- 重试与超时策略
- 故障注入与处理

### 3.6 限流（MS-SS-8）

- 基于**基础设施**和**应用需求**双维度设置限制
- 定义明确的 **API 使用计划**
- 高安全微服务必须实现**重放检测（Replay Detection）**

### 3.7 新版本完整性保证（MS-SS-9）

- 蓝绿部署时，流量通过**中心节点**路由以监控过渡风险
- 基于**使用监控**和**性能/功能正确性评估**逐步增加新版本流量
- 考虑客户端对特定版本的偏好

### 3.8 会话持久性（MS-SS-10）

- 客户端会话数据必须安全存储
- 绑定服务器信息受保护
- 内部授权令牌**不得返回给用户**；用户会话令牌**不得超出网关**用于策略决策

### 3.9 凭证滥用防护（MS-SS-11）

- 运行时预防优于离线策略：设定阈值，在既定时间窗口内认证尝试次数超限触发预防措施
- **凭证填充检测**：对照被盗凭证数据库检查用户登录，警告合法用户
- 文件上传和容器内存/文件系统扫描驻留恶意软件

## 4. 参考平台：Kubernetes + Istio

### 4.1 服务网格组件

| 组件 | 功能 |
|-----|------|
| **数据平面（Data Plane）** | Envoy 代理实例集合，作为 Sidecar 与每个服务实例并排部署；也可作为 Ingress/Egress Controller |
| **控制平面（Control Plane）** | 控制和配置整个网格的数据平面行为 |

### 4.2 数据平面能力

- **认证与授权**：证书生成、密钥管理、黑白名单、SSO 令牌、API Key
- **安全服务发现**：专用服务注册表
- **安全通信**：mTLS、加密、动态路由生成、多协议支持与协议转换
- **网络弹性**：熔断器、重试、超时、故障注入/处理、负载均衡、故障转移、限流、请求镜像
- **可观测性/监控数据**：日志、指标、分布式追踪

### 4.3 Ingress Controller

- 所有客户端的**统一外部 API**，屏蔽服务网格内部 API
- 协议转换：HTTP/S → RPC/gRPC/REST
- 入站请求分解为多个服务调用的**结果组合**
- 负载均衡、公共 TLS 终止

### 4.4 Egress Controller

- 集中式**白名单外部工作负载**（主机和 IP）
- 内部/外部身份凭证交换，隔离外部凭证
- 协议转换回 Web 友好协议

## 5. 五种代码类型与 DevSecOps

SP 800-204C 将云原生应用环境涉及的源码分为五类：

1. **Application Code**：业务逻辑
2. **Application Services Code**：服务网格、API 网关等基础设施代码
3. **Infrastructure as Code**：Terraform、CloudFormation、Crossplane 等
4. **Policy as Code**：OPA、Kyverno 等安全策略
5. **Observability as Code**：监控、告警、SLO 定义

> **复用视角**：第 2–5 类代码是跨应用的标准化复用资产，构成内部平台的核心交付物。

## 6. ABAC 与服务网格（SP 800-204B）

### 6.1 为什么 ABAC 适合微服务

- **可扩展性**：满足云原生应用大规模变量集的精度需求
- **表达性**：策略以主体、客体、环境属性的逻辑表达式表示，无需绑定特定主体或客体
- **先验无关性**：无需预先了解大量用户和资源即可表达策略

### 6.2 NIST NGAC（Next Generation Access Control）

- 标准化的 ABAC 模型表示
- 在服务网格中实现细粒度动态认证与授权

## 7. 与零信任架构（ZT）的关系

SP 800-204 系列与 SP 800-207（零信任架构）形成互补：

- **SP 800-207**：企业级零信任原则（不分具体技术）
- **SP 800-204 系列**：微服务/云原生场景的具体实现指南

## 8. 参考索引

- NIST SP 800-204: *Security Strategies for Microservices-based Application Systems* (2019, Updated 2025)
- NIST SP 800-204A: *Building Secure Microservices-Based Applications Using Service Mesh Architecture*
- NIST SP 800-204B: *Attribute-based Access Control for Microservices-based Applications Using a Service Mesh*
- NIST SP 800-204C: *Implementation of DevSecOps for a Microservices-based Application with Service Mesh*
- NIST SP 800-204D: *Strategies for the Integration of Software Supply Chain Security in DevSecOps CI/CD Pipelines*
- NIST SP 800-233: *Service Mesh Proxy Models for Cloud-Native Applications*
- NIST SP 800-207: *Zero Trust Architecture*
- PCI DSS 4.0 实施参考
