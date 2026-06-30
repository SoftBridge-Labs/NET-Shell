import os
import json
import sys
import time
from datetime import datetime
from io import StringIO

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
DIM    = "\033[2m"
RESET  = "\033[0m"

# ANSI escape stripper for clean file output
import re
ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')

def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE.sub("", text)

# ── Global session log buffer ─────────────────────────────────────────────────
_session_log: list[dict] = []
_session_start: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
_capturing = False
_capture_buffer = StringIO()

class _TeeStream:
    """Writes to both the real stdout and a capture buffer simultaneously."""
    def __init__(self, real_stream, buffer: StringIO):
        self._real = real_stream
        self._buf  = buffer

    def write(self, data):
        self._real.write(data)
        self._buf.write(data)

    def flush(self):
        self._real.flush()
        self._buf.flush()

    def __getattr__(self, attr):
        return getattr(self._real, attr)


def start_capture(tool_name: str):
    """Begins intercepting stdout so tool output is recorded."""
    global _capturing, _capture_buffer
    _capturing = True
    _capture_buffer = StringIO()
    sys.stdout = _TeeStream(sys.__stdout__, _capture_buffer)
    _session_log.append({
        "tool"      : tool_name,
        "timestamp" : datetime.now().strftime("%H:%M:%S"),
        "output"    : None,   # filled by stop_capture
    })

def stop_capture():
    """Stops stdout interception and saves captured output to the log."""
    global _capturing
    sys.stdout = sys.__stdout__
    if _session_log and _session_log[-1]["output"] is None:
        _session_log[-1]["output"] = strip_ansi(_capture_buffer.getvalue())
    _capturing = False


def view_session_log():
    """Prints the in-memory session log to the terminal."""
    print(f"\n{CYAN}{'━'*60}{RESET}")
    print(f"{CYAN} SESSION LOG — Started: {_session_start}{RESET}")
    print(f"{CYAN}{'━'*60}{RESET}")

    if not _session_log:
        print(f"  {YELLOW}[!] No tool outputs captured yet.{RESET}")
        print(f"  {DIM}Outputs are captured automatically each time you run a tool.{RESET}")
        return

    for i, entry in enumerate(_session_log, 1):
        print(f"\n{GREEN}[{i}] {entry['tool']}{RESET} — {DIM}{entry['timestamp']}{RESET}")
        print(f"{DIM}{'─'*50}{RESET}")
        lines = (entry["output"] or "").strip().splitlines()
        for line in lines[:40]:   # cap preview at 40 lines
            print(f"  {line}")
        if len(lines) > 40:
            print(f"  {DIM}... ({len(lines)-40} more lines in export){RESET}")

    print(f"\n{CYAN}{'━'*60}{RESET}")
    print(f"  Total recorded tool runs: {GREEN}{len(_session_log)}{RESET}")


def export_report(export_dir: str = None):
    """
    Exports the full session log as both .txt and .json files.
    Defaults to the current working directory.
    """
    if not _session_log:
        print(f"  {YELLOW}[!] Nothing to export — session log is empty.{RESET}")
        return

    if export_dir is None:
        export_dir = os.getcwd()

    ts_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
    base   = os.path.join(export_dir, f"net_shell_report_{ts_tag}")
    txt_path  = base + ".txt"
    json_path = base + ".json"

    # ── Plain-text report ─────────────────────────────────
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"NET-Shell Session Report\n")
        f.write(f"Session Start : {_session_start}\n")
        f.write(f"Export Time   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*60}\n\n")
        for i, entry in enumerate(_session_log, 1):
            f.write(f"[{i}] {entry['tool']} — {entry['timestamp']}\n")
            f.write(f"{'-'*50}\n")
            f.write((entry["output"] or "").strip())
            f.write("\n\n")

    # ── JSON report ───────────────────────────────────────
    payload = {
        "session_start" : _session_start,
        "export_time"   : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "entries"       : _session_log,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"\n  {GREEN}[+] TXT report saved → {txt_path}{RESET}")
    print(f"  {GREEN}[+] JSON report saved → {json_path}{RESET}")


def session_menu():
    """Interactive sub-menu for the session logger."""
    print(f"\n{CYAN}{'━'*45}{RESET}")
    print(f"{CYAN} SESSION LOGGER & REPORT EXPORTER{RESET}")
    print(f"{CYAN}{'━'*45}{RESET}")
    print(f"  {GREEN}[1]{RESET} View current session log")
    print(f"  {GREEN}[2]{RESET} Export report (.txt + .json)")
    print(f"  {RED}[3]{RESET} Clear session log")
    print(f"  {YELLOW}[B]{RESET} Back")
    print(f"{CYAN}{'━'*45}{RESET}")

    try:
        choice = input(f"\n{GREEN}logger{RESET}{DIM}@{RESET}{CYAN}net-shell{RESET}{DIM}:~${RESET} ").strip().lower()
    except KeyboardInterrupt:
        return

    if choice == '1':
        view_session_log()
    elif choice == '2':
        path_input = input(f"  Export directory [{os.getcwd()}]: ").strip()
        export_report(path_input if path_input else None)
    elif choice == '3':
        _session_log.clear()
        print(f"  {YELLOW}[!] Session log cleared.{RESET}")
