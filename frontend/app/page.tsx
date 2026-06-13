"use client";

import { Activity, Brain, Database, Network, Play, Upload } from "lucide-react";
import { useMemo, useState } from "react";

type Evidence = {
  document_id: string;
  chunk_id: string;
  text: string;
  score: number;
};

type AgentTrace = {
  agent: string;
  role: string;
  answer: string;
  confidence: number;
  evidence_ids: string[];
};

type RunResponse = {
  task: string;
  final_answer: string;
  consensus_score: number;
  agents: AgentTrace[];
  evidence: Evidence[];
  latency_ms: number;
};

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

const demoDocument = `AgeNova is an autonomous multi-agent intelligence ecosystem. It combines dynamic agent generation, a retrieval augmented generation pipeline, vector memory, graph memory, consensus debate, FastAPI serving, Next.js visualization, Docker deployment, and monitoring through Prometheus and Grafana.`;

export default function Home() {
  const [task, setTask] = useState("Explain how AgeNova uses hybrid memory and agent consensus.");
  const [documentText, setDocumentText] = useState(demoDocument);
  const [result, setResult] = useState<RunResponse | null>(null);
  const [status, setStatus] = useState("Ready");
  const [loading, setLoading] = useState(false);

  const bestAgent = useMemo(() => {
    if (!result?.agents.length) return null;
    return [...result.agents].sort((a, b) => b.confidence - a.confidence)[0];
  }, [result]);

  async function ingestDemo() {
    setLoading(true);
    setStatus("Indexing document memory...");
    try {
      const response = await fetch(`${apiUrl}/v1/documents/ingest`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          documents: [
            {
              id: `dashboard-${Date.now()}`,
              text: documentText,
              metadata: {source: "dashboard"},
            },
          ],
        }),
      });
      if (!response.ok) throw new Error("Ingestion failed");
      const data = await response.json();
      setStatus(`Indexed ${data.chunks_indexed} chunks and ${data.graph_edges} graph edges`);
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Ingestion failed");
    } finally {
      setLoading(false);
    }
  }

  async function runAgents() {
    setLoading(true);
    setStatus("Running multi-agent workflow...");
    try {
      const response = await fetch(`${apiUrl}/v1/agents/run`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({task, max_agents: 4, top_k: 5}),
      });
      if (!response.ok) throw new Error("Agent run failed");
      const data = await response.json();
      setResult(data);
      setStatus(`Completed in ${Math.round(data.latency_ms)} ms`);
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Agent run failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <section className="hero">
        <div>
          <p className="eyebrow">AgeNova</p>
          <h1>Autonomous multi-agent RAG with hybrid memory</h1>
          <p className="subtle">
            Ingest context, generate task-specific agents, retrieve evidence, debate, and return a
            traceable answer from one dashboard.
          </p>
        </div>
        <div className="statusCard">
          <Activity size={20} />
          <span>{status}</span>
        </div>
      </section>

      <section className="workspace">
        <div className="panel">
          <div className="panelTitle">
            <Database size={18} />
            <h2>Runtime Corpus</h2>
          </div>
          <textarea value={documentText} onChange={(event) => setDocumentText(event.target.value)} />
          <button onClick={ingestDemo} disabled={loading}>
            <Upload size={17} />
            Ingest document
          </button>
        </div>

        <div className="panel">
          <div className="panelTitle">
            <Brain size={18} />
            <h2>Agent Task</h2>
          </div>
          <textarea value={task} onChange={(event) => setTask(event.target.value)} />
          <button onClick={runAgents} disabled={loading}>
            <Play size={17} />
            Run AgeNova
          </button>
        </div>
      </section>

      {result && (
        <section className="results">
          <div className="metricGrid">
            <div className="metric">
              <span>Consensus</span>
              <strong>{Math.round(result.consensus_score * 100)}%</strong>
            </div>
            <div className="metric">
              <span>Agents</span>
              <strong>{result.agents.length}</strong>
            </div>
            <div className="metric">
              <span>Evidence</span>
              <strong>{result.evidence.length}</strong>
            </div>
            <div className="metric">
              <span>Best Role</span>
              <strong>{bestAgent?.role ?? "n/a"}</strong>
            </div>
          </div>

          <div className="answer">
            <div className="panelTitle">
              <Network size={18} />
              <h2>Final Consensus</h2>
            </div>
            <p>{result.final_answer}</p>
          </div>

          <div className="traceGrid">
            {result.agents.map((agent) => (
              <article className="trace" key={agent.agent}>
                <div>
                  <strong>{agent.agent}</strong>
                  <span>{agent.role}</span>
                </div>
                <p>{agent.answer}</p>
                <small>Confidence {Math.round(agent.confidence * 100)}%</small>
              </article>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}
