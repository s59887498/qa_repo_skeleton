"""Bounded local load example with staggered/simultaneous workers and honest metrics."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import ProxyHandler, Request, build_opener
from uuid import uuid4

from qa_demo.server import demo_server


def percentile(values, percent):
    """Nearest-rank percentile, including failed-request latency."""
    if not values:
        raise ValueError("No samples")
    return sorted(values)[max(0, math.ceil(len(values) * percent / 100) - 1)]


def run_load(url, *, count=40, workers=4, mode="staggered", ramp_interval=0.05, path="/health"):
    parsed = urlsplit(url)
    if parsed.scheme != "http" or parsed.hostname != "127.0.0.1" or parsed.username or parsed.password:
        raise ValueError("This teaching runner supports loopback HTTP only")
    if not 1 <= count <= 2000 or not 1 <= workers <= min(32, count):
        raise ValueError("Require 1 <= workers <= min(32, count), count <= 2000")
    if mode not in {"staggered", "simultaneous"} or not 0 <= ramp_interval <= 1:
        raise ValueError("Invalid mode or ramp interval")
    barrier = threading.Barrier(workers) if mode == "simultaneous" else None
    start = time.perf_counter()

    def worker(index):
        opener = build_opener(ProxyHandler({}))
        if barrier:
            barrier.wait(timeout=10)
        else:
            time.sleep(index * ramp_interval)
        samples = []
        for sequence in range(index, count, workers):
            request_start = time.perf_counter()
            status, ok = 0, False
            try:
                with opener.open(Request(url + path), timeout=2) as response:
                    status = response.status
                    ok = status == 200 and json.load(response) == {"status": "ok"}
            except HTTPError as error:
                status = error.code
                error.close()
            except (URLError, TimeoutError, OSError, ValueError):
                pass
            samples.append({"sequence": sequence, "status": status, "ok": ok,
                            "latency_ms": round((time.perf_counter() - request_start) * 1000, 3),
                            "started_ms": round((request_start - start) * 1000, 3)})
        return samples

    with ThreadPoolExecutor(max_workers=workers) as pool:
        samples = [sample for group in pool.map(worker, range(workers)) for sample in group]
    elapsed = time.perf_counter() - start
    failures = sum(not sample["ok"] for sample in samples)
    return {
        "scope": "synthetic local HTTP requests; not product test-case coverage",
        "mode": mode, "workers": workers, "requests": len(samples), "failures": failures,
        "error_rate": failures / len(samples), "duration_seconds": round(elapsed, 3),
        "requests_per_second": round(len(samples) / elapsed, 3),
        "p50_ms": percentile([s["latency_ms"] for s in samples], 50),
        "p95_ms": percentile([s["latency_ms"] for s in samples], 95),
        "samples": sorted(samples, key=lambda sample: sample["sequence"]),
    }


def meets_thresholds(result, *, p95_ms, error_rate):
    return result["requests"] > 0 and result["p95_ms"] <= p95_ms and result["error_rate"] <= error_rate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["staggered", "simultaneous"], default="staggered")
    parser.add_argument("--requests", type=int, default=40)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--p95-ms", type=float, default=500)
    parser.add_argument("--max-error-rate", type=float, default=0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not math.isfinite(args.p95_ms) or args.p95_ms <= 0 or not 0 <= args.max_error_rate <= 1:
        parser.error("Thresholds must be finite: p95 > 0, error rate between 0 and 1")
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    directory = args.output or Path("artifacts/load") / run_id
    directory.mkdir(parents=True, exist_ok=False)
    with demo_server() as url:
        result = run_load(url, count=args.requests, workers=args.workers, mode=args.mode)
    result["run_id"] = run_id
    result["thresholds"] = {"p95_ms": args.p95_ms, "max_error_rate": args.max_error_rate}
    result["passed"] = meets_thresholds(result, p95_ms=args.p95_ms, error_rate=args.max_error_rate)
    (directory / "results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    summary = {key: value for key, value in result.items() if key != "samples"}
    (directory / "summary.md").write_text("# Local load example\n\n```json\n" + json.dumps(summary, indent=2) + "\n```\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
