import urllib.request
import ssl
import time
import sys

# Build an SSL context — use certifi bundle if available, else unverified
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
RESET  = "\033[0m"

# Reliable public test endpoints of known size (1 MB binary)
TEST_ENDPOINTS = [
    ("Cloudflare Workers (1MB)", "https://speed.cloudflare.com/__down?bytes=1048576"),
    ("GitHub Assets CDN (1MB)",  "https://raw.githubusercontent.com/librespeed/speedtest-go/master/LICENSE"),
]

def _bar(ratio: float, width: int = 30) -> str:
    filled = int(ratio * width)
    color = GREEN if ratio > 0.6 else (YELLOW if ratio > 0.3 else RED)
    return f"{color}{'█' * filled}{'░' * (width - filled)}{RESET}"

def _download_test(url: str, label: str, timeout: int = 15) -> float | None:
    """
    Downloads a URL and returns throughput in Mbps.
    Streams the response to get real-time progress.
    """
    print(f"\n{CYAN}[*] Testing via {label}...{RESET}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "NET-Shell/1.0 SpeedTest"})
        start = time.perf_counter()
        total_bytes = 0
        chunk_size = 8192

        with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CTX) as resp:
            content_length = int(resp.headers.get("Content-Length", 0))
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                total_bytes += len(chunk)
                elapsed = time.perf_counter() - start
                mbps = (total_bytes * 8) / (elapsed * 1_000_000) if elapsed > 0 else 0
                ratio = (total_bytes / content_length) if content_length else 0

                bar = _bar(min(ratio, 1.0))
                sys.stdout.write(
                    f"\r  {bar} {total_bytes/1024:.1f} KB  "
                    f"{GREEN}{mbps:.2f} Mbps{RESET}  "
                )
                sys.stdout.flush()

        elapsed = time.perf_counter() - start
        mbps = (total_bytes * 8) / (elapsed * 1_000_000)
        print(f"\n  {GREEN}[+] Done: {total_bytes/1024:.1f} KB in {elapsed:.2f}s → {mbps:.2f} Mbps{RESET}")
        return mbps

    except KeyboardInterrupt:
        print(f"\n  {YELLOW}[!] Test interrupted.{RESET}")
        return None
    except Exception as e:
        print(f"\n  {RED}[!] Failed: {e}{RESET}")
        return None

def run_speed_test():
    """
    Runs a download speed test against multiple CDN endpoints
    and prints a consolidated bandwidth report.
    """
    print(f"\n{CYAN}{'━'*55}{RESET}")
    print(f"{CYAN} BANDWIDTH SPEED ESTIMATOR{RESET}")
    print(f"{CYAN}{'━'*55}{RESET}")
    print(f"{DIM} Tests download throughput via public CDN endpoints.{RESET}")

    results = []
    for label, url in TEST_ENDPOINTS:
        mbps = _download_test(url, label)
        if mbps is not None:
            results.append((label, mbps))

    # ── Summary ────────────────────────────────────────────
    print(f"\n{CYAN}{'━'*55}{RESET}")
    print(f" SPEED TEST SUMMARY")
    print(f"{CYAN}{'━'*55}{RESET}")

    if not results:
        print(f"  {RED}All tests failed. Check your internet connection.{RESET}")
        return

    speeds = [r[1] for r in results]
    avg    = sum(speeds) / len(speeds)

    for label, mbps in results:
        bar = _bar(min(mbps / 100, 1.0), width=20)
        print(f"  {DIM}{label:<35}{RESET} {bar} {GREEN}{mbps:.2f} Mbps{RESET}")

    print(f"\n  Average Download Speed : {CYAN}{avg:.2f} Mbps{RESET}")

    if avg >= 100:
        tier = f"{GREEN}Excellent (100+ Mbps){RESET}"
    elif avg >= 25:
        tier = f"{GREEN}Good (25–100 Mbps){RESET}"
    elif avg >= 5:
        tier = f"{YELLOW}Fair (5–25 Mbps){RESET}"
    else:
        tier = f"{RED}Poor (< 5 Mbps){RESET}"

    print(f"  Connection Tier        : {tier}")
    print(f"{CYAN}{'━'*55}{RESET}")
