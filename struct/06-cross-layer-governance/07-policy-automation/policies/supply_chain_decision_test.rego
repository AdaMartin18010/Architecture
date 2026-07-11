package supply.chain

test_critical_with_sbom_slsa3_approve if {
    result := decision with input as {
        "has_sbom": true,
        "slsa_level": 3,
        "criticality": "critical",
    }
    result == "APPROVE"
}

test_critical_no_sbom_reject if {
    result := decision with input as {
        "has_sbom": false,
        "slsa_level": 3,
        "criticality": "critical",
    }
    result == "REJECT"
}

test_critical_slsa1_reject if {
    result := decision with input as {
        "has_sbom": true,
        "slsa_level": 1,
        "criticality": "critical",
    }
    result == "REJECT"
}

test_high_slsa1_conditional if {
    result := decision with input as {
        "has_sbom": true,
        "slsa_level": 1,
        "criticality": "high",
    }
    result == "CONDITIONAL"
}

test_medium_slsa2_approve if {
    result := decision with input as {
        "has_sbom": true,
        "slsa_level": 2,
        "criticality": "medium",
    }
    result == "APPROVE"
}

test_low_with_sbom_approve if {
    result := decision with input as {
        "has_sbom": true,
        "slsa_level": 0,
        "criticality": "low",
    }
    result == "APPROVE"
}
