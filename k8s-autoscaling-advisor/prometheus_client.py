import httpx
from typing import Dict, Any
from datetime import datetime, timedelta
import os


class PrometheusClient:
    """
    Very small async client for Prometheus HTTP API.

    In this project we only fetch a couple of basic metrics (CPU, memory)
    to keep things simple.
    """

    def __init__(self, base_url: str | None = None):
        base_url = base_url or os.getenv("PROMETHEUS_URL", "http://localhost:9090")
        self.base_url = base_url.rstrip("/")

    async def _range_query(self, query: str, minutes: int = 60) -> Dict[str, Any]:
        """
        Run a range query on Prometheus for the last `minutes`.
        """
        end = datetime.utcnow()
        start = end - timedelta(minutes=minutes)
        step = "30s"

        params = {
            "query": query,
            "start": start.isoformat() + "Z",
            "end": end.isoformat() + "Z",
            "step": step,
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{self.base_url}/api/v1/query_range", params=params)
            resp.raise_for_status()
            return resp.json()

    async def fetch_metrics(self, namespace: str, app_name: str) -> Dict[str, Any]:
        """
        Fetch key metrics for an app: CPU, memory, etc.
        For this MVP, we focus on CPU and memory.
        """

        # Example: sum of container CPU usage for pods matching app_name in namespace
        cpu_query = (
            f"sum(rate(container_cpu_usage_seconds_total"
            f"{{namespace='{namespace}', pod=~'{app_name}.*'}}[5m]))"
        )

        # Example: sum of memory working set bytes for the same pods
        mem_query = (
            f"sum(container_memory_working_set_bytes"
            f"{{namespace='{namespace}', pod=~'{app_name}.*'}})"
        )

        cpu_data = await self._range_query(cpu_query, minutes=60)
        mem_data = await self._range_query(mem_query, minutes=60)

        return {
            "cpu": cpu_data,
            "memory": mem_data,
            # later: rps, latency, queue depth, etc.
        }
