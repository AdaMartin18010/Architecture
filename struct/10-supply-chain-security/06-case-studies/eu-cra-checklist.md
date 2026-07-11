# EU Cyber Resilience Act (CRA) 2024/2847 合规检查清单

> **版本**: 2026-06-10
> **法规**: Regulation (EU) 2024/2847 — Cyber Resilience Act
> **生效日期**: 2024-12-10
> **关键截止日期**:
>
> - 2026-09-11: Article 14 漏洞/事件报告义务生效
> - 2027-12-11: 全部产品完整合规义务生效（CE 标志）
> **核查日期**: 2026-06-10
> **来源 URL**: <https://eur-lex.europa.eu/eli/reg/2024/2847/oj> | ENISA: <https://www.enisa.europa.eu/topics/cyber-resilience-act>

---

## 目录

- [EU Cyber Resilience Act (CRA) 2024/2847 合规检查清单](#eu-cyber-resilience-act-cra-20242847-合规检查清单)
  - [目录](#目录)
  - [1. 法规概览](#1-法规概览)
    - [1.1 适用范围](#11-适用范围)
    - [1.2 核心义务（Article 10 + Annex I）](#12-核心义务article-10--annex-i)
  - [2. 软件复用合规检查清单](#2-软件复用合规检查清单)
    - [2.1 复用前评估（Pre-Reuse Assessment）](#21-复用前评估pre-reuse-assessment)
    - [2.2 复用中管理（In-Use Management）](#22-复用中管理in-use-management)
    - [2.3 复用后报告（Post-Incident Reporting）](#23-复用后报告post-incident-reporting)
  - [3. 复用组件供应商管理](#3-复用组件供应商管理)
    - [3.1 供应商合同检查清单](#31-供应商合同检查清单)
    - [3.2 开源组件特别注意事项](#32-开源组件特别注意事项)
  - [4. 与 SLSA / SBOM / SSDF 的协同](#4-与-slsa--sbom--ssdf-的协同)
  - [5. 实施路线图（2026-2027）](#5-实施路线图2026-2027)
  - [6. 工具推荐](#6-工具推荐)
  - [补充章节](#补充章节)
  - [概念定义](#概念定义)
  - [示例](#示例)
  - [反例](#反例)
  - [分析](#分析)

## 1. 法规概览

EU CRA 是首部对**所有带数字元素的产品**（hardware 和 software）强制实施网络安全要求的欧盟法规。
它覆盖从设计、开发到退役的全生命周期，直接影响软件复用决策——因为复用组件的安全性成为产品合规的连带责任。

### 1.1 适用范围

| 产品类别 | 示例 | 合规路径 |
|:---|:---|:---|
| **所有带数字元素的产品 (PDE)** | IoT 设备、软件、操作系统、App、工业控制器 | 自我评估 (Module A) 或 第三方认证 |
| **重要产品 (Important Products)** | 身份管理系统、浏览器、VPN、操作系统、工业自动化系统 | 第三方认证 (Module B+C 或 H) |
| **关键产品 (Critical Products)** | 硬件安全模块、智能卡、工业监控系统等 | 强制第三方认证 (Module H) |

> **软件复用特别影响**：只要您的产品在欧盟市场销售，且包含可联网的数字元素（包括复用的第三方软件组件），即受 CRA 约束。复用组件的漏洞 = 您的产品漏洞。

### 1.2 核心义务（Article 10 + Annex I）

| 义务 | 要求摘要 | 对复用的影响 |
|:---|:---|:---|
| **安全设计 (Security by Design)** | 产品在设计阶段即需集成网络安全 | 复用组件必须经过安全评估才能纳入产品 |
| **安全默认 (Security by Default)** | 出厂配置即具备适当安全设置 | 复用组件的默认配置不得引入漏洞 |
| **漏洞管理** | 识别、记录、修复漏洞的完整流程 | 复用组件的漏洞必须可追踪至上游 |
| **安全更新** | 在支持期内提供免费安全更新 | 复用组件的生命周期必须被管理 |
| **SBOM** | 维护软件物料清单 | **复用组件必须列入 SBOM** |
| **漏洞报告** | 向 ENISA 报告 actively exploited vulnerabilities（24h）和 severe incidents | 复用组件的漏洞可能触发报告义务 |
| **技术文档** | 完整的技术文档保存 10 年 | 复用组件的评估记录需归档 |
| **CE 标志** | 合规产品必须贴 CE 标志 | 不合规的复用组件可能导致产品无法上市 |

---

## 2. 软件复用合规检查清单

### 2.1 复用前评估（Pre-Reuse Assessment）

| 检查项 | 要求 | 验证方法 | 优先级 |
|:---|:---|:---|:---:|
| R-01 | 复用组件是否来自可信来源？ | 验证供应商是否提供 CRA 合规声明 | P0 |
| R-02 | 复用组件是否有已知的 actively exploited vulnerabilities？ | 查询 CVE / NVD / ENISA 威胁 Landscape | P0 |
| R-03 | 复用组件是否提供 SBOM（SPDX/CycloneDX）？ | 要求供应商提供机器可读 SBOM | P0 |
| R-04 | 复用组件的安全更新支持期是否覆盖您产品的支持期？ | 合同/SLA 审查 | P1 |
| R-05 | 复用组件的许可证是否与您的 CRA 合规策略兼容？ | 法务/合规审查 | P1 |
| R-06 | 复用组件是否经过安全测试（SAST/DAST/SCA）？ | 要求供应商提供测试报告 | P1 |
| R-07 | 复用组件的默认配置是否安全？ | 配置审计 | P1 |
| R-08 | 复用组件是否引入新的攻击面？ | 威胁建模（STRIDE） | P1 |
| R-09 | 复用组件是否支持安全更新机制（如自动更新、签名验证）？ | 技术评估 | P2 |
| R-10 | 复用组件的数据处理是否符合 GDPR？ | 隐私影响评估 (DPIA) | P2 |

### 2.2 复用中管理（In-Use Management）

| 检查项 | 要求 | 验证方法 | 优先级 |
|:---|:---|:---|:---:|
| M-01 | 您的产品 SBOM 是否完整包含所有复用组件及其版本？ | SBOM 生成工具（Syft, Trivy, FOSSology） | P0 |
| M-02 | 是否建立了复用组件的漏洞监控机制？ | CVE 订阅 + SCA 工具（Snyk, Mend, Black Duck） | P0 |
| M-03 | 是否能在 24h 内识别复用组件的 actively exploited vulnerability 对您产品的影响？ | 影响分析流程 + 自动化工具 | P0 |
| M-04 | 复用组件更新时，是否进行回归测试验证兼容性？ | CI/CD 流水线集成测试 | P1 |
| M-05 | 是否记录了复用组件的变更历史（版本升级、补丁应用）？ | 变更管理日志 | P1 |
| M-06 | 是否对复用组件进行了独立的代码审计（关键产品强制）？ | 第三方审计报告 | P1 |
| M-07 | 是否建立了复用组件的退役/替换计划（EoL 管理）？ | 供应商沟通 + 内部规划 | P2 |
| M-08 | 复用组件的传递依赖（transitive dependencies）是否也被追踪？ | 依赖树分析工具 | P2 |

### 2.3 复用后报告（Post-Incident Reporting）

| 检查项 | 要求 | 验证方法 | 优先级 |
|:---|:---|:---|:---:|
| P-01 | 发现复用组件的 actively exploited vulnerability 后，是否在 24h 内向 ENISA 报告？ | 事件响应流程 | P0 |
| P-02 | 报告内容是否包含：产品标识、漏洞描述、影响评估、缓解措施？ | 报告模板审查 | P0 |
| P-03 | 严重安全事件（severe incidents）是否在 24h 内报告 ENISA？ | 事件分级标准 | P0 |
| P-04 | 用户是否在合理时间内收到安全更新通知？ | 用户通信记录 | P1 |
| P-05 | 安全更新是否在合理时间内发布？ | 发布周期 KPI | P1 |
| P-06 | 是否记录了所有漏洞披露和修复的证据（10 年保存）？ | 文档归档审计 | P1 |

---

## 3. 复用组件供应商管理

CRA 不仅约束制造商，也影响**进口商和分销商**。作为制造商，您需要确保供应商配合 CRA 合规。

### 3.1 供应商合同检查清单

| 条款 | 建议内容 |
|:---|:---|
| **安全要求条款** | 供应商保证组件符合 CRA Annex I 的基本要求 |
| **漏洞通报义务** | 供应商在发现漏洞后 X 小时内通知您 |
| **SBOM 交付** | 每版本提供 SPDX 2.3 或 CycloneDX 1.6 格式 SBOM |
| **安全更新承诺** | 明确支持期（建议 ≥ 5 年）和更新响应时间 |
| **审计权** | 您有权对供应商进行安全审计（关键产品强制） |
| **责任分担** | 明确漏洞责任的分配机制 |
| **合规证据** | 供应商提供符合性评估程序（CAP）证据 |

### 3.2 开源组件特别注意事项

开源组件是 CRA 合规的**高风险区**，因为：

- 维护者无合同义务提供安全更新
- SBOM 通常不完整
- 传递依赖难以追踪

**建议措施**：

1. **建立开源组件准入清单**：仅允许来自活跃社区、有安全响应流程的开源项目
2. **强制 SCA 扫描**：每次构建必须生成并验证 SBOM
3. **参与社区安全**：为关键开源组件贡献安全补丁或资助安全审计
4. **备用方案**：对关键开源组件，准备商业替代方案或内部维护能力

---

## 4. 与 SLSA / SBOM / SSDF 的协同

| CRA 要求 | SLSA 对应 | SBOM 对应 | SSDF 对应 |
|:---|:---|:---|:---|
| 安全设计 | SLSA L3+（可审计构建） | — | PW.1.1（安全设计） |
| 漏洞管理 | — | VEX（漏洞利用交换） | RV.1.1（漏洞接收） |
| SBOM | SLSA Provenance | SPDX 2.3 / CycloneDX 1.6 | PO.3.2（软件组件清单） |
| 安全更新 | SLSA Source Track | — | RV.1.3（漏洞修复） |
| 传递依赖追踪 | SLSA Dependencies | 完整依赖树 | PO.3.2 |

---

## 5. 实施路线图（2026-2027）

```text
2026-06 ──→ 完成本检查清单的适配和内部培训
2026-07 ──→ 建立 SBOM 生成流水线（CI/CD 集成）
2026-08 ──→ 完成现有产品复用组件的漏洞扫描基线
2026-09 ──→ Article 14 报告义务生效 ──→ 事件响应流程就绪
2026-10 ──→ 供应商合同 CRA 条款更新完成
2027-03 ──→ 全部产品完成 CRA 差距分析
2027-06 ──→ 关键产品完成第三方认证
2027-12 ──→ 全部产品贴 CE 标志上市
```

---

## 6. 工具推荐

| 用途 | 工具 | 说明 |
|:---|:---|:---|
| SBOM 生成 | Syft, Trivy, FOSSology | 从容器/代码生成 SPDX/CycloneDX |
| SCA / 漏洞扫描 | Snyk, Mend (WhiteSource), Black Duck, OWASP Dependency-Check | 持续监控复用组件漏洞 |
| 漏洞报告 | ENISA 单一报告平台（开发中） | Article 16 要求，预计 2026 上线 |
| 合规管理 | Vanta, Drata, OneTrust | 整合 CRA/NIS2/GDPR 合规 |
| 签名验证 | Sigstore/cosign | 验证复用组件的来源和完整性 |

---

> **权威来源**:
>
> - Regulation (EU) 2024/2847 (Cyber Resilience Act). <https://eur-lex.europa.eu/eli/reg/2024/2847/oj>
> - ENISA Cyber Resilience Act. <https://www.enisa.europa.eu/topics/cyber-resilience-act>
> - Aegister: CRA Scope, Deadlines, Obligations. <https://www.aegister.com/en/cms/insights/cyber-resilience-act-cra-obligations-manufacturers/> (核查日期: 2026-06-10)
> - ADVISORI: CRA Regulation Guide. <https://www.advisori.de/services/regulatory-compliance-management/cra-cyber-resilience-act/cra-verordnung-en> (核查日期: 2026-06-10)
> - Cycode: Cyber Resilience Act Complete Guide. <https://cycode.com/blog/cyber-resilience-act/> (核查日期: 2026-06-10)
>
> **核查日期**: 2026-06-10


---

## 补充章节

## 概念定义

**定义**：软件供应链安全关注从源代码、依赖、构建、分发到部署全链路中，复用资产不被篡改、注入漏洞或引入许可证风险；SLSA、SBOM 与签名验证是核心机制。

## 示例

**示例**：组织采用 SLSA L3 构建流程：源码托管、构建环境隔离、构建产物签名并生成SPDX SBOM；Log4j 类事件发生时 2 小时内定位受影响服务。

## 反例

**反例**：XZ Utils 后门事件显示，未对压缩依赖进行来源验证与行为审计，恶意代码可潜伏数年并随复用传播到大量系统。

## 分析

**分析**：供应链安全是复用的信任基础，缺乏可追溯性的复用会放大单点风险。