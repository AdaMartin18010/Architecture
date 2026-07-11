package supply.chain

# 供应链安全复用决策策略
# 输入：
#   has_sbom        bool   是否提供 SBOM
#   slsa_level      int    SLSA 等级 (0-4)
#   criticality     string 组件关键性 (critical/high/medium/low)
#   has_provenance  bool   是否提供 provenance（可选，默认 true）
# 输出：
#   decision        string APPROVE / CONDITIONAL / REJECT
#   reason          string 决策理由

default decision := "REJECT"

decision := "APPROVE" if {
    input.has_sbom == true
    input.slsa_level >= 2
    input.criticality != "critical"
}

decision := "REJECT" if {
    input.criticality == "critical"
    not input.has_sbom
}

decision := "REJECT" if {
    input.criticality == "critical"
    input.slsa_level < 2
}

decision := "CONDITIONAL" if {
    input.has_sbom == true
    input.slsa_level == 1
}

decision := "CONDITIONAL" if {
    input.criticality == "high"
    input.slsa_level < 2
}

decision := "APPROVE" if {
    input.criticality == "low"
    input.has_sbom == true
}

reason := sprintf("关键组件 %s 必须提供 SBOM 且 SLSA >= 2，当前 SLSA=%d", [input.criticality, input.slsa_level]) if {
    input.criticality == "critical"
    not input.has_sbom
}

reason := sprintf("关键组件 %s 必须 SLSA >= 2，当前 SLSA=%d", [input.criticality, input.slsa_level]) if {
    input.criticality == "critical"
    input.slsa_level < 2
}

reason := "组件提供 SBOM 且 SLSA >= 2，供应链风险可控" if {
    input.has_sbom == true
    input.slsa_level >= 2
    input.criticality != "critical"
}

reason := sprintf("高关键组件建议 SLSA >= 2，当前 SLSA=%d，需人工复核", [input.slsa_level]) if {
    input.criticality == "high"
    input.slsa_level < 2
}

reason := sprintf("SLSA=%d 仅满足基础 provenance，建议提升到 >=2", [input.slsa_level]) if {
    input.has_sbom == true
    input.slsa_level == 1
}

reason := "低关键组件提供 SBOM 即可接受" if {
    input.criticality == "low"
    input.has_sbom == true
}

reason := "缺少 SBOM，无法评估供应链风险" if {
    not input.has_sbom
    not reason
}

allow if { decision == "APPROVE" }
