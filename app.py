import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Telco Churn Dashboard | Temi Priscilla Jokotola",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Hide Streamlit default chrome ──────────────────────────────────────────────
st.markdown("""
<style>
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  body { background: #070b14; }
</style>
""", unsafe_allow_html=True)

# ── Full dashboard as embedded HTML ───────────────────────────────────────────
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=JetBrains+Mono:wght@400;600&family=DM+Sans:wght@400;500;600;700;800&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --lr:    #38bdf8; --lr-g:  rgba(56,189,248,0.3);  --lr-b:  rgba(56,189,248,0.08);
    --sm:    #a78bfa; --sm-g:  rgba(167,139,250,0.3); --sm-b:  rgba(167,139,250,0.08);
    --rf:    #34d399; --rf-g:  rgba(52,211,153,0.3);  --rf-b:  rgba(52,211,153,0.08);
    --xgb:   #fb923c; --xgb-g: rgba(251,146,60,0.3);  --xgb-b: rgba(251,146,60,0.08);
    --all:   #f472b6; --all-g: rgba(244,114,182,0.3); --all-b: rgba(244,114,182,0.08);
    --active: #38bdf8; --active-g: rgba(56,189,248,0.3);
    --bg: #070b14; --card: rgba(15,20,35,0.85); --border: rgba(255,255,255,0.07);
    --text: #e2e8f0; --muted: #64748b; --sub: #94a3b8;
  }

  html, body { background: var(--bg); color: var(--text); font-family: 'DM Sans', sans-serif; min-height: 100vh; overflow-x: hidden; }

  canvas#particles { position: fixed; inset: 0; pointer-events: none; z-index: 0; }

  .wrap { position: relative; z-index: 1; max-width: 1280px; margin: 0 auto; padding: 36px 24px 60px; }

  /* ── Header ── */
  .header { text-align: center; margin-bottom: 40px; animation: fadeUp .7s ease forwards; }
  .header .eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 4px; color: var(--muted); text-transform: uppercase; margin-bottom: 14px; }
  .header h1 { font-family: 'DM Serif Display', serif; font-size: clamp(28px, 4vw, 50px); font-weight: 400; background: linear-gradient(135deg, #e2e8f0 0%, var(--active) 55%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; transition: background .6s; margin-bottom: 10px; }
  .header .sub { color: var(--muted); font-size: 14px; margin-bottom: 14px; }
  .badge { display: inline-flex; align-items: center; gap: 8px; background: var(--card); border: 1px solid rgba(56,189,248,0.25); border-radius: 20px; padding: 7px 18px; font-size: 12px; color: var(--sub); transition: border-color .6s; }
  .pulse { width: 7px; height: 7px; border-radius: 50%; background: var(--active); box-shadow: 0 0 8px var(--active); animation: pulse 2s infinite; transition: background .6s, box-shadow .6s; }
  .badge strong { color: var(--active); transition: color .6s; }

  /* ── Tabs ── */
  .tabs { display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; margin-bottom: 36px; }
  .tab { display: flex; align-items: center; gap: 8px; padding: 10px 20px; border-radius: 12px; cursor: pointer; border: 1.5px solid var(--border); background: var(--card); color: var(--muted); font-weight: 600; font-size: 13px; transition: all .3s ease; user-select: none; }
  .tab:hover { border-color: rgba(255,255,255,0.2); color: var(--text); transform: translateY(-1px); }
  .tab.active { transform: translateY(-3px); }

  /* ── Metric cards ── */
  .metrics { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-bottom: 28px; }
  @media(max-width:900px){ .metrics { grid-template-columns: repeat(3,1fr); } }
  @media(max-width:560px){ .metrics { grid-template-columns: repeat(2,1fr); } }
  .metric-card { background: var(--card); border-radius: 16px; padding: 20px 22px; position: relative; overflow: hidden; border: 1px solid var(--border); transition: box-shadow .4s, border-color .4s; animation: fadeUp .5s ease forwards; }
  .metric-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; border-radius:16px 16px 0 0; }
  .metric-card .label { font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--muted); letter-spacing:2px; text-transform:uppercase; margin-bottom:8px; }
  .metric-card .value { font-family:'DM Serif Display',serif; font-size:30px; line-height:1; margin-bottom:10px; }
  .metric-card .bar-track { height:4px; background:rgba(255,255,255,0.05); border-radius:4px; }
  .metric-card .bar-fill  { height:100%; border-radius:4px; transition:width 1.2s ease; }

  /* ── Two-col grid ── */
  .grid2 { display:grid; grid-template-columns:1fr 1fr; gap:24px; margin-bottom:28px; }
  @media(max-width:760px){ .grid2 { grid-template-columns:1fr; } }
  .panel { background:var(--card); border:1px solid var(--border); border-radius:16px; padding:26px; transition:border-color .4s; }
  .panel-title { font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:2px; text-transform:uppercase; color:var(--text); margin-bottom:18px; }

  /* ── Verdict card ── */
  .verdict { background:var(--card); border:1px solid var(--border); border-radius:16px; padding:26px; margin-bottom:28px; display:flex; align-items:center; gap:20px; transition:border-color .4s; }
  .verdict .emoji { font-size:44px; }
  .verdict .vname { font-family:'DM Serif Display',serif; font-size:26px; margin-bottom:6px; }
  .verdict .vdesc { color:var(--sub); font-size:14px; max-width:520px; line-height:1.6; }
  .verdict .chip  { margin-left:auto; padding:12px 18px; border-radius:12px; font-size:13px; font-weight:600; line-height:1.5; min-width:200px; }
  .verdict .chip .chip-label { font-size:10px; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:4px; font-family:'JetBrains Mono',monospace; }

  /* ── Recommendations ── */
  .recs { background:var(--card); border:1px solid var(--border); border-radius:20px; padding:30px; margin-bottom:28px; transition:border-color .4s; }
  .recs-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:16px; margin-top:18px; }
  .rec-card { background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:18px; }
  .rec-icon { font-size:22px; margin-bottom:8px; }
  .rec-title { font-weight:700; font-size:13px; margin-bottom:6px; transition:color .6s; }
  .rec-body  { color:var(--muted); font-size:12px; line-height:1.6; }

  /* ── Verdict list (combined) ── */
  .vlist-item { display:flex; align-items:center; gap:14px; padding:14px 0; border-bottom:1px solid rgba(255,255,255,0.05); }
  .vlist-item:last-child { border-bottom:none; }
  .vlist-icon { font-size:22px; }
  .vlist-name { font-weight:700; font-size:14px; }
  .vlist-desc { color:var(--muted); font-size:12px; margin-top:2px; }
  .vlist-recall { text-align:right; }
  .vlist-recall .rl { font-size:10px; color:var(--muted); }
  .vlist-recall .rv { font-size:20px; font-weight:800; font-family:'DM Serif Display',serif; }

  /* ── Footer ── */
  .footer { text-align:center; color:#334155; font-size:12px; font-family:'JetBrains Mono',monospace; margin-top:32px; }
  .footer span { transition:color .6s; }

  /* ── Animations ── */
  @keyframes fadeUp { from{opacity:0;transform:translateY(18px)} to{opacity:1;transform:translateY(0)} }
  @keyframes pulse  { 0%,100%{opacity:.5} 50%{opacity:1} }

  .view { animation: fadeUp .45s ease forwards; }
  .hidden { display:none !important; }
</style>
</head>
<body>
<canvas id="particles"></canvas>

<div class="wrap">

  <!-- Header -->
  <div class="header">
    <div class="eyebrow">◆ Machine Learning Dashboard ◆</div>
    <h1 id="main-title">Customer Churn Prediction</h1>
    <p class="sub">Telco Industry · Logistic Regression → SMOTE → Random Forest → XGBoost</p>
    <div class="badge">
      <span class="pulse" id="pulse-dot"></span>
      Developed by <strong id="dev-name">Temi Priscilla Jokotola</strong>
    </div>
  </div>

  <!-- Tabs -->
  <div class="tabs" id="tabs">
    <div class="tab active" data-model="logistic" onclick="switchModel('logistic')">📐 Logistic Regression</div>
    <div class="tab" data-model="smote"    onclick="switchModel('smote')">⚗️ Logistic + SMOTE</div>
    <div class="tab" data-model="rf"       onclick="switchModel('rf')">🌲 Random Forest</div>
    <div class="tab" data-model="xgboost"  onclick="switchModel('xgboost')">🚀 XGBoost</div>
    <div class="tab" data-model="combined" onclick="switchModel('combined')">🏆 All Models</div>
  </div>

  <!-- Single model view -->
  <div id="single-view">
    <div class="verdict" id="verdict-card">
      <div class="emoji" id="v-emoji">📐</div>
      <div>
        <div class="vname" id="v-name">Logistic Regression</div>
        <div class="vdesc" id="v-desc">Interpretable baseline model. Fast and transparent.</div>
      </div>
      <div class="chip" id="v-chip">
        <div class="chip-label">Verdict</div>
        <div id="v-insight"></div>
      </div>
    </div>

    <div class="metrics" id="metrics-grid"></div>

    <div class="grid2">
      <div class="panel">
        <div class="panel-title">📊 5-Fold Cross-Validation F1</div>
        <canvas id="cv-chart" height="160"></canvas>
        <p id="cv-stats" style="text-align:center;font-size:11px;color:var(--muted);margin-top:10px;font-family:'JetBrains Mono',monospace;"></p>
      </div>
      <div class="panel">
        <div class="panel-title">🧠 SHAP Feature Importance</div>
        <canvas id="shap-chart" height="160"></canvas>
      </div>
    </div>
  </div>

  <!-- Combined view -->
  <div id="combined-view" class="hidden">
    <div style="margin-bottom:28px;">
      <h2 style="font-family:'DM Serif Display',serif;font-size:28px;color:var(--all);margin-bottom:6px;">🏆 All Models — Head to Head</h2>
      <p style="color:var(--muted);font-size:14px;">Recall is the primary business metric — catching churners before they leave.</p>
    </div>
    <div class="panel" style="margin-bottom:24px;">
      <div class="panel-title">📊 Metric Comparison — All Models</div>
      <canvas id="compare-chart" height="200"></canvas>
    </div>
    <div class="grid2">
      <div class="panel">
        <div class="panel-title">🕸️ Radar — Full Model Profiles</div>
        <canvas id="radar-chart" height="260"></canvas>
      </div>
      <div class="panel">
        <div class="panel-title">🏅 Model Verdict</div>
        <div id="verdict-list"></div>
      </div>
    </div>
  </div>

  <!-- Recommendations -->
  <div class="recs" id="recs-panel">
    <div class="panel-title" id="recs-title">💼 Business Recommendations</div>
    <div class="recs-grid">
      <div class="rec-card"><div class="rec-icon">📋</div><div class="rec-title" id="rc1-t">Lock In Contracts</div><div class="rec-body">Month-to-month customers are the #1 churn risk. Incentivise upgrades to annual plans.</div></div>
      <div class="rec-card"><div class="rec-icon">🎯</div><div class="rec-title" id="rc2-t">Early Intervention</div><div class="rec-body">Target customers in their first 3–6 months with proactive onboarding & check-ins.</div></div>
      <div class="rec-card"><div class="rec-icon">🛡️</div><div class="rec-title" id="rc3-t">Bundle Add-ons</div><div class="rec-body">Offer Online Security & Tech Support free to new or at-risk customers.</div></div>
      <div class="rec-card"><div class="rec-icon">💳</div><div class="rec-title" id="rc4-t">Switch Payment</div><div class="rec-body">Electronic check payers churn more — nudge toward auto-pay with a small incentive.</div></div>
      <div class="rec-card"><div class="rec-icon">💰</div><div class="rec-title" id="rc5-t">Pricing Review</div><div class="rec-body">Review value proposition for customers paying above £70/month on Fiber plans.</div></div>
      <div class="rec-card"><div class="rec-icon">🗳️</div><div class="rec-title" id="rc6-t">Ensemble Signals</div><div class="rec-body">Customers flagged by 3+ models simultaneously = highest priority for intervention.</div></div>
    </div>
  </div>

  <div class="footer">Developed with ♥ by <span id="footer-name" style="color:var(--active);">Temi Priscilla Jokotola</span> &nbsp;·&nbsp; Telco Churn Prediction &nbsp;·&nbsp; Python · Scikit-Learn · XGBoost · SHAP</div>
</div>

<script>
const MODELS = {
  logistic: {
    label:"Logistic Regression", emoji:"📐",
    desc:"Interpretable baseline model. Fast and transparent — ideal for stakeholder reporting.",
    insight:"Highest accuracy (80.3%) but misses 44% of churners. Best for explainability.",
    color:"#38bdf8", glow:"rgba(56,189,248,0.3)", bg:"rgba(56,189,248,0.08)",
    metrics:{ Accuracy:.8034, Precision:.6520, Recall:.5561, "F1 Score":.6003, "ROC-AUC":.8417 },
    cv:[84.3,84.8,84.5,85.0,84.4],
    shap:{ labels:["Contract M-t-M","Tenure","OnlineSecurity_No","MonthlyCharges","TechSupport_No"], values:[1.32,1.18,0.74,0.61,0.55] }
  },
  smote: {
    label:"Logistic + SMOTE", emoji:"⚗️",
    desc:"Oversampling technique to fix class imbalance. Dramatically improves recall on the minority churn class.",
    insight:"Recall jumps to 72% — catching far more churners. Trades precision for coverage.",
    color:"#a78bfa", glow:"rgba(167,139,250,0.3)", bg:"rgba(167,139,250,0.08)",
    metrics:{ Accuracy:.7615, Precision:.5380, Recall:.7193, "F1 Score":.6156, "ROC-AUC":.8399 },
    cv:[83.8,84.1,84.0,84.3,83.9],
    shap:{ labels:["Contract M-t-M","Tenure","Fiber Optic","PayMethod ECheck","MonthlyCharges"], values:[1.28,1.10,0.80,0.65,0.58] }
  },
  rf: {
    label:"Random Forest", emoji:"🌲",
    desc:"Ensemble of decision trees with native class balancing. Achieves the highest raw recall in the comparison.",
    insight:"Best recall at 78.3% — catches the most churners. Less stable in cross-validation.",
    color:"#34d399", glow:"rgba(52,211,153,0.3)", bg:"rgba(52,211,153,0.08)",
    metrics:{ Accuracy:.7296, Precision:.4941, Recall:.7834, "F1 Score":.6060, "ROC-AUC":.8154 },
    cv:[79.9,80.3,80.1,80.0,79.3],
    shap:{ labels:["Tenure","Contract M-t-M","MonthlyCharges","TotalCharges","OnlineSecurity_No"], values:[1.40,1.22,0.90,0.72,0.60] }
  },
  xgboost: {
    label:"XGBoost", emoji:"🚀",
    desc:"Gradient boosted trees. Best overall balance of all metrics and most consistent across folds.",
    insight:"Best ROC-AUC (0.843) and highest CV F1 (~0.858). Recommended production model.",
    color:"#fb923c", glow:"rgba(251,146,60,0.3)", bg:"rgba(251,146,60,0.08)",
    metrics:{ Accuracy:.7800, Precision:.5777, Recall:.6364, "F1 Score":.6056, "ROC-AUC":.8430 },
    cv:[85.4,86.1,85.8,86.7,85.1],
    shap:{ labels:["Contract M-t-M","Tenure","OnlineSecurity_No","Fiber Optic","PayMethod ECheck"], values:[1.35,1.20,0.78,0.70,0.62] }
  }
};

let cvChart=null, shapChart=null, compareChart=null, radarChart=null;
let currentModel = "logistic";

function switchModel(model) {
  currentModel = model;
  const isCombined = model === "combined";
  const color  = isCombined ? "#f472b6" : MODELS[model].color;
  const glow   = isCombined ? "rgba(244,114,182,0.3)" : MODELS[model].glow;

  // CSS variable update
  document.documentElement.style.setProperty("--active", color);
  document.documentElement.style.setProperty("--active-g", glow);

  // Tab styling
  document.querySelectorAll(".tab").forEach(t => {
    const isActive = t.dataset.model === model;
    t.classList.toggle("active", isActive);
    t.style.border    = isActive ? `1.5px solid ${color}` : "1.5px solid rgba(255,255,255,0.08)";
    t.style.background= isActive ? (isCombined ? "rgba(244,114,182,0.08)" : MODELS[model]?.bg) : "rgba(15,20,35,0.6)";
    t.style.color     = isActive ? color : "#64748b";
    t.style.boxShadow = isActive ? `0 0 18px ${glow}` : "none";
  });

  // Pulse + badge
  document.getElementById("pulse-dot").style.background   = color;
  document.getElementById("pulse-dot").style.boxShadow    = `0 0 8px ${color}`;
  document.getElementById("dev-name").style.color         = color;
  document.getElementById("footer-name").style.color      = color;

  // Show/hide views
  document.getElementById("single-view").classList.toggle("hidden", isCombined);
  document.getElementById("combined-view").classList.toggle("hidden", !isCombined);

  // Recs border
  document.getElementById("recs-panel").style.borderColor = color + "30";
  [1,2,3,4,5,6].forEach(i => document.getElementById(`rc${i}-t`).style.color = color);

  if (isCombined) { renderCombined(); return; }

  const m = MODELS[model];

  // Verdict
  document.getElementById("v-emoji").textContent   = m.emoji;
  document.getElementById("v-name").textContent    = m.label;
  document.getElementById("v-name").style.color    = color;
  document.getElementById("v-desc").textContent    = m.desc;
  document.getElementById("v-insight").textContent = m.insight;
  document.getElementById("v-insight").style.color = color;
  document.getElementById("verdict-card").style.borderColor = color + "40";
  document.getElementById("v-chip").style.background = m.bg;
  document.getElementById("v-chip").style.border = `1px solid ${color}40`;

  // Metrics
  renderMetrics(model);

  // Charts
  renderCVChart(model);
  renderSHAPChart(model);
}

function renderMetrics(model) {
  const m = MODELS[model];
  const grid = document.getElementById("metrics-grid");
  grid.innerHTML = "";
  Object.entries(m.metrics).forEach(([label, val], i) => {
    const pct = Math.round(val * 100);
    const card = document.createElement("div");
    card.className = "metric-card";
    card.style.border = `1px solid ${m.color}30`;
    card.style.boxShadow = `0 0 18px ${m.glow}`;
    card.style.animationDelay = `${i*80}ms`;
    card.innerHTML = `
      <div style="position:absolute;top:0;left:0;right:0;height:3px;background:${m.color};border-radius:16px 16px 0 0;"></div>
      <div class="label">${label}</div>
      <div class="value" style="color:${m.color};">${val.toFixed(4)}</div>
      <div class="bar-track"><div class="bar-fill" style="width:${pct}%;background:linear-gradient(90deg,${m.color}80,${m.color});"></div></div>
    `;
    grid.appendChild(card);
  });
}

function renderCVChart(model) {
  if (cvChart) { cvChart.destroy(); cvChart = null; }
  const m = MODELS[model];
  const ctx = document.getElementById("cv-chart").getContext("2d");
  const mean = (m.cv.reduce((a,b)=>a+b,0)/m.cv.length).toFixed(2);
  const std  = Math.sqrt(m.cv.reduce((s,v)=>s+Math.pow(v-mean,2),0)/m.cv.length).toFixed(3);
  document.getElementById("cv-stats").textContent = `Mean CV F1: ${mean}%  |  Std: ±${std}%`;
  cvChart = new Chart(ctx, {
    type:"line",
    data:{ labels:["Fold 1","Fold 2","Fold 3","Fold 4","Fold 5"], datasets:[{ label:"F1 Score", data:m.cv, borderColor:m.color, backgroundColor:m.glow, borderWidth:2.5, pointBackgroundColor:m.color, pointRadius:5, tension:.35, fill:true }] },
    options:{ responsive:true, plugins:{ legend:{ display:false } }, scales:{ y:{ min:75, max:90, ticks:{ color:"#64748b", callback:v=>v+"%" }, grid:{ color:"rgba(255,255,255,0.05)" } }, x:{ ticks:{ color:"#64748b" }, grid:{ color:"rgba(255,255,255,0.04)" } } } }
  });
}

function renderSHAPChart(model) {
  if (shapChart) { shapChart.destroy(); shapChart = null; }
  const m = MODELS[model];
  const ctx = document.getElementById("shap-chart").getContext("2d");
  shapChart = new Chart(ctx, {
    type:"bar",
    data:{ labels:m.shap.labels, datasets:[{ label:"Mean |SHAP|", data:m.shap.values, backgroundColor:m.color+"cc", borderColor:m.color, borderWidth:1, borderRadius:5 }] },
    options:{ indexAxis:"y", responsive:true, plugins:{ legend:{ display:false } }, scales:{ x:{ ticks:{ color:"#64748b" }, grid:{ color:"rgba(255,255,255,0.05)" } }, y:{ ticks:{ color:"#94a3b8", font:{ size:11 } }, grid:{ display:false } } } }
  });
}

function renderCombined() {
  // Bar chart
  if (compareChart) { compareChart.destroy(); compareChart=null; }
  const metrics = ["Accuracy","Precision","Recall","F1 Score","ROC-AUC"];
  const mkeys   = Object.keys(MODELS);
  const colors  = mkeys.map(k => MODELS[k].color);
  const datasets = mkeys.map((key,i) => ({
    label: MODELS[key].label,
    data: metrics.map(met => {
      const v = met==="F1 Score" ? MODELS[key].metrics["F1 Score"] : met==="ROC-AUC" ? MODELS[key].metrics["ROC-AUC"] : MODELS[key].metrics[met];
      return +(v*100).toFixed(1);
    }),
    backgroundColor: colors[i]+"cc", borderColor: colors[i], borderWidth:1, borderRadius:4
  }));
  const cctx = document.getElementById("compare-chart").getContext("2d");
  compareChart = new Chart(cctx, {
    type:"bar",
    data:{ labels:metrics, datasets },
    options:{ responsive:true, plugins:{ legend:{ labels:{ color:"#94a3b8", font:{size:11} } } }, scales:{ y:{ min:40, max:90, ticks:{ color:"#64748b", callback:v=>v+"%" }, grid:{ color:"rgba(255,255,255,0.05)" } }, x:{ ticks:{ color:"#94a3b8" }, grid:{ display:false } } } }
  });

  // Radar chart
  if (radarChart) { radarChart.destroy(); radarChart=null; }
  const rdata = mkeys.map(key => ({
    label: MODELS[key].label,
    data: metrics.map(met => {
      const v = met==="F1 Score" ? MODELS[key].metrics["F1 Score"] : met==="ROC-AUC" ? MODELS[key].metrics["ROC-AUC"] : MODELS[key].metrics[met];
      return +(v*100).toFixed(1);
    }),
    borderColor: MODELS[key].color, backgroundColor: MODELS[key].color+"22", borderWidth:2, pointBackgroundColor: MODELS[key].color
  }));
  const rctx = document.getElementById("radar-chart").getContext("2d");
  radarChart = new Chart(rctx, {
    type:"radar",
    data:{ labels:metrics, datasets:rdata },
    options:{ responsive:true, plugins:{ legend:{ labels:{ color:"#94a3b8", font:{size:11} } } }, scales:{ r:{ min:40, max:90, ticks:{ color:"#64748b", backdropColor:"transparent", font:{size:9} }, grid:{ color:"rgba(255,255,255,0.08)" }, pointLabels:{ color:"#94a3b8", font:{size:11} } } } }
  });

  // Verdict list
  const vl = document.getElementById("verdict-list");
  vl.innerHTML = Object.entries(MODELS).map(([key,m])=>`
    <div class="vlist-item">
      <div class="vlist-icon">${m.emoji}</div>
      <div style="flex:1">
        <div class="vlist-name" style="color:${m.color}">${m.label}</div>
        <div class="vlist-desc">${m.insight}</div>
      </div>
      <div class="vlist-recall">
        <div class="rl">Recall</div>
        <div class="rv" style="color:${m.color}">${(m.metrics.Recall*100).toFixed(1)}%</div>
      </div>
    </div>
  `).join("");
}

// ── Particle network ────────────────────────────────────────────────────────
(function initParticles(){
  const c  = document.getElementById("particles");
  const cx = c.getContext("2d");
  function resize(){ c.width=window.innerWidth; c.height=window.innerHeight; }
  resize(); window.addEventListener("resize", resize);
  const pts = Array.from({length:50},()=>({ x:Math.random()*c.width, y:Math.random()*c.height, vx:(Math.random()-.5)*.4, vy:(Math.random()-.5)*.4, r:Math.random()*2+1 }));
  function draw(){
    cx.clearRect(0,0,c.width,c.height);
    const col = getComputedStyle(document.documentElement).getPropertyValue("--active").trim() || "#38bdf8";
    pts.forEach(p=>{
      p.x+=p.vx; p.y+=p.vy;
      if(p.x<0||p.x>c.width) p.vx*=-1;
      if(p.y<0||p.y>c.height) p.vy*=-1;
      cx.beginPath(); cx.arc(p.x,p.y,p.r,0,Math.PI*2);
      cx.fillStyle=col+"55"; cx.fill();
    });
    pts.forEach((a,i)=>pts.slice(i+1).forEach(b=>{
      const d=Math.hypot(a.x-b.x,a.y-b.y);
      if(d<90){ cx.beginPath(); cx.moveTo(a.x,a.y); cx.lineTo(b.x,b.y); cx.strokeStyle=col+Math.floor((1-d/90)*35).toString(16).padStart(2,"0"); cx.lineWidth=.5; cx.stroke(); }
    }));
    requestAnimationFrame(draw);
  }
  draw();
})();

// ── Boot ────────────────────────────────────────────────────────────────────
switchModel("logistic");
</script>
</body>
</html>
"""

components.html(dashboard_html, height=1800, scrolling=True)
