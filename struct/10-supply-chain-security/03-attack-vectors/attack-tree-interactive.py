#!/usr/bin/env python3
"""Supply Chain Attack Tree Interactive Visualizer.

Generates a single-file HTML report with collapsible attack trees,
hover tooltips, and defense coverage mapping.
"""

import argparse
import html
import json
import sys
from pathlib import Path

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
        for i, child in enumerate(node["children"]):
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
        # coverage stats
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


def main():
    parser = argparse.ArgumentParser(description="Supply Chain Attack Tree Interactive Visualizer")
    parser.add_argument("--scenario", default="all", help="Scenario key or 'all'")
    parser.add_argument("--output", default="report.html", help="Output HTML file path")
    args = parser.parse_args()

    if args.scenario == "all":
        scenarios = list(ATTACK_TREES.keys())
    else:
        if args.scenario not in ATTACK_TREES:
            print(f"Unknown scenario: {args.scenario}", file=sys.stderr)
            print(f"Available: {', '.join(ATTACK_TREES.keys())}", file=sys.stderr)
            sys.exit(1)
        scenarios = [args.scenario]

    html_content = generate_html(scenarios)
    out_path = Path(args.output)
    out_path.write_text(html_content, encoding="utf-8")
    print(f"Report written to {out_path.resolve()}")


if __name__ == "__main__":
    main()
