import React, { useState, useEffect } from "react";
import Card from "./Card";
import Button from "./Button";
import { datasetsAPI, analyticsAPI } from "../api/services";
import { Cpu, Save, FileSpreadsheet, RefreshCw } from "lucide-react";

export default function MLModelStudio() {
  const [datasets, setDatasets] = useState([]);
  const [selectedDs, setSelectedDs] = useState("");
  const [columns, setColumns] = useState([]);
  const [dvar, setDvar] = useState("");
  const [idvar, setIdvar] = useState("");
  
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState(null);
  
  const [modelName, setModelName] = useState("");
  const [saving, setSaving] = useState(false);
  const [savedModels, setSavedModels] = useState([]);

  useEffect(() => {
    async function load() {
      try {
        const list = await datasetsAPI.list();
        setDatasets(list);
        if (list.length > 0) {
          setSelectedDs(list[0].dataset_id);
          setColumns(list[0].columns.map(c => c.column_name));
          if (list[0].columns.length > 1) {
            setDvar(list[0].columns[0].column_name);
            setIdvar(list[0].columns[1].column_name);
          }
        }
        const saved = await analyticsAPI.listMLModels();
        setSavedModels(saved);
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
      if (cols.length > 1) {
        setDvar(cols[0]);
        setIdvar(cols[1]);
      }
    }
  };

  const handleFit = async () => {
    if (!selectedDs || !dvar || !idvar) return;
    setLoading(true);
    setSummary(null);
    try {
      const res = await analyticsAPI.calculateRegression(selectedDs, dvar, idvar);
      setSummary(res.summary);
    } catch (err) {
      alert("Regression failed: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveModel = async (e) => {
    e.preventDefault();
    if (!modelName.trim() || !summary) return;
    setSaving(true);
    try {
      await analyticsAPI.saveMLModel(modelName.trim());
      setModelName("");
      alert("Model pickled and saved successfully to Django!");
      const saved = await analyticsAPI.listMLModels();
      setSavedModels(saved);
    } catch (err) {
      alert("Failed to save model: " + err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="ml-model-studio animate-fade-in">
      <div className="analytics-header-row">
        <div>
          <h2 className="section-heading">Machine Learning Studio</h2>
          <p className="section-subheading">Train and pickle linear models directly on database tables</p>
        </div>
      </div>

      <div className="dataset-layout">
        {/* Left: Configuration */}
        <Card title="Model Config" subtitle="Specify targets and parameters">
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
              <label className="input-label">Dependent Variable (Y)</label>
              <select className="input-field" value={dvar} onChange={e => setDvar(e.target.value)}>
                {columns.map(c => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>

            <div className="input-group-container">
              <label className="input-label">Independent Variable (X)</label>
              <select className="input-field" value={idvar} onChange={e => setIdvar(e.target.value)}>
                {columns.map(c => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>

            <Button
              variant="primary"
              onClick={handleFit}
              disabled={loading || !dvar || !idvar || dvar === idvar}
              icon={<Cpu size={14} />}
            >
              {loading ? "Training…" : "Fit Linear Model"}
            </Button>
          </div>
        </Card>

        {/* Right: Results */}
        <Card title="Regression Summary" subtitle="Statsmodels OLS outputs">
          {!summary ? (
            <div className="ds-detail-empty">
              <Cpu size={40} className="ds-detail-empty-icon" />
              <p>Configure variables and fit the model to view R², F-statistic, and P-values.</p>
            </div>
          ) : (
            <div className="ds-detail animate-fade-in">
              <div className="ds-detail-stats" style={{ gridTemplateColumns: "repeat(2, 1fr)" }}>
                <div className="ds-stat-block">
                  <span className="ds-stat-val" style={{ color: "var(--accent-primary)" }}>{summary.result_score}</span>
                  <span className="ds-stat-lbl">Test R² Score</span>
                </div>
                <div className="ds-stat-block">
                  <span className="ds-stat-val">{summary.rsquared}</span>
                  <span className="ds-stat-lbl">R-squared</span>
                </div>
              </div>

              <div className="ds-preview-mock">
                <div className="ds-preview-header-row">
                  <div className="ds-preview-cell ds-preview-th">OLS Parameter</div>
                  <div className="ds-preview-cell ds-preview-th">Value</div>
                </div>
                <div className="ds-preview-row">
                  <div className="ds-preview-cell ds-preview-td">Adj. R-squared</div>
                  <div className="ds-preview-cell ds-preview-td">{summary.radjective}</div>
                </div>
                <div className="ds-preview-row">
                  <div className="ds-preview-cell ds-preview-td">F-statistic</div>
                  <div className="ds-preview-cell ds-preview-td">{summary.fvalue}</div>
                </div>
                <div className="ds-preview-row">
                  <div className="ds-preview-cell ds-preview-td">Prob (F-statistic)</div>
                  <div className="ds-preview-cell ds-preview-td">{summary.pvalue}</div>
                </div>
                <div className="ds-preview-row">
                  <div className="ds-preview-cell ds-preview-td">Std Error of Estimate</div>
                  <div className="ds-preview-cell ds-preview-td">{summary.err_of_estimate}</div>
                </div>
              </div>

              <form onSubmit={handleSaveModel} className="flex gap-2 mt-2">
                <input
                  className="input-field py-1 px-3 text-sm"
                  placeholder="Model name (e.g. Sales Forecast)"
                  value={modelName}
                  onChange={e => setModelName(e.target.value)}
                  required
                />
                <Button variant="secondary" size="sm" type="submit" disabled={saving}>
                  <Save size={13} /> {saving ? "Pickling…" : "Save pickled model"}
                </Button>
              </form>
            </div>
          )}
        </Card>
      </div>

      <Card title="Pickled ML Models Log" subtitle="History of pickled models saved to media/models/" className="mt-4">
        <div className="node-status-log">
          {savedModels.length === 0 && (
            <div className="p-3 text-center text-xs text-muted">No models pickled yet.</div>
          )}
          {savedModels.map(model => (
            <div key={model.id} className="node-log-row">
              <div className="node-log-left">
                <Cpu size={14} className="text-purple-glow" style={{ color: "var(--accent-purple)" }} />
                <span className="node-log-name font-mono">{model.mlearn_name}</span>
                <span className="node-log-type">ID: {model.mlearn_id}</span>
              </div>
              <span className="node-log-status" style={{ color: "var(--accent-primary)" }}>
                R²: {model.parameters?.rsquared || "N/A"}
              </span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
