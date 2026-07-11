# Gateway API + Istio Ambient 可复用部署模板

> **定位**：云原生网络组件复用的可执行基线，覆盖 ingress、mesh、安全、多集群模式。
> **对齐**：Gateway API v1.5、Istio Ambient 1.24+、GAMMA Initiative。

---

## 1. 示例清单

| 文件 | 说明 |
|------|------|
| `istio-ambient-gateway-api-kind.yaml` | Kind 集群最小可运行部署；含 GatewayClass、Gateway、HTTPRoute、金丝雀、GAMMA Producer Route、AuthorizationPolicy、BackendTLSPolicy |

---

## 2. 快速开始

### 前提

- [kind](https://kind.sigs.k8s.io/) 或 minikube
- [kubectl](https://kubectl.docs.kubernetes.io/)
- [istioctl](https://istio.io/latest/docs/setup/getting-started/)

### 部署步骤

```bash
# 1. 创建 Kind 集群
cat > kind-config.yaml <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
EOF
kind create cluster --config kind-config.yaml

# 2. 安装 Gateway API CRDs (v1.2 Standard)
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.0/standard-install.yaml

# 3. 安装 Istio Ambient
istioctl install --set profile=ambient -y

# 4. 部署示例
kubectl create namespace payment
kubectl apply -f istio-ambient-gateway-api-kind.yaml

# 5. 验证
kubectl get gateway
kubectl get httproute
kubectl get authorizationpolicy
```

---

## 3. 可复用模式

### 3.1 平台团队发布的 Golden Path

| 模板 | 复用价值 |
|------|----------|
| **GatewayClass 模板** | 定义批准的控制器类型（`istio`、`envoy`、`cilium`） |
| **HTTPRoute 标准模板** | 重试预算、CORS、超时默认值内建 |
| **GAMMA Producer Route** | 命名空间级服务默认路由策略 |
| **ReferenceGrant 模板** | 安全的跨命名空间服务消费授权 |
| **BackendTLSPolicy 模板** | 强制网关到后端 TLS |
| **AuthorizationPolicy 模板** | 基于服务身份的零信任访问控制 |

### 3.2 应用团队消费方式

```yaml
# 应用团队只需填写业务相关的路由规则
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-app-route
spec:
  parentRefs:
    - name: public-gateway  # 平台提供
  hostnames:
    - "my-app.example.com"
  rules:
    - backendRefs:
        - name: my-app-service
          port: 8080
```

---

## 4. 与项目结构的映射

| 项目目录 | 云原生网络角色 |
|----------|----------------|
| `struct/04-component-architecture-reuse/` | HTTPRoute/BackendTLSPolicy = 可复用网络组件 |
| `struct/06-cross-layer-governance/` | AuthorizationPolicy = 跨层安全治理 |
| `struct/10-supply-chain-security/` | mTLS + SPIFFE = 零信任供应链安全 |
| `struct/13-emerging-trends/` | Ambient Mesh / eBPF = 前沿网络架构 |

---

*文档生成时间：2026-06-06 · 对齐 Gateway API v1.5 / Istio Ambient / GAMMA*


---

## 补充说明：Gateway API + Istio Ambient 可复用部署模板

## 概念定义

**定义**：组件架构复用是在模块/组件层面复用设计模式、接口契约、依赖管理与版本策略，以实现代码级与二进制级的高效复用。

## 示例

**示例**：团队将日志、配置、缓存、健康检查等横切关注点封装为内部 SDK 组件，各微服务通过引入统一版本依赖复用，减少重复代码。

## 反例

**反例**：项目直接复制开源库源码到代码库，未通过包管理器跟踪版本与漏洞，导致安全补丁无法及时同步。

## 权威来源

> **权威来源**:
>
> - [CNCF](https://www.cncf.io)
> - [OpenSSF](https://openssf.org)
> - 核查日期：2026-07-07

## 分析

**分析**：组件复用关注依赖管理、接口稳定性与供应链安全，是现代软件工程的基础能力。
