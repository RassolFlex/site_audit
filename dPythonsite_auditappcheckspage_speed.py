# app/checks/page_speed.py - Django sync версия (ТЗ)
import requests
import os
from datetime import datetime
from django.utils import timezone


API_KEY = os.environ.get("GOOGLE_PAGESPEED_API_KEY", "")


def check_page_speed(url: str):
    """Получение PageSpeed результатов для сайта через Google API (Django sync)."""
    
    clean = url.removeprefix("http://").removeprefix("https://")\
               .removeprefix("www.").split("/")[0]
    
    result = {
        "ok": False, "url": url, 
        "timestamp": timezone.now(), "error": None,
        **{"performance_score": 0, "FCP": 0, "LCP": 0, 
            "TBT": 0, "CLS": 0, "SI": 0},
    }
    
    if not API_KEY:
        result["error"] = "GOOGLE_PAGESPEED_API_KEY не настроен"
        return result
    
    try:
        api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?&url=https://{clean}&key={API_KEY}&strategy=mobile"
        response = requests.get(api_url, timeout=30, follow_redirects=True)
        
        if response.status_code != 200:
            result["error"] = f"API error {response.status_code}: {response.text[:100]}"
            return result
        
        data = response.json()
        lighthouse = data.get("lighthouseResult", {})
        
        perf_score = round(lighthouse["categories"]["performance"]["score"] * 100, 2) if "categories" in lighthouse else None
        fcp_audit = lighthouse.get("audits", {}).get("first-contentful-paint", {})
        lcp_audit = lighthouse.get("audits", {}).get("largest-contentful-paint", {})
        tbt_audit = lighthouse.get("audits", {}).get("total-blocking-time", {})
        cls_audit = lighthouse.get("audits", {}).get("cumulative-layout-shift", {})
        si_audit = lighthouse.get("audits", {}).get("speed-index", {})
        
        FCP = fcp_audit.get("displayValue") or 0 if isinstance(fcp_audit, dict) else fcp_audit
        LCP = lcp_audit.get("displayValue") or 0 if isinstance(lcp_audit, dict) else lcp_audit
        TBT = tbt_audit.get("displayValue") or 0 if isinstance(tbt_audit, dict) else tbt_audit
        CLS = cls_audit.get("displayValue") or 0 if isinstance(cls_audit, dict) else cls_audit
        SI = si_audit.get("displayValue") or 0 if isinstance(si_audit, dict) else si_audit
        
        result.update({"ok": True, "performance_score": perf_score, "FCP": FCP, "LCP": LCP, "TBT": TBT, "CLS": CLS, "SI": SI})
        
    except requests.exceptions.Timeout:
        result["error"] = "Timeout при запросе к Google PageSpeed API"
    except requests.exceptions.RequestException as e:
        result["error"] = f"Network error: {type(e).__name__}"
    except Exception as e:
        result["error"] = f"Error: {type(e).__name__}: {str(e)}"
    
    return result


def check_page_speed_desktop(url: str):
    """PageSpeed для desktop."""
    if not API_KEY:
        return {"ok": False, "error": "API ключ не настроен"}
    
    clean = url.removeprefix("http://").removeprefix("https://")\
               .removeprefix("www.").split("/")[0]
    
    try:
        api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?&url=https://{clean}&key={API_KEY}&strategy=desktop"
        response = requests.get(api_url, timeout=30, follow_redirects=True)
        
        if response.status_code != 200:
            return {"ok": False, "error": f"API error {response.status_code}"}
        
        data = response.json()
        lighthouse = data.get("lighthouseResult", {})
        
        perf_score = round(lighthouse["categories"]["performance"]["score"] * 100, 2) if "categories" in lighthouse else None
        
        fcp_audit = lighthouse.get("audits", {}).get("first-contentful-paint", {})
        lcp_audit = lighthouse.get("audits", {}).get("largest-contentful-paint", {})
        tbt_audit = lighthouse.get("audits", {}).get("total-blocking-time", {})
        cls_audit = lighthouse.get("audits", {}).get("cumulative-layout-shift", {})
        si_audit = lighthouse.get("audits", {}).get("speed-index", {})
        
        FCP = fcp_audit.get("displayValue") or 0 if isinstance(fcp_audit, dict) else fcp_audit
        LCP = lcp_audit.get("displayValue") or 0 if isinstance(lcp_audit, dict) else lcp_audit
        TBT = tbt_audit.get("displayValue") or 0 if isinstance(tbt_audit, dict) else tbt_audit
        CLS = cls_audit.get("displayValue") or 0 if isinstance(cls_audit, dict) else cls_audit
        SI = si_audit.get("displayValue") or 0 if isinstance(si_audit, dict) else si_audit
        
        return {"ok": True, "url": url, **{"performance_score": perf_score, "FCP": FCP, "LCP": LCP, "TBT": TBT, "CLS": CLS, "SI": SI}}
    
    except Exception as e:
        return {"ok": False, "error": f"Error: {e}"}


if __name__ == "__main__":
    import sys
    test_url = sys.argv[1] if len(sys.argv) > 1 else input("URL сайта для PageSpeed: ")
    
    if not test_url:
        print("Ошибка: URL не указан")
    else:
        print("\nPageSpeed (mobile):")
        result = check_page_speed(test_url)
        
        if result["ok"]:
            print(f"OK: {result['url']} | Score: {result['performance_score']:.2f}%")
            print(f"   FCP: {result.get('FCP', 'N/A')}ms | LCP: {result.get('LCP', 'N/A')}ms")
            print(f"   TBT: {result.get('TBT', 'N/A')}ms | CLS: {result.get('CLS', 'N/A')}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
