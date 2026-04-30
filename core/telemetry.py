import random
import numpy as np
import streamlit as st
from datetime import datetime

PROCESS_NAMES = [
    "systemd", "kworker", "sshd", "nginx", "python3",
    "bash",    "mysqld",  "crond", "rsyslog","dockerd",
    "apache2", "perl",    "nc",    "nmap",   "curl",
]

def simulate_system_metrics(attack_type: str) -> dict:
    """
    Generate synthetic kernel-level metrics.
    Inject abnormal spikes based on the specific attack_type.
    """
    now = datetime.now()
    suspicious_procs = []

    if attack_type == "DDoS (Resource Exhaustion)":
        cpu    = min(100, np.random.normal(95, 2))
        mem    = min(100, np.random.normal(92, 3))
        net_rx = np.random.normal(900, 100)
        net_tx = np.random.normal(200, 30)
        disk   = np.random.normal(90, 5)
        proc_count = int(np.random.normal(200, 20))
    elif attack_type == "Reverse Shell (Malware)":
        cpu    = max(0, np.random.normal(45, 8))
        mem    = max(0, np.random.normal(60, 5))
        net_rx = max(0, np.random.normal(180, 30))
        net_tx = max(0, np.random.normal(200, 50))
        disk   = max(0, np.random.normal(50, 10))
        proc_count = int(np.random.normal(100, 5))
        suspicious_procs = ["nc", "nmap", "perl"]
    elif attack_type == "Data Exfiltration (Network)":
        cpu    = max(0, np.random.normal(60, 8))
        mem    = max(0, np.random.normal(65, 5))
        net_rx = max(0, np.random.normal(300, 50))
        net_tx = np.random.normal(1200, 150)
        disk   = max(0, np.random.normal(85, 5))
        proc_count = int(np.random.normal(105, 5))
        suspicious_procs = ["curl"]
    else: # None
        cpu    = max(0, np.random.normal(35, 8))
        mem    = max(0, np.random.normal(55, 5))
        net_rx = max(0, np.random.normal(150, 30))
        net_tx = max(0, np.random.normal(80,  20))
        disk   = max(0, np.random.normal(40,  8))
        proc_count = int(np.random.normal(95, 5))

    # Simulate active processes
    processes = []
    active_procs = random.sample(PROCESS_NAMES, k=min(8, len(PROCESS_NAMES)))
    
    if attack_type != "None" and suspicious_procs:
        active_procs[:len(suspicious_procs)] = random.sample(suspicious_procs, k=min(len(suspicious_procs), len(suspicious_procs)))

    for p in active_procs:
        is_sus = p in ["nc", "nmap", "perl", "curl"]
        processes.append({
            "Process":    p,
            "PID":        random.randint(1000, 9999),
            "CPU (%)":    round(random.uniform(20, 85) if is_sus else random.uniform(0.1, 15), 2),
            "Memory (%)": round(random.uniform(5,  30) if is_sus else random.uniform(0.1, 8),  2),
            "Status":     "⚠ SUSPICIOUS" if is_sus and attack_type != "None" else "Active",
            "User":       "root" if is_sus else random.choice(["www-data","daemon","nobody","sys"]),
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
        "uptime":      f"{random.randint(2,23):02d}h {random.randint(0,59):02d}m",
    }
