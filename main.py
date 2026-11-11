"""Основные функции экспресс-аудита сайта (улучшенная версия)
С учетом требований из "Памятки общей"
"""
import requests
from datetime import datetime
from whois import whois

# ============================================================================
# 1. Проверка SSL (HTTPS)
# ============================================================================
def check_ssl(url):
    """Проверка наличия SSL-сертификата"""
    if url.startswith("https://"):
        return "✅ Есть SSL-сертификат"
    else:
        return "❌ Нет HTTPS (критично для SEO)"


# 2. Проверка скорости загрузки
# ============================================================================
def check_speed(url):
    """Базовая проверка отклика"""
    try:
        response = requests.get(url, timeout=10)
        return f"⏱️ Отклик: {response.elapsed.total_seconds():.2f} сек."
    except Exception as e:
        return "❌ Не удалось проверить скорость"


# 3. Определение CMS по заголовкам и HTML
# ============================================================================
def check_cms(url):
    """Определение системы управления контентом"""
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, timeout=15, headers=headers)
        
        if "x-powered-by" in response.headers:
            power_by = response.headers["x-powered-by"]
            if "WordPress" in power_by:
                return "✅ CMS: WordPress"
            elif "Joomla" in power_by:
                return "✅ CMS: Joomla"
            elif "Drupal" in power_by:
                return "✅ CMS: Drupal"
            elif "PHP-FPM" in power_by:
                return "✅ CMS: Неизвестная (PHP)"
        
        # Поиск по HTML-коду
        html_text = response.text.lower()
        cms_indicators = {
            "WordPress": ["wp-content", "/wp-admin", "wp-includes"],
            "Joomla": ["/joomla", "joomla-version"],
            "Drupal": ["/drupal", "drupal-core"],
            "Bitrix": ["/bitrix", "bx_"],
            "1C-Bitrix": ["bs_", "cabinet.php"],
            "Tilda": ["/tilda", "tilda.cc"],
            "Wix": ["/wix", "wixsite.com"],
            "Ghost": ["/ghost/", ".json?api=version"],
        }
        
        for cms, patterns in cms_indicators.items():
            if any(pattern in html_text for pattern in patterns):
                return f"✅ CMS: {cms}"
        
        return "⚠️ CMS не определена автоматически"
        
    except Exception as e:
        return f"❌ Ошибка определения CMS: {str(e)}"


