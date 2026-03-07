import { useState, useEffect, useRef } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, RadarChart, Radar, PolarGrid, PolarAngleAxis, LineChart, Line, ResponsiveContainer } from "recharts";

const COLORS = {
  logistic:  { main: "#38bdf8", glow: "rgba(56,189,248,0.35)",  bg: "rgba(56,189,248,0.08)"  },
  smote:     { main: "#a78bfa", glow: "rgba(167,139,250,0.35)", bg: "rgba(167,139,250,0.08)" },
  rf:        { main: "#34d399", glow: "rgba(52,211,153,0.35)",  bg: "rgba(52,211,153,0.08)"  },
  xgboost:   { main: "#fb923c", glow: "rgba(251,146,60,0.35)",  bg: "rgba(251,146,60,0.08)"  },
  combined:  { main: "#f472b6", glow: "rgba(244,114,182,0.35)", bg: "rgba(244,114,182,0.08)" },
};

const MODELS = {
  logistic: {
    label: "Logistic Regression", short: "LR", emoji: "📐",
    desc: "Interpretable baseline model. Fast and transparent — ideal for stakeholder reporting.",
    color: COLORS.logistic,
    metrics: { accuracy: 0.8034, precision: 0.6520, recall: 0.5561, f1: 0.6003, roc: 0.8417 },
    cv: [0.843, 0.848, 0.845, 0.850, 0.844],
    shap: [
      { feature: "Contract_Month-to-month", value: 1.32 },
      { feature: "Tenure", value: 1.18 },
      { feature: "OnlineSecurity_No", value: 0.74 },
      { feature: "MonthlyCharges", value: 0.61 },
      { feature: "TechSupport_No", value: 0.55 },
    ],
    insight: "Highest accuracy (80.3%) but misses 44% of churners. Best for explainability.",
  },
  smote: {
    label: "Logistic + SMOTE", short: "SMOTE", emoji: "⚗️",
    desc: "Oversampling technique to fix class imbalance. Dramatically improves recall on minority churn class.",
    color: COLORS.smote,
    metrics: { accuracy: 0.7615, precision: 0.5380, recall: 0.7193, f1: 0.6156, roc: 0.8399 },
    cv: [0.838, 0.841, 0.840, 0.843, 0.839],
    shap: [
      { feature: "Contract_Month-to-month", value: 1.28 },
      { feature: "Tenure", value: 1.10 },
      { feature: "InternetService_Fiber", value: 0.80 },
      { feature: "PaymentMethod_ECheck", value: 0.65 },
      { feature: "MonthlyCharges", value: 0.58 },
    ],
    insight: "Recall jumps to 72% — catching far more churners. Trades precision for coverage.",
  },
  rf: {
    label: "Random Forest", short: "RF", emoji: "🌲",
    desc: "Ensemble of decision trees with native class balancing. Highest raw recall in the comparison.",
    color: COLORS.rf,
    metrics: { accuracy: 0.7296, precision: 0.4941, recall: 0.7834, f1: 0.6060, roc: 0.8154 },
    cv: [0.799, 0.803, 0.801, 0.800, 0.793],
    shap: [
      { feature: "Tenure", value: 1.40 },
      { feature: "Contract_Month-to-month", value: 1.22 },
      { feature: "MonthlyCharges", value: 0.90 },
      { feature: "TotalCharges", value: 0.72 },
      { feature: "OnlineSecurity_No", value: 0.60 },
    ],
    insight: "Best recall at 78.3% — catches the most churners. Less stable in cross-validation.",
  },
  xgboost: {
    label: "XGBoost", short: "XGB", emoji: "🚀",
    desc: "Gradient boosted trees. Best overall balance of all metrics and most consistent across folds.",
    color: COLORS.xgboost,
    metrics: { accuracy: 0.7800, precision: 0.5777, recall: 0.6364, f1: 0.6056, roc: 0.8430 },
    cv: [0.854, 0.861, 0.858, 0.867, 0.851],
    shap: [
      { feature: "Contract_Month-to-month", value: 1.35 },
      { feature: "Tenure", value: 1.20 },
      { feature: "OnlineSecurity_No", value: 0.78 },
      { feature: "InternetService_Fiber", value: 0.70 },
      { feature: "PaymentMethod_ECheck", value: 0.62 },
    ],
    insight: "Best ROC-AUC (0.843) and highest CV F1 (~0.858). Recommended production model.",
  },
};

