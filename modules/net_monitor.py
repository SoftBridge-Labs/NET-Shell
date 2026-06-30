import psutil
import time
import sys
import os

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
DIM    = "\033[2m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
CLEAR_LINE = "\033[2K\r"

def _bytes_fmt(n: float) -> str:
    """Formats bytes into a human-readable string."""
    for unit in ("B", "KB", "MB", "GB"):
        if abs(n) < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"

def _bar(ratio: float, width: int = 18) -> str:
    ratio = max(0.0, min(ratio, 1.0))
    filled = int(ratio * width)
    color = GREEN if ratio < 0.6 else (YELLOW if ratio < 0.85 else RED)
    return f"{color}{'█' * filled}{'░' * (width - filled)}{RESET}"

def _get_interface_stats() -> dict:
    """Returns per-interface counters from psutil."""
    return psutil.net_io_counters(pernic=True)

def _clear_dashboard(line_count: int):
    """Moves cursor up 'line_count' lines to redraw the dashboard in-place."""
    sys.stdout.write(f"\033[{line_count}A")

def run_interface_monitor(interval: float = 1.0, duration: int = 60):
    """
    Displays a live, auto-refreshing dashboard of per-interface network stats:
    bytes sent/received, packets, errors, and drops — updated every `interval` seconds.
    Press Ctrl+C to stop early.
    """
    print(f"\n{CYAN}{'━'*65}{RESET}")
    print(f"{CYAN} NETWORK INTERFACE MONITOR  (refresh: {interval}s | runtime: {duration}s){RESET}")
    print(f"{CYAN} Press Ctrl+C to stop{RESET}")
    print(f"{CYAN}{'━'*65}{RESET}\n")

    try:
        prev_stats  = _get_interface_stats()
        prev_time   = time.perf_counter()
        first_draw  = True
        drawn_lines = 0
        elapsed     = 0

        while elapsed < duration:
            time.sleep(interval)
            curr_stats = _get_interface_stats()
            curr_time  = time.perf_counter()
            dt = curr_time - prev_time

            # Collect all rows to know how many lines to redraw
            rows = []
            for iface, curr in curr_stats.items():
                prev = prev_stats.get(iface)
                if prev is None:
                    continue

                rx_rate = (curr.bytes_recv - prev.bytes_recv) / dt
                tx_rate = (curr.bytes_sent - prev.bytes_sent) / dt
                pkt_rx  = (curr.packets_recv - prev.packets_recv)
                pkt_tx  = (curr.packets_sent - prev.packets_sent)
                errin   = curr.errin
                errout  = curr.errout
                dropin  = curr.dropin
                dropout = curr.dropout

                rows.append((iface, rx_rate, tx_rate, pkt_rx, pkt_tx, errin, errout, dropin, dropout))

            # Redraw — move cursor up on subsequent draws
            if not first_draw:
                _clear_dashboard(drawn_lines)

            lines_written = 0
            header = (
                f"{DIM}{'INTERFACE':<14} {'▼ RX':>12} {'▲ TX':>12} "
                f"{'PKT RX':>8} {'PKT TX':>8} "
                f"{'ERR':>5} {'DROP':>5}   {'ACTIVITY'}{RESET}"
            )
            print(header)
            print(f"{DIM}{'─'*75}{RESET}")
            lines_written += 2

            for (iface, rx_rate, tx_rate, pkt_rx, pkt_tx,
                 errin, errout, dropin, dropout) in rows:

                err_total  = errin + errout
                drop_total = dropin + dropout
                activity   = _bar(min((rx_rate + tx_rate) / (10 * 1024 * 1024), 1.0))  # saturates at 10 MB/s

                err_col  = f"{RED}{err_total}{RESET}"  if err_total  else f"{DIM}0{RESET}"
                drop_col = f"{RED}{drop_total}{RESET}" if drop_total else f"{DIM}0{RESET}"

                print(
                    f"{GREEN}{iface:<14}{RESET}"
                    f"{CYAN}{_bytes_fmt(rx_rate):>10}/s{RESET}"
                    f"  {YELLOW}{_bytes_fmt(tx_rate):>10}/s{RESET}"
                    f"  {pkt_rx:>8}  {pkt_tx:>8}"
                    f"  {err_col:>5}  {drop_col:>5}   {activity}"
                )
                lines_written += 1

            # Footer
            elapsed += interval
            remaining = duration - elapsed
            sys.stdout.write(
                f"\n{DIM}╰─ Elapsed: {elapsed:.0f}s | Remaining: {remaining:.0f}s{RESET}\n"
            )
            sys.stdout.flush()
            lines_written += 2

            drawn_lines = lines_written
            first_draw  = False
            prev_stats  = curr_stats
            prev_time   = curr_time

    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}[!] Monitor stopped by operator.{RESET}")
        return

    print(f"\n{GREEN}[+] Monitoring session complete.{RESET}")
