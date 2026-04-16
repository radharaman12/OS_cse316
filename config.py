import streamlit as st

def setup_page():
    st.set_page_config(
        page_title="KIDS — Kernel Intrusion Detection",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

THRESHOLDS = {
    "cpu": {"warning": 75, "critical": 90},
    "memory": {"warning": 80, "critical": 92},
    "net_rx": {"warning": 500, "critical": 800},
    "disk": {"warning": 85, "critical": 95},
}