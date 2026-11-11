"""Проверка meta viewport."""
import requests
from datetime import datetime, timezone


def check_viewport(url):
    """Проверка meta viewport для мобильных.

    Args:
        url: URL страницы

    Returns:
        dict с информацией о viewport (viewport_available, viewport_config)
    """
    result = {
        "url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "source": "Python requests",
        "viewport_available": None,
        "viewport_config": None,
        "error": None
    }

    try:
        response = requests.get(url, timeout=10)
        
        import re
        
        viewport_match = re.search(
            r'<meta[^>]*name\s*=\s*["\']viewport["\'][^>]*content\s*=\s*["\']([^"\']+)["\'][^>]*>',
            response.text, 
            re.IGNORECASE
        )
        
        if viewport_match:
            viewport_content = viewport_match.group(1)
            
            view_config = {}
            
            if 'width' in viewport_content:
                width_match = re.search(r'\bwidth\s*=\s*(\d+)', viewport_content)
                view_config["width"] = int(width_match.group(1)) if width_match else "device"
            
            result['viewport_available'] = True
            result['viewport_config'] = view_config
        
        result['viewport_available'] = bool(viewport_match)
        
    except Exception as e:
        result['error'] = f"Ошибка проверки viewport: {str(e)}"
    
    return result


__all__ = ["check_viewport"]