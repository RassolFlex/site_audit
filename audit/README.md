# ExpresAudit - Быстрый экспресс-аудит сайтов

## Описание

Библиотека для проведения экспресс-аудита веб-сайтов с использованием Python. Проводит проверки SSL/HTTPS, редиректов, метатегов, robots.txt, структуры HTML и микроразметки Schema.org.

## Функции

### check_ssl(url)
Проверка SSL/HTTPS соединения и редиректов HTTP→HTTPS.

**Параметры:**
- `url` - URL сайта для проверки

**Возвращает:** dict с полями:
- `https_available` - True/False
- `cert_valid` - валидность сертификата
- `redirect_http_to_https` - наличие редиректа HTTP→HTTPS
- `error` - ошибка при проверке (если есть)

### check_redirect(url)
Проверка редиректов www/non-www и других перенаправлений.

**Параметры:**
- `url` - URL сайта

**Возвращает:** dict с полями:
- `redirect_chain` - список редиректов в цепочке
- `final_url` - итоговый URL после редиректов
- `http_status` - HTTP статус коды

### check_metatags(url)
Проверка наличия и правильности метатегов.

**Параметры:**
- `url` - URL сайта

**Возвращает:** dict с полями:
- `title_present` - наличие тег<title>
- `description_present` - наличие meta description/og:description
- `keywords_present` - наличие meta keywords
- `og_tags_found` - наличие Open Graph тегов

### check_robots(url)
Проверка наличия и содержимого robots.txt.

**Параметры:**
- `url` - URL сайта

**Возвращает:** dict с полями:
- `robots_file_exists` - наличие файла robots.txt
- `disallows_found` - наличие директив disallow
- `allows_found` - наличие директив allow

### check_structure(url)
Проверка структуры HTML и микроразметки Schema.org.

**Параметры:**
- `url` - URL сайта

**Возвращает:** dict с полями:
- `has_schemaorg` - наличие JSON-LD разметки
- `schema_types` - типы сущностей в JSON-LD
- `has_microdata` - наличие HTML микроразметки

### check_images(url)
Проверка изображений и alt-атрибутов.

**Параметры:**
- `url` - URL сайта

**Возвращает:** dict с полями:
- `images_with_alt` - количество изображений с alt
- `total_images` - общее количество изображений
- `has_wide_alt_coverage` - покрытие (80% считается хорошим)

### check_indexing(url)
Проверка noindex директив.

**Параметры:**
- `url` - URL сайта

**Возвращает:** dict с полями:
- `has_noindex` - наличие noindex тегов
- `can_be_indexed` - возможность индексации страницы

## Использование

```python
from audit.main import *

url = 'https://example.com'

# Выполнение всех проверок
result_ssl = check_ssl(url)
result_redirect = check_redirect(url)
result_metatags = check_metatags(url)
result_robots = check_robots(url)
result_structure = check_structure(url)
result_images = check_images(url)
result_indexing = check_indexing(url)

# Вывод результатов
print(result_ssl)
```

## Требования

- Python 3.6+
- requests (уже установлен)

