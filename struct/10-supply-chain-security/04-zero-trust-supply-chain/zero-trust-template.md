# 零信任软件供应链架构设计模板

> **版本**: 2026-06-06
> **权威来源**: NIST SP 800-207 (Zero Trust Architecture), NIST SSDF 1.2 Draft (SP 800-218r1), Google BeyondCorp, Microsoft Zero Trust Supply Chain
> **定位**: Track D 供应链安全工程深化内容，为 Phase 4（2027-Q2）预热
> **交叉引用**: `struct/10-supply-chain-security/04-zero-trust-supply-chain/zero-trust-principles.md`, `struct/07-formal-verification/`

---

## 1. 引言：为什么软件供应链需要零信任

传统的网络安全模型假设"内网可信、外网不可信"。然而，在软件供应链中，这一假设完全失效：

- **SolarWinds (2020)**: 攻击者通过入侵构建服务器，将恶意代码注入到受信任的更新包中
- **XZ Utils (2024)**: 攻击者通过长期维护者身份渗透，在压缩库中植入后门
- **3CX (2023)**: 供应链上游的钓鱼攻击导致通信软件被篡改

NIST SP 800-207 定义的零信任架构（Zero Trust Architecture, ZTA）核心原则是 **"永不信任，始终验证"**（Never Trust, Always Verify）。将其应用于软件供应链，意味着对**每一个组件、每一次构建、每一次部署**都进行持续验证，而非信任上游供应商的安全声明。

> **公理 ZT.T1** (Zero Trust Supply Chain Transitivity): 在软件供应链中，零信任要求对每一个组件、每一个环节、每一次构建都进行验证。形式化：Trust(A, M) = Product(Trust(Xi, Xi+1)) -> 0 当链长度 > 5。

---

## 2. 五层防御矩阵

本模板将零信任软件供应链架构划分为五个防御层：身份（Identity）、设备（Device）、网络（Network）、应用（Application）、数据（Data）。每层包含信任验证点、最小权限策略和持续监控指标。

| 防御层 | NIST SP 800-207 对应 | SSDF 1.2 对应 | SLSA 映射 |
|-------|---------------------|--------------|----------|
| **身份** | Identity | PO.1, PS.1 | Source Track L2-L3 |
| **设备** | Device | PS.2 | Build Track L2-L3 |
| **网络** | Network | PW.4 | Build Track L2 |
| **应用** | Application | PW.6, PW.8 | Build Track L3-L4 |
| **数据** | Data | RV.1, RV.2 | VEX + SBOM |

---

## 3. 身份层（Identity）

### 3.1 信任验证点

| 验证点 | 控制措施 | 验证方法 |
|-------|---------|---------|
| **开发者身份** | 强制 MFA + 硬件安全密钥（FIDO2/WebAuthn） | 登录日志审计 |
| **提交者身份** | 强制 GPG/SSH commit signing | `git verify-commit` 自动检查 |
| **CI/CD 身份** | OIDC 联邦身份（非长期密钥） | Sigstore Fulcio 证书验证 |
| **审批者身份** | 分支保护 + 代码审查者身份绑定 | GitHub/GitLab 审计日志 |

### 3.2 最小权限策略

| 策略 | 实施方法 | 工具 |
|------|---------|------|
| **最小仓库访问** | 仅授予必要的仓库读/写权限 | GitHub RBAC, GitLab 权限组 |
| **最小 CI 权限** | CI token 仅访问必要的 secrets 和 registry | GitHub Actions `permissions` 关键字 |
| **临时凭证** | 所有凭证有效期 <= 1 小时 | OIDC token, short-lived PAT |
| **职责分离** | 构建者 != 部署者 != 审批者 | 组织级策略 |

### 3.3 持续监控指标

| 指标 | 阈值 | 告警级别 |
|------|------|---------|
| 未签名提交比例 | > 0% | P0（阻断构建） |
| MFA 绕过事件 | >= 1 | P0 |
| 长期凭证使用 | >= 1 | P1 |
| 特权账户登录异常 | >= 1 | P1 |
| 代码审查绕过 | >= 1 | P0 |

