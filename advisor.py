from models import AnalysisResult, RecommendationResponse, HPASuggestion, VPASuggestion


class ScalingAdvisor:
    """
    Simple rule-based advisor that mimics AI-style reasoning.

    Later, this can be replaced or augmented with a real LLM call.
    """

    def recommend(self, namespace: str, app_name: str, analysis: AnalysisResult) -> RecommendationResponse:
        cpu_avg = analysis.cpu.avg
        cpu_p95 = analysis.cpu.p95

        # Very rough rules based on CPU usage
        if cpu_p95 < 0.2:
            # Underutilized -> probably over-provisioned
            min_replicas = 1
            max_replicas = 3
            target_cpu = 70
            cpu_req = "100m"
            cpu_limit = "200m"
            mem_req = "128Mi"
            mem_limit = "256Mi"
            reasoning = (
                "CPU usage is consistently low (p95 < 20%). "
                "Recommend reducing resources and using a higher CPU target "
                "to save costs while staying safe."
            )
        elif cpu_p95 < 0.6:
            # Healthy range
            min_replicas = 2
            max_replicas = 5
            target_cpu = 60
            cpu_req = "200m"
            cpu_limit = "400m"
            mem_req = "256Mi"
            mem_limit = "512Mi"
            reasoning = (
                "CPU usage is moderate (20–60% at p95). "
                "Recommend a balanced HPA range and moderate resource requests."
            )
        else:
            # High usage -> more replicas + more resources
            min_replicas = 3
            max_replicas = 8
            target_cpu = 50
            cpu_req = "300m"
            cpu_limit = "600m"
            mem_req = "512Mi"
            mem_limit = "1Gi"
            reasoning = (
                "CPU usage is high (p95 >= 60%). "
                "Recommend more replicas, lower target CPU, and higher requests/limits "
                "to keep latency under control."
            )

        hpa = HPASuggestion(
            min_replicas=min_replicas,
            max_replicas=max_replicas,
            target_cpu_utilization=target_cpu,
        )

        vpa = VPASuggestion(
            recommended_cpu_request=cpu_req,
            recommended_cpu_limit=cpu_limit,
            recommended_memory_request=mem_req,
            recommended_memory_limit=mem_limit,
        )

        return RecommendationResponse(
            namespace=namespace,
            app_name=app_name,
            hpa=hpa,
            vpa=vpa,
            reasoning=reasoning,
            analysis=analysis,
        )


