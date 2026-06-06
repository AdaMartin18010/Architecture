# NIST SSDF 1.2 对齐指南

> **版本**: 2026-06-06
> **权威来源**: NIST SP 800-218r1 Initial Public Draft (2025-12-17)
> **定位**: 对齐 NIST SSDF 1.2 与软件供应链复用实践

---

## 1. SSDF 版本演进

| 版本 | 发布时间 | 状态 |
|------|---------|------|
| SSDF v1.1 (SP 800-218) | 2022-02 | 已发布 |
| **SSDF v1.2 (SP 800-218r1)** | **2025-12-17** | **公开征求意见稿** |
| SSDF v1.2 Final | 预计 2026-03 | 最终版 |

> SSDF v1.2 是根据 Executive Order 14306 的要求编制的，旨在将 SSDF、SSDF Generative AI Community Profile (SP 800-218A) 以及供应链风险实践进行整合。

---

## 2. SSDF 1.2 四大实践组

```
SSDF v1.2
├── PO: Prepare the Organization（组织准备）
├── PS: Protect the Software（保护软件）
├── PW: Produce Well-Secured Software（生产安全软件）
└── RV: Respond to Vulnerabilities（响应漏洞）
```

### 2.1 PO - Prepare the Organization

**新增**: 明确要求将软件供应链风险管理作为基础项目元素，而非可选附加项。

关键任务：

- 建立安全的软件开发生命周期
- 将供应链风险纳入整体风险管理
- 为团队提供安全培训
- 定义安全标准和要求

### 2.2 PS - Protect the Software

**更新**: 明确引用签名发布、证明（attestations）和来源生成（provenance generation）。

关键任务：

- 保护源代码和构建产物
- 实施访问控制
- 生成并验证 provenance
- 使用签名发布

### 2.3 PW - Produce Well-Secured Software

**新增**: 与 OWASP ASVS 5.0 类别对齐，引用 CycloneDX/SPDX SBOM 输出。

关键任务：

- 威胁建模
- 安全编码实践
- 代码审查
- 安全测试
- 生成 SBOM

### 2.4 RV - Respond to Vulnerabilities

**新增**: 明确引用 VEX（Vulnerability Exploitability eXchange）和基于 SBOM 的运行时漏洞匹配。

关键任务：

- 持续漏洞监控
- 漏洞优先级排序
- 及时修补
- 发布 VEX 声明

---

## 3. SSDF 1.2 vs 1.1 的四大实质性转变

| 转变 | v1.1 | v1.2 |
|------|------|------|
| **供应链风险管理** | 可选建议 | 基础项目元素 |
| **Provenance/Attestation** | 概念性推荐 | 明确命名要求 |
| **OWASP ASVS 对齐** | 未明确 | 与 ASVS 5.0 类别对齐 |
| **VEX 和 SBOM** | 新兴实践 | 明确引用 |

---

## 4. 与 SLSA 的映射

| SSDF 1.2 实践 | SLSA 1.2 对应 | 说明 |
|--------------|--------------|------|
| PO.1 | Build Track L1 | 安全的软件开发 |
| PS.1 | Source Track L1 | 保护源代码 |
| PS.2 | Build Track L2 | 保护软件免受篡改 |
| PW.4 | Build Track L2 | 安全复用代码 |
| PW.6 | Build Track L3 | 配置编译器 |
| PW.8 | Build Track L4 | 测试可执行文件 |
| RV.1 | VEX | 识别漏洞 |
| RV.2 | SBOM + VEX | 评估漏洞优先级 |

---

## 5. 与复用实践的集成

### 复用资产准入检查表

- [ ] 组件是否有 SBOM（SPDX 或 CycloneDX）？
- [ ] 组件是否提供 SLSA provenance？
- [ ] 组件的漏洞历史是否可接受？
- [ ] 组件的许可证是否兼容？
- [ ] 组件是否有活跃的维护者？
- [ ] 组件是否经过安全测试（SAST/SCA）？
- [ ] 组件是否有 VEX 声明？

### 复用者责任

> **定理 SSDF.1** (Downstream Liability Transfer): 根据 EU CRA 和 SSDF 1.2 的趋势，下游制造商对集成组件的安全负有连带责任。这意味着复用者必须对复用资产进行尽职调查。

---

## 6. 2026 合规准备

| 时间 | 行动 |
|------|------|
| 2026 Q1 | 跟踪 SSDF v1.2 最终版发布 |
| 2026 Q2 | 评估当前实践与 v1.2 的差距 |
| 2026 Q3 | 实施 SBOM 生成和 provenance |
| 2026 Q4 | 建立 VEX 发布流程 |
| 2027+ | 持续监控和改进 |

---

> 最后更新: 2026-06-06
> 权威来源: <https://csrc.nist.gov/News/2025/draft-ssdf-version-1-2>
