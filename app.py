"""
Kernel-Level Intrusion Detection System (KIDS)
A simulated real-time security monitoring dashboard built with Streamlit.
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from datetime import datetime, timedelta
from collections import deque
import json

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="KIDS — Kernel Intrusion Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;600;700&display=swap');

/* ── Root variables ── */
:root {
    --bg-primary:    #080d14;
    --bg-secondary:  #0d1520;
    --bg-card:       #0f1c2d;
    --bg-card2:      #0a1526;
    --accent-green:  #00ff88;
    --accent-cyan:   #00d4ff;
    --accent-red:    #ff3355;
    --accent-yellow: #ffcc00;
    --accent-orange: #ff6a00;
    --text-primary:  #e2eaf5;
    --text-muted:    #5a7a9a;
    --border:        #1a3050;
    --glow-green:    0 0 12px rgba(0,255,136,0.4);
    --glow-red:      0 0 12px rgba(255,51,85,0.5);
    --glow-cyan:     0 0 12px rgba(0,212,255,0.4);
}

/* ── Global base ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Exo 2', sans-serif !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060c14 0%, #0a1220 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ── Headings ── */
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 2px !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 16px !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1.8rem !important;
}

/* ── Charts background ── */
[data-testid="stArrowVegaLiteChart"], .stPlotlyChart,
[data-testid="stArrowAltairChart"] {
    background: var(--bg-card) !important;
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
    padding: 8px !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--accent-cyan) !important;
    color: var(--accent-cyan) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    border-radius: 4px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: rgba(0,212,255,0.1) !important;
    box-shadow: var(--glow-cyan) !important;
}

/* ── Toggle / checkbox ── */
.stToggle label, .stCheckbox label { color: var(--text-primary) !important; }

/* ── Select box ── */
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
}

/* ── Alert boxes ── */
.alert-critical {
    background: rgba(255,51,85,0.12);
    border-left: 4px solid var(--accent-red);
    border-radius: 4px;
    padding: 10px 16px;
    margin: 6px 0;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.82rem;
    color: #ffb3c0;
}
.alert-warning {
    background: rgba(255,204,0,0.10);
    border-left: 4px solid var(--accent-yellow);
    border-radius: 4px;
    padding: 10px 16px;
    margin: 6px 0;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.82rem;
    color: #ffe680;
}
.alert-info {
    background: rgba(0,212,255,0.08);
    border-left: 4px solid var(--accent-cyan);
    border-radius: 4px;
    padding: 10px 16px;
    margin: 6px 0;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.82rem;
    color: #99eaff;
}

/* ── Status badge ── */
.badge-online {
    display: inline-block;
    background: rgba(0,255,136,0.15);
    border: 1px solid var(--accent-green);
    color: var(--accent-green);
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    padding: 2px 10px;
    border-radius: 20px;
    letter-spacing: 2px;
    animation: pulse-green 2s infinite;
}
.badge-attack {
    display: inline-block;
    background: rgba(255,51,85,0.2);
    border: 1px solid var(--accent-red);
    color: var(--accent-red);
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    padding: 2px 10px;
    border-radius: 20px;
    letter-spacing: 2px;
    animation: pulse-red 1s infinite;
}
@keyframes pulse-green {
    0%,100% { box-shadow: 0 0 4px rgba(0,255,136,0.3); }
    50%      { box-shadow: 0 0 12px rgba(0,255,136,0.7); }
}
@keyframes pulse-red {
    0%,100% { box-shadow: 0 0 4px rgba(255,51,85,0.4); }
    50%      { box-shadow: 0 0 16px rgba(255,51,85,0.9); }
}

/* ── Section header bar ── */
.section-header {
    background: linear-gradient(90deg, rgba(0,212,255,0.1) 0%, transparent 100%);
    border-left: 3px solid var(--accent-cyan);
    padding: 8px 16px;
    margin-bottom: 20px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: 3px;
    color: var(--accent-cyan);
}

/* ── Mono text ── */
.mono { font-family: 'Share Tech Mono', monospace; }

/* ── Progress bar override ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-green)) !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# ─── Imports for ML & data ────────────────────────────────────────────────────
from sklearn.ensemble import IsolationForest
import io

# ─── Session State Initialization ────────────────────────────────────────────
def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "attack_mode":    False,
        "monitoring":     True,
        "alert_log":      [],
        "cpu_history":    deque(maxlen=60),
        "mem_history":    deque(maxlen=60),
        "net_history":    deque(maxlen=60),
        "disk_history":   deque(maxlen=60),
        "time_history":   deque(maxlen=60),
        "anomaly_model":  None,
        "tick":           0,
        "total_alerts":   0,
        "critical_count": 0,
        "warning_count":  0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()

# ─── Data Simulation ──────────────────────────────────────────────────────────
PROCESS_NAMES = [
    "systemd", "kworker", "sshd", "nginx", "python3",
    "bash",    "mysqld",  "crond","rsyslog","dockerd",
    "apache2", "perl",    "nc",   "nmap",  "curl",
]

def simulate_system_metrics(attack_mode: bool) -> dict:
    """
    Generate synthetic kernel-level metrics.
    In attack mode, inject abnormal spikes to simulate intrusion.
    """
    now = datetime.now()

    if attack_mode:
        # Simulate a burst attack pattern
        phase = (st.session_state.tick % 20) / 20.0
        spike = abs(np.sin(phase * np.pi)) * 60

        cpu    = min(100, np.random.normal(55, 8)  + spike)
        mem    = min(100, np.random.normal(70, 6)  + spike * 0.6)
        net_rx = np.random.normal(400, 50) + spike * 15
        net_tx = np.random.normal(200, 30) + spike * 10
        disk   = np.random.normal(80, 10)  + spike * 0.4
        proc_count = int(np.random.normal(120, 10) + spike * 0.5)
    else:
        cpu    = max(0, np.random.normal(35, 8))
        mem    = max(0, np.random.normal(55, 5))
        net_rx = max(0, np.random.normal(150, 30))
        net_tx = max(0, np.random.normal(80,  20))
        disk   = max(0, np.random.normal(40,  8))
        proc_count = int(np.random.normal(95, 5))

    # Simulate active processes with CPU/MEM usage
    processes = []
    suspicious_procs = ["nc", "nmap", "perl"] if attack_mode else []
    active_procs = random.sample(PROCESS_NAMES, k=min(8, len(PROCESS_NAMES)))
    if attack_mode and suspicious_procs:
        active_procs[:2] = random.sample(suspicious_procs, k=min(2, len(suspicious_procs)))

    for p in active_procs:
        is_sus = p in ["nc", "nmap", "perl"]
        processes.append({
            "process":    p,
            "pid":        random.randint(1000, 9999),
            "cpu_%":      round(random.uniform(20, 85) if is_sus else random.uniform(0.1, 15), 2),
            "mem_%":      round(random.uniform(5,  30) if is_sus else random.uniform(0.1, 8),  2),
            "status":     "⚠ SUSPICIOUS" if is_sus else "running",
            "user":       "root" if is_sus else random.choice(["www-data","daemon","nobody","ubuntu"]),
        })

    return {
        "timestamp":   now,
        "cpu":         round(float(cpu), 2),
        "memory":      round(float(mem), 2),
        "net_rx":      round(float(net_rx), 2),
        "net_tx":      round(float(net_tx), 2),
        "disk":        round(float(disk), 2),
        "proc_count":  proc_count,
        "processes":   processes,
        "uptime":      f"{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}",
    }

# ─── Anomaly Detection ────────────────────────────────────────────────────────
THRESHOLDS = {
    "cpu":    {"warning": 75,  "critical": 90},
    "memory": {"warning": 80,  "critical": 92},
    "net_rx": {"warning": 500, "critical": 800},
    "disk":   {"warning": 85,  "critical": 95},
}

def get_isolation_forest():
    """Lazy-initialize Isolation Forest trained on normal data."""
    if st.session_state.anomaly_model is None:
        X_train = np.column_stack([
            np.random.normal(35, 8,  500),
            np.random.normal(55, 5,  500),
            np.random.normal(150, 30, 500),
            np.random.normal(40, 8,  500),
        ])
        model = IsolationForest(contamination=0.05, random_state=42)
        model.fit(X_train)
        st.session_state.anomaly_model = model
    return st.session_state.anomaly_model

def detect_anomalies(metrics: dict) -> list:
    """
    Run threshold-based and ML-based anomaly detection.
    Returns a list of alert dicts.
    """
    alerts = []
    ts = metrics["timestamp"].strftime("%H:%M:%S")

    # ── Threshold checks ──
    for key, limits in THRESHOLDS.items():
        val = metrics[key]
        if val >= limits["critical"]:
            alerts.append({
                "time":     ts,
                "level":    "CRITICAL",
                "metric":   key.upper(),
                "value":    val,
                "message":  f"{key.upper()} at {val:.1f}% — critical threshold exceeded!",
                "rule":     "threshold",
            })
        elif val >= limits["warning"]:
            alerts.append({
                "time":     ts,
                "level":    "WARNING",
                "metric":   key.upper(),
                "value":    val,
                "message":  f"{key.upper()} at {val:.1f}% — elevated activity detected.",
                "rule":     "threshold",
            })

    # ── Process-based checks ──
    for proc in metrics["processes"]:
        if proc["status"] == "⚠ SUSPICIOUS":
            alerts.append({
                "time":    ts,
                "level":   "CRITICAL",
                "metric":  "PROCESS",
                "value":   proc["cpu_%"],
                "message": f"Suspicious process '{proc['process']}' (PID {proc['pid']}) running as {proc['user']}!",
                "rule":    "process-watch",
            })

    # ── ML-based Isolation Forest ──
    model = get_isolation_forest()
    X = np.array([[metrics["cpu"], metrics["memory"], metrics["net_rx"], metrics["disk"]]])
    score = model.decision_function(X)[0]
    pred  = model.predict(X)[0]
    if pred == -1:
        alerts.append({
            "time":    ts,
            "level":   "WARNING",
            "metric":  "ML-DETECT",
            "value":   round(score, 4),
            "message": f"Isolation Forest flagged abnormal system behavior (score={score:.4f})",
            "rule":    "ml-isolation-forest",
        })

    return alerts

def log_alerts(alerts: list):
    """Append new alerts to the session log."""
    for a in alerts:
        st.session_state.alert_log.append(a)
        st.session_state.total_alerts += 1
        if a["level"] == "CRITICAL":
            st.session_state.critical_count += 1
        else:
            st.session_state.warning_count += 1
    # Keep last 200 logs
    if len(st.session_state.alert_log) > 200:
        st.session_state.alert_log = st.session_state.alert_log[-200:]

# ─── Helper: history deques → DataFrame ──────────────────────────────────────
def history_to_df() -> pd.DataFrame:
    times = list(st.session_state.time_history)
    if not times:
        return pd.DataFrame()
    return pd.DataFrame({
        "Time":    times,
        "CPU %":   list(st.session_state.cpu_history),
        "Mem %":   list(st.session_state.mem_history),
        "Net RX":  list(st.session_state.net_history),
        "Disk %":  list(st.session_state.disk_history),
    })

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 8px'>
        <div style='font-family:Rajdhani,sans-serif; font-size:1.8rem; font-weight:700;
                    letter-spacing:4px; color:#00d4ff;'>
            🛡️ KIDS
        </div>
        <div style='font-family:Share Tech Mono,monospace; font-size:0.65rem;
                    color:#5a7a9a; letter-spacing:2px; margin-top:4px;'>
            KERNEL INTRUSION DETECTION
        </div>
    </div>
    <hr style='border-color:#1a3050; margin:8px 0 16px;'>
    """, unsafe_allow_html=True)

    page = st.selectbox(
        "NAVIGATION",
        ["🏠  Home", "📡  Real-Time Monitoring", "🚨  Alerts & Logs",
         "📊  System Metrics", "ℹ️  About Project"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#1a3050; margin:16px 0;'>", unsafe_allow_html=True)

    # ── Attack Mode toggle ──
    attack_mode = st.toggle("⚡ Attack Simulation Mode",
                            value=st.session_state.attack_mode)
    st.session_state.attack_mode = attack_mode

    if attack_mode:
        st.markdown('<div class="badge-attack">⚠ ATTACK ACTIVE</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="badge-online">● NORMAL</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Refresh control ──
    auto_refresh = st.toggle("Auto Refresh (3s)", value=True)
    if st.button("🔄  Manual Refresh"):
        st.rerun()

    st.markdown("<hr style='border-color:#1a3050; margin:16px 0;'>", unsafe_allow_html=True)

    # ── Quick stats ──
    st.markdown("""
    <div style='font-family:Rajdhani,sans-serif; font-size:0.75rem;
                letter-spacing:2px; color:#5a7a9a; margin-bottom:10px;'>
        SESSION STATS
    </div>
    """, unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    col_a.metric("Alerts",   st.session_state.total_alerts)
    col_b.metric("Critical", st.session_state.critical_count)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️  Clear Logs"):
        st.session_state.alert_log      = []
        st.session_state.total_alerts   = 0
        st.session_state.critical_count = 0
        st.session_state.warning_count  = 0
        st.rerun()

# ─── Fetch & store metrics every tick ─────────────────────────────────────────
metrics = simulate_system_metrics(st.session_state.attack_mode)
st.session_state.cpu_history.append(metrics["cpu"])
st.session_state.mem_history.append(metrics["memory"])
st.session_state.net_history.append(metrics["net_rx"])
st.session_state.disk_history.append(metrics["disk"])
st.session_state.time_history.append(metrics["timestamp"].strftime("%H:%M:%S"))
st.session_state.tick += 1

# Detect & log anomalies
new_alerts = detect_anomalies(metrics)
if new_alerts:
    log_alerts(new_alerts)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════════════════════════
if "Home" in page:
    st.markdown("""
    <div style='padding:32px 0 24px; text-align:center;'>
        <div style='font-family:Rajdhani,sans-serif; font-size:3rem; font-weight:700;
                    letter-spacing:6px; color:#00d4ff; text-shadow: 0 0 30px rgba(0,212,255,0.5);'>
            KIDS
        </div>
        <div style='font-family:Share Tech Mono,monospace; font-size:0.9rem;
                    color:#5a7a9a; letter-spacing:3px; margin-top:8px;'>
            KERNEL-LEVEL INTRUSION DETECTION SYSTEM
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Mode banner ──
    if st.session_state.attack_mode:
        st.markdown("""
        <div style='background:rgba(255,51,85,0.15); border:1px solid #ff3355;
                    border-radius:6px; padding:14px 20px; text-align:center;
                    font-family:Share Tech Mono,monospace; color:#ff3355;
                    font-size:0.9rem; letter-spacing:2px; animation:pulse-red 1s infinite;'>
            ⚠  ATTACK SIMULATION MODE ACTIVE — ANOMALOUS TRAFFIC BEING GENERATED  ⚠
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background:rgba(0,255,136,0.08); border:1px solid #00ff88;
                    border-radius:6px; padding:14px 20px; text-align:center;
                    font-family:Share Tech Mono,monospace; color:#00ff88;
                    font-size:0.9rem; letter-spacing:2px;'>
            ● SYSTEM NORMAL — ALL MONITORS ACTIVE
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Live quick metrics ──
    c1, c2, c3, c4, c5 = st.columns(5)
    cpu_delta = round(metrics["cpu"] - 35, 1)
    c1.metric("CPU Usage",     f"{metrics['cpu']:.1f}%",    f"{cpu_delta:+.1f}%")
    c2.metric("Memory",        f"{metrics['memory']:.1f}%", None)
    c3.metric("Net RX (KB/s)", f"{metrics['net_rx']:.0f}",  None)
    c4.metric("Disk I/O",      f"{metrics['disk']:.1f}%",   None)
    c5.metric("Processes",     metrics["proc_count"],        None)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Overview cards ──
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background:#0f1c2d; border:1px solid #1a3050; border-radius:8px; padding:20px;'>
            <div style='font-family:Rajdhani,sans-serif; font-size:1.1rem; font-weight:700;
                        color:#00d4ff; letter-spacing:2px; margin-bottom:10px;'>
                🔍 WHAT IS KIDS?
            </div>
            <div style='font-family:Exo 2,sans-serif; font-size:0.85rem; color:#8aaccc; line-height:1.7;'>
                KIDS simulates a kernel-level IDS that monitors system calls,
                resource usage, and process behaviour to detect intrusions,
                privilege escalation, and anomalous activity in real time.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background:#0f1c2d; border:1px solid #1a3050; border-radius:8px; padding:20px;'>
            <div style='font-family:Rajdhani,sans-serif; font-size:1.1rem; font-weight:700;
                        color:#00ff88; letter-spacing:2px; margin-bottom:10px;'>
                ⚙️ DETECTION METHODS
            </div>
            <ul style='font-family:Exo 2,sans-serif; font-size:0.85rem; color:#8aaccc;
                       line-height:1.8; padding-left:18px; margin:0;'>
                <li>Threshold-based rules</li>
                <li>ML — Isolation Forest</li>
                <li>Suspicious process watch</li>
                <li>Network traffic analysis</li>
                <li>Disk anomaly detection</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background:#0f1c2d; border:1px solid #1a3050; border-radius:8px; padding:20px;'>
            <div style='font-family:Rajdhani,sans-serif; font-size:1.1rem; font-weight:700;
                        color:#ffcc00; letter-spacing:2px; margin-bottom:10px;'>
                📋 TECH STACK
            </div>
            <ul style='font-family:Share Tech Mono,monospace; font-size:0.78rem; color:#8aaccc;
                       line-height:1.9; padding-left:18px; margin:0;'>
                <li>Python 3.x + Streamlit</li>
                <li>scikit-learn (IsoForest)</li>
                <li>Pandas / NumPy</li>
                <li>Plotly / Altair</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Architecture diagram (text-based) ──
    st.markdown('<div class="section-header">SYSTEM ARCHITECTURE</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#0a1526; border:1px solid #1a3050; border-radius:8px; padding:20px;
                font-family:Share Tech Mono,monospace; font-size:0.78rem; color:#5a7a9a; line-height:2;'>
    <span style='color:#00d4ff;'>[ KERNEL LAYER ]</span>  →  CPU · MEM · DISK · NET · SYSCALL  →  <span style='color:#00ff88;'>[ DATA COLLECTOR ]</span>
    <br>
    <span style='color:#00ff88;'>[ DATA COLLECTOR ]</span>  →  Normalise · Timestamp · Enrich  →  <span style='color:#ffcc00;'>[ ANOMALY ENGINE ]</span>
    <br>
    <span style='color:#ffcc00;'>[ ANOMALY ENGINE ]</span>  →  Threshold Rules + Isolation Forest  →  <span style='color:#ff3355;'>[ ALERT MANAGER ]</span>
    <br>
    <span style='color:#ff3355;'>[ ALERT MANAGER ]</span>  →  Log · Notify · Visualise  →  <span style='color:#00d4ff;'>[ DASHBOARD UI ]</span>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: REAL-TIME MONITORING
# ═══════════════════════════════════════════════════════════════════════════════
elif "Real-Time" in page:
    st.markdown('<div class="section-header">REAL-TIME KERNEL MONITOR</div>', unsafe_allow_html=True)

    mode_col, ts_col = st.columns([2, 3])
    with mode_col:
        badge = "badge-attack" if st.session_state.attack_mode else "badge-online"
        label = "⚠ ATTACK MODE" if st.session_state.attack_mode else "● NORMAL"
        st.markdown(f'<span class="{badge}">{label}</span>', unsafe_allow_html=True)
    with ts_col:
        st.markdown(f'<span class="mono" style="color:#5a7a9a; font-size:0.8rem;">'
                    f'LAST UPDATE: {metrics["timestamp"].strftime("%Y-%m-%d %H:%M:%S")}'
                    f' | UPTIME: {metrics["uptime"]}</span>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Live metrics ──
    c1, c2, c3, c4 = st.columns(4)
    def color_val(v, warn, crit):
        if v >= crit:   return "🔴"
        elif v >= warn: return "🟡"
        else:           return "🟢"

    c1.metric(f"{color_val(metrics['cpu'],75,90)} CPU",     f"{metrics['cpu']:.1f}%")
    c2.metric(f"{color_val(metrics['memory'],80,92)} MEM",  f"{metrics['memory']:.1f}%")
    c3.metric(f"{color_val(metrics['net_rx'],500,800)} NET RX", f"{metrics['net_rx']:.0f} KB/s")
    c4.metric(f"{color_val(metrics['disk'],85,95)} DISK",   f"{metrics['disk']:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── History charts ──
    df = history_to_df()
    if not df.empty:
        df_indexed = df.set_index("Time")

        st.markdown("**CPU & Memory Usage (last 60s)**")
        st.line_chart(df_indexed[["CPU %", "Mem %"]], height=200, use_container_width=True)

        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown("**Network RX (KB/s)**")
            st.line_chart(df_indexed[["Net RX"]], height=180, use_container_width=True)
        with col_r:
            st.markdown("**Disk I/O (%)**")
            st.line_chart(df_indexed[["Disk %"]], height=180, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Process table ──
    st.markdown('<div class="section-header">PROCESS MONITOR</div>', unsafe_allow_html=True)
    proc_df = pd.DataFrame(metrics["processes"])
    st.dataframe(
        proc_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "cpu_%": st.column_config.ProgressColumn("CPU %",  min_value=0, max_value=100),
            "mem_%": st.column_config.ProgressColumn("MEM %",  min_value=0, max_value=100),
        }
    )

    # ── Bar chart of process CPU ──
    st.markdown("**Process CPU Usage**")
    proc_chart = pd.DataFrame({
        "Process": [p["process"] for p in metrics["processes"]],
        "CPU %":   [p["cpu_%"]   for p in metrics["processes"]],
    }).set_index("Process")
    st.bar_chart(proc_chart, height=200, use_container_width=True)

    # ── Latest alerts from this tick ──
    if new_alerts:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">ANOMALIES DETECTED THIS TICK</div>',
                    unsafe_allow_html=True)
        for a in new_alerts:
            cls = "alert-critical" if a["level"] == "CRITICAL" else "alert-warning"
            st.markdown(
                f'<div class="{cls}">'
                f'[{a["time"]}] [{a["level"]}] [{a["rule"].upper()}]  {a["message"]}'
                f'</div>',
                unsafe_allow_html=True,
            )

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ALERTS & LOGS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Alerts" in page:
    st.markdown('<div class="section-header">ALERTS & INTRUSION LOG</div>',
                unsafe_allow_html=True)

    # ── Summary metrics ──
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Alerts",    st.session_state.total_alerts)
    c2.metric("Critical Alerts", st.session_state.critical_count)
    c3.metric("Warnings",        st.session_state.warning_count)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Filter controls ──
    fc1, fc2 = st.columns(2)
    with fc1:
        level_filter = st.selectbox("Filter by Level",
                                    ["ALL", "CRITICAL", "WARNING", "INFO"])
    with fc2:
        rule_filter = st.selectbox("Filter by Rule",
                                   ["ALL", "threshold", "process-watch",
                                    "ml-isolation-forest"])

    # ── Log display ──
    log = list(reversed(st.session_state.alert_log))  # newest first
    if level_filter != "ALL":
        log = [a for a in log if a["level"] == level_filter]
    if rule_filter != "ALL":
        log = [a for a in log if a["rule"] == rule_filter]

    if not log:
        st.markdown("""
        <div class="alert-info">
            No alerts match the current filter. System appears normal.
        </div>
        """, unsafe_allow_html=True)
    else:
        # Scrollable alert list (last 50 shown)
        for a in log[:50]:
            cls = "alert-critical" if a["level"] == "CRITICAL" else "alert-warning"
            st.markdown(
                f'<div class="{cls}">'
                f'<span style="opacity:0.6">[{a["time"]}]</span>  '
                f'<b>[{a["level"]}]</b>  '
                f'<span style="opacity:0.7">[{a["rule"].upper()}]</span>  '
                f'{a["message"]}'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Download CSV ──
    if st.session_state.alert_log:
        log_df = pd.DataFrame(st.session_state.alert_log)
        csv = log_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇  Download Full Log as CSV",
            data=csv,
            file_name=f"kids_alert_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SYSTEM METRICS
# ═══════════════════════════════════════════════════════════════════════════════
elif "System Metrics" in page:
    st.markdown('<div class="section-header">SYSTEM METRICS DASHBOARD</div>',
                unsafe_allow_html=True)

    # ── Current snapshot ──
    st.markdown("#### Current Snapshot")
    snap_data = {
        "Metric":    ["CPU Usage", "Memory", "Net RX", "Net TX", "Disk I/O", "Processes"],
        "Value":     [f"{metrics['cpu']:.1f}%", f"{metrics['memory']:.1f}%",
                      f"{metrics['net_rx']:.1f} KB/s", f"{metrics['net_tx']:.1f} KB/s",
                      f"{metrics['disk']:.1f}%", str(metrics['proc_count'])],
        "Status":    [
            "🔴 CRITICAL" if metrics["cpu"]    >= 90 else ("🟡 WARNING" if metrics["cpu"]    >= 75 else "🟢 OK"),
            "🔴 CRITICAL" if metrics["memory"] >= 92 else ("🟡 WARNING" if metrics["memory"] >= 80 else "🟢 OK"),
            "🔴 CRITICAL" if metrics["net_rx"] >= 800 else ("🟡 WARNING" if metrics["net_rx"] >= 500 else "🟢 OK"),
            "🟢 OK",
            "🔴 CRITICAL" if metrics["disk"]   >= 95 else ("🟡 WARNING" if metrics["disk"]   >= 85 else "🟢 OK"),
            "🟢 OK",
        ],
    }
    st.dataframe(pd.DataFrame(snap_data), use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Historical trend ──
    df = history_to_df()
    if not df.empty:
        df_indexed = df.set_index("Time")
        st.markdown("#### All Metrics Trend (60s window)")
        st.line_chart(df_indexed[["CPU %", "Mem %", "Disk %"]], height=250)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Summary Statistics")
            summary = df[["CPU %", "Mem %", "Net RX", "Disk %"]].describe().round(2)
            st.dataframe(summary, use_container_width=True)
        with col2:
            st.markdown("#### Alert Distribution")
            if st.session_state.alert_log:
                alert_df = pd.DataFrame(st.session_state.alert_log)
                dist = alert_df["level"].value_counts().reset_index()
                dist.columns = ["Level", "Count"]
                st.bar_chart(dist.set_index("Level"), height=200)
            else:
                st.info("No alerts logged yet.")

    # ── Thresholds reference ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">DETECTION THRESHOLDS</div>',
                unsafe_allow_html=True)
    thr_data = []
    for metric, limits in THRESHOLDS.items():
        thr_data.append({
            "Metric":          metric.upper(),
            "Warning Level":   f"{limits['warning']}%  (or KB/s)",
            "Critical Level":  f"{limits['critical']}%  (or KB/s)",
            "Current Value":   metrics[metric],
        })
    st.dataframe(pd.DataFrame(thr_data), use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ABOUT
# ═══════════════════════════════════════════════════════════════════════════════
elif "About" in page:
    st.markdown('<div class="section-header">ABOUT THIS PROJECT</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#0f1c2d; border:1px solid #1a3050; border-radius:8px;
                padding:30px; font-family:Exo 2,sans-serif; color:#8aaccc; line-height:1.8;'>

    <h3 style='font-family:Rajdhani,sans-serif; color:#00d4ff; letter-spacing:3px;'>
        Project Overview
    </h3>
    <p>
        <b style='color:#e2eaf5;'>Kernel-Level Intrusion Detection System (KIDS)</b> is a
        cybersecurity monitoring project that simulates real-time detection of system
        intrusions, abnormal behaviour, and potential attacks at the kernel level.
    </p>
    <p>
        While actual kernel-level access requires OS-level privileges and kernel modules
        (like eBPF or loadable kernel modules), this project <b style='color:#00ff88;'>
        realistically simulates</b> the same data that a real KIDS would collect and analyse.
    </p>

    <h3 style='font-family:Rajdhani,sans-serif; color:#00d4ff; letter-spacing:3px; margin-top:24px;'>
        Detection Techniques
    </h3>
    <ul>
        <li><b style='color:#ffcc00;'>Threshold-Based Detection:</b>
            Rule-based checks on CPU, Memory, Disk, and Network metrics
            against pre-defined warning and critical thresholds.</li>
        <li style='margin-top:8px;'><b style='color:#ffcc00;'>Isolation Forest (ML):</b>
            Unsupervised ML model trained on normal behaviour; flags statistical
            outliers in real time with contamination factor of 5%.</li>
        <li style='margin-top:8px;'><b style='color:#ffcc00;'>Process Watchlist:</b>
            Monitors for suspicious processes (netcat, nmap, perl etc.) often used
            in post-exploitation or lateral movement.</li>
    </ul>

    <h3 style='font-family:Rajdhani,sans-serif; color:#00d4ff; letter-spacing:3px; margin-top:24px;'>
        Attack Simulation Mode
    </h3>
    <p>
        Toggle <b style='color:#ff3355;'>Attack Simulation Mode</b> in the sidebar to
        inject synthetic attack traffic — CPU spikes, network floods, and suspicious
        processes — mimicking real intrusion scenarios like:
    </p>
    <ul>
        <li>DDoS / resource exhaustion attacks</li>
        <li>Port scanning (nmap)</li>
        <li>Reverse shell persistence (nc / netcat)</li>
        <li>Cryptominer hijacking (high CPU)</li>
    </ul>

    <h3 style='font-family:Rajdhani,sans-serif; color:#00d4ff; letter-spacing:3px; margin-top:24px;'>
        Technologies Used
    </h3>
    <table style='width:100%; border-collapse:collapse; font-family:Share Tech Mono,monospace;
                  font-size:0.8rem;'>
        <tr style='border-bottom:1px solid #1a3050;'>
            <td style='padding:8px; color:#5a7a9a;'>FRONTEND</td>
            <td style='padding:8px; color:#e2eaf5;'>Streamlit 1.x</td>
        </tr>
        <tr style='border-bottom:1px solid #1a3050;'>
            <td style='padding:8px; color:#5a7a9a;'>ML ENGINE</td>
            <td style='padding:8px; color:#e2eaf5;'>scikit-learn — IsolationForest</td>
        </tr>
        <tr style='border-bottom:1px solid #1a3050;'>
            <td style='padding:8px; color:#5a7a9a;'>DATA</td>
            <td style='padding:8px; color:#e2eaf5;'>Pandas, NumPy</td>
        </tr>
        <tr>
            <td style='padding:8px; color:#5a7a9a;'>LANGUAGE</td>
            <td style='padding:8px; color:#e2eaf5;'>Python 3.9+</td>
        </tr>
    </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; font-family:Share Tech Mono,monospace;
                font-size:0.7rem; color:#1a3050; letter-spacing:2px;'>
        KIDS v1.0.0  ·  KERNEL INTRUSION DETECTION SYSTEM  ·  COLLEGE PROJECT
    </div>
    """, unsafe_allow_html=True)

# ─── Auto-refresh ─────────────────────────────────────────────────────────────
if auto_refresh:
    time.sleep(3)
    st.rerun()
