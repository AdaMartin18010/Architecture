<!--
  文档标识: B-05
  任务: OpenSSF Scorecard + Security Baseline 与复用决策
  版本: 2026-06-10
  定位: 供应链安全与架构复用交叉领域的技术决策指南
  对齐标准: OpenSSF Scorecard v4.x, OpenSSF Security Baseline 2024-2025, SLSA 1.2, NIST SSDF, ISO/IEC 5230 (SPDX)
  状态: ✅ 已完成
-->

# OpenSSF Scorecard + Security Baseline 与复用决策

## 目录

- [OpenSSF Scorecard + Security Baseline 与复用决策](#openssf-scorecard--security-baseline-与复用决策)
  - [目录](#目录)
  - [1. OpenSSF Scorecard 概述](#1-openssf-scorecard-概述)
    - [1.1 项目背景与目标](#11-项目背景与目标)
    - [1.2 核心检查项详解](#12-核心检查项详解)
      - [1.2.1 Code-Review（代码审查）](#121-code-review代码审查)
      - [1.2.2 Dependency-Update-Tool（依赖更新工具）](#122-dependency-update-tool依赖更新工具)
      - [1.2.3 Signed-Releases（签名验证）](#123-signed-releases签名验证)
      - [1.2.4 Security-Policy（安全策略）](#124-security-policy安全策略)
      - [1.2.5 Vulnerabilities（漏洞管理）](#125-vulnerabilities漏洞管理)
      - [1.2.6 Binary-Artifacts（二进制产物）](#126-binary-artifacts二进制产物)
      - [1.2.7 Branch-Protection（分支保护）](#127-branch-protection分支保护)
      - [1.2.8 Dangerous-Workflow（危险工作流）](#128-dangerous-workflow危险工作流)
      - [1.2.9 License（许可证合规）](#129-license许可证合规)
      - [1.2.10 Maintained（维护活跃度）](#1210-maintained维护活跃度)
    - [1.3 Scorecard 评分机制](#13-scorecard-评分机制)
  - [2. OpenSSF Security Baseline 概述](#2-openssf-security-baseline-概述)
    - [2.1 发布背景与核心定位](#21-发布背景与核心定位)
    - [2.2 Baseline 的主要内容结构](#22-baseline-的主要内容结构)
      - [2.2.1 身份与访问管理（Identity and Access Management）](#221-身份与访问管理identity-and-access-management)
      - [2.2.2 代码完整性（Code Integrity）](#222-代码完整性code-integrity)
      - [2.2.3 构建与发布安全（Build and Release Security）](#223-构建与发布安全build-and-release-security)
      - [2.2.4 漏洞管理（Vulnerability Management）](#224-漏洞管理vulnerability-management)
      - [2.2.5 依赖管理（Dependency Management）](#225-依赖管理dependency-management)
    - [2.3 Baseline 与 Scorecard/SLSA/Best Practices Badge 的联动](#23-baseline-与-scorecardslsabest-practices-badge-的联动)
  - [3. Scorecard 评分与复用决策矩阵](#3-scorecard-评分与复用决策矩阵)
    - [3.1 决策矩阵设计原则](#31-决策矩阵设计原则)
    - [3.2 三级复用决策矩阵](#32-三级复用决策矩阵)
      - [3.2.1 高信任区间：Score ≥ 8](#321-高信任区间score--8)
      - [3.2.2 条件复用区间：Score 5-7](#322-条件复用区间score-5-7)
      - [3.2.3 避免或加固复用区间：Score \< 5](#323-避免或加固复用区间score--5)
    - [3.3 决策矩阵的细化维度](#33-决策矩阵的细化维度)
  - [4. Scorecard 集成到复用决策流水线](#4-scorecard-集成到复用决策流水线)
    - [4.1 集成架构概览](#41-集成架构概览)
    - [4.2 具体集成步骤](#42-具体集成步骤)
      - [4.2.1 依赖变更检测](#421-依赖变更检测)
      - [4.2.2 自动调用 Scorecard API](#422-自动调用-scorecard-api)
      - [4.2.3 决策引擎策略配置](#423-决策引擎策略配置)
      - [4.2.4 结果反馈与开发者体验](#424-结果反馈与开发者体验)
    - [4.3 大规模集成的性能优化](#43-大规模集成的性能优化)
    - [4.4 与 SBOM 的集成](#44-与-sbom-的集成)
  - [5. Security Baseline 达标要求对复用资产库的影响](#5-security-baseline-达标要求对复用资产库的影响)
    - [5.1 复用资产库的安全门槛重塑](#51-复用资产库的安全门槛重塑)
      - [5.1.1 入库标准的升级](#511-入库标准的升级)
      - [5.1.2 资产分类与标签体系更新](#512-资产分类与标签体系更新)
    - [5.2 对内部开发组件的反向驱动](#52-对内部开发组件的反向驱动)
    - [5.3 持续合规监控](#53-持续合规监控)
  - [6. 与 SLSA 1.2 的协同](#6-与-slsa-12-的协同)
    - [6.1 SLSA 1.2 框架回顾](#61-slsa-12-框架回顾)
    - [6.2 Scorecard → SLSA 等级 → 复用安全边界 的映射](#62-scorecard--slsa-等级--复用安全边界-的映射)
      - [6.2.1 Scorecard 评估作为 SLSA 判定的前置输入](#621-scorecard-评估作为-slsa-判定的前置输入)
      - [6.2.2 SLSA 等级与复用安全边界的对应关系](#622-slsa-等级与复用安全边界的对应关系)
      - [6.2.3 联合决策流程](#623-联合决策流程)
    - [6.3 与 SLSA Provenance 的集成](#63-与-slsa-provenance-的集成)
  - [7. 供应链攻击案例：Log4j 与 XZ Utils 的历史评分分析](#7-供应链攻击案例log4j-与-xz-utils-的历史评分分析)
    - [7.1 案例研究方法论](#71-案例研究方法论)
    - [7.2 Log4j（Log4Shell, CVE-2021-44228）](#72-log4jlog4shell-cve-2021-44228)
      - [7.2.1 事件背景](#721-事件背景)
      - [7.2.2 攻击发生前的 Scorecard 评估](#722-攻击发生前的-scorecard-评估)
      - [7.2.3 Scorecard 评分反映的问题](#723-scorecard-评分反映的问题)
      - [7.2.4 复用决策启示](#724-复用决策启示)
    - [7.3 XZ Utils 后门事件（2024）](#73-xz-utils-后门事件2024)
      - [7.3.1 事件背景](#731-事件背景)
      - [7.3.2 攻击发生前的 Scorecard 评估](#732-攻击发生前的-scorecard-评估)
      - [7.3.3 Scorecard 评分的关键警示](#733-scorecard-评分的关键警示)
      - [7.3.4 复用决策启示](#734-复用决策启示)
    - [7.4 两个案例的对比总结](#74-两个案例的对比总结)
  - [8. 实施路线图建议](#8-实施路线图建议)
    - [阶段一：评估与试点（1-3 个月）](#阶段一评估与试点1-3-个月)
    - [阶段二：自动化与扩展（3-6 个月）](#阶段二自动化与扩展3-6-个月)
    - [阶段三：深度集成与持续优化（6-12 个月）](#阶段三深度集成与持续优化6-12-个月)
  - [附录：权威来源](#附录权威来源)
  - [补充说明：OpenSSF Scorecard + Security Baseline 与复用决策](#补充说明openssf-scorecard--security-baseline-与复用决策)
  - [概念定义](#概念定义)

---

## 1. OpenSSF Scorecard 概述

### 1.1 项目背景与目标

OpenSSF Scorecard 是由 Open Source Security Foundation（OpenSSF）发起并维护的开源安全评估工具，旨在通过自动化的方式对开源项目的安全 posture（安全态势）进行量化评估。该项目最初由 Google 安全团队推动，于 2021 年正式成为 OpenSSF 的核心项目之一，目标是为软件消费者提供一种标准化、可重复、可扩展的机制，以快速判断所依赖的开源组件是否满足基本的安全治理要求。

在软件架构复用的语境下，Scorecard 的价值尤为突出。当组织决定复用某个开源库、框架或工具时，传统的安全评估往往依赖于人工审计、漏洞数据库查询（如 CVE/NVD）或静态代码分析。这些方法虽然有效，但存在覆盖范围有限、更新滞后、成本高昂等问题。Scorecard 通过直接扫描项目的代码仓库、发布流程、治理实践和依赖管理策略，生成一组标准化的安全评分，从而为复用决策提供数据驱动的支持。

### 1.2 核心检查项详解

截至 2024-2025 年，OpenSSF Scorecard 涵盖了超过 10 个核心检查项（checks），每个检查项对应特定的安全实践领域。以下是各检查项的详细说明及其在复用决策中的意义：

#### 1.2.1 Code-Review（代码审查）

该检查项评估项目是否强制要求在合并代码之前进行人工审查。评分依据包括：

- 是否启用了分支保护规则（branch protection），要求至少一名审查者批准；
- 是否通过 GitHub/GitLab 等平台的 PR/MR 机制进行管理；
- 是否存在未经审查直接推送到默认分支的情况。

在复用决策中，Code-Review 分数较低的项目意味着其代码变更缺乏有效的同行评审，引入恶意代码或严重缺陷的风险显著增加。

#### 1.2.2 Dependency-Update-Tool（依赖更新工具）

评估项目是否使用 Dependabot、Renovate 或类似的自动化工具来跟踪和更新依赖项。该检查项关注：

- 配置文件中是否明确启用了依赖更新工具；
- 更新频率和覆盖范围（是否包括开发依赖、间接依赖）；
- 是否对安全相关的更新设置了自动合并策略。

依赖更新工具的缺失意味着项目可能长期运行在存在已知漏洞的依赖版本上，这对复用该组件的上游系统构成直接威胁。

#### 1.2.3 Signed-Releases（签名验证）

检查项目的发布产物（release artifacts）是否经过加密签名（如 GPG、Sigstore/cosign）。评估维度包括：

- 每个 GitHub Release 是否附带了签名文件或使用了 Sigstore 的 keyless signing；
- 签名是否可通过公钥或透明日志（transparency log）进行验证；
- 签名策略是否覆盖所有发布的二进制文件、容器镜像和 SBOM。

在复用场景中，Signed-Releases 是验证软件供应链完整性的第一道防线，缺乏签名的发布产物无法保证在分发过程中未被篡改。

#### 1.2.4 Security-Policy（安全策略）

评估项目是否在仓库根目录或文档中提供了 `SECURITY.md` 文件，明确说明：

- 漏洞报告渠道（如安全邮箱、私有漏洞披露机制）；
- 漏洞响应时间线和修复承诺；
- 安全公告的发布方式（如 GitHub Security Advisories）。

一个缺乏安全策略的项目通常意味着其安全治理处于无序状态，复用该组件时难以获得及时的安全更新和沟通渠道。

#### 1.2.5 Vulnerabilities（漏洞管理）

通过集成 OSV（Open Source Vulnerabilities）数据库，自动扫描项目及其依赖树中是否存在已知的公开漏洞。该检查项不仅关注直接依赖，还会递归分析传递依赖（transitive dependencies）的漏洞情况。

#### 1.2.6 Binary-Artifacts（二进制产物）

检查仓库中是否意外提交了编译后的二进制文件。二进制产物会降低代码的可审计性，因为它们无法像源代码一样被直接审查。在复用决策中，包含二进制产物的仓库需要额外的逆向工程分析，增加了安全评估的复杂度。

#### 1.2.7 Branch-Protection（分支保护）

评估默认分支是否启用了全面的保护机制，包括：

- 禁止强制推送（force push）；
- 要求状态检查（status checks）通过后才能合并；
- 要求代码审查和签名提交（signed commits）。

#### 1.2.8 Dangerous-Workflow（危险工作流）

分析项目的 CI/CD 工作流配置（如 GitHub Actions YAML 文件），识别是否存在危险的权限配置，例如：

- 使用 `pull_request_target` 事件触发器配合未经验证的代码执行；
- 将敏感密钥（secrets）暴露给不可信的工作流；
- 允许不可信输入直接注入到 shell 命令中。

#### 1.2.9 License（许可证合规）

检查项目是否包含明确的许可证文件。虽然该检查项主要关注合规性而非安全性，但许可证的不明确会直接影响复用的法律风险。

#### 1.2.10 Maintained（维护活跃度）

评估项目是否处于积极维护状态，包括最近提交频率、问题响应速度、维护者数量等指标。长期无人维护的项目即使当前没有已知漏洞，也可能在未来出现安全问题时无法及时修复。

### 1.3 Scorecard 评分机制

每个检查项的得分范围为 0-10 分，最终通过加权平均或风险聚合算法生成总体评分。Scorecard 提供了两种主要的输出格式：

- **JSON 格式**：适合 CI/CD 流水线集成和自动化决策；
- **人类可读的报告**：包含详细的检查项说明和改进建议。

值得注意的是，Scorecard 的评分并非静态的。OpenSSF 持续根据安全研究的最新发现和社区反馈调整检查项的权重和评估逻辑。因此，复用决策系统应定期重新评估依赖组件的 Scorecard 评分。

---

## 2. OpenSSF Security Baseline 概述

### 2.1 发布背景与核心定位

OpenSSF Security Baseline（以下简称 "Baseline"）是 OpenSSF 于 2024 年至 2025 年间正式发布的一套面向开源项目维护者的安全基线标准。与 Scorecard 的"评估"定位不同，Baseline 的核心目标是"定义最低安全要求"——即为开源项目提供一套必须满足的安全实践清单，类似于建筑行业中的"建筑规范"或医疗行业的"卫生标准"。

Baseline 的发布背景源于近年来供应链攻击的爆发式增长。从 2020 年的 SolarWinds 事件到 2024 年的 XZ Utils 后门事件，攻击者越来越多地将目标瞄准开源软件生态的上游环节。然而，传统的安全评估工具（包括 Scorecard）虽然能够识别问题，但缺乏一种强制性的、可审计的"最低门槛"。Baseline 正是为了填补这一空白而设计的。

### 2.2 Baseline 的主要内容结构

Baseline 的内容围绕多个安全域展开，每个域对应一组必须满足的要求。以下是 Baseline 的核心结构：

#### 2.2.1 身份与访问管理（Identity and Access Management）

- 要求项目维护者启用多因素认证（MFA）；
- 要求对具有发布权限的账户实施最小权限原则；
- 要求定期审查和维护者权限分配。

#### 2.2.2 代码完整性（Code Integrity）

- 要求所有合并到默认分支的代码必须经过审查；
- 鼓励使用签名提交（signed commits）以验证提交者身份；
- 要求对 CI/CD 流水线实施权限隔离和输入验证。

#### 2.2.3 构建与发布安全（Build and Release Security）

- 要求发布产物必须经过自动化构建流程生成，禁止手动上传；
- 要求对发布产物进行加密签名；
- 鼓励生成并提供 SBOM（软件物料清单）。

#### 2.2.4 漏洞管理（Vulnerability Management）

- 要求项目提供明确的安全漏洞报告渠道；
- 要求在发现漏洞后及时发布安全公告和修复版本；
- 要求持续监控依赖项中的已知漏洞。

#### 2.2.5 依赖管理（Dependency Management）

- 要求使用自动化工具跟踪依赖项更新；
- 要求对依赖项的变更进行审查和记录；
- 鼓励使用锁定文件（lock files）确保构建的可重复性。

### 2.3 Baseline 与 Scorecard/SLSA/Best Practices Badge 的联动

Baseline 并非孤立存在，而是与 OpenSSF 生态系统中的其他项目形成了互补关系：

| 工具/标准 | 定位 | 与 Baseline 的关系 |
|-----------|------|-------------------|
| Scorecard | 自动化评估工具 | Baseline 的要求可以作为 Scorecard 检查项的"及格线"，Scorecard 评分可以用来验证项目是否满足 Baseline |
| SLSA | 供应链完整性框架 | Baseline 的构建与发布安全要求直接对应 SLSA 的 Build 和 Provenance 要求 |
| Best Practices Badge | 自我认证徽章 | Baseline 可以作为 Best Practices Badge 中安全相关条目的补充和强化 |

这种联动关系在架构复用决策中具有重要意义。当评估一个开源组件时，组织可以综合参考：

- **Baseline 达标状态**：该项目是否通过了 Baseline 的最低安全要求？
- **Scorecard 评分**：该项目的安全 posture 量化得分是多少？
- **SLSA 等级**：该项目的构建和发布流程达到了 SLSA 的哪个级别？
- **Best Practices Badge**：该项目是否获得了 CII Best Practices 徽章？

---

## 3. Scorecard 评分与复用决策矩阵

### 3.1 决策矩阵设计原则

在软件架构复用的实践中，安全评估不应是"非黑即白"的二元判断，而应是一个基于风险承受能力和业务价值的梯度决策过程。基于 OpenSSF Scorecard 的评分体系，我们设计了以下三级复用决策矩阵：

### 3.2 三级复用决策矩阵

#### 3.2.1 高信任区间：Score ≥ 8

**决策建议**：**直接复用，常规监控**

当开源项目的 Scorecard 总分达到 8 分或以上时，表明该项目在安全治理方面处于行业领先水平。此类项目通常具备以下特征：

- 完善的代码审查流程和分支保护机制；
- 自动化的依赖更新和漏洞监控能力；
- 所有发布产物均经过加密签名；
- 明确的安全策略和活跃的维护团队。

**复用策略**：

- 将该组件纳入组织的"绿色清单"（Green List），允许各项目团队直接引用；
- 设置常规的安全监控频率（如每月一次重新评估）；
- 在架构文档中记录该组件的 Scorecard 评分和评估日期；
- 优先选择评分在 8 分以上的组件作为同类功能的首选方案。

#### 3.2.2 条件复用区间：Score 5-7

**决策建议**：**条件复用，附加控制措施**

得分在 5 到 7 分之间的项目表明其安全实践存在一定程度的不足，但尚未达到"高风险"的程度。这类项目可能缺少某些关键的安全实践（如未启用依赖更新工具、未对发布产物进行签名），但在核心领域（如代码审查）仍保持基本水准。

**复用策略**：

- 将该组件纳入"黄色清单"（Yellow List），允许复用但需满足附加条件；
- 在复用前进行针对性的安全加固，例如：
  - 如果 Signed-Releases 得分低，要求通过其他渠道（如官方容器镜像仓库的签名标签）验证产物完整性；
  - 如果 Dependency-Update-Tool 得分低，将该项目纳入组织的统一依赖监控范围，主动跟踪其依赖树的安全状态；
  - 如果 Maintained 得分低，评估组织内部是否有能力承担维护责任，或寻找活跃的社区分支（fork）。
- 增加监控频率（如每周一次重新评估）；
- 在复用决策文档中详细记录附加控制措施和风险接受声明。

#### 3.2.3 避免或加固复用区间：Score < 5

**决策建议**：**避免复用，除非经过深度安全加固**

得分低于 5 分的项目通常存在严重的安全治理缺陷，可能包括：

- 缺乏代码审查机制，允许未经审查的代码直接合并；
- CI/CD 工作流存在危险的权限配置，易受供应链攻击；
- 长期无人维护，依赖树中存在大量已知漏洞；
- 缺乏安全策略和漏洞响应机制。

**复用策略**：

- 默认将该组件列入"红色清单"（Red List），禁止直接复用；
- 仅在以下特殊情况下考虑复用：
  - 该组件提供了不可替代的核心功能，且市场上不存在满足要求的替代品；
  - 组织具备足够的安全工程能力，能够对该组件进行全面的安全审计和持续维护；
  - 该组件将被隔离在高度受限的运行环境中（如沙箱、无网络访问的容器）。
- 如需复用，必须执行深度安全加固流程，包括：
  - 源代码级别的安全审计（人工审计 + 高级静态分析工具）；
  - 剥离不必要的依赖和功能，最小化攻击面；
  - 建立内部的漏洞监控和补丁管理流程；
  - 将加固后的版本作为内部私有组件管理，与原项目解耦。

### 3.3 决策矩阵的细化维度

在实际应用中，总分虽然重要，但不应是唯一的决策依据。组织应结合各检查项的得分进行细化分析：

| 关键检查项 | 高信任阈值 | 条件复用阈值 | 避免阈值 |
|-----------|-----------|-------------|---------|
| Code-Review | ≥ 8 | 5-7 | < 5 |
| Signed-Releases | ≥ 8 | 5-7 | < 5 |
| Vulnerabilities | 10（无已知漏洞） | 7-9（低危漏洞） | < 7（中高危漏洞） |
| Dangerous-Workflow | ≥ 8 | 5-7 | < 5 |
| Maintained | ≥ 7 | 4-6 | < 4 |

如果某个组件在总分上处于"条件复用"区间，但 Dangerous-Workflow 或 Vulnerabilities 检查项得分处于"避免阈值"，则应自动降级为"避免复用"类别。

---

## 4. Scorecard 集成到复用决策流水线

### 4.1 集成架构概览

将 OpenSSF Scorecard 集成到 CI/CD 复用决策流水线中，是实现"安全左移"（Shift Left Security）的关键举措。
其核心思想是：在软件开发的最早阶段（即依赖引入阶段）就自动评估候选组件的安全 posture，而不是等到构建完成或部署前才进行安全审查。

典型的集成架构包含以下组件：

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    复用决策流水线（CI/CD 集成）                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   开发者提交依赖变更请求                                              │
│           │                                                         │
│           ▼                                                         │
│   ┌───────────────┐     ┌───────────────┐     ┌───────────────┐     │
│   │ 依赖解析引擎   │────▶│ Scorecard API │────▶│ 决策引擎       │   │
│   │ (SBOM 生成)   │     │ (自动评估)     │     │ (策略匹配)     │     │
│   └───────────────┘     └───────────────┘     └───────┬───────┘     │
│                                                       │             │
│                           ┌───────────────────────────┘             │
│                           ▼                                         │
│                  ┌─────────────────┐                                │
│                  │   决策结果       │                                │
│                  │ • 允许合并       │                                │
│                  │ • 要求附加控制   │                                │
│                  │ • 拒绝并建议替代 │                                │
│                  └─────────────────┘                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 具体集成步骤

#### 4.2.1 依赖变更检测

在 CI/CD 流水线中，首先需要检测依赖变更。这可以通过以下方式实现：

- 在代码提交阶段，解析 `package.json`、`requirements.txt`、`pom.xml`、`go.mod` 等依赖管理文件；
- 使用工具（如 Dependabot、Snyk、OWASP Dependency-Check）生成变更前后的依赖差异列表；
- 识别新增的直接依赖和传递依赖。

#### 4.2.2 自动调用 Scorecard API

OpenSSF 提供了 Scorecard 的公开 API 和数据集（存储在 BigQuery 中），允许 CI/CD 流水线自动查询指定仓库的评分：

```bash
# 使用 OpenSSF Scorecard CLI 进行评估
scorecard --repo=https://github.com/example/library --format=json

# 或者查询 BigQuery 公共数据集
# 数据集位置: openssf.scorecard.latest
```

对于每个新增依赖，流水线应自动触发 Scorecard 评估，并将结果以结构化格式（JSON）传递给决策引擎。

#### 4.2.3 决策引擎策略配置

决策引擎根据组织预设的策略规则对 Scorecard 结果进行匹配。策略配置通常以 YAML 或 JSON 格式存储：

```yaml
# scorecard-policy.yaml
policy:
  min_total_score: 5
  critical_checks:
    - name: Code-Review
      min_score: 5
      block_on_failure: true
    - name: Vulnerabilities
      min_score: 7
      block_on_failure: true
    - name: Dangerous-Workflow
      min_score: 5
      block_on_failure: true

  auto_approve_threshold: 8

  exceptions:
    - dependency: "internal/*"
      skip_scorecard: true
    - dependency: "legacy-system-adapter"
      require_manual_approval: true
```

#### 4.2.4 结果反馈与开发者体验

评估结果应以清晰、可操作的方式反馈给开发者：

- **允许合并（绿色）**：Scorecard 评分满足所有策略要求，流水线自动通过；
- **要求附加控制（黄色）**：评分处于条件复用区间，流水线生成警告并在 PR 评论中列出建议的控制措施，要求开发者在 `DEPENDENCY_SECURITY.md` 中记录风险接受声明；
- **拒绝并建议替代（红色）**：评分低于策略阈值，流水线阻止合并，并在 PR 评论中提供替代组件建议（基于组织内部的组件目录中评分更高的同类组件）。

### 4.3 大规模集成的性能优化

对于拥有数百个微服务和数千个依赖的大型组织，每次依赖变更都实时调用 Scorecard API 可能导致性能瓶颈。优化策略包括：

- **本地缓存**：建立内部的 Scorecard 评分缓存数据库，定期（如每日）从 OpenSSF 同步最新评分，CI/CD 流水线优先查询本地缓存；
- **增量评估**：仅对新引入的依赖触发 Scorecard 评估，已存在的依赖复用缓存结果；
- **批量评估**：在每日夜间构建中，对所有依赖的 Scorecard 评分进行批量复核，及时发现评分下降的情况。

### 4.4 与 SBOM 的集成

将 Scorecard 评分嵌入到 SBOM（Software Bill of Materials）中，是实现全生命周期供应链可视化的重要手段。
建议采用 SPDX 2.3 或更高版本，利用 `Annotations` 字段存储每个组件的 Scorecard 评分：

```spdx
PackageName: lodash
SPDXID: SPDXRef-Package-lodash
PackageVersion: 4.17.21
Annotation: scorecard-total: 6.5
Annotation: scorecard-code-review: 5
Annotation: scorecard-signed-releases: 3
Annotation: scorecard-evaluated: 2026-06-10
```

---

## 5. Security Baseline 达标要求对复用资产库的影响

### 5.1 复用资产库的安全门槛重塑

组织的内部复用资产库（Internal Reuse Asset Repository）是架构复用的核心基础设施，通常包含开源组件的镜像、内部开发的共享库、以及第三方商业组件的接口适配层。
OpenSSF Security Baseline 的达标要求对这一资产库产生了深远影响。

#### 5.1.1 入库标准的升级

传统的复用资产库入库标准主要关注功能性、性能和许可证合规性。
引入 Security Baseline 后，入库标准必须增加安全基线维度：

**一级标准（强制要求）**：

- 所有入库的开源组件必须满足 Security Baseline 的"身份与访问管理"要求，即其维护团队启用了 MFA；
- 所有组件的源代码仓库必须启用分支保护和代码审查机制；
- 所有发布产物必须提供可验证的签名。

**二级标准（优先要求）**：

- 组件应具备自动化的依赖更新机制；
- 组件应提供明确的安全漏洞报告渠道；
- 组件应生成并发布 SBOM。

#### 5.1.2 资产分类与标签体系更新

复用资产库的分类体系应引入安全维度标签：

```text
组件: axios (HTTP 客户端库)
标签:
  - 功能域: 网络通信
  - 语言: JavaScript/TypeScript
  - 许可证: MIT
  - scorecard-total: 7.2
  - security-baseline: PASSED
  - slsa-level: 3
  - 复用决策: CONDITIONAL (条件复用)
  - 附加控制: 需启用内部依赖监控
```

### 5.2 对内部开发组件的反向驱动

Security Baseline 不仅影响开源组件的复用，也对组织内部开发的共享组件提出了同等要求。
这种"反向驱动"效应体现在：

- **内部组件也必须满足 Baseline**：如果组织要求复用的开源组件满足 Security Baseline，那么逻辑上，组织自己生产的共享组件也应满足同样的标准，否则将出现"双重标准"的治理漏洞；
- **提升内部安全文化**：通过将 Baseline 纳入内部组件的开发规范，可以逐步提升整个组织的开源安全治理能力；
- **增强外部信任**：当组织的共享组件对外开源时，满足 Security Baseline 和较高的 Scorecard 评分可以显著增强外部社区和客户的信任。

### 5.3 持续合规监控

复用资产库不应是一次性评估的静态集合，而应建立持续合规监控机制：

- **每日扫描**：对所有已入库组件重新执行 Scorecard 评估，检测评分变化；
- **Baseline 版本跟踪**：OpenSSF 会持续更新 Security Baseline 的版本，组织应跟踪 Baseline 的变更，并评估其对已入库组件的影响；
- **自动降级与告警**：当某个已入库组件的 Scorecard 评分跌破策略阈值或不再满足 Baseline 要求时，自动触发告警并标记该组件为"需要复审"。

---

## 6. 与 SLSA 1.2 的协同

### 6.1 SLSA 1.2 框架回顾

SLSA（Supply Chain Levels for Software Artifacts）是由 OpenSSF 推出的供应链完整性框架，最新版本为 1.2。
SLSA 通过四个等级（Build L1-L4）定义了软件构建和发布过程的可信度：

- **SLSA Build Level 1**：构建过程完全自动化，产出 provenance（来源证明）文档；
- **SLSA Build Level 2**：使用托管的构建服务（如 GitHub Actions、Cloud Build），构建环境受版本控制；
- **SLSA Build Level 3**：构建环境具有强隔离性（如防篡改、不可变），构建参数和依赖完全声明化；
- **SLSA Build Level 4**：最高级别，要求所有构建步骤均可审计和复现，使用双人审查和封闭式构建环境。

### 6.2 Scorecard → SLSA 等级 → 复用安全边界 的映射

Scorecard、SLSA 和复用安全边界三者可以形成有机的协同关系：

```text
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Scorecard 评估  │────▶│  SLSA 等级判定   │────▶│  复用安全边界    │
│  (安全治理 posture)│     │  (构建可信度)    │     │  (运行时隔离)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

#### 6.2.1 Scorecard 评估作为 SLSA 判定的前置输入

SLSA 主要关注构建和发布过程的安全性，而 Scorecard 覆盖更广泛的安全治理维度。
在进行 SLSA 等级判定之前，可以先通过 Scorecard 进行初步筛选：

- 如果 Scorecard 总分 < 5，直接判定为"不满足 SLSA 评估前提"，无需进一步分析其 SLSA 等级；
- 如果 Scorecard 的 Dangerous-Workflow 检查项得分 < 5，意味着其 CI/CD 配置存在明显缺陷，即使构建产物看似可信，也应将其 SLSA 等级下调一级。

#### 6.2.2 SLSA 等级与复用安全边界的对应关系

| SLSA Build Level | Scorecard 总分 | 复用安全边界建议 |
|-----------------|---------------|----------------|
| L4 | ≥ 8 | 完全信任，无需额外隔离措施 |
| L3 | ≥ 7 | 标准信任，常规容器沙箱 |
| L2 | 5-7 | 条件信任，网络隔离 + 最小权限 |
| L1 | < 5 或 5-7 | 低信任，严格沙箱 + 行为监控 |
| 未评估 | < 5 | 不信任，禁止直接复用 |

#### 6.2.3 联合决策流程

完整的联合决策流程如下：

1. **阶段一：Scorecard 初筛**
   - 获取组件的 Scorecard 评分；
   - 检查关键检查项（Code-Review、Vulnerabilities、Dangerous-Workflow）是否满足最低阈值；
   - 如未通过初筛，进入"拒绝或深度加固"分支。

2. **阶段二：SLSA 等级评估**
   - 分析组件的构建流程和 provenance 文档；
   - 判定其 SLSA Build Level（L1-L4）；
   - 检查 provenance 是否包含完整的依赖树和构建参数。

3. **阶段三：复用安全边界设计**
   - 根据 Scorecard 评分和 SLSA 等级，确定运行时隔离策略：
     - **网络隔离**：是否允许该组件访问外部网络？
     - **权限隔离**：该组件运行所需的最小文件系统和系统调用权限是什么？
     - **数据隔离**：该组件是否能够访问敏感数据？是否需要数据脱敏？
   - 生成复用安全边界文档，作为架构设计的一部分。

4. **阶段四：持续监控与再评估**
   - 在组件的整个生命周期内，持续监控其 Scorecard 评分和 SLSA 等级变化；
   - 当等级下降时，自动触发安全边界复审。

### 6.3 与 SLSA Provenance 的集成

SLSA 1.2 的 provenance 文档可以使用 in-toto 格式进行编码。
在复用决策中，组织应要求所有被复用的开源组件提供可验证的 SLSA provenance，并将其与 Scorecard 评分一同存储在内部资产库中：

```json
{
  "component": "example-library",
  "version": "1.2.3",
  "scorecard": {
    "total": 7.5,
    "evaluated_at": "2026-06-10"
  },
  "slsa": {
    "build_level": 3,
    "provenance": "https://example.com/provenance/intoto.jsonl",
    "verifier": "sigstore"
  },
  "reuse_boundary": {
    "network_access": false,
    "filesystem_access": "read-only",
    "sensitive_data_access": false
  }
}
```

---

## 7. 供应链攻击案例：Log4j 与 XZ Utils 的历史评分分析

### 7.1 案例研究方法论

通过回顾历史上重大的供应链攻击事件，并分析受害组件在攻击发生前后的 OpenSSF Scorecard 评分，可以直观地验证 Scorecard 作为复用决策工具的有效性。
以下分析基于公开可获取的代码仓库状态和历史数据，部分评分可能基于当时的仓库配置进行回溯性评估。

### 7.2 Log4j（Log4Shell, CVE-2021-44228）

#### 7.2.1 事件背景

Apache Log4j 2 是 Java 生态系统中使用最广泛的日志框架之一。
2021 年 11 月，安全研究人员发现 Log4j 2 中存在一个严重的远程代码执行漏洞（CVE-2021-44228），攻击者可以通过构造特殊的日志消息触发 JNDI 查找，进而加载并执行远程恶意代码。该漏洞被命名为 "Log4Shell"，被认为是近年来影响最广泛的供应链安全事件之一。

#### 7.2.2 攻击发生前的 Scorecard 评估

在 2021 年漏洞爆发前，对 Apache Log4j 2 仓库进行回溯性 Scorecard 评估，结果大致如下：

| 检查项 | 预估评分 | 说明 |
|--------|---------|------|
| Code-Review | 6-7 | Apache 项目普遍要求代码审查，但部分提交可能存在审查不充分的情况 |
| Dependency-Update-Tool | 3-4 | Log4j 项目当时未配置 Dependabot 或类似的自动化依赖更新工具 |
| Signed-Releases | 7-8 | Apache 项目通常对发布产物进行 GPG 签名 |
| Security-Policy | 5-6 | 存在安全报告渠道，但响应速度存在历史问题 |
| Vulnerabilities | 5-6 | 在漏洞公开前，该检查项无法检测到未知的 0-day 漏洞 |
| Dangerous-Workflow | 6-7 | CI/CD 配置相对规范，但构建流程的复杂性增加了风险 |
| Maintained | 7-8 | 项目有稳定的维护团队 |
| **总分预估** | **6.0-6.5** | **处于"条件复用"区间** |

#### 7.2.3 Scorecard 评分反映的问题

Log4j 2 的预估 Scorecard 评分揭示了以下关键问题，这些问题在事后被证实与漏洞的存在和扩散密切相关：

1. **Dependency-Update-Tool 得分偏低**：Log4j 2 的 JNDI 功能在早期版本中是为了与 Java 的命名和目录服务集成而设计的。然而，随着安全威胁环境的变化，这一功能逐渐成为安全隐患。如果项目配置了自动化的依赖安全扫描和更新工具，可能会更早地发现 JNDI 相关代码的风险。

2. **Security-Policy 和漏洞响应机制不够敏捷**：Apache 安全团队虽然最终修复了漏洞，但在漏洞公开后的初期，沟通和补丁发布的速度受到了广泛批评。这表明即使有良好的安全策略，执行层面的敏捷性同样重要。

3. **复杂的功能集增加了攻击面**：Log4j 2 作为一个通用的日志框架，包含了大量并非所有用户都需要的高级功能（如 JNDI 查找、消息查找替换）。Scorecard 虽然没有直接检查"功能复杂度"，但 Maintained 和 Dependency-Update-Tool 的得分可以从侧面反映项目是否有能力持续安全地维护复杂的功能集。

#### 7.2.4 复用决策启示

如果组织在 2021 年之前就将 Scorecard 集成到复用决策流程中，Log4j 2 的预估评分（6.0-6.5）会将其归类为"条件复用"组件。
这意味着：

- 组织不会无条件地信任 Log4j 2 的安全性；
- 会在复用时附加控制措施，例如：
  - 禁用 JNDI 功能（通过配置 `log4j2.formatMsgNoLookups=true`）；
  - 将 Log4j 2 运行在受限的网络环境中；
  - 增加对日志输入的监控和过滤。

事实上，正是这些附加控制措施在漏洞爆发后成为许多组织的临时缓解方案。这验证了"条件复用 + 附加控制"策略的有效性。

### 7.3 XZ Utils 后门事件（2024）

#### 7.3.1 事件背景

2024 年 3 月，Microsoft 工程师 Andres Freund 在调查 PostgreSQL 性能问题时，意外发现 XZ Utils（一个广泛使用的压缩库）的发布 tarball 中被植入了一个高度复杂的后门。
该后门针对特定版本的 OpenSSH 服务器，通过 libsystemd 的依赖链在构建过程中注入恶意代码。
攻击者 "Jia Tan" 通过长达数年的社会工程手段逐步获得了 XZ Utils 项目的维护权限，最终实施了这次精密的供应链攻击。

#### 7.3.2 攻击发生前的 Scorecard 评估

XZ Utils 项目在攻击发生前是一个由个人维护者主导的小型开源项目，其 Scorecard 评估结果具有明显的警示信号：

| 检查项 | 预估评分 | 说明 |
|--------|---------|------|
| Code-Review | 3-4 | 项目主要由单一维护者控制，缺乏有效的多审者代码审查 |
| Dependency-Update-Tool | 2-3 | 未配置自动化的依赖更新工具 |
| Signed-Releases | 4-5 | 虽然 tarball 有签名，但签名密钥由单一维护者控制 |
| Security-Policy | 2-3 | 缺乏明确的安全漏洞报告渠道和安全策略文档 |
| Vulnerabilities | 5-6 | 在当时没有已知的 CVE |
| Dangerous-Workflow | 4-5 | 构建和发布流程主要由维护者手动控制，缺乏 CI/CD 的透明度和隔离性 |
| Maintained | 5-6 | 项目有提交活动，但维护者数量极少 |
| **总分预估** | **3.5-4.5** | **处于"避免复用"区间** |

#### 7.3.3 Scorecard 评分的关键警示

XZ Utils 案例是 Scorecard 作为复用决策工具价值的极端验证。
其预估评分（3.5-4.5）处于"避免复用"区间，主要问题集中在以下检查项：

1. **Code-Review 得分极低（3-4）**：这是最根本的问题。XZ Utils 项目在攻击者 "Jia Tan" 成为共同维护者后，代码审查机制形同虚设。攻击者能够自由地将恶意代码（以"测试文件"的形式）合并到仓库中，而没有独立的审校者进行质疑。Scorecard 的 Code-Review 检查项会明确标记这一风险。

2. **Maintained 得分中等偏低（5-6）**：虽然项目有提交活动，但维护者社区极其狭小。攻击者正是利用了原维护者 "Lasse Collin" 的倦怠和需要帮助的心理，逐步渗透并接管了项目。Scorecard 的 Maintained 检查项虽然无法检测社会工程攻击，但"维护者数量少"的指标可以作为一个重要的风险信号。

3. **Dangerous-Workflow 得分偏低（4-5）**：XZ Utils 的发布流程缺乏透明度和自动化。攻击者通过替换发布 tarball 中的测试文件来植入后门，而这种手动发布的模式使得篡改变得容易且难以被发现。如果项目使用了具有 provenance 生成的自动化构建流程（SLSA L2+），后门的植入将困难得多。

4. **Signed-Releases 得分中等（4-5）**：虽然发布产物有签名，但由于签名密钥由攻击者控制，签名本身无法提供有效的安全保障。这说明签名只是供应链安全的一个环节，必须与维护者的身份验证和密钥管理相结合。

#### 7.3.4 复用决策启示

如果组织在 2024 年之前严格执行基于 Scorecard 的复用决策流程，XZ Utils 的预估评分会触发以下响应：

- **自动拒绝直接复用**：评分低于 5 分，XZ Utils 会被列入"红色清单"，禁止在无附加控制的情况下引入；
- **强制深度审计**：如果因为功能依赖（如系统包管理器的依赖链）无法避免使用 XZ Utils，组织应执行源代码级别的审计，这将大概率发现后门植入的异常（如测试文件中的高度混淆的二进制数据）；
- **构建过程隔离**：在独立的、可审计的构建环境中重新编译 XZ Utils，而不是直接使用上游发布的 tarball，可以避免后门的激活；
- **维护者背景调查**：对于 Maintained 得分低且维护者变更频繁的项目，增加对维护者身份和贡献历史的背景调查。

### 7.4 两个案例的对比总结

| 维度 | Log4j (Log4Shell) | XZ Utils 后门 |
|------|-------------------|---------------|
| 项目规模 | 大型、广泛使用 | 小型、个人维护 |
| Scorecard 预估总分 | 6.0-6.5（条件复用） | 3.5-4.5（避免复用） |
| 根本成因 | 功能设计缺陷 + 缺乏依赖安全监控 | 社会工程 + 缺乏代码审查 |
| Scorecard 最能预警的检查项 | Dependency-Update-Tool, Security-Policy | Code-Review, Maintained, Dangerous-Workflow |
| 复用决策的教训 | 条件复用时应附加功能禁用和输入过滤控制 | 低分组件应默认拒绝，除非进行深度审计和自建构建 |

这两个案例共同证明了：OpenSSF Scorecard 虽然无法阻止所有供应链攻击（尤其是 0-day 漏洞和社会工程攻击），但能够系统性地识别和量化那些与攻击成功高度相关的安全治理缺陷。
在软件架构复用决策中，Scorecard 评分应被视为必不可少的输入维度。

---

## 8. 实施路线图建议

对于希望将 OpenSSF Scorecard 和 Security Baseline 纳入复用决策体系的组织，建议分三个阶段实施：

### 阶段一：评估与试点（1-3 个月）

- 选取 5-10 个核心依赖组件，手动执行 Scorecard 评估；
- 建立初步的三级决策矩阵和例外审批流程；
- 在 1-2 个试点项目中集成 Scorecard CLI 到 CI/CD 流水线。

### 阶段二：自动化与扩展（3-6 个月）

- 将 Scorecard 评估扩展到所有新增依赖；
- 建立内部 Scorecard 评分缓存和监控看板；
- 制定 Security Baseline 的达标检查清单，并纳入复用资产库的入库标准。

### 阶段三：深度集成与持续优化（6-12 个月）

- 实现 Scorecard、SLSA 和 SBOM 的联合评估流水线；
- 建立自动化的安全边界生成和运行时隔离部署机制；
- 定期回顾和优化决策矩阵的阈值，基于组织的安全事件数据进行校准。

---

## 附录：权威来源

1. OpenSSF Scorecard 官方文档与 GitHub 仓库
   - URL: <https://github.com/ossf/scorecard>
   - 核查日期: 2026-06-10

2. OpenSSF Scorecard 检查项详细说明
   - URL: <https://github.com/ossf/scorecard/blob/main/docs/checks.md>
   - 核查日期: 2026-06-10

3. OpenSSF Security Baseline 官方文档
   - URL: <https://github.com/ossf/security-baseline>
   - 核查日期: 2026-06-10

4. SLSA (Supply Chain Levels for Software Artifacts) 1.2 规范
   - URL: <https://slsa.dev/spec/v1.2/>
   - 核查日期: 2026-06-10

5. OpenSSF 官方博客：Security Baseline 发布说明
   - URL: <https://openssf.org/blog/>
   - 核查日期: 2026-06-10

6. NIST SP 800-204D：软件供应链安全实践指南
   - URL: <https://csrc.nist.gov/publications/detail/sp/800-204d/final>
   - 核查日期: 2026-06-10

7. CISA：Log4Shell (CVE-2021-44228) 响应指南
   - URL: <https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-356a>
   - 核查日期: 2026-06-10

8. OpenSSF 博客：XZ Utils 后门事件分析
   - URL: <https://openssf.org/blog/2024/04/02/xz-backdoor-cve-2024-3094/>
   - 核查日期: 2026-06-10

9. Google Open Source Security Team：Understanding Scorecard
   - URL: <https://security.googleblog.com/2021/11/introducing-openssf-scorecards-v3.html>
   - 核查日期: 2026-06-10

10. ISO/IEC 5230:2024 — OpenChain 规范（与 SPDX 和 SBOM 相关）
    - URL: <https://www.iso.org/standard/81039.html>
    - 核查日期: 2026-06-10


---

## 补充说明：OpenSSF Scorecard + Security Baseline 与复用决策

## 概念定义

**定义**：SLSA（Supply-chain Levels for Software Artifacts）是 OpenSSF 提出的框架，通过 Source、Build、Provenance、Common 等 Track 定义软件制品的可验证安全等级。