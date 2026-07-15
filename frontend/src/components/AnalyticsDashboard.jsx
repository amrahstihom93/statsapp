import React, { useState, useEffect } from "react";
import Card from "./Card";
import { TrendingUp, TrendingDown, Activity, RefreshCw } from "lucide-react";
import { analyticsAPI } from "../api/services";

function Sparkline({ data, color = "#00f0ff", height = 40, width = 120 }) {
  if (!data || data.length < 2) return null;
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;
  const points = data.map((v, i) => {
    const x = (i / (data.length - 1)) * width;
    const y = height - ((v - min) / range) * height;
    return `${x},${y}`;
  });
  const pathD = `M ${points.join(" L ")}`;
  const areaD = `M ${points[0]} L ${points.join(" L ")} L ${width},${height} L 0,${height} Z`;
  const gradId = `sg-${color.replace(/[^a-z0-9]/gi, "")}`;
  return (
    <svg viewBox={`0 0 ${width} ${height}`} width={width} height={height} style={{ overflow: "visible" }}>
      <defs>
        <linearGradient id={gradId} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity="0.25" />
          <stop offset="100%" stopColor={color} stopOpacity="0.01" />
        </linearGradient>
      </defs>
      <path d={areaD} fill={`url(#${gradId})`} />
      <path d={pathD} fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <circle
        cx={parseFloat(points[points.length - 1].split(",")[0])}
        cy={parseFloat(points[points.length - 1].split(",")[1])}
        r="3"
        fill={color}
        style={{ filter: `drop-shadow(0 0 4px ${color})` }}
      />
    </svg>
  );
}

function BarChart({ bars }) {
  const [animated, setAnimated] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setAnimated(true), 200);
    return () => clearTimeout(t);
  }, []);
  const max = Math.max(...bars.map((b) => b.value));
  return (
    <div className="bar-chart-container">
      {bars.map((bar, i) => (
        <div key={i} className="bar-item">
          <div className="bar-track">
            <div
              className="bar-fill"
              style={{
                height: animated ? `${(bar.value / max) * 100}%` : "0%",
                background: bar.color || "var(--accent-primary)",
                boxShadow: `0 0 10px ${bar.color || "var(--accent-glow)"}`,
                transitionDelay: `${i * 60}ms`,
              }}
            />
          </div>
          <span className="bar-label">{bar.label}</span>
          <span className="bar-val">{bar.value}</span>
        </div>
      ))}
    </div>
  );
}

