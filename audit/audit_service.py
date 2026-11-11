import requests
import json
import re
import ssl
import socket
import datetime
from urllib.parse import urlparse

TIMEOUT = 10
MAX_REDIRECTS = 5


def safe_json(obj):
    """Convert object to JSON, serializing non-serializable values."""
    def default_handler(o):
        return str(o)
    try:
        return json.dumps(obj, ensure_ascii=False, default=default_handler)
    except Exception:
        return "JSON serialization error"


def check_domain(url):
    """Check domain registration info using WHOIS."""
    try:
        import whois
        
        parsed = urlparse(url)
        domain = parsed.hostname
        if not domain:
            return {"error": "Invalid URL"}
        
        # Query WHOIS database
        w = whois.whois(domain)
        
        if not w:
            return {"error": f"WHOIS query failed for {domain}"}
        
        # Extract registration date
        created = w.created
        if not created and hasattr(w, 'creation_date'):
            created = w.creation_date
        if isinstance(created, list):
            created = created[0] if created else None
        if isinstance(created, (datetime.datetime, datetime.date)):
            created_str = created.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(created, str):
            created_str = created
        else:
            created_str = str(created) if created else "Unknown"
        
        # Calculate domain age
        age_info = {"days": None, "years": None, "months": None}
        if isinstance(created, (datetime.datetime, datetime.date)):
            now = datetime.datetime.now()
            delta = now - created
            days = delta.days
            age_info["days"] = days
            age_info["years"] = days // 365
            age_info["months"] = (days % 365) // 30
        elif isinstance(created, str):
            age_info["note"] = "Unable to calculate age - WHOIS date format not recognized"
        
        # Extract expiration date
        expires = w.expiration_date
        if isinstance(expires, list):
            expires = expires[0] if expires else None
        if isinstance(expires, (datetime.datetime, datetime.date)):
            expires_str = expires.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(expires, str):
            expires_str = expires
        else:
            expires_str = str(expires) if expires else "Unknown"
        
        # Get nameservers
        nameservers = []
        if isinstance(w.name_servers, list):
            nameservers = [ns.strip() for ns in w.name_servers]
        
        # Extract registrar info
        registrar = None
        if isinstance(w.registrar, str):
            registrar = w.registrar.strip() if w.registrar else None
        elif isinstance(w.registrar, list):
            registrar = w.registrar[0].strip() if w.registrar else None
        if not registrar:
            registrar = "Unknown"
        
        return {
            "domain": domain,
            "registrar": registrar,
            "created": created_str,
            "expires": expires_str,
            "age": age_info,
            "nameservers": nameservers,
            "registrar_url": w.name if hasattr(w, 'name') and w.name else None,
            "status": w.status if hasattr(w, 'status') else None
        }
        
    except ImportError:
        return {"error": "python-whois module not installed"}
    except Exception as e:
        return {"error": str(e)}


def check_ssl(url):
    """Check SSL/TLS configuration."""
    parsed = urlparse(url)
    host = parsed.hostname
    if not host or parsed.scheme != "https":
        return {"error": "URL must be https://"}
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                issuer = dict((k, v) for k, v in cert.get("issuer", []))
                subject = dict((k, v) for k, v in cert.get("subject", []))
                valid_from = cert["notBefore"]
                valid_to = cert["notAfter"]
                days = datetime.datetime.fromtimestamp(int(valid_to)).toordinal() - datetime.datetime.now().toordinal()
                return {
                    "ssl": True,
                    "issuer": issuer,
                    "subject": subject,
                    "valid_from": valid_from,
                    "valid_to": valid_to,
                    "days": days
                }
    except Exception as e:
        return {"error": str(e)}


def check_redirect(url, timeout):
    """Check redirects, report entire chain with status codes."""
    try:
        # Make request following redirects
        resp = requests.get(url, timeout=timeout, allow_redirects=True)

        if resp.history:
            # Build chain from redirect history
            chain = []
            for r in resp.history:
                chain.append({
                    "url": r.url,
                    "status": r.status_code,
                    "location": r.headers.get("Location", None)
                })
            # Add final destination
            chain.append({
                "url": resp.url,
                "status": resp.status_code,
                "location": None
            })
            return {"redirect_chain": chain}
        else:
            # No redirects
            return {"final_url": resp.url, "status": resp.status_code}
    except Exception as e:
        return {"error": str(e)}


def check_robots(url):
    """Check robots.txt content."""
    parsed = urlparse(url)
    robots_url = f"https://{parsed.netloc}/robots.txt"
    try:
        resp = requests.get(robots_url, timeout=TIMEOUT)
        return {"content": resp.text, "status": resp.status_code}
    except Exception as e:
        return {"error": str(e)}


def check_sitemap(url):
    """Check sitemap presence and count."""
    parsed = urlparse(url)
    host = parsed.netloc
    try:
        resp = requests.get(f"https://{host}/sitemap.xml", timeout=TIMEOUT)
        urls = re.findall(r'<url>\s*<loc>(.*?)</loc>', resp.text)
        return {"urls": urls, "count": len(urls)}
    except Exception as e:
        return {"error": str(e)}


def check_cms(url):
    """Check for CMS via HTTP headers and content."""
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        html = resp.text
        headers = resp.headers
        cms = None
        for pattern in [r'WordPress', r'WooCommerce', r'Joomla', r'CakePHP', r'Drupal']:
            if pattern.lower() in html.lower() or pattern.lower() in headers.get("x-generator", "").lower():
                cms = pattern
                break
        return {"cms_detected": cms, "cms_checked": {"WordPress": False, "WooCommerce": False, "Joomla": False, "CakePHP": False, "Drupal": False}}
    except Exception as e:
        return {"error": str(e)}


def check_www(url):
    """Check www vs non-www redirect."""
    parsed = urlparse(url)
    host = parsed.netloc
    if not host:
        return {"error": "Invalid URL"}
    try:
        if host.startswith("www."):
            target = "https://" + host[4:]
        else:
            target = "https://www." + host
        resp = requests.get(target, timeout=TIMEOUT, allow_redirects=False)
        return {"redirect_to": resp.headers.get("Location", None), "status": resp.status_code}
    except Exception as e:
        return {"error": str(e)}


def check_encoding(url):
    """Check content encoding."""
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        return {"charset": resp.encoding}
    except Exception as e:
        return {"error": str(e)}


def run_full_audit(url):
    """Run all checks and return results."""
    print(f"\n=== AUDIT STARTED: {url} ===")
    checks = [
        {"domain_info": check_domain(url)},
        {"cms": check_cms(url)},
        {"redirect": check_redirect(url, TIMEOUT)},
        {"robots": check_robots(url)},
        {"sitemap": check_sitemap(url)},
        {"www": check_www(url)},
        {"charset": check_encoding(url)},
        {"ssl": check_ssl(url)}
    ]
    for c in checks:
        for k, v in c.items():
            print(f"  {k}: {v}")
    print("=== AUDIT COMPLETED ===\n")
    return {"url": url, "checks": checks}