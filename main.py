import sys
import os

# Add current directory to path to ensure modules are found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules import menu, host, utils, scanner, system

# Conditional imports for setup, update, and maintenance utilities
try:
    import setup
    import update
    from maintain import cleaner
except ImportError:
    pass

def start():
    """
    Main execution loop for the Network Exploit Toolkit.
    """
    try:
        while True:
            # Display the main menu and get user selection
            choice = menu.display_main_menu()

            if choice == '1':
                try:
                    url = input("Enter Target URL (e.g., https://example.com): ")
                    ip, port = host.fetch(url)
                    print(f"\n\033[92m[+] Resolved: {ip}:{port}\033[0m")
                except KeyboardInterrupt:
                    print("\n\033[93m[!] Input cancelled by operator.\033[0m")
                except Exception as e:
                    print(f"\033[91m[!] Error: {e}\033[0m")
                input("\nPress Enter to return...")

            elif choice == '2':
                menu.handle_flood_input()
                input("\nPress Enter to return...")

            elif choice == '3':
                try:
                    target = input("Enter Target (IP or Domain): ")
                    print("\033[93m[*] Scanning common ports...\033[0m")
                    open_ports, ip = scanner.scan_ports(target)
                    if open_ports:
                        print(f"\033[92m[+] Found {len(open_ports)} open ports on {ip}:\033[0m")
                        for p in open_ports: 
                            print(f"  - Port {p}: OPEN")
                    else:
                        print("\033[91m[!] No open ports found or scan failed.\033[0m")
                except KeyboardInterrupt:
                    print("\n\033[93m[!] Scan cancelled by operator.\033[0m")
                input("\nPress Enter to return...")

            elif choice == '4':
                print("\033[96m[SYSTEM DATA]\033[0m")
                data = system.get_sys_info()
                for k, v in data.items(): 
                    print(f"\033[2m{k}:\033[0m {v}")
                input("\nPress Enter to return...")

            elif choice == '5':
                m_choice = menu.maintenance_menu()
                if m_choice == '1': 
                    setup.install_requirements()
                elif m_choice == '2': 
                    cleaner.purge_cache()

            elif choice == '6':
                update.check_for_updates()
                input("\nPress Enter to return...")

            elif choice == 'q':
                utils.typing_effect("\033[91mSession Terminated. Goodbye, Operator.\033[0m")
                sys.exit(0)

    except KeyboardInterrupt:
        print("\n\n\033[91m[!] Emergency Shutdown: Session Terminated by Operator.\033[0m")
        sys.exit(0)

if __name__ == "__main__":
    start()