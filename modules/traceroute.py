import socket
import time

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
DIM    = "\033[2m"
RESET  = "\033[0m"

def traceroute(target, max_hops=30, timeout=2):
    """
    Traces the network path to a target by sending UDP probes with
    incrementing TTL values and listening for ICMP TTL-exceeded replies.
    Works on macOS/Linux without root by using a raw ICMP recv socket.
    """
    try:
        dest_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"{RED}[!] Could not resolve host: {target}{RESET}")
        return

    print(f"\n{CYAN}Traceroute to {target} ({dest_ip}), max {max_hops} hops:{RESET}")
    print(f"{CYAN}{'━'*60}{RESET}")
    print(f"{DIM}{'HOP':<5} {'RTT':>8}   {'HOST'}{RESET}")
    print(f"{CYAN}{'━'*60}{RESET}")

    port = 33434  # Standard traceroute destination port

    try:
        for ttl in range(1, max_hops + 1):
            recv_sock  = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            send_sock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

            recv_sock.settimeout(timeout)
            send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

            recv_sock.bind(("", port))

            start = time.perf_counter()
            send_sock.sendto(b"", (dest_ip, port))

            curr_addr = None
            curr_name = None

            try:
                _, curr_addr = recv_sock.recvfrom(512)
                curr_addr = curr_addr[0]
                rtt_ms = (time.perf_counter() - start) * 1000

                try:
                    curr_name = socket.gethostbyaddr(curr_addr)[0]
                except socket.herror:
                    curr_name = curr_addr

                print(f"{GREEN}{ttl:<5}{RESET} {rtt_ms:>7.2f}ms   {curr_name} ({curr_addr})")

            except socket.timeout:
                print(f"{YELLOW}{ttl:<5}{RESET} {'*':>8}   Request timed out")

            finally:
                send_sock.close()
                recv_sock.close()

            if curr_addr == dest_ip:
                print(f"\n{GREEN}[+] Destination reached in {ttl} hops.{RESET}")
                break

    except PermissionError:
        print(f"{RED}[!] Permission denied: traceroute requires elevated privileges (sudo).{RESET}")
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Traceroute interrupted by operator.{RESET}")
