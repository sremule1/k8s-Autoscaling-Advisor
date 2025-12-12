from typing import Dict, Any, List
import math

from models import MetricSummary, AnalysisResult


def _extract_values(result: Dict[str, Any]) -> List[float]:
    """
    Extract numeric values from a Prometheus range query result.

    This expects the standard format:
    {
      "status": "success",
      "data": {
        "result": [
          {
            "metric": {...},
            "values": [[timestamp, value], ...]
          }
        ]
      }
    }
    """
    try:
        series = result["data"]["result"]
        if not series:
            return []
        values = [float(v[1]) for v in series[0]["values"]]
        return values
    except Exception:
        return []


def _summarize_metric(values: List[float], name: str) -> MetricSummary:
    if not values:
        return MetricSummary(name=name, avg=0.0, p95=0.0, max=0.0)

    sorted_vals = sorted(values)
    n = len(sorted_vals)
    avg = sum(sorted_vals) / n
    max_val = sorted_vals[-1]
    idx_95 = min(n - 1, math.floor(0.95 * n))
    p95 = sorted_vals[idx_95]

    return MetricSummary(name=name, avg=avg, p95=p95, max=max_val)


class MetricsAnalyzer:
    """
    Takes raw Prometheus results and turns them into simple summaries
    that are easier to use for recommendations.
    """

    def analyze(self, raw_metrics: Dict[str, Any]) -> AnalysisResult:
        cpu_vals = _extract_values(raw_metrics.get("cpu", {}))
        mem_vals = _extract_values(raw_metrics.get("memory", {}))

        cpu_summary = _summarize_metric(cpu_vals, "cpu")
        mem_summary = _summarize_metric(mem_vals, "memory")

        return AnalysisResult(
            cpu=cpu_summary,
            memory=mem_summary,
            rps=None,
            latency=None,
        )


