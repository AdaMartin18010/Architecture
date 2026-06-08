#!/usr/bin/env python3
"""Bayesian Proven-in-Use (PIU) Verification Tool.

Implements IEC 61508-3-1:2016 PIU method using Bayesian statistics.
Supports Gamma-Poisson conjugate model (constant failure rate) and
Gamma-Power-Law conjugate approximation for Weibull process
(time-dependent failure rate with known shape parameter).
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy import stats


# IEC 61508 dangerous failure rate limits (per hour), low-demand mode
SIL_LIMITS = {
    1: (1e-6, 1e-5),
    2: (1e-7, 1e-6),
    3: (1e-8, 1e-7),
    4: (1e-9, 1e-8),
}


@dataclass
class ValidationResult:
    """Container for PIU validation results."""
    component: str
    hours: float
    failures: int
    target_sil: int
    confidence: float
    posterior_mean: float
    ci_lower: float
    ci_upper: float
    p_meet_sil: float
    verdict: str
    prior_type: str
    model: str
    shape: float
    posterior_samples: list


class PIUValidator:
    """Bayesian PIU validator using conjugate Gamma models."""

    def __init__(
        self,
        prior_type: str = "jeffreys",
        prior_alpha: float = 0.5,
        prior_beta: float = 0.0,
        model: str = "poisson",
        shape: float = 1.0,
    ):
        self.prior_type = prior_type
        self.prior_alpha = prior_alpha
        self.prior_beta = prior_beta
        self.model = model
        self.shape = shape

    def posterior(self, hours: float, failures: int):
        """Return posterior Gamma distribution for the failure rate.

        Poisson model: λ ~ Gamma(α+k, β+T)
        Weibull model: θ ~ Gamma(α+k, β+T^β), then λ(T)=β·θ·T^(β-1)
        """
        alpha = self.prior_alpha + failures
        if self.model == "weibull":
            eff_exposure = hours ** self.shape
            theta_scale = 1.0 / (self.prior_beta + eff_exposure)
            # Instantaneous failure rate at time T
            lambda_scale = theta_scale * self.shape * (hours ** (self.shape - 1.0))
        else:
            lambda_scale = 1.0 / (self.prior_beta + hours)
        return stats.gamma(a=alpha, scale=lambda_scale)

    def validate(
        self,
        hours: float,
        failures: int,
        target_sil: int,
        confidence: float = 0.7,
        component: str = "Single",
    ) -> ValidationResult:
        """Perform Bayesian PIU validation."""
        sil_lower, sil_upper = SIL_LIMITS[target_sil]
        post = self.posterior(hours, failures)
        post_mean = post.mean()
        ci_lower, ci_upper = post.interval(0.95)
        p_meet = post.cdf(sil_upper)

        if p_meet >= confidence:
            verdict = "PASS"
        elif (1.0 - p_meet) >= confidence:
            verdict = "FAIL"
        else:
            verdict = "INSUFFICIENT_DATA"

        samples = post.rvs(size=1000).tolist()

        return ValidationResult(
            component=component,
            hours=hours,
            failures=failures,
            target_sil=target_sil,
            confidence=confidence,
            posterior_mean=post_mean,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            p_meet_sil=p_meet,
            verdict=verdict,
            prior_type=self.prior_type,
            model=self.model,
            shape=self.shape,
            posterior_samples=samples,
        )


def format_result(r: ValidationResult) -> str:
    """Format validation result for terminal output."""
    sil_lower, sil_upper = SIL_LIMITS[r.target_sil]
    lines = [
        f"Component: {r.component}",
        f"  Operating hours      : {r.hours:,.0f} h",
        f"  Failures observed    : {r.failures}",
        f"  Target SIL           : {r.target_sil}  (limit: ≤ {sil_upper:.0e} /h)",
        f"  Model                : {r.model}" + (f" (shape={r.shape})" if r.model == "weibull" else ""),
        f"  Prior type           : {r.prior_type}",
        f"  Posterior mean λ     : {r.posterior_mean:.3e} /h",
        f"  95% Credible interval: [{r.ci_lower:.3e}, {r.ci_upper:.3e}]",
        f"  P(λ ≤ SIL bound)     : {r.p_meet_sil:.3%}",
        f"  Confidence threshold : {r.confidence:.0%}",
        f"  Verdict              : {r.verdict}",
    ]
    return "\n".join(lines)


def cmd_validate(args):
    """Handle 'validate' subcommand."""
    validator = PIUValidator(
        prior_type=args.prior,
        model=args.model,
        shape=args.shape,
    )
    result = validator.validate(
        hours=args.hours,
        failures=args.failures,
        target_sil=args.sil,
        confidence=args.confidence,
    )
    print(format_result(result))
    if args.output:
        Path(args.output).write_text(json.dumps(asdict(result), indent=2), encoding="utf-8")
    return result


def cmd_pool(args):
    """Handle 'pool' subcommand."""
    validator = PIUValidator(
        prior_type=args.prior,
        model=args.model,
        shape=args.shape,
    )
    results = []

    with open(args.data, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    by_component = defaultdict(list)
    for row in rows:
        by_component[row["component"]].append(row)

    print(f"Pooled PIU Analysis: {args.data}")
    print("=" * 60)

    for comp, comp_rows in sorted(by_component.items()):
        total_hours = sum(float(r["hours"]) for r in comp_rows)
        total_failures = sum(int(r["failures"]) for r in comp_rows)
        target_sil = int(comp_rows[0].get("target_sil", args.sil))

        result = validator.validate(
            total_hours, total_failures, target_sil, args.confidence, component=comp
        )
        results.append(result)
        print(format_result(result))
        print()

    # Grand total
    all_hours = sum(float(r["hours"]) for r in rows)
    all_failures = sum(int(r["failures"]) for r in rows)
    pooled = validator.validate(
        all_hours, all_failures, args.sil, args.confidence, component="Grand-Pooled"
    )
    results.append(pooled)
    print(format_result(pooled))

    if args.output:
        out = {"results": [asdict(r) for r in results]}
        Path(args.output).write_text(json.dumps(out, indent=2), encoding="utf-8")


def cmd_report(args):
    """Handle 'report' subcommand."""
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    print("PIU Validation Report")
    print("=" * 60)
    if isinstance(data, dict) and "results" in data:
        for r in data["results"]:
            print(format_result(ValidationResult(**r)))
            print()
    else:
        print(format_result(ValidationResult(**data)))


def main():
    parser = argparse.ArgumentParser(
        description="Bayesian Proven-in-Use (PIU) Verification Tool (IEC 61508)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Common arguments
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--prior", choices=["jeffreys", "conjugate"], default="jeffreys")
    common.add_argument("--model", choices=["poisson", "weibull"], default="poisson")
    common.add_argument("--shape", type=float, default=1.0, help="Weibull shape parameter (β)")
    common.add_argument("--confidence", type=float, default=0.7)
    common.add_argument("--output", type=str, default=None)

    # validate
    p_val = subparsers.add_parser("validate", parents=[common], help="Single-component PIU validation")
    p_val.add_argument("--hours", type=float, required=True)
    p_val.add_argument("--failures", type=int, required=True)
    p_val.add_argument("--sil", type=int, required=True, choices=[1, 2, 3, 4])

    # pool
    p_pool = subparsers.add_parser("pool", parents=[common], help="Multi-site pooled PIU analysis")
    p_pool.add_argument("--data", type=str, required=True)
    p_pool.add_argument("--sil", type=int, required=True, choices=[1, 2, 3, 4])

    # report
    p_rep = subparsers.add_parser("report", help="Generate report from JSON")
    p_rep.add_argument("--input", type=str, required=True)

    args = parser.parse_args()

    if args.command == "validate":
        cmd_validate(args)
    elif args.command == "pool":
        cmd_pool(args)
    elif args.command == "report":
        cmd_report(args)


if __name__ == "__main__":
    main()
