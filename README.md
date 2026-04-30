<div align="center">
  
# 🛡️ KIDS.AI — Kernel-Level Intrusion Detection System

**A Top 0.1% SaaS-Grade Real-Time Cybersecurity Monitoring Dashboard**

[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Framework-FF4B4B.svg)](https://streamlit.io/)
[![Machine Learning](https://img.shields.io/badge/ML-Isolation_Forest-8A2BE2.svg)](#)

</div>

<br/>

**KIDS.AI** (Kernel-Level Intrusion Detection System) is an advanced, real-time threat intelligence platform. Built entirely in Python, it simulates kernel-level system telemetry and visualizes it through a high-performance, glassmorphism-styled Streamlit UI. It utilizes a multi-layered detection approach, combining traditional heuristic threshold rules, process signature matching, and **Unsupervised Machine Learning (Isolation Forest)** to detect zero-day system anomalies and malicious executions.

---

## ✨ Key Features

- ⚡ **Zero-Latency Real-Time UI**: Custom-built with `Streamlit` and `Plotly` using an asynchronous, non-blocking 3-second auto-refresh loop for a seamless, flicker-free dashboard.
- 🧠 **AI-Driven Inference Engine**: Implements an `Isolation Forest` machine learning algorithm to detect multidimensional statistical drift in system telemetry.
- 🚨 **Multi-Layered Threat Detection**:
  - **Threshold Rules**: Catches absolute resource exhaustion (CPU, RAM, Disk, Net Rx).
  - **Signature Engine**: Identifies specific malicious executables and potential reverse shells (e.g., `nc`, `nmap`).
  - **AI/ML Engine**: Flags complex behavioral anomalies that bypass static rules.
- 🎯 **Interactive Threat Injection**: Features an "Attack Mode" toggle to inject synthetic malicious traffic and instantly observe the system's automated incident response.
- 📊 **Enterprise Threat Intel Logs**: Searchable, filterable event streams with CSV export capabilities for digital forensics.
- 🎨 **Premium Glassmorphism Design**: High-fidelity custom CSS injected into Streamlit for a top-tier SaaS aesthetic.

---

## 🏗️ System Architecture

KIDS.AI operates on a robust, modular, three-pillar architecture:

1. **Data Aggregation (`core/telemetry.py`)**: 
   A highly efficient simulation engine that polls continuous synthetic system parameters, including CPU ticks, memory allocation, disk I/O, and process lifecycles.
   
2. **AI Inference Engine (`core/ml_engine.py`)**: 
   A high-performance evaluation layer. It runs telemetry payloads through hard-coded threshold matrices and our pre-trained Isolation Forest anomaly model to generate confidence scores.
   
3. **Real-Time UI (`ui/` & `app.py`)**: 
   The frontend visualization layer. It consumes the inference data and renders premium metrics, active thread monitors, area charts, and live security event logs.

---

## 📂 Complete Project Structure

```text
OS_cse316-main/
│
├── app.py                      # Main Streamlit application entry point
├── start.bat                   # 1-Click execution script for Windows
├── requirements.txt            # Python dependencies (Streamlit, Scikit-learn, Plotly, Pandas)
│
├── core/                       # Core Backend Services
│   ├── ml_engine.py            # Machine Learning (Isolation Forest) & Threat Rules
│   └── telemetry.py            # Simulated Kernel metric generation & Process tracking
│
├── ui/                         # Frontend Styling & Components
│   ├── components.py           # Custom Plotly charts & UI rendering logic
│   └── style.css               # Premium Glassmorphism styling and animations
│
└── utils/                      # Helper Functions
    └── state.py                # Streamlit session state management & log handling
```

---

## ⚙️ How It Works (Detection Mechanics)

### 1. Threshold Detection Matrices
The system establishes a hardcoded security perimeter to prevent simple Denial of Service (DoS) attacks or resource hijacking.

| Metric | Warning State | Critical State |
|---|---|---|
| **CPU Core** | ≥ 75% | ≥ 90% |
| **Memory Alloc.** | ≥ 80% | ≥ 92% |
| **Network Ingress** | ≥ 500 KB/s | ≥ 800 KB/s |
| **Disk I/O Stress** | ≥ 85% | ≥ 95% |

### 2. Process Signature Detection
The **Active Thread Monitor** continuously scans the process list. If a process name matches a known malicious signature (e.g., `nc` executing as `root`), a **CRITICAL** threat event is instantly dispatched.

### 3. Machine Learning (Isolation Forest)
The AI engine generates an expected baseline distribution of normal system behavior. Because intrusions often cause irregular combinations of resource usage (e.g., low CPU but massive Network I/O), the Isolation Forest identifies points falling into the extreme statistical tails (Contamination=0.05) and assigns them an anomaly confidence score.

---

## 🚀 Installation & Quick Start

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
For Windows users, simply double-click the `start.bat` file, or run the following command in your terminal:
```bash
streamlit run app.py
```

### 4. Access the Dashboard
The platform will automatically launch in your default web browser at `http://localhost:8501`.

---

## 🖥️ Usage Guide

1. **Dashboard Overview**: Monitor system health, view the live area chart, and keep an eye on the Active Threat Feed.
2. **Real-Time Telemetry**: Navigate to this tab to inspect exact gauge saturation metrics and view the **Active Thread Monitor** table.
3. **Simulate Cyber Attack**: In the left control sidebar, toggle `Simulate Cyber Attack` to `ON`. You will immediately see the UI shift to an alert state, gauges will spike, and the Threat Feed will populate with detected anomalies.
4. **Threat Intel Logs**: Go to this tab to review the historical logs of the attack. Filter by `Severity Level` or `Detection Engine`.
5. **Session Analytics**: Analyze the breakdown of incidents caught during your session and review the mathematical distribution curve of the Machine Learning baseline.

---
*Developed as an advanced Operating Systems and Cybersecurity Project. Designed to showcase how kernel-level monitoring concepts can be combined with enterprise-grade UI/UX and Machine Learning.*
