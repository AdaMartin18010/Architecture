# 欧盟网络弹性法案 (EU CRA) 合规指南

> **版本**: 2026-06-06
> **权威来源**: Regulation (EU) 2024/2847, European Commission
> **定位**: 解读 EU CRA 对软件供应链复用的影响与合规路径

---

## 1. CRA 基本信息

| 项目 | 内容 |
|------|------|
| **法规编号** | Regulation (EU) 2024/2847 |
| **生效日期** | 2024-12-30 |
| **漏洞报告义务** | **2026-09-11** 起 |
| **主要义务全面适用** | **2027-12-11** 起 |
| **适用范围** | 在欧盟市场销售的所有含数字元素的产品 |

---

## 2. 适用范围

### 涵盖产品

- 软件产品（商业分发）
- 带数字元素的硬件产品
- 云服务 / SaaS
- 物联网 (IoT) 设备
- 工业自动化系统
- 关键基础设施组件

### 豁免

- 免费开源软件（有商业活动条件的除外）
- 仅供内部使用的软件
- 研发原型
- 已受其他 EU 法规监管的医疗器械

---

## 3. 制造商四大义务

```text
EU CRA Obligations
├── 1. 安全设计与默认 (Security by Design and Default)
│   ├── 最小化攻击面
│   ├── 默认安全配置
│   ├── 无默认凭证
│   └── 威胁建模和安全编码
│
├── 2. 漏洞管理 (Vulnerability Management)
│   ├── 持续监控漏洞
│   ├── 及时修复和补丁
│   ├── 生命周期结束通知
│   └── 协调披露
│
├── 3. 事件检测与响应 (Incident Detection & Response)
│   ├── 检测影响保密性/完整性/可用性的事件
│   ├── 记录升级和响应计划
│   └── 保留证据
│
└── 4. 软件透明度 (Software Transparency)
    ├── 维护 SBOM
    ├── 技术文档
    └── CE 标记
```

---

## 4. SBOM 具体要求

### 必须包含的信息

| 字段 | 说明 |
|------|------|
| 组件名称 | 所有软件组件 |
| 版本信息 | 精确版本号 |
| 供应商/来源 | 组件制造商 |
| 许可证详情 | 许可证类型 |
| 已知漏洞 | 持续更新 |
| 依赖关系 | 包括传递依赖 |

### 格式要求

- **机器可读格式**（SPDX 或 CycloneDX）
- 随软件修改更新
- 应市场监管机构要求提供
- 纳入技术文档

---

## 5. 漏洞报告时间线

| 事件 | 时间要求 | 报告对象 |
|------|---------|---------|
| 主动利用的漏洞 | **24 小时内** | CSIRT 或 ENISA |
| 其他未修复漏洞 | 无具体天数，但需"及时" | 按程序 |
| 补丁发布 | 合理时间内 | 用户/客户 |

> 关键日期: **2026-09-11** 起，制造商必须开始报告主动利用的漏洞。

---

## 6. 开源软件特殊规定

### 开源豁免

非商业活动的开源软件通常豁免 CRA 义务。

### 商业使用触发义务

当开源软件被集成到商业产品或服务时：

- 集成商承担漏洞处理义务
- 集成商承担更新和文档义务
- 开源管家（Stewards）可能有披露义务

---

## 7. 对架构复用的影响

> **定理 CRA.1** (Component Liability Transfer): CRA 将产品安全责任从最终用户转移到制造商。这意味着**复用第三方组件并不会转移安全责任**，最终产品制造商仍需对所有集成组件负责。

> **定理 CRA.2** (SBOM as Reuse Contract): 在 CRA 背景下，SBOM 不仅是技术文档，更是复用资产的**法律契约**。缺少 SBOM 的组件将面临市场准入障碍。

### 复用策略调整

1. **优先选择提供 SBOM 的组件**
2. **要求关键供应商提供 SLSA provenance**
3. **建立组件漏洞监控流程**
4. **准备 VEX 声明**
5. **评估供应商的 CRA 合规能力**

---

## 8. 合规检查表

- [ ] 识别所有在 EU 市场销售的产品
- [ ] 为每个产品生成并维护 SBOM
- [ ] 建立漏洞管理流程
- [ ] 建立 24 小时漏洞报告机制
- [ ] 实施安全设计和默认配置
- [ ] 准备 CE 标记所需的技术文档
- [ ] 评估第三方组件的 CRA 合规性
- [ ] 建立产品生命周期结束通知流程

