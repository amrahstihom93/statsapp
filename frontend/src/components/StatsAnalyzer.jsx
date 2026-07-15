import React, { useState, useEffect } from "react";
import Card from "./Card";
import Button from "./Button";
import { datasetsAPI, analyticsAPI } from "../api/services";
import { Calculator, Save, FileText, Database } from "lucide-react";

export default function StatsAnalyzer() {
  const [datasets, setDatasets] = useState([]);
  const [selectedDs, setSelectedDs] = useState("");
  const [columns, setColumns] = useState([]);
  const [selectedCol, setSelectedCol] = useState("");
  const [method, setMethod] = useState("Descriptive Statistics");
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  
  const [saveName, setSaveName] = useState("");
  const [saving, setSaving] = useState(false);
  const [savedLogs, setSavedLogs] = useState([]);

  useEffect(() => {
    async function load() {
      try {
        const list = await datasetsAPI.list();
        setDatasets(list);
        if (list.length > 0) {
          setSelectedDs(list[0].dataset_id);
          setColumns(list[0].columns.map(c => c.column_name));
          if (list[0].columns.length > 0) {
            setSelectedCol(list[0].columns[0].column_name);
          }
        }
        const saved = await analyticsAPI.listStats();
        setSavedLogs(saved);
      } catch (e) {
        console.error(e);
      }
    }
    load();
  }, []);

  const handleDsChange = (e) => {
    const dsId = e.target.value;
    setSelectedDs(dsId);
    const ds = datasets.find(d => d.dataset_id === dsId);
    if (ds) {
      const cols = ds.columns.map(c => c.column_name);
      setColumns(cols);
      setSelectedCol(cols[0] || "");
    }
  };

  const handleCalculate = async () => {
    if (!selectedDs || !selectedCol) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await analyticsAPI.calculateStatistics(selectedDs, selectedCol, method);
      setResult(res.summary);
    } catch (err) {
      alert("Calculation failed: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    if (!saveName.trim() || !result) return;
    setSaving(true);
    try {
      await analyticsAPI.saveStatistics(
        saveName.trim(),
        selectedDs,
        method,
        result,
        { column: selectedCol }
      );
      setSaveName("");
      alert("Statistics saved successfully!");
      const saved = await analyticsAPI.listStats();
      setSavedLogs(saved);
    } catch (err) {
      alert("Failed to save: " + err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="stats-analyzer animate-fade-in">
      <div className="analytics-header-row">
        <div>
          <h2 className="section-heading">Statistical Analysis</h2>
          <p className="section-subheading">Compute descriptive and parametric test summaries on live columns</p>
        </div>
      </div>

      <div className="dataset-layout">
        {/* Left: inputs */}
        <Card title="Configure Computation" subtitle="Choose columns and methods">
          <div className="login-form">
            <div className="input-group-container">
              <label className="input-label">Select Dataset</label>
              <select className="input-field" value={selectedDs} onChange={handleDsChange}>
                {datasets.map(d => (
                  <option key={d.dataset_id} value={d.dataset_id}>{d.dataset_name}</option>
                ))}
              </select>
            </div>

            <div className="input-group-container">
              <label className="input-label">Select Target Column</label>
              <select className="input-field" value={selectedCol} onChange={e => setSelectedCol(e.target.value)}>
                {columns.map(c => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>

            <div className="input-group-container">
              <label className="input-label">Test Method</label>
              <select className="input-field" value={method} onChange={e => setMethod(e.target.value)}>
                <option value="Descriptive Statistics">Descriptive Statistics</option>
              </select>
            </div>

            <Button
              variant="primary"
              onClick={handleCalculate}
              disabled={loading || !selectedCol}
              icon={<Calculator size={14} />}
            >
              {loading ? "Computing…" : "Run Computation"}
            </Button>
          </div>
        </Card>

        {/* Right: results */}
        <Card title="Results Console" subtitle="Computed statistical indicators">
          {!result ? (
            <div className="ds-detail-empty">
              <Database size={40} className="ds-detail-empty-icon" />
              <p>Configure parameters and click "Run Computation" to see outputs.</p>
            </div>
          ) : (
            <div className="ds-detail animate-fade-in">
              <div className="ds-detail-stats" style={{ gridTemplateColumns: "repeat(2, 1fr)" }}>
                <div className="ds-stat-block">
                  <span className="ds-stat-val" style={{ fontSize: "1.2rem" }}>{result.mean}</span>
                  <span className="ds-stat-lbl">Mean</span>
                </div>
                <div className="ds-stat-block">
                  <span className="ds-stat-val" style={{ fontSize: "1.2rem" }}>{result.median}</span>
                  <span className="ds-stat-lbl">Median</span>
                </div>
                <div className="ds-stat-block">
                  <span className="ds-stat-val" style={{ fontSize: "1.2rem" }}>{result.std}</span>
                  <span className="ds-stat-lbl">Std Deviation</span>
                </div>
                <div className="ds-stat-block">
                  <span className="ds-stat-val" style={{ fontSize: "1.2rem" }}>{result.variance}</span>
                  <span className="ds-stat-lbl">Variance</span>
                </div>
              </div>

              <div className="ds-preview-mock">
                <div className="ds-preview-header-row">
                  <div className="ds-preview-cell ds-preview-th">Metric</div>
                  <div className="ds-preview-cell ds-preview-th">Value</div>
                </div>
                <div className="ds-preview-row">
                  <div className="ds-preview-cell ds-preview-td">Min / Max</div>
                  <div className="ds-preview-cell ds-preview-td">{result.min} / {result.max}</div>
                </div>
                <div className="ds-preview-row">
                  <div className="ds-preview-cell ds-preview-td">IQR Range</div>
                  <div className="ds-preview-cell ds-preview-td">{result.iqr}</div>
                </div>
                <div className="ds-preview-row">
                  <div className="ds-preview-cell ds-preview-td">Skewness</div>
                  <div className="ds-preview-cell ds-preview-td">{result.skewness}</div>
                </div>
                <div className="ds-preview-row">
                  <div className="ds-preview-cell ds-preview-td">Kurtosis</div>
                  <div className="ds-preview-cell ds-preview-td">{result.kurtosis}</div>
                </div>
              </div>

              <form onSubmit={handleSave} className="flex gap-2 mt-2">
                <input
                  className="input-field py-1 px-3 text-sm"
                  placeholder="Save name (e.g. Q2 Sales Stats)"
                  value={saveName}
                  onChange={e => setSaveName(e.target.value)}
                  required
                />
                <Button variant="secondary" size="sm" type="submit" disabled={saving}>
                  <Save size={13} /> {saving ? "Saving…" : "Save Record"}
                </Button>
              </form>
            </div>
          )}
        </Card>
      </div>

      <Card title="Saved Calculations Log" subtitle="History of statistics saved to Django" className="mt-4">
        <div className="node-status-log">
          {savedLogs.length === 0 && (
            <div className="p-3 text-center text-xs text-muted">No saved calculations yet.</div>
          )}
          {savedLogs.map(log => (
            <div key={log.id} className="node-log-row">
              <div className="node-log-left">
                <FileText size={14} className="text-accent" />
                <span className="node-log-name font-mono">{log.statistical_name}</span>
                <span className="node-log-type">{log.statistical_method}</span>
              </div>
              <span className="node-log-status" style={{ color: "var(--accent-primary)" }}>
                Mean: {log.statistical_calculated_value?.mean || "N/A"}
              </span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
