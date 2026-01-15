import platform
import psutil
import os
import socket
import sys

def get_sys_info():
    """
    Retrieves a comprehensive dictionary of local system specifications.
    Includes error and interrupt handling.
    """
    try:
        # Calculate RAM in GB
        ram_gb = round(psutil.virtual_memory().total / (1024**3), 2)
        
        info = {
            "Operating System": f"{platform.system()} {platform.release()}",
            "OS Version": platform.version(),
            "Architecture": platform.machine(),
            "Hostname": socket.gethostname(),
            "Processor": platform.processor(),
            "CPU Cores (Logical)": psutil.cpu_count(logical=True),
            "Total RAM": f"{ram_gb} GB",
            "Current User": os.getlogin() if os.name != 'nt' else os.environ.get('USERNAME'),
            "System Encoding": sys.getdefaultencoding() if hasattr(sys, 'getdefaultencoding') else "UTF-8"
        }
        return info
    except KeyboardInterrupt:
        return {"Status": "Data retrieval interrupted by operator."}
    except Exception as e:
        return {"Error": f"Could not retrieve system data: {e}"}

def get_network_interfaces():
    """
    Identifies active network interfaces and their associated IP addresses.
    """
    interfaces = {}
    try:
        for interface_name, interface_addresses in psutil.net_if_addrs().items():
            for address in interface_addresses:
                # Filter for IPv4 addresses
                if str(address.family).split('.')[-1] == 'AF_INET':
                    interfaces[interface_name] = address.address
        return interfaces
    except KeyboardInterrupt:
        return {}
    except Exception:
        return {"Error": "Network interface lookup failed"}