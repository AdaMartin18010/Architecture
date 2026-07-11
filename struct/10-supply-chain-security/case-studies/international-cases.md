# 供应链安全 — 国际化案例集

> **语言**: 英文案例 + 中文分析
> **范围**: 国际组织中软件供应链事件与防御模式的真实案例
> **版本**: 2026-07-08

---

## 概念定义

**软件供应链安全（Software supply-chain security）** 是保护可复用软件工件（源代码、依赖、构建环境、分发产物）在其全生命周期中免遭篡改、漏洞注入与许可证风险传播的学科。

---

## 正向示例 / 防御模式

### 案例 1：Google — SLSA 与 Binary Authorization

**来源**: <https://slsa.dev/>, Google Cloud 文档

**决策**: Google 在内部并通过 OpenSSF 推广 SLSA（Supply-chain Levels for Software Artifacts），将工件来源与二进制授权策略结合。

**结果**: 构建来源成为一级要求；只有满足既定 SLSA 等级的工件才被允许进入生产环境。

**经验**:

- 来源必须由构建系统自动生成，不能手动添加。
- 部署时的策略执行将构建安全与运行时信任闭环。

### 案例 2：OpenSSF — Scorecard 与 OSPS Baseline

**来源**: <https://openssf.org/>, OpenSSF Scorecard

**决策**: 开源安全基金会创建了自动化 Scorecard 与开源项目安全基线（OSPS Baseline），帮助维护者和使用者评估项目安全态势。

**结果**: 消费者可使用一组通用安全信号比较项目；维护者获得可操作的改进建议。

**经验**:

- 自动化、开放的评估可超越手动审计的规模。
- 基线必须足够简单以便采用，又足够全面以捕捉常见风险。

---

## 反例 / 失败案例

### 事件 1：SolarWinds Orion（2020）

**来源**: CISA Alert AA20-352A, NCSC 指南, SolarWinds 事件报告

**事件**: 攻击者入侵 SolarWinds 构建流水线，向 Orion 软件更新中注入恶意代码，随后分发给约 18,000 名客户，包括政府机构。

**决策失误**:

- 构建环境未充分隔离或监控。
- 客户缺乏对更新来源的独立验证。
- 信任完全建立在厂商分发渠道上，未做额外工件验证。

**当前推荐的防御模式**:

- SLSA Build L3+ 要求：隔离、可复现的构建与签名来源。
- SBOM 消费与漏洞关联。
- 构建环境隔离与最小权限 CI/CD 访问。

### 事件 2：XZ Utils 后门（2024）

**来源**: OpenSSF, CISA, 上游维护者事后分析

**事件**: 维护者账户被入侵，导致后门被插入广泛使用的压缩库 xz/liblzma。后门针对特定构建配置与 SSH 环境。

**决策失误**:

- 对新贡献者的信任逐步升级，但代码审查深度不足。
- 压缩/混淆的测试文件逃过了随意审查。
- 下游消费者未独立审计关键依赖。

**当前推荐的防御模式**:

- 安全关键代码路径的多人审查。
- 可复现构建与源码到二进制验证。
- 依赖风险评分与行为监控。

### 事件 3：Log4j（Log4Shell，2021）

**来源**: CISA Alert AA21-356A, NCSC, 厂商公告

**事件**:  ubiquitous Log4j 2 库中的远程代码执行漏洞影响了数百万应用。组织难以定位 Log4j 的使用位置。

**决策失误**:

- 许多组织缺乏准确的 SBOM。
- 传递依赖对安全团队不可见。
- 响应因手动资产盘点而放缓。

**当前推荐的防御模式**:

- 每次构建生成并保存 SBOM。
- 将软件成分分析集成到 CI/CD。
- 漏洞披露与补丁管理 SLA。

---

## 分析

供应链安全是复用的信任基础。每起事件都遵循相似模式：单一被入侵或存在漏洞的可复用资产将风险传播到大量下游系统。因此防御需要**纵深防御**：

1. **源码完整性**: 签名提交、多人审查
2. **构建完整性**: 隔离、可复现、来源生成
3. **依赖透明性**: SBOM、成分分析
4. **运行时验证**: 二进制授权、持续监控

---

## 权威来源

- CISA Alert AA20-352A, AA21-356A
- NCSC 供应链安全指南
- SLSA 1.2, <https://slsa.dev/spec/v1.2/>
- OpenSSF Scorecard, <https://github.com/ossf/scorecard>
- 核查日期：2026-07-08

---

## 相关文档

- [`../03-attack-vectors/attack-tree.md`](../03-attack-vectors/attack-tree.md)
- [`../01-slsa-framework/slsa-1-2-multi-track.md`](../01-slsa-framework/slsa-1-2-multi-track.md)
- [`../02-sbom-standards/sbom-comparison.md`](../02-sbom-standards/sbom-comparison.md)