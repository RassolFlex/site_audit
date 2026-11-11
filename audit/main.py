import requests
import re
import socket
import ssl as ssl_lib
import urllib.request
import urllib.parse
from datetime import datetime, timezone


def run_audit(url):
    """Run all audit checks on the URL."""
    results = {}
    
    try:
        results["domain_info"] = check_domain_info(url)
    except Exception as e:
        results["domain_info"] = {"error": str(e)}
    
    try:
        results["ssl"] = check_ssl(url)
    except Exception as e:
        results["ssl"] = {"error": str(e)}
    
    try:
        results["redirect"] = check_redirect(url)
    except Exception as e:
        results["redirect"] = {"error": str(e)}
    
    try:
        results["robots"] = check_robots(url)
    except Exception as e:
        results["robots"] = {"error": str(e)}
    
    try:
        results["sitemap"] = check_sitemap(url)
    except Exception as e:
        results["sitemap"] = {"error": str(e)}
    
    try:
        results["www"] = check_www(url)
    except Exception as e:
        results["www"] = {"error": str(e)}
    
    try:
        results["encoding"] = check_encoding(url)
    except Exception as e:
        results["encoding"] = {"error": str(e)}
    
    try:
        results["structure"] = check_structure(url)
    except Exception as e:
        results["structure"] = {"error": str(e)}
    
    try:
        results["metatags"] = check_metatags(url)
    except Exception as e:
        results["metatags"] = {"error": str(e)}
    
    try:
        results["images"] = check_images(url)
    except Exception as e:
        results["images"] = {"error": str(e)}
    
    try:
        results["social_signals"] = check_social_signals(url)
    except Exception as e:
        results["social_signals"] = {"error": str(e)}
    
    return results


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
    """Detect CMS with detailed checks for each CMS"""
    result = {
        "url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "cms_detected": None,
        "cms_checked": {
            "WordPress": False,
            "Joomla": False,
            "Drupal": False,
            "Tilda": False,
            "Wix": False,
            "Shopify": False,
            "Ghost": False,
            "Modx": False
        },
        "error": None
    }
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req, timeout=10)
        html = response.read().decode("utf-8", errors="ignore")
        
        # WordPress
        wp_markers = ["wp-content/", "wp-includes/", "/wp-json/"]
        if any(m in html for m in wp_markers):
            result["cms_checked"]["WordPress"] = True
            result["cms_detected"] = "WordPress"
        
        # Joomla
        joomla_markers = ["joomla!", "jf-user", "/templates/system/"]
        if any(m in html for m in joomla_markers) and not result["cms_detected"]:
            result["cms_checked"]["Joomla"] = True
            result["cms_detected"] = "Joomla"
        
        # Drupal
        drupal_markers = ["drupal", "views.js", "drupal.behaviors"]
        if any(m in html for m in drupal_markers) and not result["cms_detected"]:
            result["cms_checked"]["Drupal"] = True
            result["cms_detected"] = "Drupal"
        
        # Tilda
        tilda_markers = ["tilda.cc", "tildacms.com", "/tiles/"]
        if any(m in html for m in tilda_markers) and not result["cms_detected"]:
            result["cms_checked"]["Tilda"] = True
            result["cms_detected"] = "Tilda"
        
        # Wix
        wix_markers = ["wix.com", "wixstatic.com"]
        if any(m in html for m in wix_markers) and not result["cms_detected"]:
            result["cms_checked"]["Wix"] = True
            result["cms_detected"] = "Wix"
        
        # Shopify
        shopify_markers = ["shopify.com", "cdn.shopify.com"]
        if any(m in html for m in shopify_markers) and not result["cms_detected"]:
            result["cms_checked"]["Shopify"] = True
            result["cms_detected"] = "Shopify"
        
        # Ghost
        ghost_markers = ["ghost.io", "ghost-content"]
        if any(m in html for m in ghost_markers) and not result["cms_detected"]:
            result["cms_checked"]["Ghost"] = True
            result["cms_detected"] = "Ghost"
        
        # Modx
        modx_markers = ["/manager/", "MODX"]
        if any(m in html for m in modx_markers) and not result["cms_detected"]:
            result["cms_checked"]["Modx"] = True
            result["cms_detected"] = "Modx"
    except Exception as e:
        result["error"] = str(e)
    return result