> **引用**: NIST SP 800-207 — "Access to individual enterprise resources is granted on a per-session basis. Trust in the requester is evaluated before the access is granted." [^1]

---

## 4. 设备层（Device）

### 4.1 信任验证点

| 验证点 | 控制措施 | 验证方法 |
|-------|---------|---------|
| **开发设备** | EDR/XDR 代理安装，设备健康证明 | CrowdStrike, Microsoft Defender |
| **构建设备** | 托管 CI runner（非 self-hosted） | GitHub Actions hosted runners |
| **构建环境** | 临时 + 隔离（Ephemeral + Isolated） | 每次构建新 VM/容器 |
| **设备清单** | 所有接入设备注册至 MDM | Intune, Jamf |

### 4.2 最小权限策略

| 策略 | 实施方法 | 工具 |
|------|---------|------|
| **设备隔离** | 开发机与生产网络物理/逻辑隔离 | VLAN, VPN 分割 |
| **构建环境无持久化** | 构建后自动销毁所有状态 | GitHub Actions, Cloud Build |
| **最小工具链** | 构建镜像仅包含必要工具 | Distroless, Wolfi, Chainguard |
| **设备准入** | 未注册设备禁止访问源码仓库 | Conditional Access Policy |

### 4.3 持续监控指标

| 指标 | 阈值 | 告警级别 |
|------|------|---------|
| 未注册设备访问源码 | >= 1 | P0 |
| Self-hosted runner 使用 | >= 1（非例外审批） | P1 |
| 构建环境 CVE 评分 | >= 7.0 | P1 |
| 设备健康评分 | < 80% | P2 |
| 异常 USB/外设使用 | >= 1 | P2 |

> **交叉引用**: `struct/04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md` 指出，Rust（Cargo）和 Go（Modules）生态的原生 vendor 支持使得完全离线构建成为可能，是设备层隔离的终极形态。

---

## 5. 网络层（Network）

### 5.1 信任验证点

| 验证点 | 控制措施 | 验证方法 |
|-------|---------|---------|
| **微分段** | 按功能/团队划分网络段 | Kubernetes NetworkPolicy, Calico |
| **加密传输** | 所有流量 TLS 1.3 | cert-manager, Istio mTLS |
| **出口控制** | 构建环境禁止任意出站连接 | 防火墙规则, NetworkPolicy |
| **DNS 安全** | DNSSEC + DNS 过滤 | Cloudflare, Pi-hole |

### 5.2 最小权限策略

| 策略 | 实施方法 | 工具 |
|------|---------|------|
| **零信任网络访问** | 无 VPN，基于身份的逐资源访问 | Zscaler, BeyondCorp Enterprise |
| **构建网络隔离** | 构建环境仅允许访问内部代理仓库 | 防火墙白名单 |
| **服务间最小通信** | 默认拒绝，显式允许 | Kubernetes NetworkPolicy |
| **API 网关控制** | 所有外部 API 调用经网关审计 | Kong, Ambassador |

### 5.3 持续监控指标

| 指标 | 阈值 | 告警级别 |
|------|------|---------|
| 未加密流量比例 | > 0% | P0 |
| 构建环境异常出站连接 | >= 1 | P0 |
| 横向移动检测 | >= 1 | P0 |
| DNS 隧道检测 | >= 1 | P0 |
| 微分段违规 | >= 1 | P1 |

---

## 6. 应用层（Application）

### 6.1 信任验证点

| 验证点 | 控制措施 | 验证方法 |
|-------|---------|---------|
| **源码完整性** | 所有变更经双人审查 | 分支保护规则 |
| **构建证明** | SLSA Provenance 生成与验证 | slsa-verifier, cosign |
| **制品签名** | 容器镜像/二进制文件签名 | Sigstore/cosign, Notary |
| **部署验证** | 仅允许签名制品部署 | Kyverno, OPA/Gatekeeper |
| **运行时完整性** | 运行时行为基线监控 | Falco, Tetragon |

