# Gateway API v1.5 + GAMMA + Service Mesh 权威对齐（2025‑2026）

> **定位**：Kubernetes 网络与服务网格层的最新标准基准，指导云原生组件复用中的流量管理策略。
> **权威来源**：Kubernetes SIG Network、Gateway API 官方文档、Istio/Cilium/Linkerd 项目博客。

---

## 1. 关键结论（TL;DR）

| 标准/项目 | 最新状态 | 核心意义 |
|-----------|----------|----------|
| **Gateway API v1.5** | 2026‑02 发布，最大 GA 版本 | ListenerSet、TLSRoute、CORS Filter、Client Cert Validation 全部进入 Standard 通道 |
| **GAMMA** | Gateway API 子项目，Experimental | 将 HTTPRoute/GRPCRoute 附加到 **Service**（非 Gateway），统一东西/南北向流量 |
| **SMI** | 实质上被 GAMMA 取代 | 2022 年 SMI 社区正式加入 GAMMA；无独立重大发布 |
| **Istio Ambient** | GA (1.24+)；1.27 多集群 Ambient Alpha | Sidecar-less：Ztunnel (L4) + Waypoint Proxy (L7)；mTLS 延迟开销 8% vs sidecar 166% |
| **Cilium** | 1.19 最新稳定；1.18 支持 Gateway API v1.3 + GAMMA | eBPF L3/L4 + 共享 Envoy L7；Cluster Mesh 多集群 |
| **Linkerd** | 2.19 稳定；2.20+ 原生 Sidecar GA | 后量子密码、FIPS 140-3；HTTPRoute 作为 AuthorizationPolicy targetRef |

---

## 2. Gateway API 版本时间线

```
v1.0  (2023-10)  Gateway/GatewayClass/HTTPRoute 进入 v1 Stable
v1.1  (2024-05)  Service Mesh 支持；GRPCRoute Standard
v1.2  (2024-11)  WebSockets、Timeouts、Retries
v1.3  (2025-06)  Request Mirroring、CORS Filter、Gateway Merging、BackendTLSPolicy (Experimental)
v1.4  (2025-10)  BackendTLSPolicy (Standard)、supportedFeatures、Mesh resource (Experimental)
v1.5  (2026-02)  **最大 GA 版本**：ListenerSet、TLSRoute、CORS Filter、Client Cert Validation、Certificate Selection、ReferenceGrant → Standard
```

### 2.1 发布模式变化（v1.5+）

Gateway API 采用**发布列车模式**（类似 Kubernetes）：

- **Standard 通道**：4 个月发布周期
- **Experimental 快照**：每月发布（`monthly-2026.05` 等）
- 功能在冻结日就绪则上车；文档未就绪则等待下一班

### 2.2 合规实现（v1.4+）

截至 2025 末，**7 个实现**通过 Gateway API v1.4 合规测试：

- Envoy Gateway、GKE Gateway、Istio、kgateway、Traefik Proxy、Agent Gateway、Airlock Microgateway

---

## 3. GAMMA：Gateway API for Mesh

### 3.1 核心概念

Gateway API 原本为南北向（ingress）设计。**GAMMA** 将其语义扩展到**东西向（服务间）流量**，允许 Route 资源附加到 **Kubernetes Service** 作为 `parentRef`。

```yaml
# GAMMA 风格 HTTPRoute（东西向）
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: color-canary
  namespace: faces
spec:
  parentRefs:
    - name: color        # ← 引用 Service，非 Gateway
      kind: Service
      group: ""
      port: 80
  rules:
  - backendRefs:
    - name: color
      port: 80
      weight: 50
    - name: color2
      port: 80
      weight: 50
```

### 3.2 Producer vs. Consumer Routes

- **Producer Route**：Route 与 Service **同命名空间**；服务所有者定义入站规则。无需 ReferenceGrant。
- **Consumer Route**：Route 在 Service **不同命名空间**；消费者定义调用方式。需要 ReferenceGrant 授权。

### 3.3 当前状态

- GAMMA 在 v1.4/v1.5 中仍处于 **Experimental 通道**
- `Mesh` 资源配置实验性引入（v1.4）
- Cilium 1.18 起支持 GAMMA reconciler（多 HTTPRoute per Service）

---

## 4. Service Mesh 现状：Sidecar vs Sidecar-less

### 4.1 三种架构对比

| 维度 | Istio Ambient | Cilium (eBPF) | Linkerd (Sidecar) |
|------|---------------|---------------|-------------------|
| **L4 处理** | Ztunnel (每节点，用户空间) | eBPF + WireGuard (内核) | Rust micro-proxy (每 Pod) |
| **L7 处理** | Waypoint Proxy (每服务账号) | 每节点共享 Envoy | 每 Pod Rust proxy |
| **mTLS 延迟开销** | ~8% | ~99% (WireGuard) | 低 |
| **内存成本** | ~26MB/节点 | ~95MB/节点 | ~30MB/Pod |
| **规模上限** | 50K pods 稳定测试 | 1K+ 节点 API server 压力 | 中等规模 |
| **最佳场景** | 大规模混合 L4/L7 | 纯 L3/L4、<500 节点 | 极简运维、合规隔离 |

### 4.2 eBPF 的影响

eBPF 正在变成**云原生 2.0 的基础设施**，但**不是用户空间代理的完整替代**：

- L3/L4：eBPF 完全替代 iptables/kube-proxy
- L7：仍需 Envoy 等用户空间代理
- **混合模型**（eBPF for L4 + 用户空间 for L7）正在胜出

---

## 5. 多集群网络