def check_redirect(url):
    """Check redirects using requests library to capture redirect chain"""
    result = {
        "url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "has_redirect": False,
        "redirect_chain": [],
        "redirect_from": None,
        "redirect_to": None,
        "redirect_status": None,
        "error": None
    }
    try:
        # Use requests.get which follows redirects by default
        resp = requests.get(url, timeout=10, allow_redirects=True)
        
        # Check if there was any redirect history
        if resp.history:
            # First redirect
            first = resp.history[0]
            result["has_redirect"] = True
            result["redirect_from"] = first.url
            result["redirect_status"] = first.status_code
            result["redirect_to"] = first.headers.get("Location", None)
            
            # Build full redirect chain
            for r in resp.history:
                result["redirect_chain"].append({
                    "url": r.url,
                    "status": r.status_code,
                    "location": r.headers.get("Location", None)
                })
            # Add final response
            result["redirect_chain"].append({
                "url": resp.url,
                "status": resp.status_code,
                "location": None
            })
        else:
            # No redirect, just show final status
            result["redirect_chain"].append({
                "url": url,
                "status": resp.status_code,
                "location": None
            })
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def check_ssl(url):
    """Check SSL certificate"""
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "ssl_enabled": None, "certificate_expires": None, "error": None}
    try:
        parsed = urllib.parse.urlparse(url)
        host = parsed.netloc
        port = 443
        context = ssl_lib.create_default_context()
        with context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=host) as s:
            s.connect((host, port))
            cert = s.getpeercert()
            result["ssl_enabled"] = True
            result["certificate_expires"] = cert["notAfter"]
    except Exception as e:
        result["error"] = str(e)[:100]
        result["ssl_enabled"] = False
    return result


def check_speed(url):
    """Measure page load time"""
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "load_time_seconds": None, "error": None}
    try:
        import time
        start = time.time()
        urllib.request.urlopen(url, timeout=10)
        result["load_time_seconds"] = round(time.time() - start, 4)
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def check_structure(url):
    """Check basic HTML structure"""
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "h1_present": None, "h2_present": None, "error": None}
    try:
        response = urllib.request.urlopen(url, timeout=10)
        html = response.read().decode("utf-8", errors="ignore")
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
        html = response.read().decode("utf-8", errors="ignore")
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        result["title_present"] = bool(title_match and title_match.group(1).strip())
        desc_match = re.search(r'<meta\s+name="description"[^>]*content="(.*)?"', html, re.IGNORECASE)
        if not desc_match:
            desc_match = re.search(r'<meta\s+property="og:description"[^>]*content="(.*)?"', html, re.IGNORECASE)
        result["description_present"] = bool(desc_match and desc_match.group(1).strip())
        og_match = re.search(r'<meta\s+property="og:title"', html, re.IGNORECASE)
        result["og_tags_found"] = bool(og_match)
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def check_images(url):
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "images_with_alt": 0, "images_without_alt": 0, "total_images": 0, "error": None}
    try:
        response = urllib.request.urlopen(url, timeout=10)
        html = response.read().decode("utf-8", errors="ignore")
        img_tags = re.findall(r"<img[^>]*>", html, re.IGNORECASE)
        result["total_images"] = len(img_tags)
        for img in img_tags:
            if re.search(r"alt=", img, re.IGNORECASE):
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
        html = response.read().decode("utf-8", errors="ignore")
        result["og_tags_present"] = bool(re.search(r"<meta[^>]*property=", html, re.IGNORECASE))
        result["twitter_tags_present"] = bool(re.search(r'<meta[^>]*name="twitter:', html, re.IGNORECASE))
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def check_competitors(url):
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "competitors_found": None, "error": None}
    return result