## 9. EU CRA 合规义务清单、SBOM/漏洞管理/CE 标记实施步骤与反例

### 9.1 定义：CRA 合规义务

EU CRA 将"含数字元素的产品"（Products with Digital Elements, PDE）制造商定义为承担网络安全全生命周期责任的主体。复用第三方组件**不会**转移该责任；制造商必须对集成组件的安全状态负责。

> **定义 CRA.Comp.1** (PDE Manufacturer Obligation): 任何在欧盟市场投放 PDE 的制造商，必须实施安全设计、漏洞管理、事件响应与软件透明度四组义务，无论其自行开发或复用第三方组件。

### 9.2 义务清单矩阵

| 义务组 | 具体义务 | 适用对象 | 关键日期 | 违规风险 |
|--------|---------|---------|---------|---------|
| 安全设计与默认 | 最小攻击面、安全默认配置、无默认凭证 | 所有 PDE 制造商 | 2027-12-11 | 市场禁入、罚款 |
| 漏洞管理 | 识别、跟踪、修复漏洞；生命周期结束通知 | 所有 PDE 制造商 | 2026-09-11（报告义务） | 监管处罚 |
| 事件检测与响应 | 检测影响 CIA 的事件；24h 报告主动利用漏洞 | 所有 PDE 制造商 | 2026-09-11 | 罚款、声誉损失 |
| 软件透明度 | 维护 SBOM；提供技术文档；加贴 CE 标记 | 所有 PDE 制造商 | 2027-12-11 | 无法上市 |
| 开源 steward 义务 | 协调披露、维护漏洞政策（特定 steward） | 开源基金会 / 大型开源项目 | 2026-09-11 | 监管关注 |

### 9.3 SBOM 实施步骤

| 步骤 | 行动 | 输出物 | 工具示例 |
|------|------|--------|---------|
| 1. 工具选型 | 选择 SPDX/CycloneDX 生成工具 | 工具链决策记录 | Syft, Trivy, CycloneDX CLI |
| 2. CI/CD 集成 | 每次构建自动生成 SBOM | `sbom.spdx.json` / `bom.json` | GitHub Actions / GitLab CI |
| 3. 完整性校验 | 为 SBOM 附加哈希与签名 | 签名 SBOM | cosign |
| 4. 漏洞关联 | 将 SBOM 与 CVE/OSV 数据库关联 | 漏洞清单 | Grype, Snyk, OSV-Scanner |
| 5. VEX 生成 | 对不可利用 CVE 发布 VEX | `vex.json` | CycloneDX VEX, CSAF |
| 6. 归档交付 | 将 SBOM 纳入技术文档 | 技术文档包 | DOORS, Confluence, 文档仓库 |

### 9.4 漏洞管理实施步骤

| 步骤 | 行动 | 时间要求 |
|------|------|---------|
| 1. 持续监控 | 订阅 CVE/OSV/供应商安全通告 | 实时 |
| 2. 影响评估 | 根据 SBOM 判断受影响产品 | 48 小时内 |
| 3. 修复计划 | 制定补丁或缓解方案 | 合理时间内 |
| 4. 主动利用报告 | 向 CSIRT/ENISA 报告 | 24 小时内 |
| 5. 用户通知 | 向客户发布安全公告与补丁 | 补丁可用时 |
| 6. 生命周期结束通知 | 提前通知产品支持终止 | EOL 前至少 6 个月 |

### 9.5 CE 标记实施步骤

1. **符合性评估**：依据 CRA 附件 I（网络安全要求）与附件 II（漏洞处理要求）进行内部评估或第三方认证（高风险产品）。
2. **技术文档**：包含 SBOM、威胁模型、测试报告、漏洞管理流程、事件响应计划。
3. **欧盟代表**：非欧盟制造商需指定欧盟授权代表。
4. **加贴 CE 标记**：在产品或包装上清晰加贴 CE 标记并附带符合性声明（DoC）。
5. **市场监督**：保留技术文档至少 10 年，配合市场监管机构检查。

### 9.6 正例

