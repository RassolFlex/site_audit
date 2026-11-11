"""SSL check for Django audit application."""
import ssl
import socket
from datetime import datetime


def check_ssl(url):
    """Check SSL certificate."""
    clean = url.replace("http://", "").replace("https://", "").split("/")[0]
    
    try:
        context = ssl.create_default_context()
        with socket.create_connection((clean, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=clean) as ssock:
                cert = ssock.getpeercert()
                issuer = dict((k[0], k[1]) for k in cert.get("issuer", []))
                issuer_name = issuer.get("organizationName", "")
                not_after = cert.get("notAfter", "")
                
                if not_after:
                    cert_date = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                    days_left = (cert_date - datetime.now()).days
                else:
                    days_left = -1
                
                alt_names = cert.get("subjectAltName", [])
                covers_www = any(f"*. {clean}" in n or f"www. {clean}" in n for n in alt_names)
                
                return {
                    "ok": True,
                    "status": {
                        "issuer": issuer_name,
                        "not_after": not_after,
                        "days_left": days_left,
                        "covers_www": covers_www,
                        "covers_all": [n[1] for n in alt_names]
                    }
                }
    except Exception as e:
        return {"ok": False, "error": str(e)}