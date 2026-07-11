package reuse.matrix

test_upgrade_component_to_app_service if {
    result := decision with input as {
        "current_layer": "component",
        "consumers": 5,
        "cross_team": true,
        "cross_org": false,
        "tech_compatibility_ratio": 0.9,
        "semantic_coverage_ratio": 0.85,
        "coupling_impact_ratio": 0.1,
        "security_level_required": "L2",
        "component_cert_level": "L2",
        "confidence_gamma": 0.95,
        "config_conflicts": 0,
        "latency_requirement_ms": 200,
        "shared_service_p99_ms": 150,
        "upgrade_benefit": 10.0,
        "downgrade_benefit": 0.0,
    }
    result == "UPGRADE"
    target_layer == "app_service"
}

test_upgrade_with_security_review if {
    result := decision with input as {
        "current_layer": "app_service",
        "consumers": 5,
        "cross_team": true,
        "cross_org": false,
        "tech_compatibility_ratio": 0.9,
        "semantic_coverage_ratio": 0.85,
        "coupling_impact_ratio": 0.1,
        "security_level_required": "L4",
        "component_cert_level": "L2",
        "confidence_gamma": 0.95,
        "config_conflicts": 0,
        "latency_requirement_ms": 200,
        "shared_service_p99_ms": 150,
        "upgrade_benefit": 10.0,
        "downgrade_benefit": 0.0,
    }
    result == "SECURITY_REVIEW"
}

test_upgrade_with_adapter if {
    result := decision with input as {
        "current_layer": "component",
        "consumers": 5,
        "cross_team": true,
        "cross_org": false,
        "tech_compatibility_ratio": 0.6,
        "semantic_coverage_ratio": 0.85,
        "coupling_impact_ratio": 0.1,
        "security_level_required": "L2",
        "component_cert_level": "L2",
        "confidence_gamma": 0.95,
        "config_conflicts": 0,
        "latency_requirement_ms": 200,
        "shared_service_p99_ms": 150,
        "upgrade_benefit": 10.0,
        "downgrade_benefit": 0.0,
    }
    result == "ADAPTER"
}

test_downgrade_by_coupling if {
    result := decision with input as {
        "current_layer": "business_service",
        "consumers": 8,
        "cross_team": true,
        "cross_org": true,
        "tech_compatibility_ratio": 0.9,
        "semantic_coverage_ratio": 0.85,
        "coupling_impact_ratio": 0.4,
        "security_level_required": "L2",
        "component_cert_level": "L2",
        "confidence_gamma": 0.95,
        "config_conflicts": 0,
        "latency_requirement_ms": 200,
        "shared_service_p99_ms": 150,
        "upgrade_benefit": 0.0,
        "downgrade_benefit": 5.0,
    }
    result == "DOWNGRADE"
    target_layer == "app_service"
}

test_downgrade_by_security_mismatch if {
    result := decision with input as {
        "current_layer": "component",
        "consumers": 2,
        "cross_team": false,
        "cross_org": false,
        "tech_compatibility_ratio": 0.9,
        "semantic_coverage_ratio": 0.85,
        "coupling_impact_ratio": 0.1,
        "security_level_required": "L4",
        "component_cert_level": "L2",
        "confidence_gamma": 0.95,
        "config_conflicts": 0,
        "latency_requirement_ms": 200,
        "shared_service_p99_ms": 150,
        "upgrade_benefit": 0.0,
        "downgrade_benefit": 5.0,
    }
    result == "DOWNGRADE"
    target_layer == "function"
}

test_maintain if {
    result := decision with input as {
        "current_layer": "component",
        "consumers": 2,
        "cross_team": false,
        "cross_org": false,
        "tech_compatibility_ratio": 0.9,
        "semantic_coverage_ratio": 0.85,
        "coupling_impact_ratio": 0.1,
        "security_level_required": "L2",
        "component_cert_level": "L2",
        "confidence_gamma": 0.95,
        "config_conflicts": 0,
        "latency_requirement_ms": 200,
        "shared_service_p99_ms": 150,
        "upgrade_benefit": 0.0,
        "downgrade_benefit": 0.0,
    }
    result == "MAINTAIN"
}

test_deprecate if {
    result := decision with input as {
        "current_layer": "function",
        "consumers": 0,
        "cross_team": false,
        "cross_org": false,
        "tech_compatibility_ratio": 0.9,
        "semantic_coverage_ratio": 0.85,
        "coupling_impact_ratio": 0.1,
        "security_level_required": "L2",
        "component_cert_level": "L2",
        "confidence_gamma": 0.95,
        "config_conflicts": 0,
        "latency_requirement_ms": 200,
        "shared_service_p99_ms": 150,
        "upgrade_benefit": 0.0,
        "downgrade_benefit": 0.0,
    }
    result == "DEPRECATE"
}
