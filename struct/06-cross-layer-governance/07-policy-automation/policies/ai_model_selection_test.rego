package ai.model.selection

test_premium_by_safety if {
    result := decision with input as {
        "task_type": "critical",
        "min_accuracy": 0.90,
        "max_latency_p99_ms": 500,
        "max_cost_per_1k_tokens": 0.10,
        "data_privacy_required": false,
        "safety_level_required": "high",
        "available_tiers": ["premium", "balanced", "economy"],
    }
    result == "PREMIUM"
    allow
}

test_premium_by_accuracy if {
    result := decision with input as {
        "task_type": "classification",
        "min_accuracy": 0.95,
        "max_latency_p99_ms": 500,
        "max_cost_per_1k_tokens": 0.10,
        "data_privacy_required": false,
        "safety_level_required": "medium",
        "available_tiers": ["premium", "balanced", "economy"],
    }
    result == "PREMIUM"
}

test_premium_by_latency if {
    result := decision with input as {
        "task_type": "chat",
        "min_accuracy": 0.80,
        "max_latency_p99_ms": 80,
        "max_cost_per_1k_tokens": 0.10,
        "data_privacy_required": false,
        "safety_level_required": "low",
        "available_tiers": ["premium", "balanced", "economy"],
    }
    result == "PREMIUM"
}

test_balanced_default if {
    result := decision with input as {
        "task_type": "summarization",
        "min_accuracy": 0.80,
        "max_latency_p99_ms": 500,
        "max_cost_per_1k_tokens": 0.05,
        "data_privacy_required": false,
        "safety_level_required": "low",
        "available_tiers": ["premium", "balanced", "economy"],
    }
    result == "BALANCED"
}

test_economy_by_cost if {
    result := decision with input as {
        "task_type": "creative",
        "min_accuracy": 0.70,
        "max_latency_p99_ms": 1000,
        "max_cost_per_1k_tokens": 0.005,
        "data_privacy_required": false,
        "safety_level_required": "low",
        "available_tiers": ["premium", "balanced", "economy"],
    }
    result == "ECONOMY"
}

test_reject_accuracy_too_high if {
    result := decision with input as {
        "task_type": "classification",
        "min_accuracy": 0.99,
        "max_latency_p99_ms": 200,
        "max_cost_per_1k_tokens": 0.05,
        "data_privacy_required": false,
        "safety_level_required": "medium",
        "available_tiers": ["premium", "balanced", "economy"],
    }
    result == "REJECT"
    not allow
}

test_reject_safety_tier_unavailable if {
    result := decision with input as {
        "task_type": "critical",
        "min_accuracy": 0.80,
        "max_latency_p99_ms": 500,
        "max_cost_per_1k_tokens": 0.10,
        "data_privacy_required": false,
        "safety_level_required": "high",
        "available_tiers": ["balanced", "economy"],
    }
    result == "REJECT"
    not allow
}

test_reject_privacy_tier_unavailable if {
    result := decision with input as {
        "task_type": "chat",
        "min_accuracy": 0.80,
        "max_latency_p99_ms": 500,
        "max_cost_per_1k_tokens": 0.10,
        "data_privacy_required": true,
        "safety_level_required": "low",
        "available_tiers": ["economy"],
    }
    result == "REJECT"
    not allow
}
