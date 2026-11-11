"""HTTPS redirect check for Django audit application."""
import urllib.request
import urllib.parse


def check_https(url):
    """Check if HTTP redirects to HTTPS."""
    clean = url.replace("http://", "").replace("https://", "").split("/")[0]

    result = {
        "url": url,
        "has_https_redirect": None,
        "final_url": None
    }

    try:
        req = urllib.request.Request(f"http://{clean}", headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req, timeout=8)
        final_url = response.url

        result["has_https_redirect"] = final_url.startswith("https://")
        result["final_url"] = final_url

    except Exception as e:
        result["error"] = str(e)

    return result