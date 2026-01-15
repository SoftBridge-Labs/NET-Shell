import os
import time
from ui import name
from modules import host, flood, utils, scanner, system

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
    print(f"{YELLOW}[5]{RESET} Maintenance & Setup")
    print(f"{YELLOW}[6]{RESET} Check for Updates")
    print(f"{RED}[Q]{RESET} Exit System")
    print(f"{CYAN}{'━'*35}{RESET}")
    
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
        url = input(f"{CYAN}Target URL [https://iec.edu.in]: {RESET}") or "https://iec.edu.in"
        
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