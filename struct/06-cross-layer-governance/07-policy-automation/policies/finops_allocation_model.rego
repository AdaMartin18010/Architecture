package finops.allocation

default model := "UNKNOWN"

model := "DIRECT" if {
    input.direct_tag == true
}

model := "LAYER_BASED" if {
    not input.direct_tag
    input.quantifiable_usage == true
    input.cross_layer_shared == true
}

model := "USAGE_BASED" if {
    not input.direct_tag
    input.quantifiable_usage == true
    not input.cross_layer_shared
}

model := "RISK_BASED" if {
    not input.direct_tag
    not input.quantifiable_usage
    input.risk_contingent == true
}

model := "OVERHEAD" if {
    not input.direct_tag
    not input.quantifiable_usage
    not input.risk_contingent
}

# 强制约束：跨层共享必须使用 Layer-Based
allow if {
    model == "LAYER_BASED"
}

allow if {
    model == "DIRECT"
}

allow if {
    model == "USAGE_BASED"
}

allow if {
    model == "RISK_BASED"
}

allow if {
    model == "OVERHEAD"
}

default deny_reason := ""

deny_reason := sprintf("跨层共享成本项必须选择 Layer-Based，当前模型=%s", [model]) if {
    input.cross_layer_shared == true
    model != "LAYER_BASED"
}

violation if {
    input.cross_layer_shared == true
    model != "LAYER_BASED"
}

reason := sprintf("成本项采用 %s 分摊模型", [model]) if { allow }
reason := sprintf("跨层共享成本项必须选择 Layer-Based，当前模型=%s", [model]) if { violation }
