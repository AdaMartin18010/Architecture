# 云原生架构复用模式

> **版本**: 2026-07-07
> **定位**: 应用架构层云原生模式（服务网格、网关、容器化、Serverless、可观测性）的可复用设计指南
> **对齐标准**: NIST SP 800-204 系列、Kubernetes Gateway API、SLSA 1.2

---

## 概念定义

**定义**：云原生架构复用模式是在容器化、微服务、不可变基础设施与声明式 API 基础上，将通用能力（服务发现、流量治理、安全策略、可观测性）封装为可跨应用复用的平台级资产。

## 示例

**示例**：某电商平台通过服务网格（Istio/Linkerd）将 mTLS、熔断、重试、流量镜像能力下沉到平台层，20+ 微服务无需修改业务代码即可获得统一通信治理。

## 反例

**反例**：团队将 Kubernetes YAML、Istio VirtualService 与业务部署脚本混放在应用仓库，导致每个服务重复定义相似策略，升级平台能力时需逐个仓库修改。

## 目录

- [云原生架构复用性雷达矩阵](reusability-matrix-2026.md)
- [微服务安全架构（NIST SP 800-204）](nist-sp-800-204-microservices-security.md)

## 权威来源

> **权威来源**:
>
> - [NIST SP 800-204, Security Strategies for Microservices-based Application Systems](https://csrc.nist.gov/publications/detail/sp/800-204/final)
> - [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io)
> - [Istio Service Mesh](https://istio.io)
> - [CNCF Cloud Native Definition](https://github.com/cncf/toc/blob/main/DEFINITION.md)
>
> **核查日期**: 2026-07-07

## 交叉引用

- [03 应用架构复用总览](../README.md)
- [分层架构复用](../01-layered-architecture/layered-architecture-reuse.md)
- [服务网格通信模式](../08-service-mesh/service-mesh-communication-patterns.md)