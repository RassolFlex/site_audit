import re, socket, ssl as ssl_lib, urllib.request, urllib.parse
from datetime import datetime, timezone

content = """import re
import socket
import ssl as ssl_lib
import urllib.request
import urllib.parse
from datetime import datetime, timezone


def check_domain_info(url):
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "scheme": None, "host": None, "path": None, "error": None}
    try:
        parsed = urllib.parse.urlparse(url)
        result["scheme"] = parsed.scheme
        result["host"] = parsed.netloc
        result["path"] = parsed.path
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def check_cms(url):
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "cms_detected": None, "error": None}
    try:
        response = urllib.request.urlopen(url, timeout=10)
        html = response.read().decode('utf-8', errors='ignore')
        if 'wp-content' in html.lower():
            result["cms_detected"] = "WordPress"
        elif 'joomla!' in html.lower() or 'jf-user' in html.lower():
            result["cms_detected"] = "Joomla"
        elif 'drupal' in html.lower():
            result["cms_detected"] = "Drupal"
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def check_indexing(url):
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "indexed": None, "error": None}
    return result


def check_redirect(url):
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "redirects_to": None, "error": None}
    try:
        response = urllib.request.urlopen(url, timeout=10)
        if response.url != url:
            result["redirects_to"] = response.url
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def check_ssl(url):
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "ssl_enabled": None, "certificate_expires": None, "error": None}
    try:
        parsed = urllib.parse.urlparse(url)
        host = parsed.netloc
        context = ssl_lib.create_default_context()
        with socket.create_connection((host, 443), timeout=10) as sock:
            ssl_sock = context.wrap_socket(sock, server_hostname=host)
            cert = ssl_sock.getpeercert()
            result["ssl_enabled"] = True
            result["certificate_expires"] = cert.get('notAfter', 'Unknown')
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def check_speed(url):
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "load_time_seconds": None, "error": None}
    try:
        start = datetime.now(timezone.utc)
        response = urllib.request.urlopen(url, timeout=10)
        response.read()
        elapsed = datetime.now(timezone.utc) - start
        result["load_time_seconds"] = elapsed.total_seconds()
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def check_structure(url):
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "h1_present": None, "h2_present": None, "error": None}
    try:
        response = urllib.request.urlopen(url, timeout=10)
        html = response.read().decode('utf-8', errors='ignore')
        h1_match = re.search(r"<h1[^>]*>", html, re.IGNORECASE)
        h2_match = re.search(r"<h2[^>]*>", html, re.IGNORECASE)
        result["h1_present"] = bool(h1_match)
        result["h2_present"] = bool(h2_match)
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def check_metatags(url):
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "title_present": None, "description_present": None, "og_tags_found": None, "error": None}
    try:
        response = urllib.request.urlopen(url, timeout=10)
        html = response.read().decode('utf-8', errors='ignore')
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        result["title_present"] = bool(title_match and title_match.group(1).strip())
        desc_match = (re.search(r'<meta\s+name=["\']description["\'][^>]*content=["\'](.*?)['"]', html, re.IGNORECASE) or
                       re.search(r'<meta\s+property=["\']og:description["\'][^>]*content=["\'](.*?)['"]', html, re.IGNORECASE))
        result["description_present"] = bool(desc_match and desc_match.group(1).strip()) if desc_match else False
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def check_images(url):
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "images_with_alt": 0, "images_without_alt": 0, "total_images": 0, "error": None}
    try:
        response = urllib.request.urlopen(url, timeout=10)
        html = response.read().decode('utf-8', errors='ignore')
        img_tags = re.findall(r'<img[^>]*>', html, re.IGNORECASE)
        result["total_images"] = len(img_tags)
        for img in img_tags:
            if re.search(r'alt=["\']', img, re.IGNORECASE):
                result["images_with_alt"] += 1
            else:
                result["images_without_alt"] += 1
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def check_robots(url):
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "robots_txt_exists": None, "error": None}
    try:
        robot_url = urllib.parse.urljoin(url, "/robots.txt")
        response = urllib.request.urlopen(robot_url, timeout=10)
        result["robots_txt_exists"] = True
    except urllib.error.HTTPError as e:
        result["robots_txt_exists"] = False
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def check_duplicates(url):
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "duplicate_titles": None, "error": None}
    return result


def check_social_signals(url):
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "og_tags_present": None, "twitter_tags_present": None, "error": None}
    try:
        response = urllib.request.urlopen(url, timeout=10)
        html = response.read().decode('utf-8', errors='ignore')
        result["og_tags_present"] = bool(re.search(r'<meta[^>]*property=["\']og:', html, re.IGNORECASE))
        result["twitter_tags_present"] = bool(re.search(r'<meta[^>]*name=["\']twitter:', html, re.IGNORECASE))
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def check_competitors(url):
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "competitors_found": None, "error": None}
    return result
"""

with open('D:/Python/site_audit/audit/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("File written successfully")
