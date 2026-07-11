# 交互式复用决策工具

> ## ⛔ DEPRECATED — 已归档，仅作历史参考
>
> **本目录（v1）已归档，不再维护。** 权威实现为 **[复用决策工具 v2.0](../reuse-decision-tool-v2/README.md)**（CLI + Streamlit Web，含可执行规则引擎、数据驱动模板与单元测试）。
>
> **两套“六阶段”的关系（不矛盾，视角不同）**：
>
> - **v1 = 生命周期视角**：识别 → 评估 → 适配 → 集成 → 验证 → 治理（描述复用活动的全过程）
> - **v2 = 判定门径视角**：语义兼容 → 变性绑定 → 质量 → 安全合规 → 成本收益 → 治理合规（描述复用准入的六道判定门，见 v2 README 中的映射表）
>
> 相关治理文档：[统一复用决策模型（URDM）](../../../06-cross-layer-governance/06-up-downgrade-matrix/unified-reuse-decision-model.md)、[升级/降级矩阵](../../../06-cross-layer-governance/06-up-downgrade-matrix/upgrade-downgrade-matrix.md)。

> **定位**: 支持六阶段复用决策流程的交互式工具（Web/CLI）— **历史概念稿**
> **状态**: 📦 已归档（2026-07-12），权威实现为 [v2.0](../reuse-decision-tool-v2/README.md)
> **技术栈**: Python + Streamlit（按决策 3A）

---

## 六阶段复用决策流程

1. **识别** — 发现潜在可复用资产
2. **评估** — 质量、成熟度、合规性评估
3. **适配** — 计算 AAF、修改范围
4. **集成** — 架构兼容性、依赖影响
5. **验证** — 测试、形式化验证、SBOM 审查
6. **治理** — 度量、成熟度、成本分摊

---

## 计划功能

- 上传/输入资产元数据，自动生成复用建议
- 集成 `cocomo-calculator.py` 计算工作量
- 集成 `maturity-assessment-cli.py` 评估成熟度
- 生成复用决策报告（PDF/Markdown）

---

> 最后更新: 2026-06-06


---

## 补充说明：交互式复用决策工具

## 概念定义

**定义**：参考层是结构化知识体系的“地图”，汇总权威来源、术语表、标准索引、课程对标与审计报告，为各主题提供可追溯的引用与一致性校验。

## 示例

**示例**：维护 authoritative-sources.md 登记所有 ISO/IEC、IEEE、NIST、CNCF 来源 URL 与核查日期，确保全书引用可验证。

## 反例

**反例**：参考层链接长期不更新，术语表与正文定义冲突，读者无法确认内容准确性与时效性。

## 权威来源

> **权威来源**:
>
> - [ISO](https://www.iso.org)
> - [IEEE Standards](https://standards.ieee.org)
> - [NIST](https://www.nist.gov)
> - [CNCF](https://www.cncf.io)
> - 核查日期：2026-07-07

## 分析

**分析**：参考层的价值不在于内容本身，而在于建立知识之间的信任锚点；必须随标准演进定期审计与更新。