const METRIC_LABELS = { accuracy: "Accuracy", precision: "Precision", recall: "Recall", f1: "F1 Score", roc: "ROC-AUC" };

const radarData = ["Accuracy","Precision","Recall","F1 Score","ROC-AUC"].map(metric => {
  const row = { metric };
  Object.entries(MODELS).forEach(([key, m]) => {
    const raw = metric === "F1 Score" ? m.metrics.f1 : metric === "ROC-AUC" ? m.metrics.roc : m.metrics[metric.toLowerCase()];
    row[m.short] = +(raw * 100).toFixed(1);
  });
  return row;
});

function AnimatedNumber({ value, duration = 1200 }) {
  const [display, setDisplay] = useState(0);
  useEffect(() => {
    let start = null;
    const step = (ts) => {
      if (!start) start = ts;
      const p = Math.min((ts - start) / duration, 1);
      setDisplay(+(value * p).toFixed(4));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }, [value]);
  return <span>{display.toFixed(4)}</span>;
}

function MetricCard({ label, value, color, delay = 0 }) {
  const [visible, setVisible] = useState(false);
  useEffect(() => { const t = setTimeout(() => setVisible(true), delay); return () => clearTimeout(t); }, [delay]);
  const pct = Math.round(value * 100);
  return (
    <div style={{
      opacity: visible ? 1 : 0, transform: visible ? "translateY(0)" : "translateY(20px)",
      transition: "all 0.5s ease", background: "rgba(15,20,35,0.7)",
      border: `1px solid ${color.main}40`, borderRadius: 16, padding: "20px 24px",
      boxShadow: `0 0 20px ${color.glow}`, position: "relative", overflow: "hidden",
    }}>
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 3, background: color.main, borderRadius: "16px 16px 0 0" }} />
      <div style={{ fontSize: 12, color: "#94a3b8", letterSpacing: 2, textTransform: "uppercase", marginBottom: 8, fontFamily: "'Courier New', monospace" }}>{label}</div>
      <div style={{ fontSize: 32, fontWeight: 800, color: color.main, fontFamily: "'Georgia', serif", lineHeight: 1 }}>
        <AnimatedNumber value={value} />
      </div>
      <div style={{ marginTop: 10, height: 4, background: "rgba(255,255,255,0.05)", borderRadius: 4 }}>
        <div style={{ height: "100%", width: `${pct}%`, background: `linear-gradient(90deg, ${color.main}80, ${color.main})`, borderRadius: 4, transition: "width 1.2s ease" }} />
      </div>
    </div>
  );
}

function Particles({ color }) {
  const canvas = useRef(null);
  useEffect(() => {
    const c = canvas.current; if (!c) return;
    const ctx = c.getContext("2d");
    c.width = c.offsetWidth; c.height = c.offsetHeight;
    const pts = Array.from({ length: 40 }, () => ({
      x: Math.random() * c.width, y: Math.random() * c.height,
      vx: (Math.random() - 0.5) * 0.4, vy: (Math.random() - 0.5) * 0.4,
      r: Math.random() * 2 + 1,
    }));
    let raf;
    const draw = () => {
      ctx.clearRect(0, 0, c.width, c.height);
      pts.forEach(p => {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > c.width)  p.vx *= -1;
        if (p.y < 0 || p.y > c.height) p.vy *= -1;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = color + "60"; ctx.fill();
      });
      pts.forEach((a, i) => pts.slice(i+1).forEach(b => {
        const d = Math.hypot(a.x - b.x, a.y - b.y);
        if (d < 80) {
          ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = color + Math.floor((1 - d/80) * 40).toString(16).padStart(2,"0");
          ctx.lineWidth = 0.5; ctx.stroke();
        }
      }));
      raf = requestAnimationFrame(draw);
    };
    draw();
    return () => cancelAnimationFrame(raf);
  }, [color]);
  return <canvas ref={canvas} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", pointerEvents: "none" }} />;
}

