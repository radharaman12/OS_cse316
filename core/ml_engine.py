import numpy as np
import streamlit as st
from sklearn.ensemble import IsolationForest

THRESHOLDS = {
    "cpu":    {"warning": 75,  "critical": 90},
    "memory": {"warning": 80,  "critical": 92},
    "net_rx": {"warning": 500, "critical": 800},
    "disk":   {"warning": 85,  "critical": 95},
}

@st.cache_resource
def get_isolation_forest():
    """Cache the trained ML model for performance."""
    X_train = np.column_stack([
        np.random.normal(35, 8,  500),
        np.random.normal(55, 5,  500),
        np.random.normal(150, 30, 500),
        np.random.normal(40, 8,  500),
    ])
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X_train)
    return model

def detect_anomalies(metrics: dict) -> list:
    """Run threshold checks, pattern matching, and ML models on incoming metrics."""
    alerts = []
    ts = metrics["timestamp"].strftime("%H:%M:%S")

    # Threshold checks
    for key, limits in THRESHOLDS.items():
        val = metrics[key]
        if val >= limits["critical"]:
            alerts.append({
                "time": ts, "level": "CRITICAL", "metric": key.upper(),
                "value": val, "message": f"{key.upper()} spiked to {val:.1f}% — Critical Threshold Breach!",
                "rule": "Threshold", "icon": "🚨"
            })
        elif val >= limits["warning"]:
            alerts.append({
                "time": ts, "level": "WARNING", "metric": key.upper(),
                "value": val, "message": f"{key.upper()} elevated to {val:.1f}% — Potential anomaly.",
                "rule": "Threshold", "icon": "⚠️"
            })

    # Process checks
    for proc in metrics["processes"]:
        if proc["Status"] == "⚠ SUSPICIOUS":
            alerts.append({
                "time": ts, "level": "CRITICAL", "metric": "PROCESS",
                "value": proc["CPU (%)"], "message": f"Malicious signature detected: '{proc['Process']}' (PID {proc['PID']}) executing as {proc['User']}!",
                "rule": "Signature", "icon": "💀"
            })

    # ML Isolation Forest
    model = get_isolation_forest()
    X = np.array([[metrics["cpu"], metrics["memory"], metrics["net_rx"], metrics["disk"]]])
    score = model.decision_function(X)[0]
    pred  = model.predict(X)[0]
    
    if pred == -1:
        alerts.append({
            "time": ts, "level": "WARNING", "metric": "ML-ENGINE",
            "value": round(score, 4), "message": f"Isolation Forest detects multivariate drift (Confidence Score: {score:.4f})",
            "rule": "AI/ML", "icon": "🧠"
        })

    return alerts

def log_alerts(alerts: list):
    """Save new alerts to session history."""
    for a in alerts:
        st.session_state.alert_log.append(a)
        st.session_state.total_alerts += 1
        if a["level"] == "CRITICAL":
            st.session_state.critical_count += 1
        else:
            st.session_state.warning_count += 1
    
    if len(st.session_state.alert_log) > 500:
        st.session_state.alert_log = st.session_state.alert_log[-500:]
