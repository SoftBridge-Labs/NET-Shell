import os
import time
from ui import name
from modules import host, flood, utils, scanner, system, traceroute, whois_lookup, ping_monitor
from modules import waf_fingerprint, speedtest, session_logger, net_monitor

# ANSI Styling for a cohesive terminal look
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
DIM = "\033[2m"
RESET = "\033[0m"

# Logical Prompt for the "Operator" shell
PROMPT = f"{GREEN}operator{RESET}{DIM}@{RESET}{CYAN}net-shell{RESET}{DIM}:~${RESET} "

def clear_screen():
    """Clears the terminal screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def header():
    """Displays the standardized project banner and version info."""
    clear_screen()
    name.call()  # Displays the ASCII art banner
    print(f"{CYAN}--- NETWORK EXPLOIT TOOLKIT v1.0 ---{RESET}")

def display_main_menu():
    """Renders the main navigation menu and captures user input."""
    header()
    print(f"{GREEN}[1]{RESET} Resolve Host IP")
    print(f"{GREEN}[2]{RESET} HTTP Request Flood (Full Config)")
    print(f"{GREEN}[3]{RESET} TCP Port Scanner")
    print(f"{GREEN}[4]{RESET} Local System Information")
    print(f"{CYAN}[5]{RESET} Traceroute Path Analysis")
    print(f"{CYAN}[6]{RESET} WHOIS & IP Geolocation Lookup")
    print(f"{CYAN}[7]{RESET} Continuous Ping / Latency Monitor")
    print(f"{CYAN}[A]{RESET} WAF / Firewall Fingerprinter")
    print(f"{CYAN}[B]{RESET} Bandwidth Speed Estimator")
    print(f"{CYAN}[C]{RESET} Network Interface Monitor")
    print(f"{CYAN}[L]{RESET} Session Logger & Report Exporter")
    print(f"{YELLOW}[8]{RESET} Maintenance & Setup")
    print(f"{YELLOW}[9]{RESET} Check for Updates")
    print(f"{RED}[Q]{RESET} Exit System")
    print(f"{CYAN}{'━'*40}{RESET}")
    
    try:
        return input(PROMPT).strip().lower()
    except KeyboardInterrupt:
        # Trigger clean exit in main.py
        return 'q'

def handle_flood_input():
    """
    Manages the data collection for the HTTP Flood tool.
    Handles Ctrl+C to return to the main menu gracefully.
    """
    print(f"\n{YELLOW}--- FLOOD CONFIGURATION ---{RESET}")
    
    try:
        # Default values based on specific homework inputs
        url = input(f"{CYAN}Target URL: {RESET}")
        
        cycles_input = input(f"{CYAN}Request Count/Cycles: {RESET}")
        cycles = int(cycles_input) if cycles_input else 2
        
        interval_input = input(f"{CYAN}Interval Seconds: {RESET}")
        interval = float(interval_input) if interval_input else 3.0
        
        concurrency_input = input(f"{CYAN}Concurrency: {RESET}")
        concurrency = int(concurrency_input) if concurrency_input else 3
        
        print(f"\n{RED}[!] INITIALIZING FLOOD...{RESET}")
        utils.typing_effect(f"Target: {url} | Cycles: {cycles} | Wait: {interval}s", 0.02)
        
        # Executes the requestURL logic from flood.py
        flood.requestURL(url, cycles, interval, concurrency)
        
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Configuration aborted. Returning to net-shell...{RESET}")
        time.sleep(1)
    except ValueError:
        print(f"{RED}[!] Input Error: Please enter numeric values for counts and intervals.{RESET}")

def handle_traceroute_input():
    """Collects target and runs traceroute path analysis."""
    print(f"\n{CYAN}--- TRACEROUTE ---{RESET}")
    try:
        target = input(f"{CYAN}Target (IP or Domain): {RESET}").strip()
        hops_input = input(f"{CYAN}Max Hops [30]: {RESET}").strip()
        max_hops = int(hops_input) if hops_input.isdigit() else 30
        traceroute.traceroute(target, max_hops=max_hops)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Aborted. Returning to net-shell...{RESET}")
        time.sleep(1)

def handle_whois_input():
    """Collects target and runs WHOIS + geolocation lookup."""
    print(f"\n{CYAN}--- WHOIS & GEOLOCATION ---{RESET}")
    try:
        target = input(f"{CYAN}Target (Domain or IP): {RESET}").strip()
        whois_lookup.whois_lookup(target)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Aborted. Returning to net-shell...{RESET}")
        time.sleep(1)

def handle_ping_monitor_input():
    """Collects config and runs the continuous latency monitor."""
    print(f"\n{CYAN}--- PING / LATENCY MONITOR ---{RESET}")
    try:
        target = input(f"{CYAN}Target (IP or Domain): {RESET}").strip()
        count_input   = input(f"{CYAN}Probe Count [20]:      {RESET}").strip()
        interval_input = input(f"{CYAN}Interval Seconds [1]:  {RESET}").strip()
        port_input    = input(f"{CYAN}TCP Port [80]:         {RESET}").strip()
        count    = int(count_input)    if count_input.isdigit()    else 20
        interval = float(interval_input) if interval_input          else 1.0
        port     = int(port_input)     if port_input.isdigit()     else 80
        ping_monitor.ping_monitor(target, count=count, interval=interval, port=port)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Aborted. Returning to net-shell...{RESET}")
        time.sleep(1)
    except ValueError:
        print(f"{RED}[!] Input Error: Please enter numeric values.{RESET}")

def handle_waf_input():
    """Collects target URL and runs WAF/firewall fingerprinting."""
    print(f"\n{CYAN}--- WAF / FIREWALL FINGERPRINTER ---{RESET}")
    try:
        target = input(f"{CYAN}Target URL (e.g. https://example.com): {RESET}").strip()
        waf_fingerprint.fingerprint(target)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Aborted. Returning to net-shell...{RESET}")
        time.sleep(1)

def handle_speedtest_input():
    """Runs the bandwidth speed estimator."""
    print(f"\n{CYAN}--- BANDWIDTH SPEED ESTIMATOR ---{RESET}")
    try:
        speedtest.run_speed_test()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Aborted. Returning to net-shell...{RESET}")
        time.sleep(1)

def handle_net_monitor_input():
    """Collects config and runs the live network interface monitor."""
    print(f"\n{CYAN}--- NETWORK INTERFACE MONITOR ---{RESET}")
    try:
        interval_input = input(f"{CYAN}Refresh interval seconds [1]: {RESET}").strip()
        duration_input = input(f"{CYAN}Monitor duration seconds [60]: {RESET}").strip()
        interval = float(interval_input) if interval_input else 1.0
        duration = int(duration_input) if duration_input.isdigit() else 60
        net_monitor.run_interface_monitor(interval=interval, duration=duration)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Aborted. Returning to net-shell...{RESET}")
        time.sleep(1)
    except ValueError:
        print(f"{RED}[!] Input Error: Please enter numeric values.{RESET}")

def handle_session_logger_input():
    """Opens the session logger sub-menu."""
    session_logger.session_menu()

def maintenance_menu():
    """Renders the maintenance sub-menu with interrupt handling."""
    header()
    print(f"{CYAN}--- MAINTENANCE TOOLS ---{RESET}")
    print(f"{GREEN}[1]{RESET} Install Dependencies (Setup)")
    print(f"{GREEN}[2]{RESET} Purge Cache (__pycache__)")
    print(f"{RED}[B]{RESET} Back to Main Menu")
    
    m_prompt = f"{GREEN}operator{RESET}{DIM}@{RESET}{YELLOW}maint-shell{RESET}{DIM}:~${RESET} "
    try:
        choice = input(f"\n{m_prompt}").strip().lower()
        return choice
    except KeyboardInterrupt:
        return 'b'