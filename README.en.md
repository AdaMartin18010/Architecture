# Software Engineering Architecture Reuse — Structured Knowledge System

> **Version**: 2026-07-08 Phase 8 in progress · Health Check 100%
> **Mission**: Transform ~790,000 Chinese characters of source documents into a structured, verifiable, and exportable knowledge product; complete authoritative international content alignment, toolchain integration, and global output.
> **Aligned Standards**: ISO/IEC/IEEE 42010:2022, TOGAF 10, SLSA 1.2, IEC 61508, MCP 2025-11-25, A2A v1.0, and 30+ international standards
> **Health Status**: `python scripts/health-check.py` — all checks passing

---

## 📊 Project Scale

| Metric | Value |
|--------|-------|
| **Markdown files** | **330** (`struct/` 307 + `view/` 23, including 14 aggregated volumes and 9 historical snapshots) |
| **Formal specs / code** | **93** (TLA+ × 3, Alloy × 4, Coq × 2, Isabelle × 2, Mermaid × 75 + SVG × 75, Python × 7) |
| **Content volume** | **~790k Chinese characters** / **~977k total words** / **~2.94m characters** (`struct/` main repository) |
| **Top-level topics** | **13** (01–13) + **99-reference** layer |
| **Formal specifications** | TLA+ × 3, Alloy × 4, Coq × 2, Isabelle × 2, 20+ axiom-theorem systems |
| **Authoritative sources** | 30+ international standards and industry frameworks |
| **Quality gates** | `struct/` 300/300 passing, `view/` 14/14 passing, 0 dead links, 0 template padding issues |
| **Cross-index** | 0 undefined axioms / 0 duplicates; 0 standard version conflicts; 0 terminology conflicts |

---

## 🗂️ Knowledge Structure

```text
struct/
├── 01-meta-model-standards/            # Meta-models and standards alignment
│   ├── 01-iso-420xx-family/            # ISO 42010/42020/42030 family
│   ├── 02-togaf-10-alignment/          # TOGAF 10 enterprise architecture
│   ├── 03-iso-26550-ple/               # ISO 26550 product-line engineering
│   ├── 04-archimate-4/                 # ArchiMate 3.2/4.0
│   ├── 05-swebok-v4/                   # SWEBOK V4 knowledge areas
│   ├── 06-formal-axioms/               # Formal axiom systems
│   ├── 07-omg-ras/                     # OMG RAS reusable assets
│   ├── 08-fair4rs/                     # FAIR4RS research-software reuse
│   ├── 09-sysml-v2/                    # SysML v2 alignment
│   └── 10-mbse-reuse/                  # MBSE and reuse integration
├── 02-business-architecture-reuse/     # Business architecture reuse
├── 03-application-architecture-reuse/  # Application architecture reuse
├── 04-component-architecture-reuse/    # Component architecture reuse
├── 05-functional-architecture-reuse/   # Functional architecture reuse
├── 06-cross-layer-governance/          # Cross-layer governance and metrics
├── 07-formal-verification/             # Formal verification
├── 08-cognitive-architecture/          # Cognitive architecture
├── 09-value-quantification/            # Value quantification
├── 10-supply-chain-security/           # Supply-chain security
├── 11-industrial-iot-otit/             # Industrial IoT / OT-IT convergence
├── 12-ai-native-reuse/                 # AI-native reuse
├── 13-emerging-trends/                 # Emerging trends
└── 99-reference/                       # Reference layer
    ├── audit/                          # Audit reports
    ├── frontier-tracking/              # Frontier tracking
    ├── glossary/                       # Glossaries
    ├── standards-index/                # Authoritative sources index
    ├── templates/                      # Templates
    ├── tools/                          # Tool scripts
    └── visualizations/                 # Visualizations
```

---

## 🚀 Quick Navigation

