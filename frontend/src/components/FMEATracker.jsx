import React, { useState, useEffect } from "react";
import Card from "./Card";
import Button from "./Button";
import { datasetsAPI, analyticsAPI } from "../api/services";
import { ClipboardList, Plus, Save } from "lucide-react";

export default function FMEATracker() {
  const [datasets, setDatasets] = useState([]);
  const [selectedDs, setSelectedDs] = useState("");
  
  const [modeName, setModeName] = useState("");
  const [severity, setSeverity] = useState(5);
  const [occurrence, setOccurrence] = useState(5);
  const [detection, setDetection] = useState(5);
  
  const [fmeaList, setFmeaList] = useState([]);
  const [savedFmeas, setSavedFmeas] = useState([]);
  const [fmeaName, setFmeaName] = useState("");
  const [saving, setSaving] = useState(false);

  const fetchFmeas = async () => {
    try {
      const data = await analyticsAPI.listFMEA();
      setSavedFmeas(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    async function load() {
      try {
        const list = await datasetsAPI.list();
        setDatasets(list);
        if (list.length > 0) {
          setSelectedDs(list[0].dataset_id);
        }
        await fetchFmeas();
      } catch (e) {
        console.error(e);
      }
    }
    load();
  }, []);

  const handleAddMode = () => {
    if (!modeName.trim()) return;
    const rpn = severity * occurrence * detection;
    const item = {
      id: Date.now(),
      mode: modeName.trim(),
      severity,
      occurrence,
      detection,
      rpn
    };
    setFmeaList(prev => [...prev, item]);
    setModeName("");
    setSeverity(5);
    setOccurrence(5);
    setDetection(5);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    if (!fmeaName.trim() || fmeaList.length === 0 || !selectedDs) return;
    setSaving(true);
    try {
      await analyticsAPI.saveFMEA(
        fmeaName.trim(),
        selectedDs,
        fmeaList,
        { total_modes: fmeaList.length }
      );
      setFmeaName("");
      setFmeaList([]);
      alert("FMEA analysis saved successfully to database!");
      await fetchFmeas();
    } catch (err) {
      alert("Failed to save FMEA: " + err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fmea-tracker animate-fade-in">
      <div className="analytics-header-row">
        <div>
          <h2 className="section-heading">FMEA Quality Tools</h2>
          <p className="section-subheading">Analyze failure modes, rate risk parameters, and compute RPN metrics</p>
        </div>
      </div>

      <div className="dataset-layout">
        {/* Left: inputs */}
        <Card title="Add Failure Mode" subtitle="Set risk ratings (1-10)">
          <div className="login-form">
            <div className="input-group-container">
              <label className="input-label">Linked Dataset</label>
              <select className="input-field" value={selectedDs} onChange={e => setSelectedDs(e.target.value)}>
                {datasets.map(d => (
                  <option key={d.dataset_id} value={d.dataset_id}>{d.dataset_name}</option>
                ))}
              </select>
            </div>

            <div className="input-group-container">
              <label className="input-label">Failure Mode Description</label>
              <input
                className="input-field"
                placeholder="e.g. Memory leak in computing engine"
                value={modeName}
                onChange={e => setModeName(e.target.value)}
              />
            </div>

            <div className="grid grid-cols-3 gap-2" style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "10px" }}>
              <div className="input-group-container">
                <label className="input-label">Severity (S)</label>
                <input
                  type="number" min="1" max="10" className="input-field"
                  value={severity} onChange={e => setSeverity(parseInt(e.target.value) || 1)}
                />
              </div>
              <div className="input-group-container">
                <label className="input-label">Occurrence (O)</label>
                <input
                  type="number" min="1" max="10" className="input-field"
                  value={occurrence} onChange={e => setOccurrence(parseInt(e.target.value) || 1)}
                />
              </div>
              <div className="input-group-container">
                <label className="input-label">Detection (D)</label>
                <input
                  type="number" min="1" max="10" className="input-field"
                  value={detection} onChange={e => setDetection(parseInt(e.target.value) || 1)}
                />
              </div>
            </div>

            <Button variant="primary" onClick={handleAddMode} disabled={!modeName.trim()} icon={<Plus size={14} />}>
              Add Mode
            </Button>
          </div>
        </Card>

        {/* Right: matrix table */}
        <Card title="FMEA Analysis Matrix" subtitle={`Risk Priority Numbers (RPN = S × O × D)`}>
          {fmeaList.length === 0 ? (
            <div className="ds-detail-empty">
              <ClipboardList size={40} className="ds-detail-empty-icon" />
              <p>Add failure modes to begin building the risk assessment matrix.</p>
            </div>
          ) : (
            <div className="ds-detail animate-fade-in">
              <div className="ds-preview-mock">
                <div className="ds-preview-header-row">
                  <div className="ds-preview-cell ds-preview-th" style={{ flex: 2 }}>Failure Mode</div>
                  <div className="ds-preview-cell ds-preview-th">S</div>
                  <div className="ds-preview-cell ds-preview-th">O</div>
                  <div className="ds-preview-cell ds-preview-th">D</div>
                  <div className="ds-preview-cell ds-preview-th" style={{ color: "var(--accent-primary)" }}>RPN</div>
                </div>
                {fmeaList.map((item) => (
                  <div key={item.id} className="ds-preview-row">
                    <div className="ds-preview-cell ds-preview-td" style={{ flex: 2 }}>{item.mode}</div>
                    <div className="ds-preview-cell ds-preview-td">{item.severity}</div>
                    <div className="ds-preview-cell ds-preview-td">{item.occurrence}</div>
                    <div className="ds-preview-cell ds-preview-td">{item.detection}</div>
                    <div className="ds-preview-cell ds-preview-td font-bold" style={{ color: item.rpn > 125 ? "var(--error)" : "var(--accent-primary)" }}>
                      {item.rpn}
                    </div>
                  </div>
                ))}
              </div>

              <form onSubmit={handleSave} className="flex gap-2 mt-2">
                <input
                  className="input-field py-1 px-3 text-sm"
                  placeholder="FMEA Report Name (e.g. Engine Audit)"
                  value={fmeaName}
                  onChange={e => setFmeaName(e.target.value)}
                  required
                />
                <Button variant="secondary" size="sm" type="submit" disabled={saving}>
                  <Save size={13} /> {saving ? "Saving…" : "Save FMEA"}
                </Button>
              </form>
            </div>
          )}
        </Card>
      </div>

      <Card title="Saved FMEA Records Log" subtitle="History of risk assessments saved to Django" className="mt-4">
        <div className="node-status-log">
          {savedFmeas.length === 0 && (
            <div className="p-3 text-center text-xs text-muted">No saved FMEAs yet.</div>
          )}
          {savedFmeas.map(log => (
            <div key={log.id} className="node-log-row">
              <div className="node-log-left">
                <ClipboardList size={14} className="text-accent" />
                <span className="node-log-name font-mono">{log.fmea_name}</span>
                <span className="node-log-type">Modes analyzed: {log.parameters?.total_modes || "N/A"}</span>
              </div>
              <span className="node-log-status" style={{ color: "var(--accent-primary)" }}>
                Active
              </span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
