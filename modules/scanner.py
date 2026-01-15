import socket

def scan_ports(target_host, port_range=None):
    """
    Scans a list of common ports on a target host to check for connectivity.
    Includes interrupt handling for graceful cancellation.
    """
    if port_range is None:
        # Common ports: SSH, FTP, HTTP, HTTPS, MySQL, etc.
        port_range = [21, 22, 80, 443, 3306, 8080]

    open_ports = []
    
    try:
        # Resolve the hostname to an IP if it isn't one already
        target_ip = socket.gethostbyname(target_host)
    except socket.gaierror:
        return None, None
    except KeyboardInterrupt:
        return None, None

    try:
        for port in port_range:
            # Create a TCP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Set a short timeout for the connection attempt
            socket.setdefaulttimeout(1)
            
            try:
                # result will be 0 if the port is open
                result = sock.connect_ex((target_ip, port))
                if result == 0:
                    open_ports.append(port)
            finally:
                sock.close()
                
    except KeyboardInterrupt:
        print("\n\033[93m[!] Port scan interrupted by operator.\033[0m")
        # Return what we found so far
        return open_ports, target_ip
        
    return open_ports, target_ip