### 5.1 Multi-Cluster Services (MCS) API

- 状态：Beta（KEP-1645）
- CRD：`ServiceExport`、`ServiceImport`
- DNS：`<svc>.<ns>.svc.clusterset.local`

### 5.2 Gateway API + 多集群 (GEP-1748)

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: rebel-base-mcsapi
spec:
  parentRefs:
  - kind: Gateway
    name: my-gateway
  rules:
  - backendRefs:
    - group: multicluster.x-k8s.io
      kind: ServiceImport      # ← 多集群后端
      name: rebel-base
      port: 80
```

- GEP-1748 状态：Experimental
- GKE 已有生产级多集群 Gateway controller
- Cilium Cluster Mesh 提供独立于 MCS 的全球服务发现

---

## 6. 安全：mTLS 自动化与 SPIFFE/SPIRE

### 6.1 服务网格自动 mTLS

- **Istio**：Auto-mTLS（sidecar 和 ambient）
- **Cilium**：WireGuard pod-to-pod 加密
- **Linkerd**：自动 mTLS；2.19 引入后量子密码

### 6.2 SPIFFE/SPIRE (CNCF Graduated)

- SPIRE Agent 证明工作负载（K8s service account、容器镜像等）
- SPIRE Server 颁发 **SPIFFE ID** + 短期 X.509 证书
- **服务网格集成**：
  - Istio：通过 SDS 集成 SPIRE
  - Cilium：Cilium Network Policy 可引用 SPIFFE ID
  - Envoy/HAProxy：原生支持 SPIFFE/SPIRE

**收益**：消除静态证书和手动轮换；实现跨集群的零信任工作负载身份。

---

## 7. 平台工程与组件复用意义

### 7.1 可复用流量管理模式

Gateway API 的**角色导向设计**使平台团队能提供自服务网络：

| 角色 | 资源 | 复用模式 |
|------|------|----------|
| 基础设施提供商 | GatewayClass | 定义批准的控制器类型（如 "internal-l7"、"public-l7"） |
| 集群运维 | Gateway | 配置 TLS、IP、监听器；团队附加路由 |
| 应用开发者 | HTTPRoute/GRPCRoute | 附加到 Gateway 或 Service (GAMMA)；定义金丝雀、重试、认证 |

### 7.2 Golden Path 策略包

平台团队可创建**可复用策略包**：

- 标准 HTTPRoute 模板（重试预算、CORS、超时默认）
- GAMMA Producer Route 作为命名空间级服务默认值
- ReferenceGrant 模板实现安全的跨命名空间服务消费
- BackendTLSPolicy 强制网关到后端的 TLS

### 7.3 组件复用使能器

1. **API 可移植性**：单个 HTTPRoute 跨 Envoy Gateway、Istio、Cilium、Traefik、GKE 工作 —— 减少供应商锁定
2. **关注点分离**：Gateway 所有者管理 TLS 和入口；应用团队管理路由规则，无需 cluster-admin
3. **Mesh + Ingress 融合**：相同 API 技能适用于南北向和东西向流量
4. **Sidecar-less**：降低 "mesh tax"，使服务网格成为更多工作负载的默认平台能力
5. **SPIFFE/SPIRE**：身份和安全策略跨集群可移植

---

## 8. 选型决策框架

| 场景 | 推荐 |
|------|------|
| Greenfield 简单 L7 Ingress | Gateway API + Envoy Gateway 或 Cilium Gateway API |
| Ingress + Service Mesh, <500 节点 | Cilium（CNI + Gateway API + GAMMA Mesh 一体） |
| 大规模、多集群、企业级 | Istio Ambient（最佳多集群、成熟生态） |
| 最大 simplicity、最小开销 | Linkerd（成熟 sidecar、最易运维） |
| 高合规 / 隔离要求 | Istio sidecar 模式（每 Pod 隔离、成熟工具） |
| AI/ML 工作负载、内核可观测性 | Cilium（eBPF + Hubble 零插桩可观测性） |

### 迁移路径

1. **立即**：Gateway API 替代 Ingress + 供应商特定 API
2. **短期**：在新服务上实验 GAMMA 东西向流量
3. **中期**：评估 sidecar-less 选项（Istio Ambient 或 Cilium）降低 mesh 开销
4. **长期**：Gateway API 标准化覆盖 ingress、mesh、多集群（GEP-1748）

---

## 9. 权威来源

| 资源 | URL |
|------|-----|
| Gateway API v1.5 Blog | <https://kubernetes.io/blog/2026/04/21/gateway-api-v1-5/> |
| Gateway API v1.4 Blog | <https://kubernetes.io/blog/2025/11/06/gateway-api-v1-4/> |
| GAMMA Initiative | <https://gateway-api.sigs.k8s.io/mesh/gamma/> |
| GEP-1748 (Multi-cluster) | <https://gateway-api.sigs.k8s.io/geps/gep-1748/> |
| Istio Roadmap 2025 | <https://istio.io/latest/blog/2025/roadmap/> |
| Cilium 1.18 | <https://isovalent.com/blog/post/cilium-1-18/> |
| Linkerd 2.19 | <https://linkerd.io/2025/10/31/announcing-linkerd-2-19/> |
| SMI → GAMMA (2022) | <https://smi-spec.io/blog/announcing-smi-gateway-api-gamma/> |
| SPIFFE/SPIRE | <https://spiffe.io> |

---

*文档生成时间：2026-06-06 · 对齐 Gateway API v1.5 / GAMMA / Istio Ambient / Cilium 1.19 / Linkerd 2.19*
