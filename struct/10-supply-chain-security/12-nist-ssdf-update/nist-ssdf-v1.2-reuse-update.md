# NIST SSDF v1.2 复用组件安全实践更新

> **版本**: 2026-06-10
> **定位**: 供应链安全层 —— NIST 安全软件开发框架对第三方组件复用的安全要求演进
> **对齐标准**: NIST SP 800-218 (SSDF) v1.1/v1.2, SLSA 1.2, OWASP SCVS, OpenSSF OSPS Baseline, EU CRA
> **状态**: ✅ 已完成

---

## 目录

- [NIST SSDF v1.2 复用组件安全实践更新](#nist-ssdf-v12-复用组件安全实践更新)
  - [目录](#目录)
  - [1. SSDF 概述与演进](#1-ssdf-概述与演进)
    - [1.1 版本历史](#11-版本历史)
    - [1.2 四大实践组](#12-四大实践组)
  - [2. PW.4 "Reuse Well-Secured Software" 详解](#2-pw4-reuse-well-secured-software-详解)
    - [2.1 实践目标](#21-实践目标)
    - [2.2 具体任务](#22-具体任务)
    - [2.3 与六阶段复用决策模型的映射](#23-与六阶段复用决策模型的映射)
  - [3. SSDF v1.2 草案新增内容](#3-ssdf-v12-草案新增内容)
    - [3.1 AI 组件复用要求（草案）](#31-ai-组件复用要求草案)
    - [3.2 强化供应链要求（草案）](#32-强化供应链要求草案)
  - [4. 与 SLSA / EU CRA / OSPS 的联合实施](#4-与-slsa--eu-cra--osps-的联合实施)
    - [4.1 四维框架映射](#41-四维框架映射)
    - [4.2 联合实施检查清单](#42-联合实施检查清单)
  - [5. 实施框架](#5-实施框架)
  - [6. v1.2 最终版发布后的预对齐动作](#6-v12-最终版发布后的预对齐动作)
  - [7. 权威来源](#7-权威来源)
  - [补充章节](#补充章节)
  - [概念定义](#概念定义)
  - [示例](#示例)
  - [反例](#反例)
  - [分析](#分析)

---

## 1. SSDF 概述与演进

### 1.1 版本历史

| 版本 | 状态 | 发布时间 | 核心变化 |
|:---|:---|:---|:---|
| SSDF v1.0 | 草案 | 2020 | 初始框架，四大实践组 |
| **SSDF v1.1** | **正式版** | **2022-02** | **细化实践，增加示例** |
| **SSDF v1.2** | **草案** | **2025-12** | **扩展至 AI 组件、强化供应链要求** |

### 1.2 四大实践组

```
SSDF 框架结构
├── Prepare the Organization (PO)
│   ├── PO.1: Define Security Requirements
│   ├── PO.2: Implement Roles and Responsibilities
│   └── PO.3: Implement Supporting Toolchains
├── Protect the Software (PS)
│   ├── PS.1: Protect All Forms of Code
│   ├── PS.2: Provide a Well-Secured Software Supply Chain
│   └── PS.3: Secure the Build and Release Process
├── Produce Well-Secured Software (PW)
│   ├── PW.1: Design Software to Meet Security Requirements
│   ├── PW.2: Review the Software Design
│   ├── PW.3: Reuse Existing, Well-Secured Software
│   ├── PW.4: Reuse Well-Secured Software ← 复用核心实践
│   ├── PW.5: Create Source Code
│   ├── PW.6: Configure the Compilation and Build Processes
│   ├── PW.7: Review and/or Analyze Human-Readable Code
│   ├── PW.8: Test the Executable Code
│   └── PW.9: Configure the Software to Have Secure Settings by Default
└── Respond to Vulnerabilities (RV)
    ├── RV.1: Identify and Confirm Vulnerabilities
    ├── RV.2: Assess, Prioritize, and Remediate Vulnerabilities
    └── RV.3: Analyze Vulnerabilities to Identify Their Root Causes
```

---

## 2. PW.4 "Reuse Well-Secured Software" 详解

### 2.1 实践目标

> **目标**: 通过获取、评估和使用来自可信来源且已验证安全性的软件组件，降低自行开发软件的安全风险。

### 2.2 具体任务

| 任务 | 描述 | 与复用决策的映射 |
|:---|:---|:---|
| **PW.4.1** | 获取来源可信的软件组件 | 复用前：验证供应商/仓库的可信度 |
| **PW.4.2** | 验证组件的完整性 | 复用前：校验和 / 签名 / SLSA provenance |
| **PW.4.3** | 跟踪组件的来源 | 复用中：SBOM + 依赖图谱 |
| **PW.4.4** | 评估组件的安全状态 | 复用前：漏洞扫描 + 安全审计 |
| **PW.4.5** | 维护组件的更新 | 复用中：持续监控 + 及时更新 |

### 2.3 与六阶段复用决策模型的映射

```
SSDF PW.4              六阶段复用决策
─────────────────────────────────────────
PW.4.1 获取可信来源  → 阶段 1: 语义兼容性判定
                        （供应商可信度评估）
PW.4.2 验证完整性    → 阶段 4: 安全合规判定
                        （签名/provenance 验证）
PW.4.3 跟踪来源      → 阶段 4: 安全合规判定
                        （SBOM + 溯源）
PW.4.4 评估安全状态  → 阶段 4: 安全合规判定
                        （漏洞扫描 + 安全评估）
PW.4.5 维护更新      → 阶段 4: 安全合规判定（持续）
                        （持续监控 + 退出策略）
```

---

## 3. SSDF v1.2 草案新增内容

### 3.1 AI 组件复用要求（草案）

| 新增任务 | 描述 | 复用影响 |
|:---|:---|:---|
| **PW.4.6** | 评估 AI 模型的训练数据来源 | 复用 AI 模型前验证数据合规性 |
| **PW.4.7** | 验证 AI 模型的完整性和来源 | 复用 AI 模型前验证模型签名和 provenance |
| **PW.4.8** | 评估 AI 组件的偏见和公平性 | 复用 AI 组件前进行偏见检测 |

### 3.2 强化供应链要求（草案）

| 新增任务 | 描述 | 复用影响 |
|:---|:---|:---|
| **PW.4.9** | 评估供应商的安全成熟度 | 将供应商安全评估作为复用前置条件 |
| **PW.4.10** | 要求供应商提供安全证明 | 供应商需提供 SBOM、SLSA provenance 等 |

---

## 4. 与 SLSA / EU CRA / OSPS 的联合实施

### 4.1 四维框架映射

| SSDF 实践 | SLSA 1.2 | EU CRA | OSPS Baseline |
|:---|:---|:---|:---|
| PW.4.1 可信来源 | — | 供应链安全要求 | Access Control |
| PW.4.2 完整性验证 | Build L1+ | 软件完整性 | Build & Release |
| PW.4.3 来源追踪 | Build L2+ | SBOM 要求 | Dependencies |
| PW.4.4 安全评估 | — | 漏洞管理 | Vulnerability Management |
| PW.4.5 维护更新 | — | 安全更新义务 | Vulnerability Management |

### 4.2 联合实施检查清单

**复用前（Pre-Reuse）**:

- [ ] SSDF PW.4.1: 供应商/来源可信度验证
- [ ] SLSA Build L2+: provenance 和签名验证
- [ ] EU CRA: 供应商是否为"关键软件"
- [ ] OSPS: 项目 OSPS 等级 ≥ L2

**复用中（During Reuse）**:

- [ ] SSDF PW.4.3: SBOM 维护和依赖追踪
- [ ] SLSA（Supply-chain Levels for Software Artifacts）: 持续验证 provenance
- [ ] EU CRA: 漏洞报告义务（2026-09-11 起）
- [ ] OSPS: 监控项目安全状态变化

**复用后（Post-Reuse）**:

- [ ] SSDF PW.4.5: 及时应用安全更新
- [ ] EU CRA: 漏洞修复时限（高危 90 天）
- [ ] OSPS: 定期重新评估 OSPS 等级

---

## 5. 实施框架

```
阶段 1: 基线评估（1-2 个月）
├── 评估当前复用实践与 SSDF PW.4 的差距
├── 盘点所有第三方组件及其来源
└── 确定目标合规等级

阶段 2: 流程设计（2-3 个月）
├── 设计复用组件准入流程
├── 制定供应商安全评估模板
├── 建立 SBOM 和 provenance 验证机制
└── 集成自动化安全扫描工具

阶段 3: 试点运行（3-6 个月）
├── 选择 2-3 个关键项目进行试点
├── 收集反馈并优化流程
└── 培训开发和架构团队

阶段 4: 全面推广（6-12 个月）
├── 在所有项目中强制执行 SSDF PW.4
├── 建立度量和报告机制
└── 持续改进
```

---

## 6. v1.2 最终版发布后的预对齐动作

> NIST SSDF v1.2 当前仍为 **Initial Public Draft（2025-12-17 发布）**，最终版预计 2026-Q3 发布。以下动作为预对齐清单，最终版发布后应立即执行。

| 检查项 | v1.1 现状 | v1.2 草案变化 | 最终版发布后的动作 | 优先级 |
|---|---|---|---|:---:|
| AI 组件复用 | PW.4 通用复用要求 | **新增 AI 组件安全复用要求** | 在 AI 原生复用主题中补充 SSDF AI 组件映射 | P0 |
| 供应链强化 | PS.2 / PW.4 基础要求 | **强化来源验证、SBOM、 provenance 要求** | 更新 SBOM 与 SLSA 联合实施检查清单 | P0 |
| 威胁场景 | 覆盖通用软件供应链 | **增加生成式 AI 与 Agent 供应链威胁** | 在 OWASP Agentic AI / MCP Top 10 映射中引用 SSDF v1.2 | P1 |
| 与 NIST AI RMF / AI 600-1 对齐 | 无直接引用 | 草案暗示与 AI 风险管理框架对齐 | 更新 AI 治理主题中的框架映射 | P1 |
| 实施示例 | 较通用 | 可能增加针对开源与商业组件的示例 | 替换本项目模板中的 SSDF v1.1 引用为 v1.2 | P1 |

---

## 7. 权威来源

| 来源 | URL | 核查日期 |
|:---|:---|:---|
| NIST SP 800-218 (SSDF) v1.1 | <https://csrc.nist.gov/projects/ssdf> | 2026-06-10 |
| NIST SP 800-218 v1.2 (草案) | <https://csrc.nist.gov/pubs/sp/800/218/r1/ipd> | 2026-07-08 |
| SLSA 1.2 | <https://slsa.dev/spec/v1.2/> | 2026-06-10 |
| EU CRA 2024/2847 | <https://eur-lex.europa.eu/eli/reg/2024/2847> | 2026-06-10 |
| OpenSSF OSPS Baseline | <https://baseline.openssf.org> | 2026-06-10 |


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
