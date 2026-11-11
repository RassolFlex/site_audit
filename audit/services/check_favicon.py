"""Проверка наличия favicon."""
import requests
from datetime import datetime, timezone


def check_favicon(url):
    """Проверка наличия favicon.

    Args:
        url: URL сайта

    Returns:
        dict с информацией о наличии favicon (favicon_found, favicon_url)
    """
    result = {
        "url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "source": "Python requests",
        "favicon_found": None,
        "favicon_url": None,
        "http_status": None,
        "error": None
    }

    try:
        standard_paths = [
            f"{url.rstrip('/')}/favicon.ico",
            f"{url.rstrip('/')}/images/favicon.ico",
            f"{url.rstrip('/')}/img/favicon.ico"
        ]
        
        headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'image/x-icon,*/*'}
        
        found = False
        
        for path in standard_paths:
            try:
                response = requests.head(path, timeout=5, headers=headers)
                
                if response.status_code == 200 or response.status_code == 404:
                    result['favicon_found'] = True
                    result['favicon_url'] = path
                    result['http_status'] = response.status_code
                    found = True
                    break
                
            except Exception:
                pass
        
        if not found:
            result['favicon_found'] = False
            result['error'] = "Favicon не найден в стандартных путях"
        
    except Exception as e:
        result['error'] = f"Ошибка проверки favicon: {str(e)}"
    
    return result


__all__ = ["check_favicon"]