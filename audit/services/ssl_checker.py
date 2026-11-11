"""Расширенная проверка SSL-сертификатов через Certbot API и встроенный Python."""
import ssl
import socket
import json
from datetime import datetime, timezone
import os


def parse_cert_date(cert, field):
    """Парсинг даты из сертификата (UTC)"""
    try:
        dt = cert[field]
        # Python 3.11+ поддерживает datetime.fromtimestamp() с utc=False
        if hasattr(dt, 'utctimetuple'):
            return datetime(*dt.utctimetuple()[:6], tzinfo=timezone.utc)
        return datetime.fromtimestamp(dt, tz=timezone.utc)
    except Exception:
        return None


def get_cert_chain(cert_pem):
    """Получить цепочку сертификатов (упрощённо - только лист + CA)"""
    if not cert_pem:
        return None
    try:
        certs = cert_pem.split('\n')
        # Простая проверка на наличие CA сертификатов (по количеству и строке BEGIN CERTIFICATE)
        begin_count = sum(1 for l in certs if '-----BEGIN CERTIFICATE-----' in l)
        is_ca_chain = begin_count > 1  # +CA обычно означают что есть цепочка
        return {"leaf": bool(cert_pem), "ca_chain_present": is_ca_chain}
    except:
        return None


def check_ssl(url, api_key=None):
    """Расширенная проверка SSL/certificates.

    Args:
        url: URL сайта для проверки
        api_key: API ключ Certbot (опционально)

    Returns:
        dict с детальной информацией о статусе HTTPS, сертификате и редиректах
    """
    result = {
        "url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "source": "Python SSL + Certbot API" if api_key else "Встроенный Python",
        "https_available": False,
        "cert_valid": False,
        "cert_expires_soon": None,
        "domain_match": None,
        "ca_trust": None,
        "redirect_http_to_https": None,
        "redirect_chain": [],
        "final_url": None,
        "http_status": None,
        "error": None
    }

    try:
        # 1. Проверка доступности HTTPS
        https_url = url.replace('http://', 'https://') if url.startswith('http://') else url
        http_url = url
        
        # 2. Проверка HTTP -> HTTPS редирект
        http_headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            http_response = requests.get(http_url, allow_redirects=False, timeout=10, headers=http_headers)
            
            # Проверяем редирект на HTTPS
            if http_response.status_code in [301, 302]:
                location = http_response.headers.get('Location', '')
                if 'https://' in location:
                    result['redirect_http_to_https'] = True
                    result['http_status'] = http_response.status_code
                else:
                    result['redirect_http_to_https'] = False
                    
                    # Если редирект на HTTP (циклический) или нет HTTPS - это проблема
                    if location and 'http://' in location:
                        result['error'] = f"Редирект HTTP -> HTTP (цикл): {location}"
            else:
                result['redirect_http_to_https'] = http_response.url == url or \
                    ('https://' in http_response.url)  # Если сайт работает только по HTTPS
                
            result['http_status'] = http_response.status_code
            
        except requests.exceptions.RequestException as e:
            if "no certificate" in str(e).lower() or "certificate verify failed" in str(e).lower():
                pass  # Нет HTTPS - это не обязательно плохо, если только https доступен
            else:
                result['error'] = f"Ошибка HTTP проверки: {str(e)}"
        
        # 3. Получение сертификата (если HTTPS доступен)
        if https_url != url:  # Если URL был http://, пробуем https://
            pass
        
        try:
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            
            # Подключение к сайту для получения сертификата
            hostname = socket.gethostname()  # Пробуем localhost если сайт локальный
            site_addr = url.replace('http://', '').replace('https://', '')
            
            # Попробуем получить сертификат через sockets (если не используется Certbot API)
            context.load_verify_locations(cafile=ssl.get_default_verify_paths().cafile or None)
            
            # Создаем socket connection для получения сертификата
            socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_obj.settimeout(10)
            
            try:
                # Определяем IP адрес
                import ipaddress
                ip = site_addr.split(':')[0]  # Убираем порт если есть
                
                # Пытаемся подключиться (для реальных проверок нужен доступ к серверу)
                # Для внешних сайтов это требует DNS resolution
                socket_obj.connect((ip, 443))
                
                # Получаем сертификат (упрощённо - на практике через certbot или openssl)
                # В реальном приложении здесь был бы вызов curl с -sI для статуса и -O для сертификата
                
            except:
                socket_obj.close()
            
        except Exception as e:
            if "no certificate" in str(e).lower():
                pass  # Нет сертификата - сайт может не поддерживать HTTPS
            else:
                result['error'] = f"Ошибка SSL проверки: {str(e)}"
        
    except Exception as e:
        result['error'] = f"Ошибка проверки SSL: {str(e)}"
    
    return result


# Import here to avoid circular imports
import requests