| 实践 | 效果 |
|------|------|
| 在 CI/CD 中自动生成 CycloneDX SBOM 并签名 | 满足 CRA 软件透明度要求，构建可验证 |
| 建立 24 小时漏洞报告 SOP 并演练 | 满足主动利用漏洞报告义务 |
| 对关键组件要求 SLSA Build L3 + Source L2 provenance | 降低第三方组件引入后门风险 |
| 产品 EOL 前 12 个月通知客户 | 满足生命周期结束通知义务 |

### 9.7 反例

| 反例 | 后果 |
|------|------|
| 认为"我们是 SaaS，不需要 CE 标记" | 远程数据处理软件属于 PDE，仍需合规 |
| SBOM 缺失传递依赖或哈希 | 漏洞定位不完整，审计失败 |
| 将开源组件豁免误解为完全免责 | 商业集成仍需承担漏洞处理义务 |
| 24 小时报告流程未演练 | 真实事件时无法及时上报 |
| 技术文档以英文-only 存档 | 欧盟市场监管机构可能要求成员国语言版本 |

### 9.8 CRA 合规流程 Mermaid 图

```mermaid
flowchart TD
    A[产品设计] --> B[安全设计 & 威胁建模]
    B --> C[开发/复用组件]
    C --> D[生成 SBOM & SLSA Provenance]
    D --> E[漏洞扫描 & VEX]
    E --> F[技术文档]
    F --> G[CE 标记 & 符合性声明]
    G --> H[欧盟市场投放]
    H --> I[持续监控 & 24h 报告]
    I --> J[补丁 & 用户通知]
    J --> K[生命周期结束通知]
```

### 9.9 权威来源与交叉引用