### 6.2 最小权限策略

| 策略 | 实施方法 | 工具 |
|------|---------|------|
| **最小容器权限** | 非 root，只读文件系统，drop all capabilities | Kubernetes securityContext |
| **最小依赖** | 仅引入必要的直接依赖 | Dependabot, Renovate |
| **最小运行时** | 使用 Distroless 或 scratch 镜像 | Google Distroless, Chainguard |
| **最小 API 权限** | 服务账户仅拥有必要的 RBAC 权限 | Kubernetes RBAC |

### 6.3 持续监控指标

| 指标 | 阈值 | 告警级别 |
|------|------|---------|
| 未签名镜像部署 | >= 1 | P0（阻断） |
| SLSA Provenance 验证失败 | >= 1 | P0（阻断） |
| 运行时异常系统调用 | >= 1 | P1 |
| 依赖漏洞 CVSS >= 7.0 | >= 1 | P1 |
| 容器逃逸尝试 | >= 1 | P0 |

> **引用**: Google BeyondCorp — "Every access request must be authenticated, authorized, and encrypted based on device state and user credentials, regardless of network location." [^2]

---

## 7. 数据层（Data）

### 7.1 信任验证点

| 验证点 | 控制措施 | 验证方法 |
|-------|---------|---------|
| **SBOM 完整性** | 每次构建生成并签名 SBOM | Syft, Trivy + cosign |
| **数据加密** | 静态加密 + 传输加密 | AES-256-GCM, TLS 1.3 |
| **数据溯源** | 数据血缘追踪 | OpenLineage, DataHub |
| **审计日志** | 不可篡改的集中审计 | SIEM (Splunk, Sentinel) |

### 7.2 最小权限策略

| 策略 | 实施方法 | 工具 |
|------|---------|------|
| **数据分类** | 按敏感度分级（公开/内部/机密/绝密） | Microsoft Purview |
| **最小数据访问** | 按需访问，自动过期 | ABAC, Just-In-Time Access |
| **SBOM 分级共享** | 根据客户/合作伙伴级别共享不同粒度 SBOM | SBOM 分发平台 |
| **日志最小化** | 仅收集必要的审计数据 | GDPR/CCPA 合规 |

### 7.3 持续监控指标

| 指标 | 阈值 | 告警级别 |
|------|------|---------|
| 未签名 SBOM | >= 1 | P1 |
| 数据泄露检测 | >= 1 | P0 |
| 异常数据访问模式 | >= 1 | P1 |
| 审计日志完整性检查失败 | >= 1 | P0 |
| 未加密数据存储 | >= 1 | P0 |

---

## 8. 零信任供应链架构与 SLSA 等级映射

| SLSA 等级 | 身份层要求 | 设备层要求 | 网络层要求 | 应用层要求 | 数据层要求 |
|----------|-----------|-----------|-----------|-----------|-----------|
| **L1** | 基础身份验证 | 无特殊要求 | 基础 TLS | Provenance 生成 | SBOM 生成 |
| **L2** | MFA + 签名提交 | 托管构建环境 | 微分段 | 签名 Provenance | 签名 SBOM |
| **L3** | OIDC 联邦身份 | 临时 + 隔离环境 | 构建网络隔离 | 硬化构建平台 | 完整审计日志 |
| **L4** | 双人审查 + 硬件密钥 | 可复现构建环境 | 密闭网络 | 可复现构建 | 不可篡改审计 |

> **定理 ZT.T2** (Defense-in-Depth Sufficiency): 若五层防御中任意一层完全失效，其余四层仍应能独立阻止供应链攻击的成功执行。形式化：P(success|layer_i_compromised) < epsilon，其中 epsilon 为组织可接受的风险阈值。

---

## 9. 可执行检查清单（Checklist）

### 9.1 身份层检查清单

