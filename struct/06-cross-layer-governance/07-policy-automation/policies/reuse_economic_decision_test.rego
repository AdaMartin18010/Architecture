package reuse.economic

test_reuse_green if { decision == {"aaf": 0.3, "absolute_upper": 1.0, "verdict": "REUSE_ECONOMIC", "reason": "AAF 0.30 < 0.70, 优先复用"} with input as {"aaf": 0.3} }

test_reuse_yellow if { decision.verdict == "TRADE_OFF" with input as {"aaf": 0.75} }

test_reuse_red if { decision.verdict == "REBUILD" with input as {"aaf": 0.95} }

test_percent_compat if { decision.aaf == 0.65 with input as {"aaf": 65} }

test_strategic_override if { allow with input as {"aaf": 0.95, "strategic_value": true} }
