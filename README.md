# 🛡️ KIDS — Kernel-Level Intrusion Detection System

A real-time cybersecurity monitoring dashboard built with **Python + Streamlit**.
Simulates kernel-level monitoring, detects anomalies using threshold rules and
an Isolation Forest ML model, and displays live alerts and metrics.

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the application
```bash
streamlit run app.py
```

### 3. Open in browser
Streamlit will open automatically at `http://localhost:8501`

---

## 📂 Project Structure

```
kids_app/
├── app.py            ← Main Streamlit application
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## 🧠 Features

| Feature | Description |
|---|---|
| Real-Time Monitoring | Auto-refreshes every 3 seconds with live charts |
| Threshold Detection | CPU/Mem/Disk/Net rules with WARNING and CRITICAL levels |
| ML Detection | Isolation Forest trained on normal baseline data |
| Process Watchlist | Flags nc, nmap, perl — common intrusion tools |
| Attack Mode | Toggle to inject synthetic attack traffic |
| Alert Logs | Colour-coded log table, filterable by level and rule |
| CSV Export | Download full alert log as CSV |

---

## ⚙️ Detection Thresholds

| Metric | Warning | Critical |
|---|---|---|
| CPU | ≥ 75% | ≥ 90% |
| Memory | ≥ 80% | ≥ 92% |
| Net RX | ≥ 500 KB/s | ≥ 800 KB/s |
| Disk I/O | ≥ 85% | ≥ 95% |

---

## 🎓 College Project Note

This project simulates kernel-level data realistically without requiring
actual kernel privileges (eBPF, LKM, etc.), making it safe to run on
any standard Python environment.
