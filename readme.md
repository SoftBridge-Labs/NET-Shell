# ⚡ NET-Shell: Advanced Network Diagnostic Suite

[![Version](https://img.shields.io/badge/Version-1.0.0-cyan.svg?style=for-the-badge&logo=gitbook)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Operational-brightgreen.svg?style=for-the-badge&logo=checkmarx)](https://github.com/)

> **Operator-Grade Asynchronous Toolkit** for high-performance network analysis, DNS resolution, and infrastructure stress-testing.

---

## ⚡ Core Capabilities

| Feature | Description | Tech Stack |
| :--- | :--- | :--- |
| **Asynchronous Flood** | Real-time HTTP request streaming with latency tracking. | `aiohttp` |
| **Host Resolver** | Advanced URL parsing and DNS-to-IP translation. | `socket` |
| **Port Scanner** | Multi-threaded TCP handshake verification. | `threading` |
| **System Intel** | Deep-dive hardware and OS telemetry. | `psutil` |
| **Shell UI** | Dynamic ANSI-styled operator interface. | `colorama` |

---

## 🛠️ Deployment

### 1. Initialize Environment
```bash
git clone [https://github.com/PrakharDoneria/NET-Shell.git](https://github.com/PrakharDoneria/NET-Shell.git)
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

---

## 📁 System Architecture

```bash
📦 NET-Shell
 ┣ 📂 modules
 ┃ ┣ 📜 flood.py      # Async Engine
 ┃ ┣ 📜 host.py       # DNS Logic
 ┃ ┣ 📜 scanner.py    # TCP Probe
 ┃ ┗ 📜 menu.py       # Shell Core
 ┣ 📂 maintain
 ┃ ┗ 📜 cleaner.py    # Cache Purge
 ┣ 📜 main.py         # Kernel Entry
 ┗ 📜 setup.py        # Dependency Mgmt

```

---

## ⚖️ Operational Security (OPSEC)

**Disclaimer:** This software is intended for **White-Hat testing and educational research only.** Use of this tool for attacking targets without prior authorization is strictly prohibited. The author assumes no liability for misuse.

---