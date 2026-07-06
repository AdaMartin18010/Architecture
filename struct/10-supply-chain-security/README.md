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
> **公理 S.10** (Trust Transitivity Collapse): 软件供应链中的信任是传递的，但传递链的长度与信任度成指数反比。形式化：Trust(A, M) = ∏ Trust(Xᵢ, Xᵢ₊₁) ≈ 0 当链长度 > 5（工程启发式，依赖低单段信任度假设）。

## 当前状态

- [x] SLSA 四级框架详解
- [x] SLSA 1.2 Multi-Track 深度解析
- [x] XZ Utils 后门深度分析
- [x] 供应链攻击树 (`03-attack-vectors/attack-tree.md`)
- [x] 供应链攻击树交互式可视化 (Python CLI)
- [x] 供应链攻击树 Mermaid / Graphviz 双格式源文件 (`03-attack-vectors/attack-tree.{mmd,dot}`)
- [x] 供应链攻击树 MITRE ATT&CK 映射 (`03-attack-vectors/attack-tree-mitre-mapping.md`)
- [x] 组件复用准入检查单与 SBOM/Provenance 模板 (`04-provenance-examples/templates/`)
- [x] SLSA 1.0 复用安全边界详解 (`01-slsa-framework/slsa-reuse-boundaries.md`)
- [x] SLSA L4 分布式构建验证实践
- [x] SPDX/CycloneDX/SWID 复用安全对比 (`02-sbom-standards/sbom-reuse-security.md`)
- [x] 零信任供应链架构模板 (`05-zero-trust-supply-chain/zero-trust-template.md`)
- [x] NIST SSDF 1.2 Initial Public Draft 对齐 (`06-case-studies/nist-ssdf-1-2-alignment.md`)
- [x] EU CRA 合规检查清单工具 (`06-case-studies/eu-cra-checklist.py`)
- [x] EU CRA 合规检查清单工具 (Python CLI)

## 关联主题

- `04-component-architecture-reuse`（依赖治理）
- `07-formal-verification`（Rust 安全形式化）
