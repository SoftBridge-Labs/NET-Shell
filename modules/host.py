import socket
from urllib.parse import urlparse

def fetch(url: str):
    """
    Returns (ip_address, port) for a given website URL.
    """
    parsed = urlparse(url)

    # Ensure the URL has a scheme (http/https) and a hostname
    if not parsed.scheme or not parsed.hostname:
        raise ValueError("Invalid URL: Scheme (http/https) or Hostname missing")

    host = parsed.hostname

    # Determine the network port
    if parsed.port:
        # Use port specified in the URL if present
        port = parsed.port
    else:
        # Default to standard ports based on the scheme
        if parsed.scheme == "https":
            port = 443
        elif parsed.scheme == "http":
            port = 80
        else:
            raise ValueError("Unsupported URL scheme: Only http and https are supported")

    # Resolve the domain hostname to an IP address
    try:
        ip_address = socket.gethostbyname(host)
    except socket.gaierror:
        raise ValueError(f"Could not resolve host: {host}")

    return ip_address, port