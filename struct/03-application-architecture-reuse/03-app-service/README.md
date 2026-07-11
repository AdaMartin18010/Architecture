# 03 应用服务复用

> **版本**: 2026-06-12
> **定位**: 03-application-architecture-reuse / 03-app-service
> **对齐标准**: SOA, OASIS SOA Reference Architecture, NIST SP 800-204

---

## 核心内容

- 应用服务复用模式（服务目录、API 网关、门面、组合服务）
- 应用服务与微服务复用的关系与边界
- 服务契约与 SLA 治理

---

## 文档导航

| 文件 | 主题 |
|:---|:---|
| `app-service-reuse-patterns.md` | 应用服务复用模式与检查清单 |
| `service-reuse-decision-checklist.md` | 服务复用决策检查清单 |

---

## 关联主题

- `02-business-architecture-reuse/05-business-service-reuse/` — 业务服务复用
- `03-application-architecture-reuse/02-microservices/` — 微服务架构复用模式
- `03-application-architecture-reuse/08-service-mesh/` — 服务网格通信复用


---

## 补充说明：03 应用服务复用

## 概念定义

**定义**：应用服务复用是在应用层将通用能力（如认证、通知、支付、搜索）封装为服务目录，通过 API 网关与服务契约实现跨应用复用。

## 示例

**示例**：企业通过 API 网关暴露统一的支付服务，移动 App、Web 端与合作伙伴系统均调用同一服务，确保支付逻辑与合规要求一致。

## 反例

**反例**：各应用自行实现支付逻辑，导致费率计算、对账与风控规则不一致，财务审计困难。

## 权威来源

> **权威来源**:
>
> - [NIST](https://www.nist.gov)
> - [OASIS SOA Reference Architecture](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=soa-rm)
> - 核查日期：2026-07-07

## 分析

**分析**：应用服务复用的收益与治理成本成正比，需要通过服务目录、SLA 与成熟度评估控制范围。
