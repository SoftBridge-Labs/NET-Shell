import urllib.request
import urllib.error
import ssl
import time
import re

# SSL context — certifi if available, else unverified
try:
    import certifi
    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CTX = ssl._create_unverified_context()

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
DIM    = "\033[2m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# Known WAF signatures: (pattern_in_headers_or_body, waf_name)
WAF_SIGNATURES = [
    (r"cloudflare",            "Cloudflare"),
    (r"__cfduid|cf-ray",       "Cloudflare"),
    (r"x-sucuri-id",           "Sucuri"),
    (r"x-firewall-protection", "Generic Firewall"),
    (r"x-waf-event-info",      "Barracuda WAF"),
    (r"x-amzn-requestid|x-amz-cf-id", "AWS CloudFront"),
    (r"x-cdn|x-check-cacheable", "Varnish Cache"),
    (r"akamai|akamaighost",    "Akamai"),
    (r"x-fw-hash",             "Wordfence"),
    (r"incap_ses|visid_incap", "Imperva Incapsula"),
    (r"x-iinfo",               "Imperva Incapsula"),
    (r"mod_security|modsec",   "ModSecurity"),
    (r"fortigate|fortiweb",    "Fortinet FortiGate"),
    (r"f5-trafficshield|bigip","F5 BIG-IP"),
    (r"ats/",                  "Apache Traffic Server"),
    (r"naxsi",                 "NAXSI"),
    (r"x-denyall",             "DenyAll WAF"),
]

PROBE_PAYLOADS = [
    ("Normal",          "/"),
    ("SQLi probe",      "/?id=1'OR'1'='1"),
    ("XSS probe",       "/?q=<script>alert(1)</script>"),
    ("Path traversal",  "/../../../etc/passwd"),
    ("Bad User-Agent",  "/"),
]

def _make_request(url: str, path: str, extra_headers: dict = None) -> tuple:
    """Sends an HTTP request and returns (status_code, headers_dict, elapsed_ms)."""
    full_url = url.rstrip("/") + path
    req = urllib.request.Request(full_url)
    req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) NET-Shell/1.0")
    if extra_headers:
        for k, v in extra_headers.items():
            req.add_header(k, v)
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=6, context=_SSL_CTX) as resp:
            elapsed = (time.perf_counter() - start) * 1000
            return resp.status, dict(resp.headers), elapsed
    except urllib.error.HTTPError as e:
        elapsed = (time.perf_counter() - start) * 1000
        return e.code, dict(e.headers), elapsed
    except Exception:
        return None, {}, (time.perf_counter() - start) * 1000

def _detect_waf(headers: dict, body_hint: str = "") -> list:
    """Matches response headers against known WAF signatures."""
    detected = []
    combined = " ".join(f"{k.lower()} {v.lower()}" for k, v in headers.items())
    combined += " " + body_hint.lower()
    for pattern, name in WAF_SIGNATURES:
        if re.search(pattern, combined) and name not in detected:
            detected.append(name)
    return detected

def fingerprint(target_url: str):
    """
    Sends a series of probe requests to detect WAF/firewall presence,
    fingerprint server headers, and identify anomalous blocking behavior.
    """
    if not target_url.startswith(("http://", "https://")):
        target_url = "http://" + target_url

    print(f"\n{CYAN}{'━'*60}{RESET}")
    print(f"{CYAN} WAF / FIREWALL FINGERPRINTER — {target_url}{RESET}")
    print(f"{CYAN}{'━'*60}{RESET}")

    all_detected = set()
    server_banner = None

    print(f"\n{YELLOW}[*] Sending probe requests...{RESET}\n")
    print(f"{DIM}{'PROBE':<20} {'CODE':>5}   {'RTT':>8}   {'VERDICT'}{RESET}")
    print(f"{DIM}{'─'*58}{RESET}")

    for label, path in PROBE_PAYLOADS:
        extra = {"User-Agent": "() { :; }; echo Content-Type: text/html; echo; echo; /bin/bash -i"} \
                if label == "Bad User-Agent" else None
        status, headers, rtt = _make_request(target_url, path, extra)

        # Grab server banner once
        if server_banner is None:
            server_banner = headers.get("Server", headers.get("server", "Unknown"))

        if status is None:
            print(f"  {label:<20} {'ERR':>5}   {rtt:>7.0f}ms   {RED}Connection failed{RESET}")
            continue

        detected = _detect_waf(headers)
        all_detected.update(detected)

        # Color code by status
        if 200 <= status < 300:
            sc = f"{GREEN}{status}{RESET}"
            verdict = f"{GREEN}Passed through{RESET}"
        elif status in (403, 406, 429, 503):
            sc = f"{RED}{status}{RESET}"
            verdict = f"{RED}Blocked / Rate-limited{RESET}"
            if detected:
                verdict += f" — {YELLOW}{', '.join(detected)}{RESET}"
        else:
            sc = f"{YELLOW}{status}{RESET}"
            verdict = f"{YELLOW}Unusual response{RESET}"

        print(f"  {label:<20} {sc:>5}   {rtt:>7.0f}ms   {verdict}")

    # ── Summary ───────────────────────────────────────────────
    print(f"\n{CYAN}{'━'*60}{RESET}")
    print(f"{BOLD} FINGERPRINT REPORT{RESET}")
    print(f"{CYAN}{'━'*60}{RESET}")
    print(f"  {DIM}Server Banner   :{RESET} {GREEN}{server_banner}{RESET}")

    if all_detected:
        print(f"  {DIM}Detected WAF/CDN:{RESET} {RED}{', '.join(all_detected)}{RESET}")
    else:
        print(f"  {DIM}Detected WAF/CDN:{RESET} {GREEN}None detected (may be custom or absent){RESET}")
    print(f"{CYAN}{'━'*60}{RESET}")
