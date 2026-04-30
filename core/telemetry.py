import random
import numpy as np
import streamlit as st
from datetime import datetime

PROCESS_NAMES = [
    "systemd", "kworker", "sshd", "nginx", "python3",
    "bash",    "mysqld",  "crond", "rsyslog","dockerd",
    "apache2", "perl",    "nc",    "nmap",   "curl",
]

def simulate_system_metrics(attack_mode: bool) -> dict:
    """
    Generate synthetic kernel-level metrics.
    In attack mode, inject abnormal spikes to simulate intrusion.
    """
    now = datetime.now()

    if attack_mode:
        # Simulate a burst attack pattern
        phase = (st.session_state.tick % 20) / 20.0
        spike = abs(np.sin(phase * np.pi)) * 60

        cpu    = min(100, np.random.normal(55, 8)  + spike)
        mem    = min(100, np.random.normal(70, 6)  + spike * 0.6)
        net_rx = np.random.normal(400, 50) + spike * 15
        net_tx = np.random.normal(200, 30) + spike * 10
        disk   = np.random.normal(80, 10)  + spike * 0.4
        proc_count = int(np.random.normal(120, 10) + spike * 0.5)
    else:
        cpu    = max(0, np.random.normal(35, 8))
        mem    = max(0, np.random.normal(55, 5))
        net_rx = max(0, np.random.normal(150, 30))
        net_tx = max(0, np.random.normal(80,  20))
        disk   = max(0, np.random.normal(40,  8))
        proc_count = int(np.random.normal(95, 5))

    # Simulate active processes
    processes = []
    suspicious_procs = ["nc", "nmap", "perl"] if attack_mode else []
    active_procs = random.sample(PROCESS_NAMES, k=min(8, len(PROCESS_NAMES)))
    
    if attack_mode and suspicious_procs:
        active_procs[:2] = random.sample(suspicious_procs, k=min(2, len(suspicious_procs)))

    for p in active_procs:
        is_sus = p in ["nc", "nmap", "perl"]
        processes.append({
            "Process":    p,
            "PID":        random.randint(1000, 9999),
            "CPU (%)":    round(random.uniform(20, 85) if is_sus else random.uniform(0.1, 15), 2),
            "Memory (%)": round(random.uniform(5,  30) if is_sus else random.uniform(0.1, 8),  2),
            "Status":     "⚠ SUSPICIOUS" if is_sus else "Active",
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
