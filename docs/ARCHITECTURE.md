# Architecture

AgeNova separates the system into five layers.

## 1. API Layer

The FastAPI service exposes document ingestion, agent execution, memory inspection, and health endpoints.

## 2. Orchestration Layer

The orchestrator creates a task-specific group of agents. Each agent receives a role, goal, constraints, and access to shared retrieval memory.

## 3. RAG Layer

The RAG pipeline chunks documents, embeds them, stores vectors, and retrieves relevant evidence for agent reasoning.

## 4. Hybrid Memory Layer

Vector memory handles semantic recall. Graph memory extracts lightweight entity co-occurrences and relation hints so the system can preserve structured context across tasks.

## 5. Evaluation Layer

Retrieval and agent coordination scripts provide reproducible checks for precision, completion rate, and trace quality.
