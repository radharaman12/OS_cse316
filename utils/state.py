import streamlit as st
from collections import deque
import pandas as pd

def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "attack_type":    "None",
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

def clear_logs():
    """Purge all current session logs."""
    st.session_state.alert_log = []
    st.session_state.total_alerts = 0
    st.session_state.critical_count = 0
    st.session_state.warning_count = 0

def history_to_df() -> pd.DataFrame:
    """Convert deque history into a Pandas DataFrame for charting."""
    times = list(st.session_state.time_history)
    if not times:
        return pd.DataFrame()
    return pd.DataFrame({
        "Time":    times,
        "CPU":     list(st.session_state.cpu_history),
        "Memory":  list(st.session_state.mem_history),
        "Net_RX":  list(st.session_state.net_history),
        "Disk":    list(st.session_state.disk_history),
    })
