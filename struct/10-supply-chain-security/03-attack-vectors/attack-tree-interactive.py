#!/usr/bin/env python3
"""Supply Chain Attack Tree Interactive Visualizer.

Generates a single-file HTML report with collapsible attack trees,
hover tooltips, and defense coverage mapping.

Additionally supports:
  - Mermaid (flowchart TD) export of the 7-path supply chain attack tree
  - Graphviz DOT export of the same tree
  - MITRE ATT&CK Technique ID annotations
  - Built-in self-test mode

Only Python standard library is required.
"""

import argparse
import html
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Scenario-based trees (legacy HTML visualizer)
# ---------------------------------------------------------------------------

ATTACK_TREES = {
    "dependency-confusion": {
        "title": "Dependency Confusion",
        "description": "Attacker publishes malicious package with same name as internal dependency to public registry.",
        "risk": "critical",
        "root": {
            "name": "Inject Malicious Code via Dependency",
            "risk": "critical",
            "defense": ["Private registry proxy", "Namespace scoping", "Package lock integrity"],
            "children": [
                {
                    "name": "Publish Confusing Package",
                    "risk": "high",
                    "defense": ["Internal namespace reservation", "Registry monitoring"],
                    "children": [
                        {"name": "Squat internal package name", "risk": "high", "defense": ["Proactive name reservation"]},
                        {"name": "Use higher semver version", "risk": "high", "defense": ["Version pinning", "Lockfile audits"]},
                    ],
                },
                {
                    "name": "Client Fetches Malicious Package",
                    "risk": "high",
                    "defense": ["Private registry enforcement", "Dependency firewall"],
                    "children": [
                        {"name": "Resolver prefers public registry", "risk": "medium", "defense": [".npmrc / pip.conf hardening"]},
                        {"name": "Build pipeline pulls latest", "risk": "medium", "defense": ["Immutable builds", "CI lockfile verification"]},
                    ],
                },
            ],
        },
    },
    "typosquatting": {
        "title": "Typosquatting",
        "description": "Attacker registers package names with typos of popular packages.",
        "risk": "high",
        "root": {
            "name": "Trick Developer into Installing Fake Package",
            "risk": "high",
            "defense": ["Package reputation scoring", "Automated typosquat detection"],
            "children": [
                {
                    "name": "Register Typo Name",
                    "risk": "medium",
                    "defense": ["Registry typosquat filters"],
                    "children": [
                        {"name": "Character substitution (1/l, 0/O)", "risk": "medium", "defense": ["Visual similarity scanners"]},
                        {"name": "Missing/extra hyphen", "risk": "medium", "defense": ["Fuzzy matching audits"]},
                    ],
                },
                {
                    "name": "User Mistypes Install Command",
                    "risk": "medium",
                    "defense": ["Shell autocomplete", "Package manager warnings"],
                    "children": [
                        {"name": "Copy-paste from untrusted source", "risk": "high", "defense": ["Security awareness training"]},
                        {"name": "Manual CLI entry error", "risk": "low", "defense": ["IDE integration with verification"]},
                    ],
                },
            ],
        },
    },
    "maintainer-takeover": {
        "title": "Malicious Maintainer Takeover",
        "description": "Attacker compromises or co-opts legitimate package maintainer account (XZ Utils style).",
        "risk": "critical",
        "root": {
            "name": "Insert Backdoor into Trusted Package",
            "risk": "critical",
            "defense": ["Multi-party review", "Reproducible builds", "Behavioral monitoring"],
            "children": [
                {
                    "name": "Gain Maintainer Privileges",
                    "risk": "high",
                    "defense": ["MFA enforcement", "Activity anomaly detection"],
                    "children": [
                        {"name": "Social engineering / burnout", "risk": "high", "defense": ["Project governance", "Sustainability funding"]},
                        {"name": "Credential compromise", "risk": "high", "defense": ["Passwordless / hardware tokens"]},
                    ],
                },
                {
                    "name": "Introduce Subtle Backdoor",
                    "risk": "critical",
                    "defense": ["Source code audits", "Diff reviews"],
                    "children": [
                        {"name": "Obfuscated test file injection", "risk": "critical", "defense": ["Test file integrity checks"]},
                        {"name": "Build script manipulation", "risk": "high", "defense": ["SLSA L3", "Hermetic builds"]},
                    ],
                },
            ],
        },
    },
    "build-system-compromise": {
        "title": "Build System Compromise",
        "description": "Attacker infiltrates CI/CD or build infrastructure to inject artifacts (SolarWinds style).",
        "risk": "critical",
        "root": {
            "name": "Distribute Compromised Binaries",
            "risk": "critical",
            "defense": ["SLSA L3+", "Signed provenance", "Binary transparency"],
            "children": [
                {
                    "name": "Infiltrate CI/CD Pipeline",
                    "risk": "high",
                    "defense": ["Least privilege CI tokens", "Ephemeral build environments"],
                    "children": [
                        {"name": "Compromise build agent", "risk": "high", "defense": ["Hardened runner images", "Network segmentation"]},
                        {"name": "Poison dependency cache", "risk": "high", "defense": ["Cache integrity checks", "Immutable caches"]},
                    ],
                },
                {
                    "name": "Tamper with Build Output",
                    "risk": "critical",
                    "defense": ["Signed SBOM", "Artifact attestation"],
                    "children": [
                        {"name": "Inject code post-compilation", "risk": "critical", "defense": ["Reproducible builds", "Cross-builder comparison"]},
                        {"name": "Replace signed artifact", "risk": "high", "defense": ["Key custody in HSM", "Timestamping"]},
                    ],
                },
            ],
        },
    },
    "upstream-repo-tampering": {
        "title": "Upstream Repository Tampering",
        "description": "Attacker modifies source repository or distribution channel (Codecov style).",
        "risk": "high",
        "root": {
            "name": "Serve Modified Artifacts to Consumers",
            "risk": "high",
            "defense": ["Git commit signing", "Branch protection", "Mirroring with verification"],
            "children": [
                {
                    "name": "Modify Distribution Script",
                    "risk": "high",
                    "defense": ["Checksum verification", "CDN integrity"],
                    "children": [
                        {"name": "Bash script injection", "risk": "high", "defense": ["Pipe-to-shell avoidance", "Script auditing"]},
                        {"name": "Release asset swap", "risk": "high", "defense": ["Sigstore/cosign verification"]},
                    ],
                },
                {
                    "name": "Alter Git History",
                    "risk": "medium",
                    "defense": ["Signed commits", "Immutable refs"],
                    "children": [
                        {"name": "Force-push to main", "risk": "medium", "defense": ["Branch protection rules", "Required reviews"]},
                        {"name": "Tag overwrite", "risk": "high", "defense": ["Tag signing", "Tag immutability policy"]},
                    ],
                },
            ],
        },
    },
}

