import React, { useState, useEffect } from "react";
import Card from "./Card";
import Button from "./Button";
import { Database, Upload, Search, FileText, CheckCircle2, Clock, AlertCircle, Trash2, Eye, Plus } from "lucide-react";
import { datasetsAPI } from "../api/services";

const STATUS_COLORS = {
  ready:      { color: "#22c55e", label: "Ready"      },
  processing: { color: "#f59e0b", label: "Processing" },
  error:      { color: "#ef4444", label: "Error"      },
};

function StatusBadge({ status }) {
  const s = STATUS_COLORS[status] || STATUS_COLORS.ready;
  const Icon = status === "ready" ? CheckCircle2 : status === "processing" ? Clock : AlertCircle;
  return (
    <span className="ds-status-badge" style={{ borderColor: `${s.color}30`, color: s.color, background: `${s.color}10` }}>
      <Icon size={11} />
      {s.label}
    </span>
  );
}

export default function DatasetManager() {
  const [datasets, setDatasets] = useState([]);
  const [search, setSearch] = useState("");
  const [selectedId, setSelectedId] = useState(null);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [datasetName, setDatasetName] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewData, setPreviewData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  const fetchDatasets = async () => {
    try {
      setLoading(true);
      const data = await datasetsAPI.list();
      setDatasets(data);
    } catch (err) {
      console.error("Failed to load datasets:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchPreview = async (id) => {
    try {
      const data = await datasetsAPI.preview(id);
      setPreviewData(data);
    } catch (err) {
      console.error("Failed to load dataset preview:", err);
      setPreviewData(null);
    }
  };

  useEffect(() => {
    if (selectedId) {
      fetchPreview(selectedId);
    } else {
      setPreviewData(null);
    }
  }, [selectedId]);

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this dataset?")) return;
    try {
      await datasetsAPI.delete(id);
      setDatasets((prev) => prev.filter((d) => d.dataset_id !== id));
      if (selectedId === id) setSelectedId(null);
    } catch (err) {
      alert("Failed to delete dataset: " + err.message);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!datasetName.trim() || !selectedFile) {
      alert("Please enter a name and select a file");
      return;
    }
    setUploading(true);
    try {
      await datasetsAPI.upload(datasetName.trim(), selectedFile);
      setDatasetName("");
      setSelectedFile(null);
      setShowUploadModal(false);
      await fetchDatasets();
    } catch (err) {
      alert("Upload failed: " + err.message);
    } finally {
      setUploading(false);
    }
  };

  const filtered = datasets.filter((d) =>
    d.dataset_name.toLowerCase().includes(search.toLowerCase())
  );

  const selected = datasets.find((d) => d.dataset_id === selectedId);

  return (
    <div className="dataset-manager animate-fade-in">
      <div className="analytics-header-row">
        <div>
          <h2 className="section-heading">Dataset Manager</h2>
          <p className="section-subheading">Upload, inspect, and manage analytical datasets</p>
        </div>
        <Button variant="primary" size="sm" icon={<Plus size={13} />} onClick={() => setShowUploadModal(true)}>
          Upload Dataset
        </Button>
      </div>

      <div className="dataset-layout">
        {/* Left — list */}
        <Card title="Datasets" subtitle={loading ? "Loading…" : `${filtered.length} files`}>
          <div className="ds-search-bar">
            <Search size={14} className="ds-search-icon" />
            <input
              className="ds-search-input"
              placeholder="Search datasets by name…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <div className="ds-list">
            {filtered.length === 0 && !loading && (
              <div className="ds-empty">No datasets available. Upload one to start.</div>
            )}
            {filtered.map((ds) => (
              <div
                key={ds.dataset_id}
                className={`ds-row ${selectedId === ds.dataset_id ? "ds-row-active" : ""}`}
                onClick={() => setSelectedId(ds.dataset_id)}
              >
                <div className="ds-row-left">
                  <FileText size={16} className="ds-file-icon" />
                  <div className="ds-row-info">
                    <span className="ds-row-name">{ds.dataset_name}</span>
                    <div className="ds-row-meta">
                      <span>{ds.row_count} rows</span>
                      <span className="ds-meta-sep">·</span>
                      <span>{ds.col_count} cols</span>
                      <span className="ds-meta-sep">·</span>
                      <span>{new Date(ds.uploaded_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
                <div className="ds-row-right">
                  <StatusBadge status="ready" />
                  <button className="ds-icon-btn" onClick={(e) => { e.stopPropagation(); handleDelete(ds.dataset_id); }} title="Delete">
                    <Trash2 size={13} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Right — detail panel */}
        <Card title={selected ? selected.dataset_name : "Dataset Preview"} subtitle={selected ? `Registered ID: ${selected.dataset_id}` : "Select a dataset to inspect"}>
          {!selected ? (
            <div className="ds-detail-empty">
              <Database size={40} className="ds-detail-empty-icon" />
              <p>Click a dataset row to view its details and metadata.</p>
            </div>
          ) : (
            <div className="ds-detail animate-fade-in">
              <div className="ds-detail-badges">
                <StatusBadge status="ready" />
                <span className="ds-tag">SQLite</span>
                <span className="ds-tag">JSON data field</span>
              </div>
              <div className="ds-detail-stats">
                <div className="ds-stat-block">
                  <span className="ds-stat-val">{selected.row_count.toLocaleString()}</span>
                  <span className="ds-stat-lbl">Rows</span>
                </div>
                <div className="ds-stat-block">
                  <span className="ds-stat-val">{selected.col_count}</span>
                  <span className="ds-stat-lbl">Columns</span>
                </div>
                <div className="ds-stat-block">
                  <span className="ds-stat-val">Online</span>
                  <span className="ds-stat-lbl">Sync Status</span>
                </div>
              </div>

              {previewData && previewData.preview && (
                <div className="ds-preview-mock">
                  <div className="ds-preview-header-row">
                    {previewData.columns.slice(0, 5).map((col) => (
                      <div key={col} className="ds-preview-cell ds-preview-th">{col}</div>
                    ))}
                  </div>
                  {previewData.preview.slice(0, 5).map((row, rIdx) => (
                    <div key={rIdx} className="ds-preview-row">
                      {previewData.columns.slice(0, 5).map((col) => (
                        <div key={col} className="ds-preview-cell ds-preview-td">
                          {row[col] !== undefined ? String(row[col]) : ""}
                        </div>
                      ))}
                    </div>
                  ))}
                  <div className="ds-preview-footer">
                    <Eye size={12} /> Showing first {Math.min(5, previewData.preview.length)} rows
                  </div>
                </div>
              )}

              <div className="ds-detail-actions">
                <Button variant="primary" size="sm">Calculate statistics</Button>
                <Button variant="secondary" size="sm">Open process map</Button>
              </div>
            </div>
          )}
        </Card>
      </div>

      {/* Upload modal */}
      {showUploadModal && (
        <div className="modal-overlay" onClick={() => setShowUploadModal(false)}>
          <div className="modal-panel glass-panel" onClick={(e) => e.stopPropagation()}>
            <h3 className="modal-title">Upload New Dataset</h3>
            <p className="modal-sub">Upload CSV or Excel file to parse into PostgreSQL/SQLite</p>
            
            <form onSubmit={handleUpload} className="ds-upload-form">
              <div className="ds-upload-icon-area">
                <Upload size={32} className="upload-icon" />
                <input
                  type="file"
                  accept=".csv,.xlsx,.xls"
                  onChange={(e) => setSelectedFile(e.target.files[0])}
                  className="ds-file-input-field"
                  required
                />
                <span className="mt-2 text-xs">
                  {selectedFile ? selectedFile.name : "Select a CSV/XLS file"}
                </span>
              </div>
              
              <input
                className="input-field mt-3"
                placeholder="Dataset Name (e.g. Sales Report)"
                value={datasetName}
                onChange={(e) => setDatasetName(e.target.value)}
                required
              />

              <div className="modal-actions mt-4">
                <Button variant="secondary" size="sm" type="button" onClick={() => setShowUploadModal(false)}>Cancel</Button>
                <Button variant="primary" size="sm" type="submit" disabled={uploading}>
                  {uploading ? "Ingesting…" : "Ingest Dataset"}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
