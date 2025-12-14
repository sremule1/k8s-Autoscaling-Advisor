# Kubernetes Auto-Scaling Advisor (Prometheus + AI)

This project is an experimental **Auto-Scaling Advisor** for Kubernetes workloads.


> It watches how your Kubernetes apps behave (CPU, memory, load) and suggests better auto-scaling settings so your app stays fast and you don’t waste money and save money and time 

---


## 📸 Kubernetes Auto-Scaling Screenshot
<p align="center">
<img width="1480" height="905" alt="image" src="https://github.com/user-attachments/assets/d29940d4-ee95-4dc2-a475-1bc28103d054" />

---


### Example API Response

```json
{
  "namespace": "default",
  "app_name": "myapp",
  "hpa": {
    "min_replicas": 2,
    "max_replicas": 5,
    "target_cpu_utilization": 60
  },
  "vpa": {
    "recommended_cpu_request": "200m",
    "recommended_cpu_limit": "400m",
    "recommended_memory_request": "256Mi",
    "recommended_memory_limit": "512Mi"
  },
  "reasoning": "CPU usage is moderate (20–60% at p95). Recommend a balanced HPA range and moderate requests.",
  "analysis": {
    "cpu": { "name": "cpu", "avg": 0.1575, "p95": 0.2, "max": 0.2 },
    "memory": { "name": "memory", "avg": 0.1575, "p95": 0.2, "max": 0.2 },
    "rps": null,
    "latency": null
  }
}

```




---

## What this project will do

- Connect to **Prometheus** and read metrics such as:
  - Pod CPU usage
  - Pod memory usage
  - Requests per second (RPS)
  - API latency
- Analyze these metrics over time to understand:
  - When the app is overloaded
  - When resources are being wasted
- Generate **recommendations** for:
  - Horizontal Pod Autoscaler (**HPA**) settings  
  - Vertical Pod Autoscaler (**VPA**) resource requests/limits

The idea is to eventually plug in an **AI/LLM** model so the advisor can explain the reasoning in natural language and suggest YAML snippets that can be applied directly.

---

## Tech stack (planned)

- **Language:** Python
- **API framework:** FastAPI
- **Metrics source:** Prometheus (Kubernetes cluster metrics)
- **Future:** LLM integration for smarter scaling advice

---

## Status

This repository is currently a **work in progress**.  
I am building it step by step to learn:

- Kubernetes scaling (HPA/VPA)
- Prometheus metrics
- How AI can help DevOps/SRE workflows

---

## What I Learned / Why I Built This

This project was designed to explore how AI-assisted automation can help DevOps and SRE workflows.  
During development, I learned:

- How Prometheus queries and time-series metrics work  
- How to compute statistical summaries from raw metric data  
- How HPA and VPA make scaling decisions in Kubernetes  
- How to design clean, modular services in Python/FastAPI  
- How to build a structured API with validation, documentation, and consistent response models  

The long-term goal is to replace the rule-based advisor with a true LLM that can:
- Analyze complex metric patterns  
- Suggest scaling policies  
- Explain decisions  
- Generate YAML snippets automatically  

This project represents the first version of that idea.

---

## Roadmap

- Integrate real Prometheus queries instead of mock data
- Add YAML export for HPA/VPA manifests
- Introduce ML/LLM-based advisor for adaptive scaling strategies
- Support multi-namespace and multi-cluster analysis

---

## Goals

- Build a small API that:
  1. Fetches metrics from Prometheus for a given app/namespace.
  2. Calculates simple summaries (average, p95, max).
  3. Returns a JSON response with suggested HPA/VPA values and explanations.
- Later: add a simple UI and real AI integration.