RISK_COLORS = {
    "critical": "#e53e3e",
    "high": "#dd6b20",
    "medium": "#d69e2e",
    "low": "#38a169",
}

RISK_LABELS = {"critical": "Critical", "high": "High", "medium": "Medium", "low": "Low"}


# ---------------------------------------------------------------------------
# 7-path supply chain attack tree (matches attack-tree.md section 3)
# ---------------------------------------------------------------------------

SUPPLY_CHAIN_SEVEN_PATHS = {
    "id": "R",
    "type": "OR",
    "label": "损害软件供应链\nCompromise Software Supply Chain",
    "risk": "critical",
    "mitre": ["T1195", "T1195.001"],
    "children": [
        {
            "id": "P1",
            "type": "OR",
            "label": "3.1 开发环境渗透\nCompromise Development Environment",
            "risk": "high",
            "mitre": ["T1195.001", "T1078", "T1552", "T1566"],
            "children": [
                {
                    "id": "P1A1",
                    "type": "AND",
                    "label": "窃取开发者凭证\nSteal Developer Credentials",
                    "risk": "high",
                    "mitre": ["T1078", "T1552", "T1566", "T1056"],
                    "children": [
                        {"id": "P1A1L1", "type": "LEAF", "label": "网络钓鱼攻击\nPhishing Attack", "risk": "high", "mitre": ["T1566"]},
                        {"id": "P1A1L2", "type": "LEAF", "label": "凭证填充攻击\nCredential Stuffing", "risk": "high", "mitre": ["T1078"]},
                        {"id": "P1A1L3", "type": "LEAF", "label": "键盘记录恶意软件\nMalware Keylogger", "risk": "high", "mitre": ["T1056"]},
                    ],
                },
                {
                    "id": "P1A2",
                    "type": "AND",
                    "label": "攻陷 IDE / 编辑器\nCompromise IDE or Editor",
                    "risk": "high",
                    "mitre": ["T1195.001"],
                    "children": [
                        {"id": "P1A2L1", "type": "LEAF", "label": "恶意扩展 / 插件\nMalicious Extension/Plugin", "risk": "high", "mitre": ["T1195.001"]},
                        {"id": "P1A2L2", "type": "LEAF", "label": "IDE 自身供应链污染\nSupply Chain of IDE Itself", "risk": "medium", "mitre": ["T1195.001"]},
                        {"id": "P1A2L3", "type": "LEAF", "label": "被攻陷的 LSP 服务器\nCompromised LSP Server", "risk": "high", "mitre": ["T1195.001"]},
                    ],
                },
                {
                    "id": "P1A3",
                    "type": "AND",
                    "label": "污染本地工具链\nPoison Local Toolchain",
                    "risk": "medium",
                    "mitre": ["T1195.001"],
                    "children": [
                        {"id": "P1A3L1", "type": "LEAF", "label": "被篡改的编译器\nTampered Compiler", "risk": "critical", "mitre": ["T1195.001"]},
                        {"id": "P1A3L2", "type": "LEAF", "label": "恶意 Linter / Formatter\nMalicious Linter/Formatter", "risk": "medium", "mitre": ["T1195.001"]},
                        {"id": "P1A3L3", "type": "LEAF", "label": "被攻陷的调试器\nCompromised Debugger", "risk": "medium", "mitre": ["T1195.001"]},
                    ],
                },
            ],
        },
        {
            "id": "P2",
            "type": "OR",
            "label": "3.2 构建系统篡改\nCompromise Build System",
            "risk": "critical",
            "mitre": ["T1195.001", "T1059", "T1078", "T1552"],
            "children": [
                {
                    "id": "P2A1",
                    "type": "AND",
                    "label": "注入恶意构建步骤\nInject Malicious Build Step",
                    "risk": "critical",
                    "mitre": ["T1195.001", "T1059"],
                    "children": [
                        {"id": "P2A1L1", "type": "LEAF", "label": "被攻陷的 CI/CD 流水线\nCompromised CI/CD Pipeline", "risk": "critical", "mitre": ["T1195.001"]},
                        {"id": "P2A1L2", "type": "LEAF", "label": "恶意构建脚本\nMalicious Build Script", "risk": "high", "mitre": ["T1059"]},
                        {"id": "P2A1L3", "type": "LEAF", "label": "被篡改的容器镜像\nTampered Container Image", "risk": "high", "mitre": ["T1195.001"]},
                    ],
                },
                {
                    "id": "P2A2",
                    "type": "AND",
                    "label": "绕过构建验证\nBypass Build Verification",
                    "risk": "high",
                    "mitre": ["T1078", "T1552"],
                    "children": [
                        {"id": "P2A2L1", "type": "LEAF", "label": "伪造构建来源证明\nForge Build Provenance", "risk": "high", "mitre": ["T1078", "T1552"]},
                        {"id": "P2A2L2", "type": "LEAF", "label": "重放旧的有效签名\nReplay Old Valid Signature", "risk": "high", "mitre": ["T1078", "T1552"]},
                        {"id": "P2A2L3", "type": "LEAF", "label": "利用构建工具 RCE 漏洞\nExploit RCE in Build Tool", "risk": "high", "mitre": ["T1190"]},
                    ],
                },
                {
                    "id": "P2A3",
                    "type": "AND",
                    "label": "破坏构建产物\nCompromise Build Artifacts",
                    "risk": "high",
                    "mitre": ["T1195.001"],
                    "children": [
                        {"id": "P2A3L1", "type": "LEAF", "label": "构建后替换二进制\nReplace Binary After Build", "risk": "critical", "mitre": ["T1195.001"]},
                        {"id": "P2A3L2", "type": "LEAF", "label": "注入构建后钩子\nInject Post-Build Hook", "risk": "high", "mitre": ["T1195.001", "T1059"]},
                        {"id": "P2A3L3", "type": "LEAF", "label": "操纵制品仓库\nManipulate Artifact Repository", "risk": "high", "mitre": ["T1195.001"]},
                    ],
                },
            ],
        },
        {
            "id": "P3",
            "type": "OR",
            "label": "3.3 包管理器投毒\nCompromise Package Manager",
            "risk": "high",
            "mitre": ["T1195.001", "T1583", "T1584", "T1078"],
            "children": [
                {
                    "id": "P3O1",
                    "type": "OR",
                    "label": "发布恶意包\nPublish Malicious Package",
                    "risk": "high",
                    "mitre": ["T1583", "T1195.001"],
                    "children": [
                        {"id": "P3O1L1", "type": "LEAF", "label": "拼写混淆 Typosquatting", "risk": "high", "mitre": ["T1583"]},
                        {"id": "P3O1L2", "type": "LEAF", "label": "品牌抢注 Brandjacking", "risk": "high", "mitre": ["T1583"]},
                        {"id": "P3O1L3", "type": "LEAF", "label": "依赖混淆 Dependency Confusion", "risk": "high", "mitre": ["T1583", "T1195.001"]},
                    ],
                },
                {
                    "id": "P3A1",
                    "type": "AND",
                    "label": "攻陷已有包\nCompromise Existing Package",
                    "risk": "high",
                    "mitre": ["T1078", "T1199"],
                    "children": [
                        {"id": "P3A1L1", "type": "LEAF", "label": "窃取维护者凭证\nSteal Maintainer Credentials", "risk": "high", "mitre": ["T1078"]},
                        {"id": "P3A1L2", "type": "LEAF", "label": "社会工程学接管\nSocial Engineering Takeover", "risk": "high", "mitre": ["T1199"]},
                        {"id": "P3A1L3", "type": "LEAF", "label": "购买废弃包\nBuy Abandoned Package", "risk": "medium", "mitre": ["T1583"]},
                    ],
                },
                {
                    "id": "P3A2",
                    "type": "AND",
                    "label": "操纵注册表元数据\nManipulate Registry Metadata",
                    "risk": "medium",
                    "mitre": ["T1584"],
                    "children": [
                        {"id": "P3A2L1", "type": "LEAF", "label": "篡改下载统计\nAlter Download Statistics", "risk": "low", "mitre": ["T1584"]},
                        {"id": "P3A2L2", "type": "LEAF", "label": "伪造正面评价\nFake Positive Reviews", "risk": "low", "mitre": ["T1584"]},
                        {"id": "P3A2L3", "type": "LEAF", "label": "压制安全公告\nSuppress Security Advisories", "risk": "medium", "mitre": ["T1584"]},
                    ],
                },
            ],
        },
        {
            "id": "P4",
            "type": "OR",
            "label": "3.4 依赖混淆\nDependency Confusion Attack",
            "risk": "high",
            "mitre": ["T1195.001", "T1593", "T1594", "T1071", "T1567"],
            "children": [
                {
                    "id": "P4A1",
                    "type": "AND",
                    "label": "识别内部包名\nIdentify Internal Package Names",
                    "risk": "medium",
                    "mitre": ["T1593", "T1594"],
                    "children": [
                        {"id": "P4A1L1", "type": "LEAF", "label": "扫描公开仓库\nScan Public Repositories", "risk": "medium", "mitre": ["T1593"]},
                        {"id": "P4A1L2", "type": "LEAF", "label": "分析错误信息\nAnalyze Error Messages", "risk": "medium", "mitre": ["T1594"]},
                        {"id": "P4A1L3", "type": "LEAF", "label": "社会工程学\nSocial Engineering", "risk": "medium", "mitre": ["T1598"]},
                    ],
                },
                {
                    "id": "P4A2",
                    "type": "AND",
                    "label": "向公共注册表发布更高版本\nPublish Higher Version to Public Registry",
                    "risk": "high",
                    "mitre": ["T1583", "T1195.001"],
                    "children": [
                        {"id": "P4A2L1", "type": "LEAF", "label": "版本号膨胀 (9999.0.0)\nVersion Number Inflation", "risk": "high", "mitre": ["T1583"]},
                        {"id": "P4A2L2", "type": "LEAF", "label": "预发布版本操纵 (1.0.0-rc999)\nPre-release Manipulation", "risk": "high", "mitre": ["T1583"]},
                    ],
                },
            ],
        },
        {
            "id": "P5",
            "type": "OR",
            "label": "3.5 上游代码植入\nCompromise Upstream Source",
            "risk": "critical",
            "mitre": ["T1195.001", "T1071", "T1199"],
            "children": [
                {
                    "id": "P5A1",
                    "type": "AND",
                    "label": "提交恶意贡献\nSubmit Malicious Contribution",
                    "risk": "high",
                    "mitre": ["T1195.001", "T1199"],
                    "children": [
                        {"id": "P5A1L1", "type": "LEAF", "label": "伪装良性的隐藏后门 PR\nBenign-Looking PR with Hidden Backdoor", "risk": "critical", "mitre": ["T1195.001"]},
                        {"id": "P5A1L2", "type": "LEAF", "label": "利用对维护者的信任\nExploit Trust in Maintainer", "risk": "high", "mitre": ["T1199"]},
                        {"id": "P5A1L3", "type": "LEAF", "label": "攻陷贡献者账户\nCompromise Contributor Account", "risk": "high", "mitre": ["T1078"]},
                    ],
                },
                {
                    "id": "P5A2",
                    "type": "AND",
                    "label": "操纵源代码仓库\nManipulate Source Repository",
                    "risk": "high",
                    "mitre": ["T1491", "T1071"],
                    "children": [
                        {"id": "P5A2L1", "type": "LEAF", "label": "强制推送重写历史\nForce-push to Rewrite History", "risk": "high", "mitre": ["T1491"]},
                        {"id": "P5A2L2", "type": "LEAF", "label": "攻陷 Git 托管服务\nCompromise Git Hosting Service", "risk": "high", "mitre": ["T1584"]},
                        {"id": "P5A2L3", "type": "LEAF", "label": "利用 Git 漏洞\nExploit Git Vulnerability", "risk": "medium", "mitre": ["T1190"]},
                    ],
                },
                {
                    "id": "P5A3",
                    "type": "AND",
                    "label": "破坏代码审查\nSubvert Code Review",
                    "risk": "high",
                    "mitre": ["T1078"],
                    "children": [
                        {"id": "P5A3L1", "type": "LEAF", "label": "审查者疲劳攻击\nReviewer Fatigue Attack", "risk": "high", "mitre": ["T1195.001"]},
                        {"id": "P5A3L2", "type": "LEAF", "label": "被攻陷的审查者账户\nCompromised Reviewer Account", "risk": "high", "mitre": ["T1078"]},
                        {"id": "P5A3L3", "type": "LEAF", "label": "利用合并竞态条件\nExploit Race Condition in Merge", "risk": "medium", "mitre": ["T1195.001"]},
                    ],
                },
            ],
        },
        {
            "id": "P6",
            "type": "OR",
            "label": "3.6 分发渠道劫持\nCompromise Distribution Channel",
            "risk": "high",
            "mitre": ["T1195.001", "T1584", "T1557", "T1553"],
            "children": [
                {
                    "id": "P6A1",
                    "type": "AND",
                    "label": "DNS 劫持\nDNS Hijacking",
                    "risk": "high",
                    "mitre": ["T1584"],
                    "children": [
                        {"id": "P6A1L1", "type": "LEAF", "label": "攻陷 DNS 注册商\nCompromise DNS Registrar", "risk": "high", "mitre": ["T1584"]},
                        {"id": "P6A1L2", "type": "LEAF", "label": "BGP 劫持\nBGP Hijacking", "risk": "high", "mitre": ["T1584"]},
                        {"id": "P6A1L3", "type": "LEAF", "label": "污染 DNS 解析器\nPoison DNS Resolver", "risk": "medium", "mitre": ["T1584"]},
                    ],
                },
                {
                    "id": "P6A2",
                    "type": "AND",
                    "label": "下载过程 MITM\nMITM on Download",
                    "risk": "high",
                    "mitre": ["T1557"],
                    "children": [
                        {"id": "P6A2L1", "type": "LEAF", "label": "攻陷 CDN 边缘节点\nCompromise CDN Edge Node", "risk": "high", "mitre": ["T1584"]},
                        {"id": "P6A2L2", "type": "LEAF", "label": "伪造 WiFi 热点\nRogue WiFi Hotspot", "risk": "medium", "mitre": ["T1557"]},
                        {"id": "P6A2L3", "type": "LEAF", "label": "攻陷证书颁发机构\nCompromise Certificate Authority", "risk": "high", "mitre": ["T1553"]},
                    ],
                },
                {
                    "id": "P6A3",
                    "type": "AND",
                    "label": "镜像篡改\nMirror Tampering",
                    "risk": "medium",
                    "mitre": ["T1584"],
                    "children": [
                        {"id": "P6A3L1", "type": "LEAF", "label": "攻陷官方镜像\nCompromise Official Mirror", "risk": "high", "mitre": ["T1584"]},
                        {"id": "P6A3L2", "type": "LEAF", "label": "搭建 rogue 镜像\nSetup Rogue Mirror", "risk": "medium", "mitre": ["T1583"]},
                        {"id": "P6A3L3", "type": "LEAF", "label": "利用镜像同步延迟\nExploit Mirror Sync Lag", "risk": "medium", "mitre": ["T1584"]},
                    ],
                },
            ],
        },
        {
            "id": "P7",
            "type": "OR",
            "label": "3.7 运行时加载恶意组件\nRuntime Malicious Component Loading",
            "risk": "high",
            "mitre": ["T1195.001", "T1059", "T1071", "T1105", "T1574"],
            "children": [
                {
                    "id": "P7A1",
                    "type": "AND",
                    "label": "动态依赖解析\nDynamic Dependency Resolution",
                    "risk": "high",
                    "mitre": ["T1105", "T1059"],
                    "children": [
                        {"id": "P7A1L1", "type": "LEAF", "label": "运行时无验证下载\nRuntime Download Without Verification", "risk": "high", "mitre": ["T1105"]},
                        {"id": "P7A1L2", "type": "LEAF", "label": "无沙箱的插件系统\nPlugin System Without Sandbox", "risk": "high", "mitre": ["T1059"]},
                    ],
                },
                {
                    "id": "P7A2",
                    "type": "AND",
                    "label": "运行时自身供应链污染\nSupply Chain of Runtime Itself",
                    "risk": "high",
                    "mitre": ["T1195.001"],
                    "children": [
                        {"id": "P7A2L1", "type": "LEAF", "label": "被攻陷的 JVM 运行时\nCompromised JVM Runtime", "risk": "critical", "mitre": ["T1195.001"]},
                        {"id": "P7A2L2", "type": "LEAF", "label": "被篡改的 Node.js 二进制\nTampered Node.js Binary", "risk": "critical", "mitre": ["T1195.001"]},
                        {"id": "P7A2L3", "type": "LEAF", "label": "恶意 Python 解释器\nMalicious Python Interpreter", "risk": "critical", "mitre": ["T1195.001"]},
                    ],
                },
                {
                    "id": "P7A3",
                    "type": "AND",
                    "label": "运行时依赖混淆\nDependency Confusion at Runtime",
                    "risk": "medium",
                    "mitre": ["T1574"],
                    "children": [
                        {"id": "P7A3L1", "type": "LEAF", "label": "动态版本解析歧义\nDynamic Version Resolution Ambiguity", "risk": "medium", "mitre": ["T1574"]},
                    ],
                },
            ],
        },
    ],
}


