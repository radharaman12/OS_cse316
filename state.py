import streamlit as st
from collections import deque

def init_session_state():
    defaults = {
        "attack_mode": False,
        "monitoring": True,
        "alert_log": [],
        "cpu_history": deque(maxlen=60),
        "mem_history": deque(maxlen=60),
        "net_history": deque(maxlen=60),
        "disk_history": deque(maxlen=60),
        "time_history": deque(maxlen=60),
        "anomaly_model": None,
        "tick": 0,
        "total_alerts": 0,
        "critical_count": 0,
        "warning_count": 0,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v