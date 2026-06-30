# 🛠️ Contribution — NET-Shell Feature Expansion

## Overview

This contribution significantly expands the NET-Shell toolkit from a 4-tool diagnostic suite into a comprehensive **7-module operator platform**, adding active reconnaissance, infrastructure analysis, performance benchmarking, and full session logging capabilities.

---

## Modules Added

### 1. 🗺️ Traceroute Path Analysis (`modules/traceroute.py`)
Implements network hop tracing using raw ICMP/UDP socket probes with incrementing TTL values — the same technique used by the Unix `traceroute` utility. Each hop is resolved to a hostname where possible, with per-hop RTT displayed in a formatted operator table. Supports configurable max hop depth and graceful Ctrl+C interruption.

### 2. 🌍 WHOIS & IP Geolocation Lookup (`modules/whois_lookup.py`)
Performs a two-part intelligence query on any domain or IP address:
- **Geolocation** via the `ip-api.com` JSON API — returns country, region, city, ISP, ASN, and organization.
- **WHOIS registration data** via the `python-whois` library — returns registrar, creation/expiry dates, name servers, and contact emails.

### 3. 📡 Continuous Ping / Latency Monitor (`modules/ping_monitor.py`)
A TCP-based connectivity probe that continuously measures round-trip time to a target host on a configurable port. Displays per-probe results with a color-coded latency bar (green/yellow/red) and live statistics including minimum, maximum, average latency, jitter (mean absolute deviation), and packet loss percentage. Final summary printed on exit.

### 4. 🔍 WAF / Firewall Fingerprinter (`modules/waf_fingerprint.py`)
Sends a battery of 5 crafted HTTP probes (normal request, SQL injection, XSS, path traversal, malicious User-Agent) to a target and analyzes response status codes and headers against a database of **15 known WAF/CDN signatures** including Cloudflare, Akamai, AWS CloudFront, Imperva Incapsula, ModSecurity, F5 BIG-IP, and more. Produces a fingerprint report with server banner and detected protection layers.

### 5. ⚡ Bandwidth Speed Estimator (`modules/speedtest.py`)
Measures real-world download throughput by streaming test payloads from public CDN endpoints (Cloudflare Workers, GitHub). Displays a live animated progress bar with real-time Mbps readout during download, then produces a summary report with per-endpoint results, average speed, and a connection tier rating (Excellent / Good / Fair / Poor).

### 6. 📊 Network Interface Monitor (`modules/net_monitor.py`)
A live, auto-refreshing terminal dashboard powered by `psutil` that displays per-interface network statistics for every adapter on the system. Metrics include download/upload rates (human-readable), packet counts, error counts, and drop counts — all updated every configurable interval using in-place ANSI cursor redraw. Activity levels are visualized with a color-coded bar that saturates at 10 MB/s.

### 7. 🗂️ Session Logger & Report Exporter (`modules/session_logger.py`)
A stdout interception system using a `TeeStream` wrapper that transparently captures the output of any tool run during the session without disrupting live display. Captured entries are stored in memory with timestamps and tool labels. Operators can view a paginated in-session log or export the full session as:
- A structured **plain-text report** (`.txt`)
- A machine-readable **JSON report** (`.json`)

Automatic capture is wired into the WAF Fingerprinter, Speed Estimator, and Interface Monitor — no manual intervention required.

---

## Files Modified

| File | Change |
|------|--------|
| `modules/menu.py` | Added imports, 7 new menu entries (`[5]`–`[7]`, `[A]`–`[C]`, `[L]`), and handler functions for each new tool |
| `main.py` | Added imports and routing for all new menu choices in the main event loop |
| `requirements.txt` | Added `python-whois` dependency |

---

## Technical Highlights

- **No heavy new dependencies** — all network operations use Python stdlib (`socket`, `urllib`, `ssl`, `asyncio`); only `python-whois` added
- **macOS SSL compatibility** — all HTTPS requests use a safe SSL context (certifi bundle or unverified fallback) to prevent `CERTIFICATE_VERIFY_FAILED` errors common on macOS Python installs
- **Consistent operator UX** — all modules follow the existing ANSI color scheme (green/cyan/yellow/red), use the same interrupt-handling pattern (`KeyboardInterrupt`), and return cleanly to the main menu
- **Modular architecture** — each feature is fully self-contained in its own module file, keeping `main.py` and `menu.py` as thin orchestration layers
