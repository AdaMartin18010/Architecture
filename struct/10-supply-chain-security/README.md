# 10 供应链安全工程

## 定位

组件复用的关键风险领域。2026 年，软件供应链攻击已成为组织面临的最严峻安全威胁之一。

## 核心内容

- **SLSA 1.0 四级框架深度解析**
  - L1: 基础构建（Provenance）
  - L2: 托管构建（Build Isolation）
  - L3: 强化构建（Hermetic Build）
  - L4: 最高等级（可复现 + 双因素审查）
- **SBOM 深度**: SPDX 2.3 vs CycloneDX 1.6 vs SWID
- **供应链攻击案例**（2021-2026）
  - Log4j / SolarWinds / XZ Utils / 3CX / PyTorch 恶意依赖
- **纵深防御**: 零信任软件供应链架构（5 层防御）
- **Rust 生态复用安全**: Cargo 依赖解析、统一版本策略、unsafe 边界

## 权威对齐

- [SLSA.dev](https://slsa.dev) (OpenSSF)
- [Sigstore](https://www.sigstore.dev) (Linux Foundation)
- [OpenSSF](https://openssf.org) (Supply Chain Security)
- [NIST SSDF](https://csrc.nist.gov/projects/ssdf)
- [OWASP SCVS](https://owasp.org/www-project-software-component-verification-standard/)

## 关键公理
>
> **公理 S.1** (Trust Transitivity Collapse): 软件供应链中的信任是传递的，但传递链的长度与信任度成指数反比。形式化：Trust(A, M) = ∏ Trust(Xᵢ, Xᵢ₊₁) ≈ 0 当链长度 > 5。

## 当前状态

- [x] SLSA 四级框架详解
- [x] XZ Utils 后门深度分析
- [ ] SLSA L4 分布式构建验证（多签名、可复现性）
- [ ] 供应链攻击树（Attack Tree）可视化

## 关联主题

- `04-component-architecture-reuse`（依赖治理）
- `07-formal-verification`（Rust 安全形式化）
