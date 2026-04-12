# ⚡ Real-Time Process Monitoring Dashboard

A dark-mode, industrial-style system monitor built with
**Python · Streamlit · psutil · Plotly · Pandas**.

---

## 📁 Project Structure

```
process_monitor/
├── app.py                    ← Main Streamlit application
├── README.md                 ← This file
├── static/
│   ├── css/
│   │   └── dashboard.css     ← All CSS styles (loaded at runtime by app.py)
│   └── html/
│       ├── snippets.html     ← HTML fragment reference & documentation
│       └── preview.html      ← Static browser preview (no Python needed)
└── templates/
    └── (reserved for Jinja2 templates)
```

---

## 📦 Installation

```bash
pip install streamlit psutil pandas plotly
```

---

## 🚀 Run the App

```bash
cd process_monitor
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 🖼️ Preview Without Running Python

Open `static/html/preview.html` directly in any browser to see
the dashboard layout and CSS styling with static sample data.

---

## ✨ Features

- **4 live metric cards** — CPU, RAM, Disk, Network
- **3 animated gauges** — colour-coded threshold zones
- **Rolling time-series charts** — last 60 readings of CPU & RAM
- **Top-5 CPU bar chart** — colour-scaled horizontal bars
- **Full process table** — 50 rows by default, all with one checkbox
- **Search / filter** — instant name search across all processes
- **Sort controls** — by CPU, Memory, PID, or Process Name
- **Manual Refresh button** + **auto-refresh every 2 s**
- **Safe error handling** — `NoSuchProcess`, `AccessDenied`, `ZombieProcess` silently skipped
