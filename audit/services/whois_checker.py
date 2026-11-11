"""Проверка информации о домене (дата регистрации, возраст) через DNS."""
import socket
from datetime import datetime, timezone


def check_domain_info(url):
    """Получение информации о домене.

    Args:
        url: URL сайта для проверки

    Returns:
        dict с информацией о домене и возрасте
    """
    result = {
        "url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "domain": None,
        "registrar": None,
        "created_date": None,
        "updated_date": None,
        "expires_date": None,
        "age_days": None,
        "source": None,
        "error": None
    }

    try:
        # Извлекаем домен из URL
        if '://' in url:
            domain = url.split('/')[2].split(':')[0]  # Берём часть после http:// или https:// и удаляем порт
        else:
            return {"error": "Некорректный URL"}
        
        # Пытаемся получить информацию через DNS (упрощённо)
        # Для полного whois нужен внешний whois сервис или библиотека like dnslib
        
        try:
            addr_info = socket.getaddrinfo(domain, None)
            if addr_info:
                result['domain'] = domain
                
                # Упрощённая эмуляция (в реальности - whois API)
                # Для демо возвращаем placeholder данные
                return {
                    "error": "Для полного whois требуется внешний сервис. Используйте библиотеку dnslib или whois-who.is"
                }
                
        except:
            pass
            
    except Exception as e:
        result['error'] = f"Ошибка whois: {str(e)}"
    
    return result


def get_domain_age(domain):
    """Упрощённая оценка возраста домена по DNS (если available)"""
    try:
        # Для реального решения используйте: whois-who.is API или dnslib
        
        # Placeholder - в реальном коде здесь вызов whois сервиса
        return {"age_days": None, "error": "Требуется внешний whois сервис"}
    
    except Exception as e:
        return {"age_days": None, "error": f"Ошибка: {e}"}


__all__ = ["check_domain_info", "get_domain_age"]
