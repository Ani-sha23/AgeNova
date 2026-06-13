# Deployment Guide

AgeNova deploys as an inference-time application, not as a single trained model artifact. The deployed model service includes:

- FastAPI orchestration API
- Embedding model loader
- Agent routing and debate engine
- RAG memory adapters
- Monitoring endpoint for Prometheus
- Optional Qdrant and Neo4j backing services

## Local Docker Deployment

```bash
docker compose up --build
```

## Production Notes

1. Replace the mock LLM provider with an OpenAI-compatible or self-hosted model adapter.
2. Set `USE_SENTENCE_TRANSFORMERS=true` only on machines with enough memory for the embedding model.
3. Use persistent Qdrant and Neo4j volumes.
4. Put the API behind HTTPS and configure CORS for your dashboard domain.
5. Add authentication before exposing ingestion endpoints publicly.

## Suggested Cloud Layout

- API: AWS ECS, AWS App Runner, EC2, or Kubernetes
- Dashboard: Vercel, Amplify, S3 + CloudFront, or container service
- Vector database: Qdrant Cloud or self-hosted Qdrant
- Graph database: Neo4j Aura or self-hosted Neo4j
- Monitoring: Prometheus + Grafana, CloudWatch, or managed observability
