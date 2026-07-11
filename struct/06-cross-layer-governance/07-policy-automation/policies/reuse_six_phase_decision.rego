package reuse.six.phase

# 跨主题复用六阶段统一判定策略
# 对应 99-reference/tools/reuse-decision-tool-v2/data/decision_rules.json 的六阶段决策流程
# 输入：
#   semantic_compatible    bool    语义兼容性是否通过
#   variation_bindable     bool    变性绑定是否可行
#   quality_pass           bool    质量达标
#   security_pass          bool    安全合规通过
#   economic_pass          bool    成本收益通过
#   governance_pass        bool    治理合规通过
#   conditional_phases     int     条件通过的阶段数量
# 输出：
#   decision   string  APPROVE / CONDITIONAL / REJECT / NEED_MORE_INFO
#   reason     string  决策理由
#   allow      bool    是否允许复用

default decision := "NEED_MORE_INFO"

decision := "REJECT" if {
    input.semantic_compatible == false
}

decision := "REJECT" if {
    input.security_pass == false
}

decision := "REJECT" if {
    input.economic_pass == false
}

decision := "REJECT" if {
    input.conditional_phases > 2
}

decision := "APPROVE" if {
    input.semantic_compatible
    input.variation_bindable
    input.quality_pass
    input.security_pass
    input.economic_pass
    input.governance_pass
}

decision := "CONDITIONAL" if {
    decision != "REJECT"
    decision != "APPROVE"
    input.conditional_phases > 0
}

decision := "CONDITIONAL" if {
    decision != "REJECT"
    decision != "APPROVE"
    input.quality_pass == false
}

decision := "CONDITIONAL" if {
    decision != "REJECT"
    decision != "APPROVE"
    input.governance_pass == false
}

reason := "语义不兼容，拒绝复用" if {
    input.semantic_compatible == false
}

reason := "安全合规未通过，拒绝复用" if {
    input.security_pass == false
}

reason := "经济可行性不满足，拒绝复用" if {
    input.economic_pass == false
}

reason := sprintf("条件通过阶段数 %d 超过最大允许值 2，拒绝复用", [input.conditional_phases]) if {
    input.conditional_phases > 2
}

reason := "六阶段全部通过，批准复用" if {
    decision == "APPROVE"
}

reason := sprintf("存在 %d 个条件通过阶段，需附加条件满足后正式批准", [input.conditional_phases]) if {
    decision == "CONDITIONAL"
    input.conditional_phases > 0
}

reason := "质量或治理阶段未完全通过，条件批准并需整改" if {
    decision == "CONDITIONAL"
    input.conditional_phases == 0
}

reason := "缺少必要输入，无法做出复用决策" if {
    decision == "NEED_MORE_INFO"
}

allow if { decision == "APPROVE" }
allow if { decision == "CONDITIONAL" }
