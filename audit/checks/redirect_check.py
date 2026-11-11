"""Redirect check for Django audit application."""
import urllib.request
import urllib.parse


def check_redirect(url):
    """Check for www to non-www redirects."""
    clean = url.replace("http://", "").replace("https://", "").split("/")[0]
    www_url = f"http://www.{clean}"

    result = {
        "url": url,
        "has_www_redirect": None,
        "redirect_chain": []
    }

    try:
        req = urllib.request.Request(www_url, headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req, timeout=8)
        final_url = response.url

        # Check if www redirects to non-www
        has_redirect = "www." in clean and "www." not in final_url

        result["has_www_redirect"] = has_redirect
        result["redirect_chain"] = [www_url, final_url] if has_redirect else [www_url]

    except Exception as e:
        result["error"] = str(e)

    return result