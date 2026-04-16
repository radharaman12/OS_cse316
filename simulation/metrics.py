import numpy as np
import random
from datetime import datetime
import streamlit as st

PROCESS_NAMES = ["systemd", "kworker", "sshd", "nginx", "python3", "nmap", "nc"]

def simulate_system_metrics(attack_mode: bool):
    now = datetime.now()

    if attack_mode:
        cpu = min(100, np.random.normal(70, 10))
        mem = min(100, np.random.normal(75, 8))
    else:
        cpu = max(0, np.random.normal(35, 8))
        mem = max(0, np.random.normal(55, 5))

    processes = []
    for p in random.sample(PROCESS_NAMES, 5):
        processes.append({
            "process": p,
            "cpu_%": round(random.uniform(0.1, 50), 2),
        })

    return {
        "timestamp": now,
        "cpu": round(cpu, 2),
        "memory": round(mem, 2),
        "processes": processes,
    }