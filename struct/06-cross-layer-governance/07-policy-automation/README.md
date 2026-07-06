# 07 策略自动化（Policy Automation）

> **版本**: 2026-06-12
> **定位**: 06-cross-layer-governance / 07-policy-automation
> **对齐标准**: OPA (Open Policy Agent), Sentinel, Cedar, NIST SP 800-53, ISO/IEC 42001:2023

---

## 核心概念

策略自动化将跨层治理规则（安全、合规、成本、质量、复用准入）编码为**可执行、可审计、可版本控制**的策略。它使治理从“人工检查”转变为“自动门禁”，从而在大规模复用场景中保持一致性。

| 策略类型 | 关注点 | 典型规则示例 |
|:---|:---|:---|
| **安全策略** | 组件/服务准入、漏洞阈值 | 禁止引入 CVSS ≥ 7.0 的依赖 |
| **合规策略** | 许可证、数据主权、行业法规 | 禁止 GPL-3.0 依赖进入闭源产品 |
| **成本策略** | FinOps、资源利用率 | 未使用超过 30 天的资源自动降级 |
| **质量策略** | 测试覆盖率、架构规则 | 核心服务单元测试覆盖率 ≥ 80% |
| **复用策略** | 资产准入、版本策略 | 只有 SLSA L3+ 的构建产物可进入资产目录 |

---

## 技术栈对照

| 工具/框架 | 适用场景 | 与复用治理的结合 |
|:---|:---|:---|
| **Open Policy Agent (OPA)** | 云原生、Kubernetes、API 网关策略 | 准入控制：镜像/依赖是否允许复用 |
| **HashiCorp Sentinel** | Terraform Enterprise/Cloud | 基础设施即代码复用的合规门禁 |
| **Cedar** | AWS 风格授权 | 细粒度 RBAC：谁可以消费/发布资产 |
| **OPAL** | 实时策略更新 | 动态更新复用黑名单/白名单 |
| **Sigstore Policy Controller** | 容器镜像签名验证 | 仅允许签名镜像被复用 |

---

## 策略自动化流水线

```text
资产提交
    │
    ▼
[策略评估] ──► OPA/Sentinel/Cedar 执行规则集
    │
    ├── 通过 ──► 进入资产目录 / 允许消费
    │
    └── 失败 ──► 阻断并返回具体违规项
```

---

## 检查清单

- [ ] 是否将治理规则编码为版本化策略？
- [ ] 策略评估是否集成到 CI/CD 和资产目录？
- [ ] 策略违规是否有清晰的可解释反馈？
- [ ] 是否区分强制策略（blocking）和建议策略（warning）？
- [ ] 策略变更是否经过审批和审计？

---

## 关联主题

- `06-cross-layer-governance/01-process-governance/` — 复用过程治理框架
- `10-supply-chain-security/` — 供应链安全策略
- `12-ai-native-reuse/06-ai-governance/` — AI 治理策略


---

## 补充说明：07 策略自动化（Policy Automation）

## 示例

**示例**：组织使用 OPA Gatekeeper 强制所有部署到生产的服务必须使用经批准的 Golden Path 模板与 SBOM，否则拒绝部署。

## 反例

**反例**：策略仅存在于文档中，依赖人工检查，导致违规部署频繁发生且难以追溯。

## 权威来源

> **权威来源**:
>
> - [Open Policy Agent](https://www.openpolicyagent.org)
> - [CNCF](https://www.cncf.io)
> - 核查日期：2026-07-07

## 分析

**分析**：策略自动化将治理从“事后审计”转变为“事前预防”，大幅提升治理可扩展性。
