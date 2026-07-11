# ISO/IEC 25010:2023 AI/ML 质量特性与复用评估

> **版本**: 2026-06-08
> **定位**: 元模型层（Level 0）—— ISO/IEC 25010:2023 新增 AI/ML 质量特性的架构复用映射
> **对齐标准**: ISO/IEC 25010:2023 Systems and software engineering — SQuaRE — Product quality model
> **状态**: ⏳ 框架填充中

---

## 1. ISO/IEC 25010:2023 的 AI/ML 质量演进

ISO/IEC 25010:2023 是继 2011 版后的重大修订，其核心驱动力之一是**AI/ML 系统的质量评估需求**。2024 版通过以下方式为 AI/ML 系统提供质量框架：

1. **新增 Safety 特性**: 直接覆盖 AI 系统的功能安全、风险识别与故障安全
2. **扩展 Interaction Capability**: 纳入 AI 系统的可解释性、人机协同交互
3. **细化 Flexibility**: 明确 AI 模型在不同数据分布下的适应能力（Domain Adaptation）
4. **强化 Security 中的 Resistance**: 新增对对抗样本攻击（Adversarial Attacks）的抵抗能力要求

### 1.1 版本对比

| 维度 | 2011 版 | 2024 版 | AI/ML 相关性 |
|------|---------|---------|-------------|
| 质量特性数量 | 8 | 9 | — |
| Safety | 隐含于 Reliability | 独立特性 | ✅ 关键新增 |
| Usability | 独立特性 | 扩展为 Interaction Capability | ✅ 纳入 AI 交互 |
| Portability | 独立特性 | 扩展为 Flexibility | ✅ 模型跨域迁移 |
| Security 子特性 | 5 项 | 6 项（新增 Resistance） | ✅ 对抗安全 |

---

## 2. AI/ML 相关质量特性详解

### 2.1 Safety（安全性/功能安全）

2024 版将 Safety 从 Reliability 中独立，反映 AI 系统在自动驾驶、医疗诊断等安全关键领域的特殊地位。

| 子特性 | AI/ML 映射 | 复用含义 |
|--------|-----------|---------|
| Operational Constraint | AI 模型的运行边界条件 | 复用模型时必须复用其约束条件 |
| Risk Identification | 模型失效模式的识别能力 | 复用组件需提供已知失效案例 |
| Fail Safe | 故障时的安全降级策略 | 复用时需验证 Fail Safe 机制是否适配新上下文 |
| Hazard Warning | 危险状态的预警能力 | 预警阈值可能需要根据部署环境重校准 |
| Safe Integration | 与其他系统的安全集成 | 复用多个 AI 组件时的叠加风险 |

### 2.2 Interaction Capability（交互能力）

Interaction Capability 替代了原有的 Usability，其新增子特性对 AI 系统尤为关键：

- **Self-descriptiveness（自描述性）**: AI 模型需解释其决策依据（XAI / Explainable AI）
- **User Assistance（用户辅助）**: AI 系统主动提示其置信度和不确定性范围
- **Inclusivity（包容性）**: 模型训练数据的多样性保证不同用户群体的公平性

### 2.3 Flexibility（灵活性）

Flexibility 替代 Portability，其 **Adaptability** 子特性直接关联 AI 模型的跨域复用：

- **Domain Adaptation**: 模型在新数据分布下的性能保持能力
- **Fine-tuning 友好性**: 预训练模型是否支持高效微调
- **Scalability**: 模型推理的横向扩展能力（如模型并行、流水线并行）

---

## 3. 质量特性对架构复用决策的影响矩阵

| 质量特性 | 复用决策问题 | AI 组件复用影响 | 权重（安全关键域） |
|---------|------------|----------------|----------------|
| Functional Suitability | 模型功能是否匹配需求？ | 任务类型对齐（分类/检测/生成） | 高 |
| Performance Efficiency | 推理延迟/吞吐量是否达标？ | 硬件加速器依赖、量化策略 | 高 |
| Safety | 是否满足功能安全等级？ | SIL/ASIL 等级匹配 | **必要** |
| Security (Resistance) | 是否存在对抗漏洞？ | 模型窃取、对抗样本风险 | 高 |
| Reliability | 模型输出是否稳定？ | 随机性控制（Temperature, Seed） | 高 |
| Interaction Capability | 可解释性是否满足监管？ | XAI 方法、置信度输出 | 中 |
| Flexibility | 是否需要微调/适配？ | 迁移学习成本、数据需求 | 中 |
| Maintainability | 模型版本管理是否规范？ | MLflow / Model Registry | 中 |
| Compatibility | 输入输出格式是否兼容？ | ONNX / TensorRT / OpenVINO | 高 |

> **定理 AI.1** (AI Reuse Safety Gate): 在安全关键领域复用 AI 组件时，**Safety** 和 **Security (Resistance)** 为**必要准入条件**，不满足则无论其他指标多优均不可复用。

---

## 4. AI 生成代码/组件的复用质量评估框架

### 4.1 评估维度

针对 AI 生成代码（如 GitHub Copilot、CodeT5 等）和 AI 生成组件的复用，建议采用以下评估框架：

| 评估维度 | 检查项 | 通过标准 |
|---------|--------|---------|
| 来源可信度 | 训练数据许可 | OSI 认可的开源许可证 |
| 功能正确性 | 单元测试通过率 | ≥ 90% 且边界条件覆盖 |
| 安全卫生 | 已知漏洞扫描 | OWASP Top 10 无高危 |
| 可维护性 | 代码复杂度 | Cyclomatic Complexity ≤ 15 |
| 可解释性 | 生成过程可追溯 | 提示词 + 参数可记录 |
| 合规性 | 许可证兼容性 | 与目标项目许可证兼容 |

### 4.2 复用风险分级

| 风险等级 | 特征 | 复用策略 |
|---------|------|---------|
| 🟢 低风险 | 生成代码经人工审查 + 测试覆盖 | 可直接复用 |
| 🟡 中风险 | 生成代码逻辑简单但未经完整测试 | 复用后补充测试 |
| 🔴 高风险 | 生成代码涉及安全/并发/资源管理 | 禁止直接复用，仅作参考 |

> **定理 AI.2** (Generative AI Reuse Prudence): AI 生成代码的复用风险与其**状态管理复杂度**和**安全敏感程度**正相关。涉及身份认证、加密、并发控制的代码，无论生成质量如何，均需人工逐行审查。

---

> 最后更新: 2026-06-08
> 权威来源:
>
> - <https://www.iso.org/standard/78176.html> (ISO/IEC 25010:2023)
> - <https://www.iso.org/standard/35733.html> (ISO/IEC 25012:2008 数据质量模型)
> - <https://owasp.org/www-project-top-ten/> (OWASP Top 10)


---

## 补充说明：ISO/IEC 25010:2023 AI/ML 质量特性与复用评估

## 概念定义

**定义**：ISO/IEC 25010:2023 定义了软件产品质量模型，包括功能适合性、性能效率、兼容性、交互能力、可靠性、安全性、可维护性、灵活性与安全性等特性。

## 示例

**示例**：在评估可复用 UI 组件库时，团队依据 25010 的交互能力、可维护性与兼容性制定验收准则，确保组件在多前端框架中一致表现。

## 反例

**反例**：团队仅关注功能正确性，忽视可维护性与灵活性，导致复用组件在框架升级时无法平滑迁移。

## 权威来源

> **权威来源**:
>
> - [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html)
> - [ISO/IEC/IEEE Standards](https://www.iso.org)
> - 核查日期：2026-07-07