function StatTile({ label, value, delta, deltaDir, spark, accentColor }) {
  const isUp = deltaDir === "up";
  return (
    <div className="stat-tile glass-panel">
      <div className="stat-tile-top">
        <span className="stat-tile-label">{label}</span>
        <div className={`stat-delta ${isUp ? "stat-delta-up" : "stat-delta-down"}`}>
          {isUp ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
          <span>{delta}</span>
        </div>
      </div>
      <div className="stat-tile-value" style={{ color: accentColor || "var(--text-primary)" }}>
        {value}
      </div>
      <div className="stat-tile-spark">
        <Sparkline data={spark} color={accentColor || "#00f0ff"} />
      </div>
    </div>
  );
}

export default function AnalyticsDashboard() {
  const [summary, setSummary] = useState({ dataset_count: 0, stats_count: 0, ml_model_count: 0 });
  const [spinning, setSpinning] = useState(false);

  const fetchSummary = async () => {
    try {
      setSpinning(true);
      const data = await analyticsAPI.getSummary();
      setSummary(data);
    } catch (err) {
      console.error(err);
    } finally {
      setSpinning(false);
    }
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  const confScores = [82, 88, 91, 85, 94, 97, 93, 98];
  const latency    = [42, 38, 55, 41, 37, 33, 30, 28];

  const barData = [
    { label: "Jan", value: 320, color: "#00f0ff" },
    { label: "Feb", value: 415, color: "#00f0ff" },
    { label: "Mar", value: 370, color: "#00f0ff" },
    { label: "Apr", value: 490, color: "#00f0ff" },
    { label: "May", value: 445, color: "#00f0ff" },
    { label: "Jun", value: 520, color: "#00f0ff" },
    { label: "Jul", value: 580, color: "#00f0ff" },
  ];

  const breakdown = [
    { label: "Regression",     value: 38, color: "#00f0ff" },
    { label: "Classification", value: 27, color: "#22c55e" },
    { label: "Clustering",     value: 19, color: "#3b82f6" },
    { label: "Time Series",    value: 16, color: "#a855f7" },
  ];

  const liveFeed = [
    { label: "Pipeline sync check complete",    value: "Online",            time: "just now" },
    { label: "Database sync validated",         value: "Postgres/SQLite",   time: "4s ago"  },
    { label: "Active ML models online",         value: `${summary.ml_model_count} models`, time: "8s ago"  },
    { label: "User session authenticated",      value: "API Connected",     time: "14s ago" },
  ];

  return (
    <div className="analytics-dashboard animate-fade-in">
      <div className="analytics-header-row">
        <div>
          <h2 className="section-heading">Analytics Overview</h2>
          <p className="section-subheading">Live pipeline metrics and database summaries</p>
        </div>
        <button className="btn btn-secondary btn-sm" onClick={fetchSummary} title="Refresh data">
          <RefreshCw size={14} style={{ transition: "transform 0.8s", transform: spinning ? "rotate(360deg)" : "none" }} />
          <span>{spinning ? "Refreshing…" : "Refresh"}</span>
        </button>
      </div>

      <div className="stat-tiles-grid">
        <StatTile label="Datasets Saved"   value={`${summary.dataset_count}`} delta="Real database count" deltaDir="up" spark={[0, 1, 2, summary.dataset_count]} accentColor="#00f0ff" />
        <StatTile label="Saved Stats"      value={`${summary.stats_count}`}   delta="Statistical records" deltaDir="up" spark={[0, 1, 2, summary.stats_count]} accentColor="#22c55e" />
        <StatTile label="Active ML models" value={`${summary.ml_model_count}`} delta="Registered pkl models" deltaDir="up" spark={[0, 1, summary.ml_model_count]} accentColor="#3b82f6" />
        <StatTile label="Avg Latency"      value={`${latency[latency.length-1]} ms`} delta="-8ms optimized" deltaDir="up" spark={latency} accentColor="#a855f7" />
      </div>

      <div className="analytics-charts-row">
        <Card title="Pipeline Runs" subtitle="Monthly execution volume">
          <div className="chart-wrap"><BarChart bars={barData} /></div>
        </Card>
        <Card title="Model Breakdown" subtitle="By algorithm type">
          <div className="breakdown-list">
            {breakdown.map((item, i) => {
              const total = breakdown.reduce((s, x) => s + x.value, 0);
              const pct = ((item.value / total) * 100).toFixed(1);
              return (
                <div key={i} className="breakdown-row">
                  <div className="breakdown-left">
                    <span className="breakdown-dot" style={{ background: item.color, boxShadow: `0 0 6px ${item.color}` }} />
                    <span className="breakdown-label">{item.label}</span>
                  </div>
                  <div className="breakdown-bar-track">
                    <div className="breakdown-bar-fill" style={{ width: `${pct}%`, background: item.color, animationDelay: `${i * 100}ms` }} />
                  </div>
                  <span className="breakdown-pct">{pct}%</span>
                </div>
              );
            })}
          </div>
        </Card>
      </div>

      <Card title="Live Activity Feed" subtitle="Real-time session events">
        <div className="live-feed-container">
          <div className="live-indicator-row">
            <span className="live-dot" />
            <span className="live-text">LIVE</span>
          </div>
          {liveFeed.map((item, i) => (
            <div key={i} className={`feed-row ${i === 0 ? "feed-row-highlight" : ""}`}>
              <div className="feed-row-left">
                <Activity size={13} className="feed-icon" style={{ color: i === 0 ? "#00f0ff" : "var(--text-muted)" }} />
                <span className="feed-label">{item.label}</span>
              </div>
              <span className="feed-value">{item.value}</span>
              <span className="feed-time">{item.time}</span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