- Regulation (EU) 2024/2847 (Cyber Resilience Act): <https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R2847>
- European Commission — Cyber Resilience Act: <https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act>
- ENISA — Cyber Resilience Act: <https://www.enisa.europa.eu/topics/cyber-resilience-act>
- CEN/CENELEC standards for CRA: <https://www.cencenelec.eu/>
- 相关概念: [Cyber Resilience Act](https://en.wikipedia.org/wiki/Cyber_Resilience_Act)
- **交叉引用**: `struct/10-supply-chain-security/02-sbom-standards/sbom-comparison.md` §7；`struct/10-supply-chain-security/01-slsa-framework/slsa-1-2-multi-track.md` §3.1；`struct/10-supply-chain-security/06-case-studies/eu-cra-checklist.md`

---

> 最后更新: 2026-07-07
> 权威来源: <https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act>


## 10. EU CRA 合规实施清单、SBOM/漏洞管理要求与示例补强

### 10.1 定义：CRA 合规义务与复用资产的法律关系

EU CRA 将"含数字元素的产品"（Products with Digital Elements, PDE）制造商定义为承担网络安全全生命周期责任的主体。在架构复用语境下，复用第三方组件**不会**转移该责任；最终产品制造商必须对集成组件的安全状态、漏洞处理和更新义务负责。

> **定义 CRA.Comp.2** (PDE Manufacturer Obligation — 补强): 任何在欧盟市场投放 PDE 的制造商，无论其自行开发或复用第三方组件，都必须实施安全设计、漏洞管理、事件响应与软件透明度四组义务。SBOM 是证明这些义务履行的关键技术文档。

### 10.2 EU CRA 合规义务完整清单

下表将 CRA 的核心义务从法规条款映射到可执行检查项，便于组织进行差距分析。

| 义务组 | 法规条款 | 具体义务 | 适用对象 | 关键日期 | 违规风险 |
|--------|---------|---------|---------|---------|---------|
| 安全设计与默认 | Article 10 + Annex I | 最小攻击面、安全默认配置、无默认凭证、加密、访问控制 | 所有 PDE 制造商 | 2027-12-11 | 市场禁入、罚款 |
| 漏洞管理 | Article 13 + Annex II | 识别、跟踪、修复漏洞；生命周期结束通知 | 所有 PDE 制造商 | 2026-09-11（报告义务） | 监管处罚 |
| 事件检测与响应 | Article 14 | 检测影响 CIA 的事件；24h 报告主动利用漏洞 | 所有 PDE 制造商 | 2026-09-11 | 罚款、声誉损失 |
| 软件透明度 | Article 14(10) + Annex V/VI | 维护 SBOM；提供技术文档；加贴 CE 标记 | 所有 PDE 制造商 | 2027-12-11 | 无法上市 |
| 开源 steward 义务 | Article 24 | 协调披露、维护漏洞政策（特定 steward） | 开源基金会 / 大型开源项目 | 2026-09-11 | 监管关注 |
| 进口商/分销商义务 | Article 25/26 | 验证制造商合规、配合市场监管 | 进口商/分销商 | 2027-12-11 | 连带责任 |

### 10.3 SBOM 具体要求补强

#### 必须包含的信息

| 字段 | 说明 | 示例 |
|------|------|------|
| 组件名称 | 所有软件组件的名称 | `log4j-core` |
| 版本信息 | 精确版本号 | `2.17.1` |
| 供应商/来源 | 组件制造商或维护者 | Apache Software Foundation |
| 许可证详情 | 许可证类型与标识符 | `Apache-2.0` (SPDX) |
| 已知漏洞 | 持续更新的 CVE/OSV 关联 | CVE-2021-44228 |
| 依赖关系 | 包括传递依赖 | `log4j-api:2.17.1` |
| 哈希校验 | 组件完整性验证 | SHA-256 digest |
|  provenance 链接 | SLSA provenance 引用 | OCI referrer 或 URL |

#### 格式与交付要求

- **机器可读格式**：SPDX 2.3+ 或 CycloneDX 1.6+ 为推荐格式。
- **随软件修改更新**：每次构建或补丁发布后，SBOM 必须同步更新。
- **应市场监管机构要求提供**：通常以电子形式交付，保存至少 10 年。
- **纳入技术文档**：SBOM 是技术文档包的必要组成部分。
- **签名与完整性**：建议对 SBOM 进行密码学签名，防止篡改。

> **定理 CRA.SBOM.1** (SBOM 作为复用契约): 在 CRA 背景下，SBOM 不仅是技术文档，更是复用资产的法律契约。缺少 SBOM 的组件将面临市场准入障碍和合规风险。

### 10.4 漏洞管理要求补强

#### 漏洞管理生命周期

| 阶段 | 行动 | 时间要求 | 输出物 |
|------|------|---------|--------|
| 1. 持续监控 | 订阅 CVE/OSV/供应商安全通告 | 实时 | 安全通告订阅列表 |
| 2. 影响评估 | 根据 SBOM 判断受影响产品 | 48 小时内 | 影响评估报告 |
| 3. 修复计划 | 制定补丁或缓解方案 | 合理时间内 | 修复计划与时间表 |
| 4. 主动利用报告 | 向 CSIRT/ENISA 报告 | 24 小时内 | 事件报告 |
| 5. 用户通知 | 向客户发布安全公告与补丁 | 补丁可用时 | 安全公告 |
| 6. 生命周期结束通知 | 提前通知产品支持终止 | EOL 前至少 6 个月 | EOL 通知 |

#### 主动利用漏洞的 24 小时报告流程

```text
发现主动利用漏洞
    ↓
30 分钟内：启动事件响应小组
    ↓
2 小时内：完成 SBOM 影响评估，确定受影响产品/版本
    ↓
6 小时内：制定临时缓解措施（如 WAF 规则、配置变更）
    ↓
24 小时内：向 ENISA/CSIRT 提交初始报告
    ↓
72 小时内：发布安全公告，提供补丁或缓解方案
    ↓
持续：跟踪漏洞修复，更新 SBOM 与 VEX
```

### 10.5 CE 标记实施步骤补强

1. **符合性评估**：依据 CRA 附件 I（网络安全要求）与附件 II（漏洞处理要求）进行内部评估或第三方认证（高风险产品）。
2. **技术文档**：包含 SBOM、威胁模型、测试报告、漏洞管理流程、事件响应计划、用户安全指南。
3. **欧盟代表**：非欧盟制造商需指定欧盟授权代表（Authorized Representative）。
4. **加贴 CE 标记**：在产品或包装上清晰加贴 CE 标记并附带符合性声明（DoC）。
5. **市场监督**：保留技术文档至少 10 年，配合市场监管机构检查。
6. **产品注册**：在欧盟市场投放前，按要求向相关数据库注册产品信息。

### 10.6 开源组件合规特别注意事项

开源组件是 CRA 合规的**高风险区**，原因包括：

- 维护者无合同义务提供安全更新。
- SBOM 通常不完整或缺失。
- 传递依赖难以追踪。
- 漏洞披露流程不一致。

**建议措施**：

1. **建立开源组件准入清单**：仅允许来自活跃社区、有安全响应流程的开源项目。
2. **强制 SCA 扫描**：每次构建必须生成并验证 SBOM。
3. **参与社区安全**：为关键开源组件贡献安全补丁或资助安全审计。
4. **备用方案**：对关键开源组件，准备商业替代方案或内部维护能力。
5. **理解 steward 义务**：若组织作为大型开源项目的 steward，需履行 CRA Article 24 的协调披露义务。

### 10.7 正例补强

| 实践 | 效果 |
|------|------|
| 在 CI/CD 中自动生成 CycloneDX SBOM 并签名 | 满足 CRA 软件透明度要求，构建可验证 |
| 建立 24 小时漏洞报告 SOP 并每季度演练 | 满足主动利用漏洞报告义务 |
| 对关键组件要求 SLSA Build L3 + Source L2 provenance | 降低第三方组件引入后门风险 |
| 产品 EOL 前 12 个月通知客户 | 满足生命周期结束通知义务 |
| 将 SBOM 与漏洞扫描工具集成，实现自动影响评估 | 缩短漏洞响应时间 |
| 对供应商合同加入 CRA 合规条款 | 明确责任分担与 SBOM 交付要求 |

### 10.8 反例补强

| 反例 | 后果 |
|------|------|
| 认为"我们是 SaaS，不需要 CE 标记" | 远程数据处理软件属于 PDE，仍需合规 |
| SBOM 缺失传递依赖或哈希 | 漏洞定位不完整，审计失败 |
| 将开源组件豁免误解为完全免责 | 商业集成仍需承担漏洞处理义务 |
| 24 小时报告流程未演练 | 真实事件时无法及时上报 |
| 技术文档以英文-only 存档 | 欧盟市场监管机构可能要求成员国语言版本 |
| 忽视产品退役后的漏洞通知义务 | EOL 后仍需在合理时间内响应未修复漏洞 |

### 10.9 CRA 合规与架构复用流程 Mermaid 图

```mermaid
flowchart TD
    A[识别 EU 市场产品] --> B[产品分类：普通/重要/关键]
    B --> C[安全设计 & 威胁建模]
    C --> D[开发/复用组件]
    D --> E[SBOM 生成与签名]
    E --> F[SLSA Provenance 验证]
    F --> G[漏洞扫描 & VEX]
    G --> H[技术文档编制]
    H --> I[符合性评估]
    I --> J[CE 标记 & DoC]
    J --> K[欧盟市场投放]
    K --> L[持续监控]
    L --> M{主动利用漏洞?}
    M -->|是| N[24h 报告 ENISA]
    M -->|否| O[常规漏洞修复]
    N --> P[补丁 & 用户通知]
    O --> P
    P --> Q[更新 SBOM & VEX]
    Q --> L
```

### 10.10 权威来源与交叉引用补强

- Regulation (EU) 2024/2847 (Cyber Resilience Act): <https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R2847>
- European Commission — Cyber Resilience Act: <https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act>
- ENISA — Cyber Resilience Act: <https://www.enisa.europa.eu/topics/cyber-resilience-act>
- CEN/CENELEC standards for CRA: <https://www.cencenelec.eu/>
- SPDX Specification: <https://spdx.dev/specifications/>
- CycloneDX Specification: <https://cyclonedx.org/specification/overview/>
- 相关概念: [Cyber Resilience Act](https://en.wikipedia.org/wiki/Cyber_Resilience_Act)
- **交叉引用**: `struct/10-supply-chain-security/02-sbom-standards/sbom-comparison.md` §7；`struct/10-supply-chain-security/01-slsa-framework/slsa-1-2-multi-track.md` §3.1；`struct/10-supply-chain-security/06-case-studies/eu-cra-checklist.md`；`struct/10-supply-chain-security/12-nist-ssdf-update/nist-ssdf-v1.2-reuse-update.md`

## 11. EU CRA 合规角色、交付物与示例清单

> **定义 CRA.Role.1** (CRA 责任主体): 在欧盟市场投放 PDE 的制造商是 CRA 义务的第一责任人；进口商与分销商承担验证与连带责任；开源 steward 在符合 Article 24 条件时承担协调披露义务。复用第三方组件并不改变制造商对产品网络安全负有的最终责任。

### 11.1 责任主体属性表

| 角色 | 法规定位 | 核心义务 | 关键交付物 | 时间要求 | 示例 |
|------|----------|----------|------------|----------|------|
| PDE 制造商 | Article 3/10/13/14 | 安全设计、漏洞管理、事件报告、SBOM | SBOM、技术文档、DoC、CE 标记 | 2026-09-11 报告义务；2027-12-11 全面适用 | 工业软件供应商 |
| 进口商 | Article 25 | 验证制造商合规、保留符合性证据 | 合规证据档案、DoC 副本 | 2027-12-11 | 欧盟外产品进口商 |
| 分销商 | Article 26 | 不销售不合规产品、配合市场监管 | 产品追溯记录、下架记录 | 2027-12-11 | 电子设备经销商 |
| 开源 steward | Article 24 | 制定漏洞政策、协调披露 | 安全政策、VEX、披露流程 | 2026-09-11 | 大型开源基金会 |

### 11.2 义务-交付物-示例关系

CRA 的合规逻辑呈链式关系：

```text
PDE 制造商（责任起点）
├── 安全设计 → 威胁模型、安全编码规范、默认安全配置
├── 漏洞管理 → SBOM + CVE 监控 + VEX + 补丁流程
├── 事件响应 → 24h 报告机制、事件记录、升级计划
└── 软件透明度 → SBOM、技术文档、CE 标记、DoC
    ↑ 进口商/分销商验证并追溯
    ↑ 开源 steward 协调披露
```

### 11.3 正例

| 实践 | 效果 |
|------|------|
| 在 CI/CD 中自动生成并签名 CycloneDX SBOM | 满足软件透明度要求，构建过程可验证 |
| 建立 24h 主动利用漏洞报告 SOP 并每季度演练 | 满足 Article 14 报告义务 |
| 对关键组件要求 SLSA Build L3 + Source L2 provenance | 降低第三方组件引入后门风险 |
| 产品 EOL 前 12 个月通知客户 | 满足生命周期结束通知义务 |
| 在供应商合同中加入 CRA 合规与 SBOM 交付条款 | 明确责任分担，降低合规盲区 |

### 11.4 反例

| 反例 | 后果 |
|------|------|
| “我们是 SaaS，不需要 CE 标记” | 远程数据处理软件属于 PDE，仍需合规 |
| SBOM 缺失传递依赖或哈希 | 漏洞定位不完整，审计失败 |
| 未指定欧盟授权代表 | 非欧盟制造商无法合法投放市场 |
| 将开源组件豁免误解为完全免责 | 商业集成仍需承担漏洞处理义务 |
| 24h 报告流程未演练 | 真实事件时无法及时上报 |
| 技术文档仅以英文存档 | 欧盟市场监管机构可能要求成员国语言版本 |

### 11.5 CRA 合规角色与交付物流程 Mermaid 图

```mermaid
flowchart LR
    M[PDE 制造商] --> SBOM[SBOM]
    M --> TD[技术文档]
    M --> VM[漏洞管理流程]
    M --> IR[事件响应计划]
    SBOM --> VEX[VEX]
    VM --> ENISA[ENISA/CSIRT 24h 报告]
    TD --> DoC[符合性声明 DoC]
    DoC --> CE[CE 标记]
    IM[进口商] -->|验证| M
    DS[分销商] -->|追溯| IM
    OS[开源 steward] -->|协调披露| VM
```

### 11.6 权威来源与交叉引用

- Regulation (EU) 2024/2847 (Cyber Resilience Act): <https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R2847>
- European Commission — Cyber Resilience Act: <https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act>
- ENISA — Cyber Resilience Act: <https://www.enisa.europa.eu/topics/cyber-resilience-act>
- CEN/CENELEC standards for CRA: <https://www.cencenelec.eu/>
- SPDX Specification: <https://spdx.dev/specifications/>
- CycloneDX Specification: <https://cyclonedx.org/specification/overview/>
- 相关概念: [Cyber Resilience Act](https://en.wikipedia.org/wiki/Cyber_Resilience_Act)
- **交叉引用**: `struct/10-supply-chain-security/02-sbom-standards/sbom-comparison.md` §7；`struct/10-supply-chain-security/01-slsa-framework/slsa-1-2-multi-track.md` §3.1；`struct/10-supply-chain-security/12-nist-ssdf-update/nist-ssdf-v1.2-reuse-update.md`


> 最后更新: 2026-07-07
> 权威来源: <https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act>
