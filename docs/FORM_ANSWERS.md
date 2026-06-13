# Amazon ML Summer School 2026 Form Answers

## Project Title

AgeNova: Autonomous Multi-Agent Intelligence Ecosystem with Dynamic Agent Generation and Hybrid Memory

## Portfolio / Work Samples Link

https://github.com/Ani-sha23/AgeNova

## Domain

Generative AI (GenAI)

## Project Type

Original Project

## Dataset(s) Used

No fixed training dataset. AgeNova is an inference-time system.

For RAG:

- Custom runtime document corpus, variable size
- Tested target scale: approximately 10K documents / 2 GB
- Sentence embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- Vector store: in-memory default, Qdrant-compatible deployment
- Graph memory: in-memory default, Neo4j-compatible deployment

For evaluation:

- HotpotQA-style subset for retrieval accuracy
- Synthetic multi-agent coordination tasks

## Key Metrics

Metrics should be reported after reproducing them with scripts in `evaluation/`.

- RAG precision@5
- Multi-agent completion rate
- Consensus latency
- Entity relation extraction quality
- Memory retrieval hit rate
- End-to-end workflow latency

## Contribution Statement

Designed and built AgeNova end-to-end, including dynamic agent orchestration, hybrid RAG with vector and graph memory, multi-agent debate workflows, FastAPI backend, Next.js dashboard, evaluation scripts, Docker deployment, and GitHub Actions CI/CD. Implemented prompt optimization and monitoring integrations for iterative system improvement.
