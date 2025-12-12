# Kubernetes Auto-Scaling Advisor (Prometheus + AI)

This project is an experimental **Auto-Scaling Advisor** for Kubernetes workloads.


> It watches how your Kubernetes apps behave (CPU, memory, load) and suggests better auto-scaling settings so your app stays fast and you don’t waste money and save money and time 

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

## Goals

- Build a small API that:
  1. Fetches metrics from Prometheus for a given app/namespace.
  2. Calculates simple summaries (average, p95, max).
  3. Returns a JSON response with suggested HPA/VPA values and explanations.
- Later: add a simple UI and real AI integration.
