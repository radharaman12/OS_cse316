"""
Kernel-Level Intrusion Detection System (KIDS)
A top 0.1% SaaS-level simulated real-time security monitoring dashboard.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go

# ─── Modular Imports ─────────────────────────────────────────────────────────
from utils.state import init_session_state, clear_logs, history_to_df
from core.telemetry import simulate_system_metrics
from core.ml_engine import detect_anomalies, log_alerts
from ui.components import inject_css, premium_metric, create_premium_area_chart, create_gauge_chart

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="KIDS | Advanced Threat Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Initialize Dependencies ─────────────────────────────────────────────────
init_session_state()
inject_css("ui/style.css")

# ─── Non-blocking Auto-Refresh ───────────────────────────────────────────────
# Install streamlit-autorefresh if needed; otherwise fall back gracefully
try:
    from streamlit_autorefresh import st_autorefresh
    _HAS_AUTOREFRESH = True
except ImportError:
    _HAS_AUTOREFRESH = False

# ─── Data Gathering ───────────────────────────────────────────────────────────
metrics = simulate_system_metrics(st.session_state.attack_mode)
st.session_state.cpu_history.append(metrics["cpu"])
st.session_state.mem_history.append(metrics["memory"])
st.session_state.net_history.append(metrics["net_rx"])
st.session_state.disk_history.append(metrics["disk"])
st.session_state.time_history.append(metrics["timestamp"].strftime("%H:%M:%S"))
st.session_state.tick += 1

new_alerts = detect_anomalies(metrics)
if new_alerts:
    log_alerts(new_alerts)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-brand'>KIDS.AI</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; font-family:Fira Code, monospace; font-size:0.7rem; color:#64748b; margin-bottom: 2rem; letter-spacing: 1.5px;'>
        KERNEL THREAT INTELLIGENCE
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["Dashboard", "Real-Time Telemetry", "Threat Intel Logs", "System Analytics", "Architecture"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: rgba(255,255,255,0.04); margin: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Space Grotesk; font-weight:600; margin-bottom:1rem; color:#f1f5f9; font-size:0.9rem; letter-spacing:0.5px;'>Control Center</div>", unsafe_allow_html=True)

    attack_mode = st.toggle("Simulate Cyber Attack", value=st.session_state.attack_mode)
    st.session_state.attack_mode = attack_mode

    auto_refresh = st.toggle("Live Sync (3s)", value=True)
    if st.button("Force Sync Data"):
        st.rerun()

    st.markdown("<hr style='border-color: rgba(255,255,255,0.04); margin: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Space Grotesk; font-weight:600; margin-bottom:1rem; color:#f1f5f9; font-size:0.9rem; letter-spacing:0.5px;'>Session Analytics</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.25); border-radius: 12px; padding: 18px; border: 1px solid rgba(255,255,255,0.04);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color:#94a3b8; font-size:0.85rem;">Total Events</span>
            <span style="color:#38bdf8; font-weight:700; font-family:Space Grotesk;">{st.session_state.total_alerts}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color:#94a3b8; font-size:0.85rem;">Critical Threats</span>
            <span style="color:#fb7185; font-weight:700; font-family:Space Grotesk;">{st.session_state.critical_count}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color:#94a3b8; font-size:0.85rem;">Uptime</span>
            <span style="color:#34d399; font-weight:700; font-family:Space Grotesk;">{metrics["uptime"]}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Purge Logs"):
        clear_logs()
        st.rerun()

# ─── Main Content Area ────────────────────────────────────────────────────────

col_title, col_status = st.columns([1, 1])
with col_title:
    st.markdown(f"<h2 style='margin:0; padding:0;'>{page}</h2>", unsafe_allow_html=True)
with col_status:
    badge_class = "status-attack" if st.session_state.attack_mode else "status-normal"
    badge_text = "⚠️ ATTACK IN PROGRESS" if st.session_state.attack_mode else "✓ SECURE ENVIRONMENT"
    st.markdown(f"""
    <div style='display:flex; justify-content:flex-end; align-items:center; height:100%;'>
        <div class='status-badge {badge_class}'>
            {badge_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
if page == "Dashboard":

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        premium_metric("CPU Core utilization", f"{metrics['cpu']:.1f}%", round(metrics['cpu'] - 35, 1), 0.1, "⚡")
    with m2:
        premium_metric("Memory allocation", f"{metrics['memory']:.1f}%", round(metrics['memory'] - 55, 1), 0.2, "🧠")
    with m3:
        premium_metric("Network Ingress", f"{metrics['net_rx']:.0f} <span style='font-size:1rem'>KB/s</span>", round(metrics['net_rx'] - 150, 0), 0.3, "🌐")
    with m4:
        premium_metric("Active Processes", str(metrics['proc_count']), round(metrics['proc_count'] - 95, 0), 0.4, "⚙️")

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-header'>System Telemetry Trend</div>", unsafe_allow_html=True)
        df_hist = history_to_df()
        if not df_hist.empty:
            fig = create_premium_area_chart(df_hist, ["CPU", "Memory"], "", ["#38bdf8", "#a78bfa"], height=320)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown("<div style='height:200px; display:flex; align-items:center; justify-content:center; color:#64748b;'>Collecting telemetry data…</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        html = "<div class='glass-panel' style='height: 100%;'>"
        html += "<div class='panel-header'>Active Threat Feed</div>"

        if new_alerts:
            for a in new_alerts[:4]:
                cls = "alert-critical" if a["level"] == "CRITICAL" else "alert-warning"
                html += f"""
<div class="alert-box {cls}">
    <div class="alert-icon">{a['icon']}</div>
    <div>
        <div style="font-weight: 700; margin-bottom: 4px;">{a['metric']} ALERT</div>
        <div style="opacity: 0.9; line-height: 1.4;">{a['message']}</div>
    </div>
</div>
"""
        elif st.session_state.alert_log:
            for a in list(reversed(st.session_state.alert_log))[:4]:
                cls = "alert-critical" if a["level"] == "CRITICAL" else "alert-warning"
                html += f"""
<div class="alert-box {cls}">
    <div class="alert-icon">{a['icon']}</div>
    <div>
        <div style="font-weight: 700; margin-bottom: 4px;">{a['metric']} ALERT <span style='font-size:0.7rem; opacity:0.5; font-weight:400;'>{a['time']}</span></div>
        <div style="opacity: 0.9; line-height: 1.4;">{a['message']}</div>
    </div>
</div>
"""
        else:
            html += """
<div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:200px; opacity:0.5;">
    <div style="font-size: 3rem; margin-bottom: 1rem;">🛡️</div>
    <div style="font-family:Space Grotesk; font-weight:600;">No Active Threats</div>
    <div style="font-size:0.85rem; font-family:Inter; color:#64748b;">System operates within normal parameters</div>
</div>
"""

        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: REAL-TIME TELEMETRY
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Real-Time Telemetry":

    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown("<div class='glass-panel' style='padding: 12px;'>", unsafe_allow_html=True)
        fig_cpu = create_gauge_chart(metrics['cpu'], "CPU Saturation", 75, 90, "#38bdf8")
        st.plotly_chart(fig_cpu, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
    with g2:
        st.markdown("<div class='glass-panel' style='padding: 12px;'>", unsafe_allow_html=True)
        fig_mem = create_gauge_chart(metrics['memory'], "Memory Saturation", 80, 92, "#a78bfa")
        st.plotly_chart(fig_mem, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
    with g3:
        st.markdown("<div class='glass-panel' style='padding: 12px;'>", unsafe_allow_html=True)
        fig_disk = create_gauge_chart(metrics['disk'], "Disk I/O Stress", 85, 95, "#34d399")
        st.plotly_chart(fig_disk, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-header'>Network Ingress / Egress Topology</div>", unsafe_allow_html=True)
    df_hist = history_to_df()
    if not df_hist.empty:
        fig_net = go.Figure()
        fig_net.add_trace(go.Bar(
            x=df_hist['Time'], y=df_hist['Net_RX'],
            name='Ingress (KB/s)',
            marker_color='rgba(56, 189, 248, 0.65)',
            marker_line_color='rgba(56, 189, 248, 1)',
            marker_line_width=1
        ))
        fig_net.update_layout(
            barmode='group', height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', zeroline=False),
            font=dict(family="Inter", color="#94a3b8"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_net, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Active Thread Monitor — ONLY on this page ──
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-header'>Active Thread Monitor</div>", unsafe_allow_html=True)
    proc_df = pd.DataFrame(metrics["processes"])

    # Round numeric columns for clean display
    proc_df["CPU (%)"] = proc_df["CPU (%)"].round(2)
    proc_df["Memory (%)"] = proc_df["Memory (%)"].round(2)

    def color_status(val):
        color = '#fb7185' if val == '⚠ SUSPICIOUS' else '#34d399'
        return f'color: {color}; font-weight: bold;'

    styled_df = proc_df.style.map(color_status, subset=['Status'])\
                             .background_gradient(cmap='Blues', subset=['CPU (%)'], vmin=0, vmax=100)\
                             .background_gradient(cmap='Purples', subset=['Memory (%)'], vmin=0, vmax=100)\
                             .format({"CPU (%)": "{:.2f}", "Memory (%)": "{:.2f}"})

    st.dataframe(styled_df, use_container_width=True, hide_index=True, height=320)
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: THREAT INTEL LOGS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Threat Intel Logs":

    f1, f2, f3 = st.columns([1, 1, 2])
    with f1:
        level_filter = st.selectbox("Severity Level", ["ALL", "CRITICAL", "WARNING"])
    with f2:
        rule_filter = st.selectbox("Detection Engine", ["ALL", "Threshold", "Signature", "AI/ML"])

    log = list(reversed(st.session_state.alert_log))
    if level_filter != "ALL": log = [a for a in log if a["level"] == level_filter]
    if rule_filter != "ALL":  log = [a for a in log if a["rule"] == rule_filter]

    html = "<div class='glass-panel' style='min-height: 500px;'>"
    html += "<div class='panel-header'>Security Event Stream</div>"

    if not log:
        html += """
<div class="alert-box alert-info">
    <div class="alert-icon">✓</div>
    <div>No matching security events found in the intelligence stream.</div>
</div>
"""
    else:
        for a in log[:50]:
            cls = "alert-critical" if a["level"] == "CRITICAL" else "alert-warning"
            html += f"""
<div class="alert-box {cls}" style="margin-bottom: 14px;">
    <div class="alert-icon">{a['icon']}</div>
    <div style="flex-grow: 1;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 4px;">
            <span style="font-family:Space Grotesk; font-weight: 700; letter-spacing:1px;">{a['level']} // {a['metric']}</span>
            <span style="opacity: 0.45; font-size: 0.8rem;">{a['time']}</span>
        </div>
        <div style="opacity: 0.9; font-size: 0.92rem;">{a['message']}</div>
        <div style="margin-top: 8px; font-size: 0.75rem; opacity: 0.6; display:flex; gap:16px;">
            <span>Engine: <b style='color:var(--text-main)'>{a['rule']}</b></span>
            <span>Recorded Value: <b style='color:var(--text-main)'>{a['value']}</b></span>
        </div>
    </div>
</div>
"""

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

    if st.session_state.alert_log:
        csv = pd.DataFrame(st.session_state.alert_log).to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Export Threat Data (CSV)", data=csv, file_name=f"kids_intel_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SYSTEM ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "System Analytics":

    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-header'>ML Isolation Forest Confidence Scores</div>", unsafe_allow_html=True)

    np.random.seed(42)
    x = np.random.normal(0, 1, 500)

    fig_ml = go.Figure()
    fig_ml.add_trace(go.Histogram(
        x=x, nbinsx=30,
        marker_color='rgba(167, 139, 250, 0.55)',
        marker_line_color='rgba(167, 139, 250, 1)',
        marker_line_width=1
    ))
    fig_ml.update_layout(
        height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        title=dict(text="Anomaly Score Distribution (Baseline)", font=dict(family="Space Grotesk", color="#f1f5f9")),
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)'),
        font=dict(family="Inter", color="#94a3b8"),
    )
    st.plotly_chart(fig_ml, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<p style='color:#94a3b8; font-size:0.9rem; margin-top:16px; line-height:1.6;'>The AI engine uses an Isolation Forest algorithm. Data points falling in the extreme tails (Contamination=0.05) are flagged as potential intrusions.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-header'>Threshold Rules Matrix</div>", unsafe_allow_html=True)
        thr_df = pd.DataFrame([
            {"Metric": "CPU", "Warning": "75%", "Critical": "90%"},
            {"Metric": "Memory", "Warning": "80%", "Critical": "92%"},
            {"Metric": "Disk I/O", "Warning": "85%", "Critical": "95%"},
            {"Metric": "Network RX", "Warning": "500 KB/s", "Critical": "800 KB/s"},
        ])
        st.dataframe(thr_df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-header'>Incident Distribution</div>", unsafe_allow_html=True)
        if st.session_state.alert_log:
            df_alerts = pd.DataFrame(st.session_state.alert_log)
            dist = df_alerts['rule'].value_counts()

            fig_pie = go.Figure(data=[go.Pie(
                labels=dist.index, values=dist.values, hole=.65,
                marker=dict(colors=['#38bdf8', '#a78bfa', '#fb7185', '#fbbf24']),
                textinfo='percent+label', textfont_family="Inter", textfont_color="#fff"
            )])
            fig_pie.update_layout(
                height=240, margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)', showlegend=False
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown("<div style='height:220px; display:flex; align-items:center; justify-content:center; color:#64748b;'>No incidents recorded to analyze.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Architecture":
    st.markdown("""
<div class="glass-panel" style="padding: 44px;">
<h2 style="color: var(--accent-cyan); font-family: 'Space Grotesk'; font-size: 2.4rem; margin-bottom: 16px; letter-spacing:-1px;">Platform Architecture</h2>
<p style="color: #94a3b8; font-size: 1.05rem; line-height: 1.85; margin-bottom: 44px; max-width: 820px;">
KIDS.AI represents a paradigm shift in simulated kernel-level monitoring. Built on a modular Python architecture and accelerated by machine learning, it processes continuous telemetry streams to identify anomalous execution patterns.
</p>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 28px; margin-bottom: 44px;">
<div class="arch-card">
<div style="font-size: 2rem; margin-bottom: 14px;">🔍</div>
<h3 style="font-size: 1.15rem; color: #fff; margin-bottom: 10px;">Data Aggregation</h3>
<p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.7;">Simulated continuous polling of synthetic kernel parameters including syscall frequency, resource saturation, and process lifecycles.</p>
</div>

<div class="arch-card">
<div style="font-size: 2rem; margin-bottom: 14px;">🧠</div>
<h3 style="font-size: 1.15rem; color: #fff; margin-bottom: 10px;">AI Inference Engine</h3>
<p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.7;">Unsupervised Isolation Forest algorithm identifies multidimensional statistical outliers that bypass standard threshold rules.</p>
</div>

<div class="arch-card">
<div style="font-size: 2rem; margin-bottom: 14px;">⚡</div>
<h3 style="font-size: 1.15rem; color: #fff; margin-bottom: 10px;">Real-Time UI</h3>
<p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.7;">A top 0.1% SaaS-grade frontend delivering zero-latency data visualization via Plotly and high-performance modular Streamlit rendering.</p>
</div>
</div>

<div style="border-top: 1px solid rgba(255,255,255,0.06); padding-top: 28px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
<div style="font-family: 'Fira Code', monospace; color: var(--accent-cyan); font-size: 0.85rem;">
SYSTEM VERSION: 4.0.0-ENTERPRISE (Modular Architecture)
</div>
<div style="color: #64748b; font-size: 0.85rem;">
Built with Streamlit • Scikit-Learn • Plotly
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ─── Auto-Refresh Loop ────────────────────────────────────────────────────────
if auto_refresh:
    if _HAS_AUTOREFRESH:
        st_autorefresh(interval=3000, limit=None, key="kids_autorefresh")
    else:
        import time
        time.sleep(3)
        st.rerun()
