import socket
import urllib.request
import ssl
import json

# SSL context — certifi if available, else unverified (common macOS issue)
try:
    import certifi
    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CTX = ssl._create_unverified_context()

try:
    import whois as python_whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
DIM    = "\033[2m"
RESET  = "\033[0m"

def _resolve_to_ip(target: str) -> str:
    """Resolve a domain or raw IP to its IP address string."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        return None

def geo_lookup(ip: str):
    """
    Fetches geolocation data for an IP using the free ip-api.com JSON endpoint.
    No API key required, rate-limited to 45 req/min on free tier.
    """
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,isp,org,as,query"
        req = urllib.request.Request(url, headers={"User-Agent": "NET-Shell/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        return data
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def whois_lookup(target: str):
    """
    Performs a WHOIS lookup on a domain and an IP geolocation lookup.
    Prints all results in a formatted operator-style table.
    """
    print(f"\n{CYAN}{'━'*55}{RESET}")
    print(f"{CYAN} WHOIS & GEOLOCATION INTEL — {target}{RESET}")
    print(f"{CYAN}{'━'*55}{RESET}")

    # ── IP Geolocation ────────────────────────────────────────
    ip = _resolve_to_ip(target)
    if ip:
        print(f"\n{YELLOW}[GEO] IP Geolocation → {ip}{RESET}")
        geo = geo_lookup(ip)
        if geo.get("status") == "success":
            fields = {
                "IP Address" : geo.get("query", "N/A"),
                "Country"    : geo.get("country", "N/A"),
                "Region"     : geo.get("regionName", "N/A"),
                "City"       : geo.get("city", "N/A"),
                "ISP"        : geo.get("isp", "N/A"),
                "Org"        : geo.get("org", "N/A"),
                "AS"         : geo.get("as", "N/A"),
            }
            for k, v in fields.items():
                print(f"  {DIM}{k:<14}{RESET}: {GREEN}{v}{RESET}")
        else:
            print(f"  {RED}[!] Geolocation failed: {geo.get('message', 'Unknown error')}{RESET}")
    else:
        print(f"{RED}[!] Could not resolve host: {target}{RESET}")

    # ── WHOIS ─────────────────────────────────────────────────
    print(f"\n{YELLOW}[WHOIS] Domain Registration Data{RESET}")
    if not WHOIS_AVAILABLE:
        print(f"  {RED}[!] python-whois not installed. Run: pip install python-whois{RESET}")
        return

    try:
        w = python_whois.whois(target)
        fields = {
            "Registrar"   : w.registrar,
            "Created"     : w.creation_date,
            "Expires"     : w.expiration_date,
            "Updated"     : w.updated_date,
            "Name Servers": w.name_servers,
            "Status"      : w.status,
            "Emails"      : w.emails,
        }
        for k, v in fields.items():
            if v is None:
                continue
            # Handle lists (e.g. multiple name servers)
            if isinstance(v, list):
                v = ", ".join(str(x) for x in v[:3])
            print(f"  {DIM}{k:<14}{RESET}: {GREEN}{v}{RESET}")
    except Exception as e:
        print(f"  {RED}[!] WHOIS query failed: {e}{RESET}")