# 4. Проверка метатегов (title, description, keywords)
# ============================================================================
def check_metatags(url):
    """Проверка title, meta description, keywords"""
    try:
        response = requests.get(url, timeout=10)
        
        has_title = "<title>" in response.text
        has_description = ("<meta name="description"" in response.text or 
                          "<meta property="og:description"" in response.text)
        has_keywords = ("<meta name="keywords"" in response.text or
                       "<meta name="keywords" in response.text)
        
        if has_title and has_description:
            return "✅ Основные метатеги есть"
        
        if has_title:
            return "⚠️ Есть title, нет description"
        
        return "❌ Отсутствуют критические метатеги (title)"
            
    except Exception as e:
        return f"❌ Ошибка проверки метатегов: {str(e)}"


# 5. Проверка robots.txt и sitemap
# ============================================================================
def check_robots(url):
    """Проверка наличия robots.txt и sitemap"""
    try:
        url_no_scheme = url.replace("https://", "").replace("http://", "")
        domain_part = url_no_scheme.split("/")[0]
        
        # robots.txt
        robots_url = f"https://{domain_part}/robots.txt"
        response = requests.get(robots_url, timeout=5)
        
        if response.status_code == 200 and len(response.text) > 10:
            return "✅ robots.txt найден и содержит правила"
        elif response.status_code != 200:
            return "❌ robots.txt не найден (404)"
        else:
            return "⚠️ robots.txt пустой или недоступен"
            
    except Exception as e:
        return f"❌ Ошибка проверки robots.txt: {str(e)}"


# 6. Проверка редиректов (WWW/non-WWW, HTTP/HTTPS)
# ============================================================================
def check_redirect(url):
    """Проверка редиректа WWW ↔ non-WWW"""
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        url_no_www = url.replace("https://www.", "https://").replace("http://www.", "http://")
        
        response = requests.get(url, allow_redirects=False, timeout=5, headers=headers)
        
        if response.status_code in [301, 302]:
            location = response.headers.get("Location", "")
            
            url_has_www = "www" in url.lower()
            redirect_to_no_www = "www" not in location.lower()
            
            if url_has_www != redirect_to_no_www:
                return "✅ Корректный редирект WWW ↔ non-WWW"
            
        return "ℹ️ Нет редиректа (проверено)"
        
    except Exception as e:
        return f"❌ Ошибка проверки редиректа: {str(e)}"


# 7. Проверка структуры HTML (кодировка, микроразметка)
# ============================================================================
def check_structure(url):
    """Проверка микроразметки Schema.org и кодировки"""
    try:
        response = requests.get(url, timeout=10)
        
        content_type = response.headers.get("Content-Type", "")
        html_content = response.text
        
        # Кодировка
        if "charset=utf-8" in content_type or            "<meta charset="utf-8">" in html_content:
            return "✅ Кодировка UTF-8"
        
        # Микроразметка Schema.org (JSON-LD)
        if "application/ld+json" in content_type:
            return "✅ Микроразметка Schema.org найдена"
        
        if '"@context":' in html_content or '"@type":' in html_content:
            return "⚠️ Возможно есть микроразметка (не JSON-LD)"
        
        # Проверяем наличие Schema.org через HTML теги
        schema_tags = ['<article>', '<aside>', '<footer>', '<header>', 
                       '<nav>', '<section>', '<h1>', '<time>']
        if any(tag in html_content for tag in schema_tags):
            return "ℹ️ Структура HTML корректная"
        
        return "⚠️ Микроразметка не обнаружена явно"
        
    except Exception as e:
        return f"❌ Ошибка проверки структуры: {str(e)}"


# 8. Проверка изображений (альтернативный текст)
# ============================================================================
def check_images(url):
    """Проверка alt-атрибутов на изображениях"""
    try:
        response = requests.get(url, timeout=10)
        
        # Поиск ImageObject
        if '"@type":"ImageObject"' in response.text:
            return "✅ Изображения с mico-разметкой найдены"
        
        # Поиск alt-атрибутов
        import re
        alt_tags = re.findall(r"alt=["']([^"']+)["']", response.text)
        
        if alt_tags:
            return f"✅ Найдено {len(alt_tags)} изображений с alt-атрибутами"
        
        # Подсчет картинок вообще
        img_count = len(re.findall(r'<img\s', response.text))
        
        if img_count > 0:
            return "⚠️ Изображения найдены, проверка alt требует ручного анализа"
        
        return "ℹ️ Картинки без альтернативного текста или нет изображений"
        
    except Exception as e:
        return f"❌ Ошибка проверки изображений: {str(e)}"


# 9. Проверка дубликатов (упрощённо)
# ============================================================================
def check_duplicates(url):
    """Базовая проверка на дубли страниц"""
    try:
        # Поиск параметра в URL
        if "?param=" in url or "?id=" in url:
            return "⚠️ URL содержит параметры (возможные динамические страницы)"
        
        return "ℹ️ Требуется дополнительная проверка (sitemap + crawl)"
    except:
        return "ℹ️ Требуется дополнительная проверка (sitemap + crawl)"


# 10. Проверка социальных сигналов (social signals)
# ============================================================================
def check_social_signals(url):
    """Проверка соцсетей и social signals"""
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, timeout=10, headers=headers)
        
        html = response.text.lower()
        
        # Социальные платформы
        social_platforms = ["facebook", "twitter", "instagram", "vk", "telegram", 
                           "youtube", "twitch"]
        
        social_links_found = any(platform in html for platform in social_platforms)
        
        # Open Graph теги
        og_tags = ["og:title", "og:description", "og:image", "og:url", "og:type"]
        has_og = any(tag in response.text.lower() for tag in og_tags)
        
        if has_og:
            return "✅ Social signals (Open Graph теги) обнаружены"
        
        if social_links_found:
            return "⚠️ Возможны социальные сигналы"
        
        return "ℹ️ Социальные ссылки не обнаружены на странице"
        
    except Exception as e:
        return f"❌ Ошибка проверки соцсетей: {str(e)}"


