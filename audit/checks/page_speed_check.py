"""Page speed check for Django audit application."""
import urllib.request
import urllib.parse
import json


def check_page_speed(url):
    """Check page speed using Google PageSpeed Insights API."""
    clean = url.replace("http://", "").replace("https://", "").split("/")[0]

    result = {
        "url": url,
        "performance_score": None,
        "FCP": None,
        "LCP": None,
        "TBT": None,
        "CLS": None,
        "SI": None
    }

    api_key = os.environ.get("GOOGLE_PAGESPEED_API_KEY", "")
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://{clean}&key={api_key}&strategy=mobile"

    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req, timeout=30)
        data = json.loads(response.read().decode("utf-8"))

        result["performance_score"] = data["lighthouseResult"]["categories"]["performance"]["score"] * 100
        result["FCP"] = data["lighthouseResult"]["audits"]["first-contentful-paint"]["displayValue"]
        result["LCP"] = data["lighthouseResult"]["audits"]["largest-contentful-paint"]["displayValue"]
        result["TBT"] = data["lighthouseResult"]["audits"]["total-blocking-time"]["displayValue"]
        result["CLS"] = data["lighthouseResult"]["audits"]["cumulative-layout-shift"]["displayValue"]
        result["SI"] = data["lighthouseResult"]["audits"]["speed-index"]["displayValue"]

    except Exception as e:
        result["error"] = str(e)

    return result


import os