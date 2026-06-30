import socket
import time
import sys

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
DIM    = "\033[2m"
RESET  = "\033[0m"

def _tcp_ping(host: str, port: int, timeout: float) -> float | None:
    """
    Measures TCP connect latency to host:port.
    Returns latency in ms, or None on failure/timeout.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    start = time.perf_counter()
    try:
        sock.connect((host, port))
        latency = (time.perf_counter() - start) * 1000
        return round(latency, 2)
    except (socket.timeout, socket.error):
        return None
    finally:
        sock.close()

def _latency_bar(latency: float, threshold_ms: float = 200, width: int = 25) -> str:
    """Renders a color-coded latency bar."""
    ratio = min(latency / threshold_ms, 1.0)
    filled = int(ratio * width)
    color = GREEN if latency < 80 else (YELLOW if latency < 200 else RED)
    return f"{color}{'█' * filled}{'░' * (width - filled)}{RESET}"

def ping_monitor(target: str, count: int = 20, interval: float = 1.0, port: int = 80, timeout: float = 2.0):
    """
    Continuously TCP-pings a host and prints live latency with statistics.
    Press Ctrl+C to stop early and see the final summary.
    """
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"{RED}[!] Could not resolve host: {target}{RESET}")
        return

    print(f"\n{CYAN}{'━'*60}{RESET}")
    print(f"{CYAN} PING MONITOR → {target} ({ip}) on port {port}{RESET}")
    print(f"{CYAN} Probes: {count} | Interval: {interval}s | Timeout: {timeout}s{RESET}")
    print(f"{CYAN}{'━'*60}{RESET}")
    print(f"{DIM}{'#':<5} {'LATENCY':>10}   {'BAR':<26} STATUS{RESET}")
    print(f"{CYAN}{'━'*60}{RESET}")

    latencies = []
    lost = 0

    try:
        for i in range(1, count + 1):
            ms = _tcp_ping(ip, port, timeout)

            if ms is None:
                lost += 1
                print(f"{RED}{i:<5}{RESET} {'TIMEOUT':>10}   {'░'*25}  {RED}LOSS{RESET}")
            else:
                latencies.append(ms)
                bar = _latency_bar(ms)
                color = GREEN if ms < 80 else (YELLOW if ms < 200 else RED)
                print(f"{GREEN}{i:<5}{RESET} {color}{ms:>9.2f}ms{RESET}   {bar}  {GREEN}OK{RESET}")

            # Live stats footer (overwrite same line)
            if latencies:
                mn  = min(latencies)
                mx  = max(latencies)
                avg = sum(latencies) / len(latencies)
                # Jitter = mean absolute deviation of successive differences
                jitter = 0.0
                if len(latencies) > 1:
                    diffs = [abs(latencies[j] - latencies[j-1]) for j in range(1, len(latencies))]
                    jitter = sum(diffs) / len(diffs)
                loss_pct = (lost / i) * 100
                sys.stdout.write(
                    f"\r{DIM}╰─ min:{mn:.1f}ms  max:{mx:.1f}ms  "
                    f"avg:{avg:.1f}ms  jitter:{jitter:.1f}ms  "
                    f"loss:{loss_pct:.0f}%{RESET}  "
                )
                sys.stdout.flush()

            if i < count:
                time.sleep(interval)

    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}[!] Monitor interrupted by operator.{RESET}")

    # Final summary
    print(f"\n\n{YELLOW}{'━'*40}{RESET}")
    print(f"{YELLOW} FINAL SUMMARY{RESET}")
    print(f"{YELLOW}{'━'*40}{RESET}")
    total = len(latencies) + lost
    if latencies:
        print(f"  Probes sent  : {total}")
        print(f"  Received     : {GREEN}{len(latencies)}{RESET}")
        print(f"  Lost         : {RED}{lost} ({(lost/total)*100:.1f}%){RESET}")
        print(f"  Min latency  : {GREEN}{min(latencies):.2f} ms{RESET}")
        print(f"  Max latency  : {RED}{max(latencies):.2f} ms{RESET}")
        print(f"  Avg latency  : {CYAN}{sum(latencies)/len(latencies):.2f} ms{RESET}")
        if len(latencies) > 1:
            diffs = [abs(latencies[j] - latencies[j-1]) for j in range(1, len(latencies))]
            print(f"  Jitter       : {YELLOW}{sum(diffs)/len(diffs):.2f} ms{RESET}")
    else:
        print(f"  {RED}All probes lost — host may be down or blocking TCP on port {port}.{RESET}")
