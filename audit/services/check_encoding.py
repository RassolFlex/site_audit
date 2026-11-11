"""Проверка кодировки страниц."""
import requests
from datetime import datetime, timezone


def check_encoding(url):
    """Проверка кодировки страницы.

    Args:
        url: URL страницы

    Returns:
        dict с информацией о кодировке (charset_declared, charset_used, is_utf8)
    """
    result = {
        "url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "source": "Python requests",
        "charset_declared": None,
        "charset_used": None,
        "is_utf8": None,
        "error": None
    }

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=10, headers=headers)
        
        # 1. Проверка meta charset в head
        import re
        
        charset_declared = None
        
        if '<meta' in response.text.lower():
            meta_charset = re.search(
                r'<meta[^>]*charset\s*=\s*["\']([^"\']+)["\'][^>]*>', 
                response.text, 
                re.IGNORECASE
            )
            if meta_charset:
                charset_declared = meta_charset.group(1).lower()
            
            # Или в content-type заголовке
            content_type = response.headers.get('Content-Type', '')
            if 'charset=' in content_type.lower():
                charset_declared = content_type.split('charset=')[1].split(';')[0].strip().lower()
        
        # 2. Реальная кодировка текста (detected by Python)
        charset_used = response.encoding
        
        result['charset_declared'] = charset_declared
        result['charset_used'] = charset_used
        result['is_utf8'] = charset_used in ['utf-8', 'utf8', None]
        
    except Exception as e:
        result['error'] = f"Ошибка проверки кодировки: {str(e)}"
    
    return result


__all__ = ["check_encoding"]