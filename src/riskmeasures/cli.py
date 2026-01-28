"""
CLI entrypoint for the riskmeasures bootstrap OLS pipeline.

Example usage:
    python -m riskmeasures.cli
        --N 200 --B 1000
        --beta0 1 --beta1 2
        --x-sigma 1 --eps-sigma 1
        --seed 17 --log
        --out artifacts/result.json
        --save-data artifacts/data.csv
        --parallel --n-jobs 4
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Optional

import numpy as np
from riskmeasures.simulation import simulate_data
from riskmeasures.methods import estimate_beta, bootstrap_beta
from riskmeasures.utils import validate_int, validate_positive, validate_rng_seed

@dataclass(frozen=True)
class RunMetadata:
    """Metadata about a CLI run for reproducibility and logging."""
    timestamp_utc: str
    runtime_ms: int
    python_version: str


def _ensure_parent_dir(path: str) -> None:
    """Create parent directories for a file path if they don't exist."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def build_parser() -> argparse.ArgumentParser:
    """
    HELPER FUNCTION: Build the argument parser for the CLI

    Returns
    -------
    argparse.ArgumentParser
    """
    p = argparse.ArgumentParser(
        prog="riskmeasures",
        description="Simulate linear regression data and estimate bootstrap SE of OLS slope.",
    )

    p.add_argument("--N", type=int, required=True,
                   help="Number of observations to simulate.")
    p.add_argument("--beta0", type=float, default=1.0,
                   help="True intercept (beta_0). Default: 1.0")
    p.add_argument("--beta1", type=float, default=2.0,
                   help="True slope (beta_1). Default: 2.0")
    p.add_argument("--x-sigma", type=float, default=1.0,
                   help="Standard deviation of x values. Default: 1.0")
    p.add_argument("--eps-sigma", type=float, default=1.0,
                   help="Standard deviation of epsilon (error). Default: 1.0")
    p.add_argument("--seed", type=int, default=None,
                   help="Seed for RNG (both simulation and bootstrap). Default: random")
    p.add_argument("--B", type=int, required=True,
                   help="Number of bootstrap resamples.")
    p.add_argument("--parallel", action="store_true",
                   help="Enable parallel bootstrap computation.")
    p.add_argument("--n-jobs", type=int, default=1,
                   help="Number of parallel jobs (if --parallel). Default: 1")
    p.add_argument("--out", type=str, default=None,
                   help="Path to write JSON results (e.g., artifacts/result.json).")
    p.add_argument("--save-data", type=str, default=None,
                   help="Path to write simulated data CSV (e.g., artifacts/data.csv).")
    p.add_argument("--log-level", type=str, default="INFO",
                   choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                   help="Logging verbosity. Default: INFO")
    p.add_argument("--log", action="store_true",
                   help="Save results and data to timestamped artifacts directory.")

    return p


def main(argv: Optional[list[str]] = None) -> int:
    """
    Main CLI entrypoint.
    
    Parameters
    ----------
    argv : Optional[list[str]]
        Command line arguments. If None, uses sys.argv.
    
    Returns
    -------
    int
        Exit code (0 for success, non-zero for errors).
    """
    args = build_parser().parse_args(argv)

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(message)s",
    )
    log = logging.getLogger("riskmeasures")

    #Mass-validation
    try:
        N = validate_int("N", args.N, min_value=2)
        B = validate_int("B", args.B, min_value=2)
        n_jobs = validate_int("n_jobs", args.n_jobs, min_value=1)
        x_sigma = validate_positive("x_sigma", args.x_sigma)
        eps_sigma = validate_positive("eps_sigma", args.eps_sigma)
        beta0 = float(args.beta0)
        beta1 = float(args.beta1)
        seed, _ = validate_rng_seed(args.seed)
        
    except (TypeError, ValueError) as e:
        log.error("Input validation error: %s", e)
        return 2

    t0 = time.perf_counter() #For logging
    
    #--log: timestamped directory setup
    if args.log:
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = os.path.join("artifacts", timestamp_str)
        log.info("Logging enabled: saving to %s", log_dir)

    log.info("Simulating data: N=%d beta0=%.4g beta1=%.4g x_sigma=%.4g eps_sigma=%.4g seed=%d",
             N, beta0, beta1, x_sigma, eps_sigma, seed)
    data = simulate_data(
        N=N,
        beta_0=beta0,
        beta_1=beta1,
        x_sigma=x_sigma,
        epsilon_sigma=eps_sigma,
        seed=seed,
    )

    beta_hat = estimate_beta(data)
    log.info("OLS estimates: beta0_hat=%.6g beta1_hat=%.6g", beta_hat[0], beta_hat[1])
    log.info("Bootstrapping: B=%d parallel=%s n_jobs=%d seed=%d",
             B, args.parallel, n_jobs, seed)

    se_boot = bootstrap_beta(
        data=data,
        B=B,
        parallel=args.parallel,
        n_jobs=n_jobs,
        seed=seed,
    )
    log.info("Bootstrap SE(beta1_hat) = %.6g", se_boot)

    if args.save_data:
        _ensure_parent_dir(args.save_data)
        np.savetxt(args.save_data, data, delimiter=",", header="x,y", comments="")
        log.info("Saved simulated data to %s", args.save_data)
    if args.log:
        log_data_path = os.path.join(log_dir, "data.csv")
        _ensure_parent_dir(log_data_path)
        np.savetxt(log_data_path, data, delimiter=",", header="x,y", comments="")
        log.info("Saved simulated data to %s", log_data_path)

    runtime_ms = int((time.perf_counter() - t0) * 1000)
    meta = RunMetadata(
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        runtime_ms=runtime_ms,
        python_version=sys.version.split()[0],
    )

    result: dict[str, Any] = {
        "inputs": {
            "N": N,
            "B": B,
            "beta0": beta0,
            "beta1": beta1,
            "x_sigma": x_sigma,
            "eps_sigma": eps_sigma,
            "seed": seed,
            "parallel": args.parallel,
            "n_jobs": n_jobs,
        },
        "outputs": {
            "beta_hat": beta_hat.tolist(),
            "se_boot_beta1": float(se_boot),
        },
        "meta": asdict(meta),
    }

    #JSON/stdout
    if args.out:
        _ensure_parent_dir(args.out)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        log.info("Wrote results to %s", args.out)
    
    #Save to timestamped log directory if --log is enabled
    if args.log:
        log_result_path = os.path.join(log_dir, "result.json")
        _ensure_parent_dir(log_result_path)
        with open(log_result_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        log.info("Wrote results to %s", log_result_path)
    
    if not args.out and not args.log:
        print(json.dumps(result, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())