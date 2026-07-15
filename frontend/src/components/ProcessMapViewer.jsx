import React, { useState, useEffect } from "react";
import Card from "./Card";
import Button from "./Button";
import { Play, Pause, RotateCcw, Zap, CheckCircle2, Circle, ArrowRight, Plus } from "lucide-react";
import { processesAPI } from "../api/services";

const NODE_COLORS = {
  source:  "#3b82f6",
  process: "#a855f7",
  compute: "#00f0ff",
  output:  "#22c55e",
};

const STATUS_STYLE = {
  done:    { border: "#22c55e", bg: "rgba(34,197,94,0.08)",   icon: <CheckCircle2 size={11} color="#22c55e" /> },
  active:  { border: "#00f0ff", bg: "rgba(0,240,255,0.08)",  icon: <Zap size={11} color="#00f0ff" />          },
  pending: { border: "#3f3f46", bg: "rgba(255,255,255,0.02)", icon: <Circle size={11} color="#52525b" />       },
  error:   { border: "#ef4444", bg: "rgba(239,68,68,0.08)",  icon: <Circle size={11} color="#ef4444" />       },
};

function FlowNode({ node }) {
  const s = STATUS_STYLE[node.status] || STATUS_STYLE.pending;
  const typeColor = NODE_COLORS[node.type] || "#fff";
  return (
    <div
      className="flow-node"
      style={{ borderColor: s.border, background: s.bg, boxShadow: node.status === "active" ? `0 0 14px ${s.border}50` : "none" }}
    >
      <div className="flow-node-dot" style={{ background: typeColor, boxShadow: `0 0 6px ${typeColor}` }} />
      <span className="flow-node-label">{node.label}</span>
      <div className="flow-node-status">{s.icon}</div>
      {node.status === "active" && <div className="flow-node-pulse-ring" />}
    </div>
  );
}

export default function ProcessMapViewer() {
  const [pipelines, setPipelines] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [paused, setPaused] = useState(false);
  const [newProcessName, setNewProcessName] = useState("");
  const [loading, setLoading] = useState(true);

  const fetchProcesses = async () => {
    try {
      setLoading(true);
      const data = await processesAPI.list();
      setPipelines(data);
      if (data.length > 0 && !selectedId) {
        setSelectedId(data[0].process_id);
      }
    } catch (err) {
      console.error("Failed to load processes:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProcesses();
  }, []);

  const handleCreateProcess = async (e) => {
    e.preventDefault();
    if (!newProcessName.trim()) return;
    try {
      const created = await processesAPI.create(newProcessName.trim(), selectedId || 'root');
      setNewProcessName("");
      await fetchProcesses();
      setSelectedId(created.process_id);
    } catch (err) {
      alert("Failed to create process: " + err.message);
    }
  };

  const selected = pipelines.find((p) => p.process_id === selectedId);

  // Generate a mock flow chain based on the actual processes list to represent flow connection dynamically
  const nodes = selected
    ? [
        { id: "n1", label: `Ingest ${selected.process_name}`, type: "source", status: "done" },
        { id: "n2", label: "Normalize schema", type: "process", status: "done" },
        { id: "n3", label: "Execute workflow step", type: "compute", status: "active" },
        { id: "n4", label: "Sync DB stats", type: "output", status: "pending" },
      ]
    : [];

  const doneCount = nodes.filter((n) => n.status === "done").length;
  const pct = nodes.length > 0 ? Math.round((doneCount / nodes.length) * 100) : 0;

  return (
    <div className="process-map animate-fade-in">
      <div className="analytics-header-row">
        <div>
          <h2 className="section-heading">Process Maps</h2>
          <p className="section-subheading">Visualize and manage pipeline workflows linked to your clients</p>
        </div>
        <div className="pmap-controls">
          <Button variant="secondary" size="sm" icon={paused ? <Play size={12}/> : <Pause size={12}/>} onClick={() => setPaused(!paused)}>
            {paused ? "Resume" : "Pause"}
          </Button>
        </div>
      </div>

      <div className="pmap-layout">
        {/* Pipeline selector list */}
        <div className="pmap-sidebar">
          <div className="pmap-list-header">Real Process List</div>
          {loading && <div className="p-3 text-xs text-muted">Loading…</div>}
          {pipelines.map((p) => (
            <button
              key={p.process_id}
              className={`pmap-list-item ${selectedId === p.process_id ? "pmap-list-item-active" : ""}`}
              onClick={() => setSelectedId(p.process_id)}
            >
              <span className="pmap-list-dot" style={{ background: "var(--accent-primary)", boxShadow: `0 0 6px var(--accent-primary)` }} />
              <div className="pmap-list-text">
                <span className="pmap-list-name">{p.process_name}</span>
                <span className="pmap-list-desc">ID: {p.process_id.substring(0, 12)}…</span>
              </div>
            </button>
          ))}
          
          <form onSubmit={handleCreateProcess} className="mt-4 p-2 border-t border-card flex flex-col gap-2">
            <span className="text-[10px] text-muted uppercase font-bold tracking-wider">Create Sub-Process</span>
            <input
              className="input-field py-1 px-2 text-xs"
              placeholder="e.g. Sales Pipeline"
              value={newProcessName}
              onChange={(e) => setNewProcessName(e.target.value)}
              required
            />
            <Button variant="primary" size="sm" className="w-full text-xs py-1" type="submit">
              <Plus size={10} /> Add
            </Button>
          </form>
        </div>

        {/* Flow canvas */}
        <div className="pmap-canvas-wrap">
          {selected ? (
            <>
              <Card title={selected.process_name} subtitle={`Parent Chain ID: ${selected.parent_p_id}`}>
                <div className="pmap-progress-row">
                  <span className="pmap-progress-label">Execution Progress</span>
                  <span className="pmap-progress-pct">{pct}%</span>
                </div>
                <div className="pmap-progress-track">
                  <div className="pmap-progress-fill" style={{ width: `${pct}%` }} />
                </div>

                {/* Flow nodes */}
                <div className="flow-canvas">
                  {nodes.map((node, i) => (
                    <React.Fragment key={node.id}>
                      <FlowNode node={node} />
                      {i < nodes.length - 1 && (
                        <div className={`flow-connector ${node.status === "done" ? "flow-connector-active" : ""}`}>
                          <div className="flow-connector-line" />
                          <ArrowRight size={14} className="flow-connector-arrow" />
                        </div>
                      )}
                    </React.Fragment>
                  ))}
                </div>

                {/* Legend */}
                <div className="flow-legend">
                  {Object.entries(NODE_COLORS).map(([type, color]) => (
                    <div key={type} className="legend-item">
                      <span className="legend-dot" style={{ background: color, boxShadow: `0 0 4px ${color}` }} />
                      <span className="legend-label">{type}</span>
                    </div>
                  ))}
                </div>
              </Card>

              <Card title="Node status log" subtitle="Execution details">
                <div className="node-status-log">
                  {nodes.map((node) => {
                    const s = STATUS_STYLE[node.status] || STATUS_STYLE.pending;
                    return (
                      <div key={node.id} className="node-log-row">
                        <div className="node-log-left">
                          {s.icon}
                          <span className="node-log-name">{node.label}</span>
                          <span className="node-log-type" style={{ color: NODE_COLORS[node.type] }}>{node.type}</span>
                        </div>
                        <span className="node-log-status" style={{ color: s.border }}>{node.status}</span>
                      </div>
                    );
                  })}
                </div>
              </Card>
            </>
          ) : (
            <div className="p-8 text-center text-muted text-sm glass-panel">
              Select or create a process map to visualize the active flow pipeline.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
