package finops.allocation

test_direct if { model == "DIRECT" with input as {"direct_tag": true} }

test_layer_based if {
    model == "LAYER_BASED"
    allow
    with input as {"direct_tag": false, "quantifiable_usage": true, "cross_layer_shared": true}
}

test_usage_based if { model == "USAGE_BASED" with input as {"direct_tag": false, "quantifiable_usage": true, "cross_layer_shared": false} }

test_risk_based if { model == "RISK_BASED" with input as {"direct_tag": false, "quantifiable_usage": false, "risk_contingent": true} }

test_overhead if { model == "OVERHEAD" with input as {"direct_tag": false, "quantifiable_usage": false, "risk_contingent": false} }