| You want to learn about... | Start here |
|----------------------------|------------|
| Logical foundation of the whole system | [`01-meta-model-standards/06-formal-axioms/axiom-system.md`](struct/01-meta-model-standards/06-formal-axioms/axiom-system.md) |
| Comparison of 6 language ecosystems | [`04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md`](struct/04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md) |
| MCP / A2A protocol deep dive | [`12-ai-native-reuse/01-mcp-protocol/`](struct/12-ai-native-reuse/01-mcp-protocol/) |
| Cloud-native architecture patterns | [`03-application-architecture-reuse/07-cloud-native-patterns/reusability-matrix-2026.md`](struct/03-application-architecture-reuse/07-cloud-native-patterns/reusability-matrix-2026.md) |
| Software supply-chain attacks and defense | [`10-supply-chain-security/03-attack-vectors/attack-tree.md`](struct/10-supply-chain-security/03-attack-vectors/attack-tree.md) |
| ISA-95 + OPC UA industrial assets | [`11-industrial-iot-otit/01-isa-95-model/`](struct/11-industrial-iot-otit/01-isa-95-model/) |
| TLA+ / Alloy formal examples | [`07-formal-verification/`](struct/07-formal-verification/) |
| Visualization gallery | [`99-reference/visualizations/README.md`](struct/99-reference/visualizations/README.md) |
| Reuse maturity assessment | [`06-cross-layer-governance/03-maturity-models/assessment-questionnaire.md`](struct/06-cross-layer-governance/03-maturity-models/assessment-questionnaire.md) |
| International standards alignment | [`99-reference/standards-index/authoritative-sources-v2.md`](struct/99-reference/standards-index/authoritative-sources-v2.md) |
| English-Chinese terminology | [`99-reference/glossary/glossary-bilingual.md`](struct/99-reference/glossary/glossary-bilingual.md) |

---

## 📐 Standards Alignment Overview

This knowledge system is aligned with the following international standards and industry frameworks:

**Architecture Standards**

- ISO/IEC/IEEE 42010:2022 — Architecture description
- ISO/IEC/IEEE 42020:2019 — Architecture processes
- ISO/IEC 25010:2023 — System and software quality models
- TOGAF® Standard, 10th Edition
- ArchiMate® 3.2 / 4.0 Specification (4.0 published 2026-04-27)

**Software Engineering**

- ISO/IEC 26550:2015 — Product line engineering
- ISO/IEC 26566:2026 — Product line texture methods and tools
- ISO/IEC/IEEE 12207:2026 — Software life cycle processes
- SWEBOK V4

**Security and Supply Chain**

- SLSA 1.2
- NIST SP 800-218 / SSDF 1.2 (Initial Public Draft)
- EU CRA 2024/2847
- OWASP SCVS / LLM Top 10 / MCP Top 10

**Industrial Automation**

- ISA-95
- IEC 61508 (Ed.3 expected late 2026 / early 2027)
- ISO 26262
- IEC 63278 (Asset Administration Shell)
- PLCopen Motion Control

**Emerging Protocols**

- Model Context Protocol 2025-11-25 (RC 2026-07-28 released 2026-05-29)
- Google A2A Protocol v1.0
- WebAssembly Component Model / WASI 0.3

---

## 🗓️ Roadmap

See [`struct/MASTER_PLAN.md`](struct/MASTER_PLAN.md) for the full plan.

| Phase | Timeframe | Goal | Status |
|-------|-----------|------|--------|
| 0 | 2026-Q2 | Foundation: source document structuring | ✅ Done |
| 1–7 | 2026-Q2–2026-Q3 | Layered knowledge depth + authoritative alignment | ✅ Done |
| 8 | 2026-Q3 | Sustainable frontier tracking + internationalization | 🔄 In progress |
| 9 | 2026-Q4 | Academic output + community tooling | 🔄 Warm-up |

---

## 📖 How to Use

1. **Browse by topic**: use the Quick Navigation above.
2. **Study systematically**: read `01` → `13` in order.
3. **Practice verification**: use TLA+/Alloy/Coq specs in `07-formal-verification/`.
4. **Self-assess**: use the maturity questionnaire in `06-cross-layer-governance/`.
5. **Contribute**: follow `99-reference/book-format-guide.md`.

---

## 🔧 Toolchain

```bash
# Run all health checks
python scripts/health-check.py

# Check standard URL health
python scripts/standard-status-checker.py

# Generate quarterly frontier report
python struct/99-reference/tools/standard-tracker.py --quarterly-report

# Build deliverables
python scripts/build-deliverables.py
```

---

## ⚠️ Known Limitations

- The Docker-based formal-verification environment is configured but the local Docker daemon is not running; CI workflow `.github/workflows/formal-verification.yml` runs best-effort verification in GitHub Actions.
- MCP 2025-11-25 remains the current production-stable specification; 2026-07-28 is at Release Candidate stage.
- Git push to `origin/main` is blocked due to unauthorized SSH key; local `main` is ahead of origin.

---

## 📄 License

See [`LICENSE`](LICENSE).

---

> **Last updated**: 2026-07-08 (Phase 8: frontier tracking, standard tracker upgrade, i18n output)
> **Maintained by**: Software Engineering Architecture Reuse Knowledge System Project