- [ ] 所有开发者账户启用 MFA（优先 FIDO2/WebAuthn）
- [ ] 所有提交强制 GPG 或 SSH 签名
- [ ] CI/CD 使用 OIDC 联邦身份，禁用长期 Personal Access Token
- [ ] 代码审查强制至少 1 名审批者（L3 要求 2 名）
- [ ] 离职员工账户在 24 小时内禁用
- [ ] 特权账户使用 Just-In-Time 访问

### 9.2 设备层检查清单

- [ ] 所有开发设备注册至 EDR/MDM 平台
- [ ] 构建使用托管 CI runner（GitHub Actions / Cloud Build / GitLab CI）
- [ ] 构建环境每次运行后销毁（Ephemeral）
- [ ] 构建镜像每月更新并扫描 CVE
- [ ] 禁止在个人设备上执行构建或访问生产环境

### 9.3 网络层检查清单

- [ ] 所有流量强制 TLS 1.3
- [ ] 构建环境禁止任意出站连接（白名单模式）
- [ ] 服务间通信默认拒绝，显式允许
- [ ] DNSSEC 在所有域名启用
- [ ] 网络微分段按团队/功能划分

### 9.4 应用层检查清单

- [ ] 所有容器镜像在构建时签名
- [ ] Kubernetes 准入控制器拒绝未签名镜像
- [ ] SLSA Provenance 生成并验证
- [ ] 容器以非 root 运行，文件系统只读
- [ ] 运行时安全监控（Falco/Tetragon）启用
- [ ] 依赖漏洞扫描集成至 CI/CD

### 9.5 数据层检查清单

- [ ] 每次构建生成 SPDX 或 CycloneDX 格式 SBOM
- [ ] SBOM 随制品签名并分发
- [ ] 静态数据加密（AES-256-GCM）
- [ ] 审计日志集中收集，保留 >= 12 个月
- [ ] 数据分类标签应用于所有敏感数据
- [ ] 第三方共享数据前签署 DPA（数据处理协议）

---

## 10. 与 SSDF 1.2 的映射

NIST SSDF 1.2 Draft（SP 800-218r1）明确将供应链风险管理作为基础项目元素。本模板的五层防御与 SSDF 实践映射如下：

| 零信任层 | SSDF 1.2 实践 | 任务 |
|---------|--------------|------|
| 身份 | PO.1, PS.1 | 组织准备、保护软件 |
| 设备 | PS.2, PW.4 | 保护软件、安全复用代码 |
| 网络 | PW.4, PW.6 | 安全复用代码、配置编译器 |
| 应用 | PW.6, PW.8 | 配置编译器、测试可执行文件 |
| 数据 | RV.1, RV.2 | 响应漏洞、VEX 发布 |

> **引用**: NIST SP 800-218r1 Draft — "SSDF v1.2 integrates supply chain risk management as a foundational project element, not an optional add-on." [^3]

---

## 11. 2026-2027 实施路线图

| 阶段 | 时间 | 目标 | 关键里程碑 |
|------|------|------|-----------|
| **Phase 1: 基础** | 2026 Q3 | 身份 + 网络层 | MFA 全覆盖、TLS 1.3 全覆盖、基础微分段 |
| **Phase 2: 构建** | 2026 Q4 | 设备 + 应用层 | 托管 CI 迁移、镜像签名、准入控制 |
| **Phase 3: 数据** | 2027 Q1 | 数据层 | SBOM 全覆盖、审计日志集中化、数据分类 |
| **Phase 4: 优化** | 2027 Q2 | 全栈自动化 | AI 辅助威胁检测、自适应零信任、L4 关键系统 |

---

## 12. 参考索引

[^1]: NIST, "Zero Trust Architecture" (SP 800-207), 2020
[^2]: Google, "BeyondCorp: A New Approach to Enterprise Security", 2014; "BeyondCorp 6: Building a Healthy Fleet", 2023
[^3]: NIST, "Secure Software Development Framework (SSDF) Version 1.2" (SP 800-218r1 Draft), 2025-12-17

---

> 最后更新: 2026-06-06
> 关联文件: zero-trust-principles.md, struct/04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md, struct/07-formal-verification/
