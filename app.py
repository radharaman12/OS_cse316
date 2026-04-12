# ============================================================
#   Real-Time Process Monitoring Dashboard
#   Built with Python · Streamlit · psutil · Plotly · Pandas
# ============================================================

import streamlit as st
import psutil
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


# ──────────────────────────────────────────────
# PAGE CONFIG  (must be the very first st call)
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Process Monitor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# CUSTOM CSS  – dark, industrial, neon-accent UI
# ──────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Syne:wght@400;700;800&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0c10 !important;
    color: #c9d1d9 !important;
}

/* ── Top header bar ── */
.dash-header {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    border-bottom: 1px solid #21262d;
    padding: 1.2rem 2rem;
    margin-bottom: 1.5rem;
    border-radius: 0 0 12px 12px;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.dash-title {
    font-size: 1.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #58a6ff, #3fb950, #f78166);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
    margin: 0;
}
.dash-subtitle {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #6e7681;
    margin: 0;
}

/* ── Metric cards ── */
.metric-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    text-align: center;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #58a6ff; }
.metric-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: #6e7681;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1;
}
.metric-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: #6e7681;
    margin-top: 0.25rem;
}
.cpu-color  { color: #58a6ff; }
.ram-color  { color: #3fb950; }
.disk-color { color: #d2a8ff; }
.net-color  { color: #ffa657; }

/* ── Section headings ── */
.section-heading {
    font-size: 0.7rem;
    font-family: 'Share Tech Mono', monospace;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #6e7681;
    border-left: 3px solid #58a6ff;
    padding-left: 0.6rem;
    margin: 1.5rem 0 0.8rem;
}

/* ── Process table tweaks ── */
div[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #21262d;
}

/* ── Streamlit default overrides ── */
div[data-testid="stMetricValue"] { font-size: 2rem !important; }
div[data-testid="stButton"] > button {
    background: #21262d;
    color: #58a6ff;
    border: 1px solid #30363d;
    border-radius: 8px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    padding: 0.4rem 1.2rem;
    transition: all 0.2s;
}
div[data-testid="stButton"] > button:hover {
    background: #58a6ff;
    color: #0a0c10;
    border-color: #58a6ff;
}
section[data-testid="stSidebar"] { background: #0d1117; }
div[data-testid="stTextInput"] > div > input {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    color: #c9d1d9 !important;
    border-radius: 8px !important;
    font-family: 'Share Tech Mono', monospace !important;
}
div[data-testid="stSelectbox"] > div { background: #161b22; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SESSION STATE  (rolling history for graphs)
# ──────────────────────────────────────────────
MAX_HISTORY = 60  # keep last 60 data-points (~2 min at 2 s refresh)

if "cpu_history"  not in st.session_state:
    st.session_state.cpu_history  = []
if "ram_history"  not in st.session_state:
    st.session_state.ram_history  = []
if "time_history" not in st.session_state:
    st.session_state.time_history = []


# ══════════════════════════════════════════════
# DATA HELPERS
# ══════════════════════════════════════════════

def get_system_stats() -> dict:
    """Return a snapshot of key system-wide metrics."""
    cpu      = psutil.cpu_percent(interval=0.5)
    ram      = psutil.virtual_memory()
    disk     = psutil.disk_usage("/")
    net      = psutil.net_io_counters()

    return {
        "cpu_pct":       cpu,
        "ram_pct":       ram.percent,
        "ram_used_gb":   ram.used  / 1e9,
        "ram_total_gb":  ram.total / 1e9,
        "disk_pct":      disk.percent,
        "disk_used_gb":  disk.used  / 1e9,
        "disk_total_gb": disk.total / 1e9,
        "net_sent_mb":   net.bytes_sent / 1e6,
        "net_recv_mb":   net.bytes_recv / 1e6,
    }


def get_process_dataframe() -> pd.DataFrame:
    """
    Iterate over all running processes and collect name, pid,
    cpu%, memory%.  Silently skip processes we have no access to.
    """
    rows = []
    for proc in psutil.process_iter(
        attrs=["pid", "name", "cpu_percent", "memory_percent", "status"]
    ):
        try:
            info = proc.info
            rows.append({
                "Process Name": info["name"] or "—",
                "PID":          info["pid"],
                "CPU (%)":      round(info["cpu_percent"] or 0.0, 2),
                "Memory (%)":   round(info["memory_percent"] or 0.0, 3),
                "Status":       info["status"] or "—",
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Process vanished or we lack permission — skip it safely
            pass

    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return df.sort_values("CPU (%)", ascending=False).reset_index(drop=True)


def append_history(cpu: float, ram: float) -> None:
    """Push new readings into the rolling history lists."""
    now = datetime.now().strftime("%H:%M:%S")
    st.session_state.cpu_history.append(cpu)
    st.session_state.ram_history.append(ram)
    st.session_state.time_history.append(now)

    # Keep only the last MAX_HISTORY entries
    if len(st.session_state.cpu_history) > MAX_HISTORY:
        st.session_state.cpu_history  = st.session_state.cpu_history[-MAX_HISTORY:]
        st.session_state.ram_history  = st.session_state.ram_history[-MAX_HISTORY:]
        st.session_state.time_history = st.session_state.time_history[-MAX_HISTORY:]


# ══════════════════════════════════════════════
# CHART HELPERS
# ══════════════════════════════════════════════

_CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font         =dict(family="Share Tech Mono, monospace", color="#6e7681", size=11),
    margin       =dict(l=40, r=20, t=30, b=30),
    xaxis        =dict(showgrid=False, color="#30363d", tickfont=dict(size=9)),
    yaxis        =dict(gridcolor="#21262d", range=[0, 100], ticksuffix="%"),
    hovermode    ="x unified",
    legend       =dict(orientation="h", y=1.15, x=0),
)


def cpu_chart() -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=st.session_state.time_history,
        y=st.session_state.cpu_history,
        mode="lines",
        name="CPU",
        line=dict(color="#58a6ff", width=2),
        fill="tozeroy",
        fillcolor="rgba(88,166,255,0.08)",
    ))
    fig.update_layout(**_CHART_LAYOUT, title=dict(
        text="CPU Usage  (%)", font=dict(size=13, color="#58a6ff")))
    return fig


def ram_chart() -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=st.session_state.time_history,
        y=st.session_state.ram_history,
        mode="lines",
        name="RAM",
        line=dict(color="#3fb950", width=2),
        fill="tozeroy",
        fillcolor="rgba(63,185,80,0.08)",
    ))
    fig.update_layout(**_CHART_LAYOUT, title=dict(
        text="RAM Usage  (%)", font=dict(size=13, color="#3fb950")))
    return fig


def gauge_chart(value: float, title: str, color: str) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode ="gauge+number",
        value=value,
        number=dict(suffix="%", font=dict(size=28, color=color)),
        title=dict(text=title, font=dict(size=13, color="#6e7681")),
        gauge=dict(
            axis     =dict(range=[0, 100], tickwidth=1, tickcolor="#30363d"),
            bar      =dict(color=color),
            bgcolor  ="rgba(0,0,0,0)",
            borderwidth=0,
            steps    =[
                dict(range=[0, 60],  color="rgba(255,255,255,0.03)"),
                dict(range=[60, 85], color="rgba(255,166,87,0.08)"),
                dict(range=[85,100], color="rgba(247,129,102,0.12)"),
            ],
            threshold=dict(line=dict(color="#f78166", width=2), value=85),
        ),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
        font=dict(family="Share Tech Mono, monospace", color="#6e7681"),
        margin=dict(l=20, r=20, t=40, b=10),
        height=200,
    )
    return fig


# ══════════════════════════════════════════════
# DASHBOARD  – main render function
# ══════════════════════════════════════════════

def render_dashboard() -> None:

    # ── Header ────────────────────────────────
    st.markdown("""
    <div class="dash-header">
        <div>
            <p class="dash-title">⚡ Process Monitor</p>
            <p class="dash-subtitle">REAL-TIME SYSTEM TELEMETRY · AUTO-REFRESH EVERY 2 s</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Fetch live data ────────────────────────
    stats = get_system_stats()
    append_history(stats["cpu_pct"], stats["ram_pct"])
    df_all = get_process_dataframe()

    # ── Top control bar ────────────────────────
    ctrl_l, ctrl_r = st.columns([3, 1])
    with ctrl_l:
        st.markdown(f"""
        <p style="font-family:'Share Tech Mono',monospace;font-size:0.72rem;
                  color:#6e7681;margin:0;">
          🕐  Last updated: <span style="color:#c9d1d9;">
          {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}</span>
        </p>""", unsafe_allow_html=True)
    with ctrl_r:
        if st.button("⟳  Refresh Now"):
            st.rerun()

    st.markdown("---", unsafe_allow_html=True)

    # ── Row 1 – Metric cards ───────────────────
    st.markdown('<p class="section-heading">System Overview</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "CPU USAGE",       f"{stats['cpu_pct']:.1f}",
         "cpu-color",  f"Cores: {psutil.cpu_count(logical=False)} physical"),
        (c2, "RAM USAGE",       f"{stats['ram_pct']:.1f}",
         "ram-color",  f"{stats['ram_used_gb']:.1f} / {stats['ram_total_gb']:.1f} GB"),
        (c3, "DISK USAGE",      f"{stats['disk_pct']:.1f}",
         "disk-color", f"{stats['disk_used_gb']:.0f} / {stats['disk_total_gb']:.0f} GB"),
        (c4, "NET SENT / RECV", f"{stats['net_sent_mb']:.0f}",
         "net-color",  f"↑ {stats['net_sent_mb']:.0f} MB  ↓ {stats['net_recv_mb']:.0f} MB"),
    ]
    for col, label, value, css_cls, sub in cards:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label">{label}</p>
                <p class="metric-value {css_cls}">{value}<span style="font-size:1rem">%</span></p>
                <p class="metric-sub">{sub}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2 – Gauges ─────────────────────────
    g1, g2, g3 = st.columns(3)
    with g1:
        st.plotly_chart(gauge_chart(stats["cpu_pct"],  "CPU",  "#58a6ff"),
                        use_container_width=True, config={"displayModeBar": False})
    with g2:
        st.plotly_chart(gauge_chart(stats["ram_pct"],  "RAM",  "#3fb950"),
                        use_container_width=True, config={"displayModeBar": False})
    with g3:
        st.plotly_chart(gauge_chart(stats["disk_pct"], "DISK", "#d2a8ff"),
                        use_container_width=True, config={"displayModeBar": False})

    # ── Row 3 – Time-series charts ─────────────
    st.markdown('<p class="section-heading">Live Usage History</p>', unsafe_allow_html=True)
    ch1, ch2 = st.columns(2)
    with ch1:
        st.plotly_chart(cpu_chart(), use_container_width=True,
                        config={"displayModeBar": False})
    with ch2:
        st.plotly_chart(ram_chart(), use_container_width=True,
                        config={"displayModeBar": False})

    # ── Row 4 – Top-5 CPU processes ───────────
    st.markdown('<p class="section-heading">Top 5 Processes by CPU</p>',
                unsafe_allow_html=True)

    if not df_all.empty:
        top5 = df_all.head(5).copy()
        # Small horizontal bar chart
        fig_top5 = go.Figure(go.Bar(
            x   =top5["CPU (%)"],
            y   =top5["Process Name"],
            orientation="h",
            marker=dict(
                color=top5["CPU (%)"],
                colorscale=[[0,"#21262d"],[0.5,"#388bfd"],[1,"#f78166"]],
                showscale=False,
            ),
            text=[f"{v:.1f}%" for v in top5["CPU (%)"]],
            textposition="outside",
            textfont=dict(family="Share Tech Mono", size=10, color="#c9d1d9"),
        ))
        fig_top5.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor ="rgba(0,0,0,0)",
            font=dict(family="Share Tech Mono, monospace", color="#6e7681", size=11),
            margin=dict(l=130, r=60, t=10, b=20),
            height=200,
            xaxis=dict(showgrid=False, visible=False),
            yaxis=dict(autorange="reversed", tickfont=dict(size=11, color="#c9d1d9")),
        )
        st.plotly_chart(fig_top5, use_container_width=True,
                        config={"displayModeBar": False})
    else:
        st.info("No process data available.")

    # ── Row 5 – Full process table ─────────────
    st.markdown('<p class="section-heading">All Running Processes</p>',
                unsafe_allow_html=True)

    # Filter / search controls
    fi1, fi2, fi3 = st.columns([2, 1, 1])
    with fi1:
        search = st.text_input("🔍  Search process name", placeholder="e.g. python, chrome…",
                               label_visibility="collapsed")
    with fi2:
        sort_by = st.selectbox("Sort by", ["CPU (%)", "Memory (%)", "PID", "Process Name"],
                               label_visibility="collapsed")
    with fi3:
        show_all = st.checkbox("Show all processes", value=False)

    if not df_all.empty:
        df_display = df_all.copy()

        # Apply name filter
        if search:
            df_display = df_display[
                df_display["Process Name"].str.contains(search, case=False, na=False)
            ]

        # Re-sort
        ascending = sort_by in ("PID", "Process Name")
        df_display = df_display.sort_values(sort_by, ascending=ascending)

        # Limit rows for performance unless user wants all
        if not show_all:
            df_display = df_display.head(50)

        total = len(df_all)
        shown = len(df_display)
        st.markdown(
            f'<p style="font-family:\'Share Tech Mono\',monospace;font-size:0.7rem;'
            f'color:#6e7681;margin-bottom:0.4rem;">Showing {shown} of {total} processes</p>',
            unsafe_allow_html=True,
        )

        st.dataframe(
            df_display.style
                .background_gradient(subset=["CPU (%)"],    cmap="Blues")
                .background_gradient(subset=["Memory (%)"], cmap="Greens")
                .format({"CPU (%)": "{:.2f}", "Memory (%)": "{:.3f}"}),
            use_container_width=True,
            height=420,
        )
    else:
        st.warning("Could not retrieve process list.")

    # ── Auto-refresh footer ────────────────────
    st.markdown("""
    <p style="text-align:center;font-family:'Share Tech Mono',monospace;
              font-size:0.65rem;color:#30363d;margin-top:2rem;">
        ⚡ Process Monitor · data sourced from psutil · auto-refreshes every 2 s
    </p>""", unsafe_allow_html=True)

    # 2-second auto-refresh via Streamlit's rerun mechanism
    import time
    time.sleep(2)
    st.rerun()


# ──────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────
if __name__ == "__main__" or True:
    render_dashboard()