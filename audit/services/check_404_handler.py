"""Проверка обработки страниц 404."""
import requests
from datetime import datetime, timezone


def check_404_handling(url):
    """Проверка обработки страницы 404 (перенаправление на главную или user-friendly message).

    Args:
        url: URL сайта

    Returns:
        dict с информацией о ручании ошибок (handles_404_gracefully, redirects_to_home)
    """
    result = {
        "url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "source": "Python requests",
        "handles_404_gracefully": None,
        "redirects_to_home": None,
        "error_response_status": None,
        "error_html_length": 0,
        "user_friendly_message": None,
        "error": None
    }

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        # Создаём тестовую URL для проверки 404
        broken_url = f"{url.rstrip('/')}/nonexistent-page-test-12345"
        
        response = requests.get(broken_url, timeout=10, headers=headers)
        
        result['error_response_status'] = response.status_code
        
        if response.status_code == 404:
            # Проверяем перенаправление на главную
            location = response.headers.get('Location', '')
            
            if location and 'http://' in location.lower():
                home_base = url.rstrip('/').split('//')[1]  # http://example.com
                result['redirects_to_home'] = home_base in location
                
                # Проверяем пользовательское сообщение
                error_text = response.text
                has_friendly_msg = any(x in error_text.lower() for x in [
                    'page not found', 'not found', '404', 
                    'error 404', 'file not found', 'url not found'
                ])
                
                if has_friendly_msg:
                    result['user_friendly_message'] = "Есть пользовательское сообщение 404"
                else:
                    result['user_friendly_message'] = "Простой HTML или отсутствие сообщения"
            elif location:
                # Редирект на другую страницу (не домашнюю)
                result['error'] = f"Редирект на другую страницу: {location}"
        
        result['handles_404_gracefully'] = response.status_code == 404
        
    except Exception as e:
        result['error'] = f"Ошибка проверки 404: {str(e)}"
    
    return result


__all__ = ["check_404_handling"]