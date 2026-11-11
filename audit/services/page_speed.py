"""Проверка производительности через Google PageSpeed Insights API."""
import requests


def check_page_speed(url):
    """Синхронная проверка производительности сайта через PageSpeed API (mobile).

    Args:
        url: URL сайта для проверки

    Returns:
        dict с результатами или ошибкой
    """
    import os
    api_key = os.environ.get("GOOGLE_PAGESPEED_API_KEY", "")
    
    if not api_key:
        return {"ok": False, "error": "API ключ не настроен"}
    
    # Очистка URL (без http/https, www)
    clean = url.removeprefix("http://").removeprefix("https://").removeprefix("www.")
    
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://{clean}&key={api_key}&strategy=mobile"
    
    try:
        response = requests.get(api_url, timeout=30)
        
        if response.status_code != 200:
            return {"ok": False, "error": f"HTTP {response.status_code}"}
        
        data = response.json()
        lh = data.get("lighthouseResult", {})
        audits = lh.get("audits", {})
        
        ps = round(lh["categories"]["performance"]["score"] * 100, 2) if "categories" in lh else None
        FCP = audits.get("first-contentful-paint", {}).get("displayValue") or 0
        LCP = audits.get("largest-contentful-paint", {}).get("displayValue") or 0
        TBT = audits.get("total-blocking-time", {}).get("displayValue") or 0
        CLS = audits.get("cumulative-layout-shift", {}).get("displayValue") or 0
        SI = audits.get("speed-index", {}).get("displayValue") or 0
        
        return {"ok": True, "performance_score": ps, "FCP": FCP, "LCP": LCP, 
                "TBT": TBT, "CLS": CLS, "SI": SI}
        
    except Exception as e:
        return {"ok": False, "error": f"Error: {e}"}


def check_page_speed_desktop(url):
    """Синхронная проверка производительности сайта через PageSpeed API (desktop).

    Args:
        url: URL сайта для проверки

    Returns:
        dict с результатами или ошибкой
    """
    import os
    api_key = os.environ.get("GOOGLE_PAGESPEED_API_KEY", "")
    
    if not api_key:
        return {"ok": False, "error": "API ключ не настроен"}
    
    clean = url.removeprefix("http://").removeprefix("https://").removeprefix("www.")
    
    try:
        api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://{clean}&key={api_key}&strategy=desktop"
        response = requests.get(api_url, timeout=30)
        
        if response.status_code != 200:
            return {"ok": False, "error": f"HTTP {response.status_code}"}
        
        data = response.json()
        lh = data.get("lighthouseResult", {})
        audits = lh.get("audits", {})
        
        ps = round(lh["categories"]["performance"]["score"] * 100, 2) if "categories" in lh else None
        FCP = audits.get("first-contentful-paint", {}).get("displayValue") or 0
        LCP = audits.get("largest-contentful-paint", {}).get("displayValue") or 0
        TBT = audits.get("total-blocking-time", {}).get("displayValue") or 0
        CLS = audits.get("cumulative-layout-shift", {}).get("displayValue") or 0
        SI = audits.get("speed-index", {}).get("displayValue") or 0
        
        return {"ok": True, "performance_score": ps, "FCP": FCP, "LCP": LCP, 
                "TBT": TBT, "CLS": CLS, "SI": SI}
        
    except Exception as e:
        return {"ok": False, "error": f"Error: {e}"}


__all__ = ["check_page_speed", "check_page_speed_desktop"]