# ---------------------------------------------------------------------------
# HTML generator (legacy, unchanged)
# ---------------------------------------------------------------------------

def _render_node(node, idx):
    name = html.escape(node["name"])
    risk = node.get("risk", "medium")
    color = RISK_COLORS.get(risk, "#718096")
    defense = html.escape(", ".join(node.get("defense", ["None recorded"])))
    desc = html.escape(node.get("description", ""))
    has_children = bool(node.get("children"))
    children_html = ""
    if has_children:
        child_bits = []
        for i, child in enumerate(node.get("children", [])):
            child_bits.append(_render_node(child, f"{idx}-{i}"))
        children_html = f'<div class="children" id="children-{idx}">{"".join(child_bits)}</div>'
    toggle = f'<span class="toggle" onclick="toggle(\'{idx}\')">{"▼" if has_children else "•"}</span>' if has_children else '<span class="toggle">•</span>'
    tooltip = f'<div class="tooltip">Risk: {RISK_LABELS.get(risk, risk)}<br>Defense: {defense}</div>'
    return (
        f'<div class="node" data-risk="{risk}">'
        f'{toggle} <span class="node-text" style="color:{color}">{name}</span>'
        f'{tooltip}'
        f'{children_html}'
        f'</div>'
    )


def generate_html(scenarios):
    body_parts = []
    total_nodes = 0
    covered = 0
    for key in scenarios:
        tree = ATTACK_TREES[key]
        root = tree["root"]
        body_parts.append(f'<h2>{html.escape(tree["title"])}</h2>')
        body_parts.append(f'<p class="scenario-desc">{html.escape(tree["description"])}</p>')
        body_parts.append(_render_node(root, key))

        def count(n):
            nonlocal total_nodes, covered
            total_nodes += 1
            if n.get("defense"):
                covered += 1
            for c in n.get("children", []):
                count(c)
        count(root)

    coverage_pct = round((covered / total_nodes) * 100, 1) if total_nodes else 0

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Supply Chain Attack Tree Visualization</title>
<style>
body {{ font-family: system-ui, -apple-system, sans-serif; margin: 2rem; background:#f7fafc; color:#2d3748; }}
h1 {{ color:#1a202c; }}
.node {{ margin: 4px 0 4px 24px; position: relative; }}
.toggle {{ cursor: pointer; user-select: none; font-weight: bold; color:#4a5568; }}
.node-text {{ font-weight: 600; cursor: default; }}
.children {{ margin-left: 18px; border-left: 2px solid #e2e8f0; padding-left: 8px; }}
.collapsed {{ display: none; }}
.tooltip {{ display:none; position:absolute; left:28px; top:20px; background:#1a202c; color:#fff; padding:8px 12px; border-radius:6px; font-size:0.85rem; max-width:360px; z-index:10; line-height:1.4; }}
.node:hover .tooltip {{ display:block; }}
.scenario-desc {{ color:#4a5568; margin-bottom:12px; }}
.stats {{ background:#fff; padding:16px; border-radius:8px; border:1px solid #e2e8f0; margin-bottom:24px; }}
.legend {{ display:flex; gap:12px; margin-bottom:16px; flex-wrap:wrap; }}
.legend-item {{ display:flex; align-items:center; gap:6px; font-size:0.9rem; }}
.dot {{ width:12px; height:12px; border-radius:50%; }}
</style>
</head>
<body>
<h1>Supply Chain Attack Tree Visualization</h1>
<div class="stats">
  <strong>Coverage:</strong> {covered}/{total_nodes} nodes have defense mappings ({coverage_pct}%)<br>
  <div class="legend">
    <div class="legend-item"><div class="dot" style="background:{RISK_COLORS['critical']}"></div>Critical</div>
    <div class="legend-item"><div class="dot" style="background:{RISK_COLORS['high']}"></div>High</div>
    <div class="legend-item"><div class="dot" style="background:{RISK_COLORS['medium']}"></div>Medium</div>
    <div class="legend-item"><div class="dot" style="background:{RISK_COLORS['low']}"></div>Low</div>
  </div>
</div>
{''.join(body_parts)}
<script>
function toggle(id) {{
  const el = document.getElementById('children-' + id);
  if (!el) return;
  el.classList.toggle('collapsed');
  const btn = el.previousElementSibling.previousElementSibling;
  if (btn && btn.classList.contains('toggle')) {{
    btn.textContent = el.classList.contains('collapsed') ? '▶' : '▼';
  }}
}}
// collapse all medium/low risk subtrees by default
document.querySelectorAll('.children').forEach(function(el) {{
  const parent = el.closest('.node');
  if (parent && ['medium','low'].includes(parent.dataset.risk)) {{
    el.classList.add('collapsed');
    const btn = el.previousElementSibling.previousElementSibling;
    if (btn && btn.classList.contains('toggle')) btn.textContent = '▶';
  }}
}});
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# 7-path tree exporters
# ---------------------------------------------------------------------------

def _risk_class_prefix(node_type, risk):
    """Return Mermaid class name prefix, e.g. orCritical."""
    return f"{node_type.lower()}{risk.capitalize()}"


def _mermaid_escaped_label(label, node_type=None, mitre=None):
    """Escape label for Mermaid and optionally prepend type + append MITRE IDs."""
    text = label.replace('"', '#quot;').replace("\n", "<br/>")
    if node_type == "OR":
        text = f"[OR] {text}"
    elif node_type == "AND":
        text = f"[AND] {text}"
    if mitre:
        mitre_text = ", ".join(mitre)
        text = f"{text}<br/><small>MITRE: {mitre_text}</small>"
    return text


def generate_mermaid(tree=None, include_mitre=False):
    """Generate a Mermaid flowchart TD for the 7-path supply chain attack tree."""
    tree = tree or SUPPLY_CHAIN_SEVEN_PATHS
    lines = [
        "%% 版本: 2026-06-12 | 状态: 完成 | 主题: 10 供应链安全工程 — 攻击树",
        "%% 说明: 基于 attack-tree.md 的 7 大攻击路径，使用 flowchart TD 绘制",
        "%% 图例: 菱形=AND 节点，圆角矩形=OR 节点，椭圆=叶节点；颜色按风险等级",
        "flowchart TD",
    ]

    used_classes = set()

    def walk(node):
        node_type = node["type"]
        risk = node.get("risk", "medium")
        mitre = node.get("mitre") if include_mitre else None
        label = _mermaid_escaped_label(node["label"], node_type, mitre)
        class_name = _risk_class_prefix(node_type, risk)
        used_classes.add(class_name)

        if node_type == "OR":
            lines.append(f'    {node["id"]}["{label}"]:::{class_name}')
        elif node_type == "AND":
            lines.append(f'    {node["id"]}{{"{label}"}}:::{class_name}')
        else:  # LEAF
            lines.append(f'    {node["id"]}["{label}"]:::{class_name}')

        for child in node.get("children", []):
            walk(child)
            lines.append(f'    {node["id"]} --> {child["id"]}')

    walk(tree)

    lines.append("")
    lines.append("    %% 样式定义")
    for class_name in sorted(used_classes):
        parts = class_name.lower()
        if parts.startswith("or"):
            risk = parts[2:]
        elif parts.startswith("and"):
            risk = parts[3:]
        elif parts.startswith("leaf"):
            risk = parts[4:]
        else:
            risk = "medium"
        color = RISK_COLORS.get(risk, "#718096")
        font_color = "#fff" if risk in ("critical", "high", "low") else "#000"
        penwidth = 3 if risk == "critical" else 2 if risk == "high" else 1
        if class_name.startswith("or"):
            lines.append(
                f'    classDef {class_name} fill:{color},stroke:#333,stroke-width:{penwidth}px,color:{font_color}'
            )
        elif class_name.startswith("and"):
            lines.append(
                f'    classDef {class_name} fill:{color},stroke:#333,stroke-width:{penwidth}px,color:{font_color},stroke-dasharray: 5 5'
            )
        else:
            lines.append(
                f'    classDef {class_name} fill:{color},stroke:#333,stroke-width:{penwidth}px,color:{font_color}'
            )

    return "\n".join(lines) + "\n"


def _dot_escaped_label(label, node_type=None):
    text = label.replace('"', '\\"')
    if node_type == "OR":
        text = f"[OR] {text}"
    elif node_type == "AND":
        text = f"[AND] {text}"
    return text


def generate_graphviz(tree=None, include_mitre=False):
    """Generate a Graphviz DOT file for the 7-path supply chain attack tree."""
    tree = tree or SUPPLY_CHAIN_SEVEN_PATHS
    lines = [
        "// 版本: 2026-06-12 | 状态: 完成 | 主题: 10 供应链安全工程 — 攻击树",
        "// 说明: 基于 attack-tree.md 的 7 大攻击路径的 Graphviz DOT 源文件",
        "// 图例: 菱形=AND 节点，圆角矩形=OR 节点，椭圆=叶节点；颜色按风险等级",
        "digraph SupplyChainAttackTree {",
        '    rankdir=TB;',
        '    graph [fontname="Microsoft YaHei,Segoe UI,sans-serif", bgcolor=white, margin=0];',
        '    node [fontname="Microsoft YaHei,Segoe UI,sans-serif", shape=box, style="rounded,filled", fontsize=10];',
        '    edge [fontname="Microsoft YaHei,Segoe UI,sans-serif", fontsize=9, arrowhead=none];',
        "",
        "    // 风险等级颜色（与 Mermaid 一致）",
        "    // critical=#e53e3e, high=#dd6b20, medium=#d69e2e, low=#38a169",
        "",
    ]

    def walk(node):
        node_type = node["type"]
        risk = node.get("risk", "medium")
        color = RISK_COLORS.get(risk, "#718096")
        font_color = "white" if risk in ("critical", "high", "low") else "black"
        penwidth = 3 if risk == "critical" else 2 if risk == "high" else 1
        label = _dot_escaped_label(node["label"], node_type)
        attrs = [
            f'label="{label}"',
            f'fillcolor="{color}"',
            f'fontcolor="{font_color}"',
            f'penwidth={penwidth}',
        ]
        if include_mitre and node.get("mitre"):
            mitre_text = ", ".join(node["mitre"])
            attrs.append(f'tooltip="MITRE: {mitre_text}"')

        if node_type == "OR":
            attrs.append('shape=box')
            attrs.append('style="rounded,filled"')
        elif node_type == "AND":
            attrs.append('shape=diamond')
        else:  # LEAF
            attrs.append('shape=ellipse')

        lines.append(f'    {node["id"]} [{", ".join(attrs)}];')

        for child in node.get("children", []):
            walk(child)
            lines.append(f'    {node["id"]} -> {child["id"]};')

    walk(tree)
    lines.append("}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def run_tests():
    """Built-in smoke tests for HTML, Mermaid, and Graphviz exporters."""
    errors = []

    # HTML generation (legacy)
    html_out = generate_html(list(ATTACK_TREES.keys()))
    if not html_out.strip():
        errors.append("HTML output is empty")
    for key in ATTACK_TREES:
        if key not in html_out:
            errors.append(f"HTML missing scenario key: {key}")

    # Mermaid generation
    mermaid_out = generate_mermaid()
    if not mermaid_out.strip():
        errors.append("Mermaid output is empty")
    for key_node in ("R", "P1", "P2", "P3", "P4", "P5", "P6", "P7"):
        if key_node not in mermaid_out:
            errors.append(f"Mermaid missing key node: {key_node}")
    if "flowchart TD" not in mermaid_out:
        errors.append("Mermaid missing 'flowchart TD' directive")

    # Graphviz generation
    dot_out = generate_graphviz()
    if not dot_out.strip():
        errors.append("Graphviz output is empty")
    if "digraph SupplyChainAttackTree" not in dot_out:
        errors.append("Graphviz missing 'digraph SupplyChainAttackTree'")
    for key_node in ("R", "P1", "P2", "P3", "P4", "P5", "P6", "P7"):
        if key_node not in dot_out:
            errors.append(f"Graphviz missing key node: {key_node}")

    # MITRE annotations
    mermaid_mitre = generate_mermaid(include_mitre=True)
    dot_mitre = generate_graphviz(include_mitre=True)
    if "T1195" not in mermaid_mitre:
        errors.append("Mermaid MITRE output missing T1195")
    if "T1195" not in dot_mitre:
        errors.append("Graphviz MITRE output missing T1195")

    if errors:
        print("TEST FAILED", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("TEST PASSED")
    node_attr = 'class="node"'
    print(f"  - HTML nodes: {html_out.count(node_attr)}")
    print(f"  - Mermaid lines: {len(mermaid_out.splitlines())}")
    print(f"  - Graphviz lines: {len(dot_out.splitlines())}")
    print("  - MITRE annotations present in Mermaid and Graphviz")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Supply Chain Attack Tree Interactive Visualizer")
    parser.add_argument("--scenario", default="all", help="Scenario key or 'all' (HTML mode only)")
    parser.add_argument("--output", default="report.html", help="Output file path (default: report.html)")
    parser.add_argument(
        "--format",
        choices=["html", "mermaid", "graphviz"],
        default="html",
        help="Output format (default: html). HTML uses legacy scenario trees; Mermaid/Graphviz use the 7-path tree.",
    )
    parser.add_argument("--mitre", action="store_true", help="Include MITRE ATT&CK Technique IDs in output")
    parser.add_argument("--test", action="store_true", help="Run built-in tests and exit")
    args = parser.parse_args()

    if args.test:
        return run_tests()

    if args.format == "html":
        if args.scenario == "all":
            scenarios = list(ATTACK_TREES.keys())
        else:
            if args.scenario not in ATTACK_TREES:
                print(f"Unknown scenario: {args.scenario}", file=sys.stderr)
                print(f"Available: {', '.join(ATTACK_TREES.keys())}", file=sys.stderr)
                return 1
            scenarios = [args.scenario]
        content = generate_html(scenarios)
    elif args.format == "mermaid":
        content = generate_mermaid(include_mitre=args.mitre)
    elif args.format == "graphviz":
        content = generate_graphviz(include_mitre=args.mitre)
    else:
        print(f"Unknown format: {args.format}", file=sys.stderr)
        return 1

    out_path = Path(args.output)
    out_path.write_text(content, encoding="utf-8")
    print(f"Report written to {out_path.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
