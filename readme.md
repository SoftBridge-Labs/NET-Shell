# ⚡ NET-Shell: Advanced Network Diagnostic Suite

[![Version](https://img.shields.io/badge/Version-2.0.0-cyan.svg?style=for-the-badge&logo=gitbook)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Operational-brightgreen.svg?style=for-the-badge&logo=checkmarx)](https://github.com/)

> **Operator-Grade Asynchronous Toolkit** for high-performance network analysis, DNS resolution, reconnaissance, and infrastructure stress-testing.

---

## ⚡ Core Capabilities

| Feature | Description | Tech Stack |
| :--- | :--- | :--- |
| **Asynchronous Flood** | Real-time HTTP request streaming with latency tracking. | `aiohttp` |
| **Host Resolver** | Advanced URL parsing and DNS-to-IP translation. | `socket` |
| **Port Scanner** | Multi-threaded TCP handshake verification. | `threading` |
| **System Intel** | Deep-dive hardware and OS telemetry. | `psutil` |
| **Traceroute** | ICMP/UDP hop tracing with per-hop RTT and hostname resolution. | `socket` |
| **WHOIS & Geolocation** | Domain/IP registration data and geographic intelligence. | `python-whois`, `ip-api` |
| **Ping Monitor** | Continuous TCP latency probing with live jitter and loss stats. | `socket` |
| **WAF Fingerprinter** | Crafted HTTP probe battery against 15 known WAF/CDN signatures. | `urllib` |
| **Speed Estimator** | Real-world download throughput benchmarking from public CDNs. | `urllib`, `ssl` |
| **Network Interface Monitor** | Live per-interface traffic dashboard with rate and error tracking. | `psutil` |
| **Session Logger** | Transparent stdout capture with TXT/JSON report export. | `io`, `json` |
| **Shell UI** | Dynamic ANSI-styled operator interface. | `colorama` |

---

## 🛠️ Deployment

### 1. Initialize Environment
```bash
git clone https://github.com/SoftBridge-Labs/NET-Shell.git
cd NET-Shell
```

### 2. Auto-Configuration

The toolkit features a self-healing setup script that manages virtual environments and dependencies.

```bash
python setup.py
```

### 3. Execution

```bash
python main.py
```

---

## 🛰️ Technical Workflow

The toolkit operates on a modular architecture, ensuring that network operations do not block the UI thread.

1. **The Request Cycle**: When a "Flood" is initiated, the `asyncio` loop spawns multiple non-blocking tasks.
2. **Real-Time Hook**: As each worker returns a status code, the UI is updated immediately without waiting for the entire batch to finish.
3. **Telemetry**: Latency is calculated per-request to identify "Spikes" and server-side throttling.
4. **Reconnaissance Pipeline**: Traceroute, WHOIS, and WAF modules chain together for full target profiling.
5. **Session Capture**: The Session Logger transparently intercepts stdout for WAF, Speed, and Interface Monitor tools — no manual wiring required.

---

## 📁 System Architecture

```bash
📦 NET-Shell
 ┣ 📂 modules
 ┃ ┣ 📜 flood.py            # Async HTTP Engine
 ┃ ┣ 📜 host.py             # DNS Resolution
 ┃ ┣ 📜 scanner.py          # TCP Port Probe
 ┃ ┣ 📜 system.py           # System Telemetry
 ┃ ┣ 📜 traceroute.py       # Hop Path Analysis
 ┃ ┣ 📜 whois_lookup.py     # WHOIS & Geolocation
 ┃ ┣ 📜 ping_monitor.py     # Latency Monitor
 ┃ ┣ 📜 waf_fingerprint.py  # WAF/CDN Detection
 ┃ ┣ 📜 speedtest.py        # Bandwidth Estimator
 ┃ ┣ 📜 net_monitor.py      # Interface Dashboard
 ┃ ┣ 📜 session_logger.py   # Report Exporter
 ┃ ┣ 📜 menu.py             # Shell Core
 ┃ ┗ 📜 utils.py            # Shared Utilities
 ┣ 📂 ui
 ┃ ┗ 📜 name.py             # Banner / Branding
 ┣ 📂 maintain
 ┃ ┗ 📜 cleaner.py          # Cache Purge
 ┣ 📜 main.py               # Kernel Entry
 ┣ 📜 setup.py              # Dependency Mgmt
 ┣ 📜 update.py             # Self-Update Script
 ┗ 📜 requirements.txt      # pip Dependencies
```

---

## 📦 Dependencies

| Package | Purpose |
| :--- | :--- |
| `aiohttp` | Asynchronous HTTP flood engine |
| `psutil` | System telemetry and network interface stats |
| `python-whois` | WHOIS domain registration lookups |

All other modules use the Python standard library (`socket`, `threading`, `asyncio`, `urllib`, `ssl`, `json`).

---

## ⚖️ Operational Security (OPSEC)

**Disclaimer:** This software is intended for **White-Hat testing and educational research only.** Use of this tool for attacking targets without prior authorization is strictly prohibited. The author assumes no liability for misuse.

---