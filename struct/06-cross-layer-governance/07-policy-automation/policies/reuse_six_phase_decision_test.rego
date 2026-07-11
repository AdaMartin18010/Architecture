package reuse.six.phase

test_approve_all_pass if {
    result := decision with input as {
        "semantic_compatible": true,
        "variation_bindable": true,
        "quality_pass": true,
        "security_pass": true,
        "economic_pass": true,
        "governance_pass": true,
        "conditional_phases": 0,
    }
    result == "APPROVE"
    allow
}

test_reject_semantic if {
    result := decision with input as {
        "semantic_compatible": false,
        "variation_bindable": true,
        "quality_pass": true,
        "security_pass": true,
        "economic_pass": true,
        "governance_pass": true,
        "conditional_phases": 0,
    }
    result == "REJECT"
    not allow
}

test_reject_security if {
    result := decision with input as {
        "semantic_compatible": true,
        "variation_bindable": true,
        "quality_pass": true,
        "security_pass": false,
        "economic_pass": true,
        "governance_pass": true,
        "conditional_phases": 0,
    }
    result == "REJECT"
    not allow
}

test_reject_economic if {
    result := decision with input as {
        "semantic_compatible": true,
        "variation_bindable": true,
        "quality_pass": true,
        "security_pass": true,
        "economic_pass": false,
        "governance_pass": true,
        "conditional_phases": 0,
    }
    result == "REJECT"
    not allow
}

test_reject_too_many_conditional if {
    result := decision with input as {
        "semantic_compatible": true,
        "variation_bindable": true,
        "quality_pass": true,
        "security_pass": true,
        "economic_pass": true,
        "governance_pass": true,
        "conditional_phases": 3,
    }
    result == "REJECT"
    not allow
}

test_conditional_quality if {
    result := decision with input as {
        "semantic_compatible": true,
        "variation_bindable": true,
        "quality_pass": false,
        "security_pass": true,
        "economic_pass": true,
        "governance_pass": true,
        "conditional_phases": 1,
    }
    result == "CONDITIONAL"
    allow
}

test_conditional_governance if {
    result := decision with input as {
        "semantic_compatible": true,
        "variation_bindable": true,
        "quality_pass": true,
        "security_pass": true,
        "economic_pass": true,
        "governance_pass": false,
        "conditional_phases": 1,
    }
    result == "CONDITIONAL"
    allow
}