function CVChart({ model }) {
  const m = MODELS[model];
  const data = m.cv.map((v, i) => ({ fold: `Fold ${i+1}`, F1: +(v * 100).toFixed(2) }));
  return (
    <ResponsiveContainer width="100%" height={180}>
      <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
        <XAxis dataKey="fold" tick={{ fill: "#64748b", fontSize: 11 }} />
        <YAxis domain={[75, 90]} tick={{ fill: "#64748b", fontSize: 11 }} tickFormatter={v => v + "%"} />
        <Tooltip contentStyle={{ background: "#0f141e", border: `1px solid ${m.color.main}40`, borderRadius: 8 }} formatter={v => [v + "%", "F1 Score"]} />
        <Line type="monotone" dataKey="F1" stroke={m.color.main} strokeWidth={2.5} dot={{ fill: m.color.main, r: 5 }} activeDot={{ r: 7 }} />
      </LineChart>
    </ResponsiveContainer>
  );
}

function SHAPChart({ model }) {
  const m = MODELS[model];
  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart data={m.shap} layout="vertical" margin={{ left: 8, right: 20, top: 5, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
        <XAxis type="number" tick={{ fill: "#64748b", fontSize: 10 }} />
        <YAxis type="category" dataKey="feature" width={190} tick={{ fill: "#94a3b8", fontSize: 10 }} />
        <Tooltip contentStyle={{ background: "#0f141e", border: `1px solid ${m.color.main}40`, borderRadius: 8 }} formatter={v => [v.toFixed(2), "Mean |SHAP|"]} />
        <Bar dataKey="value" fill={m.color.main} radius={[0, 6, 6, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

function ModelView({ model }) {
  const m = MODELS[model];
  const metrics = Object.entries(m.metrics);
  return (
    <div style={{ animation: "fadeSlide 0.5s ease forwards" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 32 }}>
        <div style={{ fontSize: 48 }}>{m.emoji}</div>
        <div>
          <h2 style={{ margin: 0, fontSize: 28, fontWeight: 900, color: m.color.main, fontFamily: "'Georgia', serif" }}>{m.label}</h2>
          <p style={{ margin: "6px 0 0", color: "#94a3b8", fontSize: 14, maxWidth: 520 }}>{m.desc}</p>
        </div>
        <div style={{ marginLeft: "auto", background: m.color.bg, border: `1px solid ${m.color.main}50`, borderRadius: 12, padding: "10px 18px" }}>
          <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }}>Verdict</div>
          <div style={{ color: m.color.main, fontSize: 13, fontWeight: 600, maxWidth: 200 }}>{m.insight}</div>
        </div>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 14, marginBottom: 32 }}>
        {metrics.map(([key, val], i) => (
          <MetricCard key={key} label={METRIC_LABELS[key]} value={val} color={m.color} delay={i * 100} />
        ))}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
        <div style={{ background: "rgba(15,20,35,0.7)", border: `1px solid ${m.color.main}25`, borderRadius: 16, padding: 24 }}>
          <h3 style={{ margin: "0 0 16px", color: "#e2e8f0", fontSize: 14, textTransform: "uppercase", letterSpacing: 2, fontFamily: "'Courier New', monospace" }}>
            📊 5-Fold Cross-Validation F1
          </h3>
          <CVChart model={model} />
          <p style={{ margin: "12px 0 0", fontSize: 12, color: "#64748b", textAlign: "center" }}>
            Mean CV F1: {(m.cv.reduce((a,b) => a+b,0)/m.cv.length * 100).toFixed(2)}% &nbsp;|&nbsp; Std: ±{(Math.sqrt(m.cv.reduce((s,v) => s + Math.pow(v - m.cv.reduce((a,b)=>a+b)/m.cv.length, 2), 0)/m.cv.length)*100).toFixed(3)}%
          </p>
        </div>
        <div style={{ background: "rgba(15,20,35,0.7)", border: `1px solid ${m.color.main}25`, borderRadius: 16, padding: 24 }}>
          <h3 style={{ margin: "0 0 16px", color: "#e2e8f0", fontSize: 14, textTransform: "uppercase", letterSpacing: 2, fontFamily: "'Courier New', monospace" }}>
            🧠 SHAP Feature Importance
          </h3>
          <SHAPChart model={model} />
        </div>
      </div>
    </div>
  );
}

function CombinedView() {
  const barData = ["Accuracy","Precision","Recall","F1 Score","ROC-AUC"].map(metric => {
    const row = { metric };
    Object.entries(MODELS).forEach(([key, m]) => {
      const raw = metric === "F1 Score" ? m.metrics.f1 : metric === "ROC-AUC" ? m.metrics.roc : m.metrics[metric.toLowerCase()];
      row[m.short] = +(raw * 100).toFixed(1);
    });
    return row;
  });

  return (
    <div style={{ animation: "fadeSlide 0.5s ease forwards" }}>
      <div style={{ marginBottom: 32 }}>
        <h2 style={{ margin: "0 0 6px", fontSize: 28, fontWeight: 900, color: "#f472b6", fontFamily: "'Georgia', serif" }}>
          🏆 All Models — Head to Head
        </h2>
        <p style={{ margin: 0, color: "#94a3b8", fontSize: 14 }}>Comparing all four models across every metric. Recall is the primary business metric.</p>
      </div>
      <div style={{ background: "rgba(15,20,35,0.7)", border: "1px solid rgba(244,114,182,0.2)", borderRadius: 16, padding: 28, marginBottom: 24 }}>
        <h3 style={{ margin: "0 0 20px", color: "#e2e8f0", fontSize: 13, textTransform: "uppercase", letterSpacing: 2, fontFamily: "'Courier New', monospace" }}>📊 Metric Comparison</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={barData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis dataKey="metric" tick={{ fill: "#94a3b8", fontSize: 12 }} />
            <YAxis domain={[40, 90]} tick={{ fill: "#64748b", fontSize: 11 }} tickFormatter={v => v + "%"} />
            <Tooltip contentStyle={{ background: "#0f141e", border: "1px solid rgba(244,114,182,0.3)", borderRadius: 8 }} formatter={v => v + "%"} />
            <Legend wrapperStyle={{ color: "#94a3b8", fontSize: 12 }} />
            <Bar dataKey="LR"    fill={COLORS.logistic.main} radius={[4,4,0,0]} name="Logistic" />
            <Bar dataKey="SMOTE" fill={COLORS.smote.main}   radius={[4,4,0,0]} name="SMOTE" />
            <Bar dataKey="RF"    fill={COLORS.rf.main}      radius={[4,4,0,0]} name="Random Forest" />
            <Bar dataKey="XGB"   fill={COLORS.xgboost.main} radius={[4,4,0,0]} name="XGBoost" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
        <div style={{ background: "rgba(15,20,35,0.7)", border: "1px solid rgba(244,114,182,0.2)", borderRadius: 16, padding: 28 }}>
          <h3 style={{ margin: "0 0 20px", color: "#e2e8f0", fontSize: 13, textTransform: "uppercase", letterSpacing: 2, fontFamily: "'Courier New', monospace" }}>🕸️ Radar — Full Profile</h3>
          <ResponsiveContainer width="100%" height={280}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="rgba(255,255,255,0.08)" />
              <PolarAngleAxis dataKey="metric" tick={{ fill: "#94a3b8", fontSize: 11 }} />
              {Object.entries(MODELS).map(([key, m]) => (
                <Radar key={key} name={m.short} dataKey={m.short} stroke={m.color.main} fill={m.color.main} fillOpacity={0.12} strokeWidth={2} />
              ))}
              <Legend wrapperStyle={{ color: "#94a3b8", fontSize: 11 }} />
              <Tooltip contentStyle={{ background: "#0f141e", border: "1px solid #f472b650", borderRadius: 8 }} formatter={v => v + "%"} />
            </RadarChart>
          </ResponsiveContainer>
        </div>
        <div style={{ background: "rgba(15,20,35,0.7)", border: "1px solid rgba(244,114,182,0.2)", borderRadius: 16, padding: 28 }}>
          <h3 style={{ margin: "0 0 20px", color: "#e2e8f0", fontSize: 13, textTransform: "uppercase", letterSpacing: 2, fontFamily: "'Courier New', monospace" }}>🏅 Model Verdict</h3>
          {Object.entries(MODELS).map(([key, m]) => (
            <div key={key} style={{ display: "flex", alignItems: "center", gap: 14, padding: "12px 0", borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
              <div style={{ fontSize: 22 }}>{m.emoji}</div>
              <div style={{ flex: 1 }}>
                <div style={{ color: m.color.main, fontWeight: 700, fontSize: 14 }}>{m.label}</div>
                <div style={{ color: "#64748b", fontSize: 12, marginTop: 2 }}>{m.insight}</div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: 11, color: "#64748b" }}>Recall</div>
                <div style={{ fontSize: 18, fontWeight: 800, color: m.color.main }}>{(m.metrics.recall * 100).toFixed(1)}%</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [active, setActive] = useState("xgboost");
  const [loaded, setLoaded] = useState(false);

  useEffect(() => { setTimeout(() => setLoaded(true), 100); }, []);

  const tabs = [
    ...Object.entries(MODELS).map(([key, m]) => ({ key, label: m.label, short: m.short, emoji: m.emoji, color: m.color })),
    { key: "combined", label: "All Models", short: "ALL", emoji: "🏆", color: COLORS.combined },
  ];

  const activeColor = active === "combined" ? COLORS.combined : MODELS[active]?.color || COLORS.combined;

  return (
    <div style={{ minHeight: "100vh", background: "#070b14", fontFamily: "'Segoe UI', sans-serif", color: "#e2e8f0", position: "relative", overflow: "hidden" }}>
      <style>{`
        @keyframes fadeSlide { from { opacity:0; transform:translateY(16px) } to { opacity:1; transform:translateY(0) } }
        @keyframes pulse { 0%,100%{opacity:.5} 50%{opacity:1} }
        @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
        * { box-sizing:border-box; }
        ::-webkit-scrollbar { width:6px }
        ::-webkit-scrollbar-track { background:#0f141e }
        ::-webkit-scrollbar-thumb { background:#1e293b; border-radius:4px }
      `}</style>

      {/* Ambient blobs */}
      <div style={{ position: "fixed", inset: 0, pointerEvents: "none", zIndex: 0 }}>
        <div style={{ position: "absolute", width: 600, height: 600, borderRadius: "50%", background: `radial-gradient(circle, ${activeColor.main}12 0%, transparent 70%)`, top: -200, left: -200, transition: "background 0.8s ease" }} />
        <div style={{ position: "absolute", width: 500, height: 500, borderRadius: "50%", background: `radial-gradient(circle, ${activeColor.main}08 0%, transparent 70%)`, bottom: -150, right: -150, transition: "background 0.8s ease" }} />
        <Particles color={activeColor.main} />
      </div>

      <div style={{ position: "relative", zIndex: 1, maxWidth: 1300, margin: "0 auto", padding: "32px 24px" }}>

        {/* Header */}
        <div style={{ opacity: loaded ? 1 : 0, transform: loaded ? "none" : "translateY(-20px)", transition: "all 0.7s ease", marginBottom: 40, textAlign: "center" }}>
          <div style={{ fontSize: 13, letterSpacing: 4, color: "#475569", textTransform: "uppercase", fontFamily: "'Courier New', monospace", marginBottom: 12 }}>
            ◆ Machine Learning Dashboard ◆
          </div>

          {/* ── FIXED: solid colour title, no gradient clip ── */}
          <h1 style={{
            margin: "0 0 10px",
            fontSize: "clamp(28px, 4vw, 48px)",
            fontWeight: 900,
            fontFamily: "'Georgia', serif",
            color: activeColor.main,
            transition: "color 0.6s ease",
            background: "none",
            WebkitTextFillColor: "unset",
          }}>
            Customer Churn Prediction
          </h1>

          <p style={{ margin: "0 0 8px", color: "#64748b", fontSize: 15 }}>
            Telco Industry · Logistic Regression → SMOTE → Random Forest → XGBoost
          </p>
          <div style={{ display: "inline-flex", alignItems: "center", gap: 8, background: "rgba(15,20,35,0.8)", border: `1px solid ${activeColor.main}30`, borderRadius: 20, padding: "6px 16px", fontSize: 12, color: "#94a3b8", transition: "border-color 0.6s" }}>
            <span style={{ width: 7, height: 7, borderRadius: "50%", background: activeColor.main, boxShadow: `0 0 8px ${activeColor.main}`, animation: "pulse 2s infinite" }} />
            Developed by <strong style={{ color: activeColor.main, marginLeft: 4, transition: "color 0.6s" }}>Temi Priscilla Jokotola</strong>
          </div>
        </div>

        {/* Tab Bar */}
        <div style={{ display: "flex", gap: 10, marginBottom: 36, flexWrap: "wrap", justifyContent: "center", opacity: loaded ? 1 : 0, transition: "opacity 0.7s ease 0.2s" }}>
          {tabs.map(({ key, label, emoji, color }) => {
            const isActive = active === key;
            return (
              <button key={key} onClick={() => setActive(key)} style={{
                display: "flex", alignItems: "center", gap: 8,
                padding: "10px 20px", borderRadius: 12, cursor: "pointer",
                border: isActive ? `1.5px solid ${color.main}` : "1.5px solid rgba(255,255,255,0.08)",
                background: isActive ? color.bg : "rgba(15,20,35,0.6)",
                color: isActive ? color.main : "#64748b",
                fontWeight: isActive ? 700 : 500, fontSize: 13,
                boxShadow: isActive ? `0 0 18px ${color.glow}` : "none",
                transition: "all 0.3s ease", transform: isActive ? "translateY(-2px)" : "none",
              }}>
                <span>{emoji}</span> {label}
              </button>
            );
          })}
        </div>

        {/* Main content */}
        <div style={{ opacity: loaded ? 1 : 0, transition: "opacity 0.7s ease 0.3s" }}>
          {active === "combined" ? <CombinedView /> : <ModelView model={active} />}
        </div>

        {/* Business Insights */}
        <div style={{ marginTop: 40, background: "rgba(15,20,35,0.7)", border: `1px solid ${activeColor.main}20`, borderRadius: 20, padding: 32, transition: "border-color 0.6s" }}>
          <h3 style={{ margin: "0 0 20px", fontSize: 13, textTransform: "uppercase", letterSpacing: 2, color: "#e2e8f0", fontFamily: "'Courier New', monospace" }}>
            💼 Business Recommendations
          </h3>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: 16 }}>
            {[
              { icon: "📋", title: "Lock In Contracts", body: "Month-to-month customers are the #1 churn risk. Incentivise upgrades to annual plans." },
              { icon: "🎯", title: "Early Intervention", body: "Target customers in their first 3–6 months with proactive onboarding & check-ins." },
              { icon: "🛡️", title: "Bundle Add-ons", body: "Offer Online Security & Tech Support free to new or high-risk customers." },
              { icon: "💳", title: "Switch Payment Method", body: "Electronic check payers churn more — nudge toward auto-pay with a small incentive." },
              { icon: "💰", title: "Pricing Review", body: "Review value proposition for customers paying above £70/month on Fiber plans." },
              { icon: "🗳️", title: "Ensemble Signals", body: "Customers flagged by 3+ models simultaneously = highest priority for intervention." },
            ].map(({ icon, title, body }) => (
              <div key={title} style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)", borderRadius: 12, padding: 18 }}>
                <div style={{ fontSize: 22, marginBottom: 8 }}>{icon}</div>
                <div style={{ fontWeight: 700, color: activeColor.main, fontSize: 14, marginBottom: 6, transition: "color 0.6s" }}>{title}</div>
                <div style={{ color: "#64748b", fontSize: 13, lineHeight: 1.6 }}>{body}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div style={{ marginTop: 32, textAlign: "center", color: "#334155", fontSize: 12, fontFamily: "'Courier New', monospace" }}>
          Developed with ♥ by <span style={{ color: activeColor.main, transition: "color 0.6s" }}>Temi Priscilla Jokotola</span> &nbsp;·&nbsp; Telco Churn Prediction &nbsp;·&nbsp; Python · Scikit-Learn · XGBoost · SHAP
        </div>
      </div>
    </div>
  );
}