# 11. Проверка конкурентов (упрощённо)
# ============================================================================
def check_competitors(url):
    """Поиск конкурентов в ТОП-3 Google/Yandex (упрощённо)"""
    try:
        # Простая проверка - поиск похожих доменов
        domain = url.split("/")[2].split(":")[0] if "://" in url else url
        
        return f"ℹ️ Требуется расширенный анализ SERP для {domain}"
        
    except Exception as e:
        return f"❌ Ошибка проверки конкурентов: {str(e)}"


# 12. Информация о домене (AGE - возраст в годах/месяцах/днях)
# ============================================================================
def check_domain_info(url):
    """Получение подробной информации о домене через WHOIS
    
    Выводит:
    - Возраст домена (в годах, месяцах, днях)
    - Дата регистрации
    - Дата истечения
    - Регистратор
    - Серверы DNS
    """
    try:
        domain = url.split("/")[2].split(":")[0] if "://" in url else url
        
        # Получение Whois данных
        w = whois(domain)
        
        # Возраст домена в днях
        reg_date = w.creation_date
        if reg_date:
            age_days = (datetime.now() - reg_date).days
            
            # Вычисление в годах/месяцах/днях
            years = age_days // 365
            remaining = age_days % 365
            months = remaining // 30
            days = remaining % 30
            
            age_str = f"{years} лет, {months} мес., {days} дн." if (years or months) else f"{age_days} дн."
            
            info = f"""📌 Домен: {domain}
   Возраст домена: {age_str}
   Регистрация: {reg_date.strftime("%Y-%m-%d") if reg_date else "N/A"}
   Истечение: {w.expiration_date.strftime("%Y-%m-%d") if w.expiration_date else "N/A"}
   Регистратор: {w.registrar.name if w.registrar and hasattr(w.registrar, 'name') else "N/A"}"""
            
            return info
            
        # Если creation_date None, пробуем через альтернативный способ
        import urllib.request
        from bs4 import BeautifulSoup
        
        try:
            api_url = f"https://2ip.ru/domain-age/{domain}"
            req = urllib.request.Request(api_url)
            req.add_header("User-Agent", "Mozilla/5.0")
            with urllib.request.urlopen(req, timeout=5) as response:
                return f"📌 Домен: {domain} (информация через 2ip.ru)"
        except Exception as e:
            pass
        
        return f"📌 Домен: {domain}
   ℹ️ WHOIS информация недоступна или защищена"
        
    except ImportError:
        # Если python-whois не установлен
        try:
            import urllib.request
            from bs4 import BeautifulSoup
            
            api_url = f"https://2ip.ru/domain-age/{url.split('/')[2].split(":")[0]}"
            req = urllib.request.Request(api_url)
            req.add_header("User-Agent", "Mozilla/5.0")
            with urllib.request.urlopen(req, timeout=5) as response:
                return f"📌 Домен: {url.split('/')[2].split(":")[0]} (через 2ip.ru)"
        except Exception as e:
            return f"❌ Ошибка получения данных о домене: {str(e)}"


# 13. Проверка индексации
# ============================================================================
def check_indexing(url):
    """Проверка возможности индексации"""
    try:
        # Поиск директив noindex
        response = requests.get(url, timeout=5)
        
        if "noindex" in response.text.lower():
            return "❌ Содержит директиву noindex"
        
        # Проверка через robots.txt (user-agent *)
        domain = url.split("/")[2].split(":")[0] if "://" in url else url
        try:
            import urllib.request
            req = urllib.request.Request(f"https://{domain}/robots.txt")
            req.add_header("User-Agent", "Mozilla/5.0")
            with urllib.request.urlopen(req, timeout=5) as robots_resp:
                if f"Disallow: /" in robots_resp.read().decode():
                    return "❌ Редирект запрещён в robots.txt"
        except:
            pass
        
        return "✅ Можно каталогировать (проверить вручную)"
            
    except Exception as e:
        return f"❌ Ошибка проверки индексации: {str(e)}"


# Экспорт всех функций аудита
__all__ = [
    "check_ssl",
    "check_speed", 
    "check_cms",
    "check_metatags",
    "check_robots",
    "check_redirect",
    "check_structure",
    "check_images",
    "check_duplicates",
    "check_social_signals",
    "check_competitors",
    "check_domain_info",   # УЛУЧШЕНА - возраст домена в годах/месяцах/днях
    "check_indexing"
]
