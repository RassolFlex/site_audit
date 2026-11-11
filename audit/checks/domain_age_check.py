"""Domain age check for Django audit application."""
import urllib.request
import urllib.parse
from datetime import datetime, timezone


def check_domain_age(url):
    """Check domain age using WHOIS."""
    clean = url.replace("http://", "").replace("https://", "").split("/")[0]
    bare = clean.replace("www.", "")

    result = {
        "url": url,
        "registered": None,
        "age_years": None,
        "registrar": None
    }

    try:
        whois_url = f"https://whois.domaintools.com/{bare}"
        req = urllib.request.Request(whois_url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        response = urllib.request.urlopen(req, timeout=10)
        data = json.loads(response.read().decode("utf-8"))

        creation = data.get("creationDate")
        if creation:
            dt = datetime.fromisoformat(creation)
            age = (datetime.now(timezone.utc) - dt).days / 365.25
            result["registered"] = creation
            result["age_years"] = round(age, 1)

    except Exception as e:
        result["error"] = str(e)

    return result


import json