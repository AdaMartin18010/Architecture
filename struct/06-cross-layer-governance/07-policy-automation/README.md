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

## Rego 策略清单

| 策略文件 | 包名 | 决策点 | 输出 |
|:---|:---|:---|:---|
| `policies/reuse_economic_decision.rego` | `reuse.economic` | 复用经济判定（AAF 阈值） | `decision` / `allow` / `reason` |
| `policies/finops_allocation_model.rego` | `finops.allocation` | FinOps 四级分摊模型选择 | `model` / `allow` / `reason` / `violation` |
| `policies/supply_chain_decision.rego` | `supply.chain` | 供应链安全复用准入 | `decision` / `allow` / `reason` |
| `policies/ai_model_selection.rego` | `ai.model.selection` | AI 模型层级选择 | `decision` / `allow` / `reason` |
| `policies/upgrade_downgrade_matrix.rego` | `reuse.matrix` | 跨层复用升级/降级矩阵 | `decision` / `target_layer` / `risk_level` / `reason` / `allow` |
| `policies/reuse_six_phase_decision.rego` | `reuse.six.phase` | 六阶段统一复用判定 | `decision` / `allow` / `reason` |

### 运行方式

```bash
# 方式 1：使用 OPA CLI（推荐）
opa test struct/06-cross-layer-governance/07-policy-automation/policies --verbose

# 方式 2：使用项目脚本（未安装 OPA 时自动走 Python fallback）
python scripts/policy-check.py
```

### 输入/输出约定

所有策略均遵循统一输入/输出约定：

- **输入**：通过 OPA `input` 传入结构化 JSON。
- **输出**：
  - `decision` / `model`：策略判定结果（字符串）。
  - `allow`：布尔值，`true` 表示允许/通过。
  - `reason`：可解释的自然语言理由。
  - 升级/降级矩阵额外输出 `target_layer`（目标层级）和 `risk_level`（风险等级）。

### AI 模型选择策略示例

```bash
# OPA 评估示例
echo '{"task_type":"classification","min_accuracy":0.95,"max_latency_p99_ms":200,"max_cost_per_1k_tokens":0.05,"data_privacy_required":false,"safety_level_required":"medium","available_tiers":["premium","balanced","economy"]}' | \
  opa eval --data policies/ai_model_selection.rego --stdin-input 'data.ai.model.selection.decision'
```

预期输出：`"PREMIUM"`。

### 升级/降级矩阵策略示例

```bash
echo '{"current_layer":"component","consumers":5,"cross_team":true,"cross_org":false,"tech_compatibility_ratio":0.9,"semantic_coverage_ratio":0.85,"coupling_impact_ratio":0.1,"security_level_required":"L2","component_cert_level":"L2","confidence_gamma":0.95,"config_conflicts":0,"latency_requirement_ms":200,"shared_service_p99_ms":150,"upgrade_benefit":10.0,"downgrade_benefit":0.0}' | \
  opa eval --data policies/upgrade_downgrade_matrix.rego --stdin-input 'data.reuse.matrix'
```

预期输出包含 `{"decision":"UPGRADE","target_layer":"app_service","risk_level":"中"}`。

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
