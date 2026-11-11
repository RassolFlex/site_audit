"""CMS detection for Django audit application."""
import urllib.request
import urllib.parse


def check_cms(url):
    """Detect CMS using HTTP request and HTML content analysis."""
    result = {
        "url": url,
        "cms_detected": None,
        "cms_checked": {
            "WordPress": False,
            "Bitrix": False,
            "Tilda": False,
            "1C-UMI": False,
            "Drupal": False,
            "Joomla": False,
        }
    }

    clean = url.replace("http://", "").replace("https://", "").split("/")[0]
    full_url = f"https://{clean}"

    try:
        req = urllib.request.Request(full_url, headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req, timeout=10)
        html = response.read().decode("utf-8", errors="ignore").lower()
        headers = response.headers

        # WordPress
        wp_markers = ["/wp-content/", "/wp-includes/", "name=\"generator\" content=\"wordpress"]
        if any(m in html for m in wp_markers) or (headers.get("x-powered-by", "").lower() == "wordpress"):
            result["cms_detected"] = "WordPress"
            result["cms_checked"]["WordPress"] = True

        # Bitrix
        if not result["cms_detected"]:
            bitrix_markers = ["/bitrix/", "bx.ready"]
            if any(m in html for m in bitrix_markers):
                result["cms_detected"] = "Bitrix"
                result["cms_checked"]["Bitrix"] = True

        # Tilda
        if not result["cms_detected"]:
            tilda_markers = ["tilda.ws", "tildacdn.com"]
            if any(m in html for m in tilda_markers):
                result["cms_detected"] = "Tilda"
                result["cms_checked"]["Tilda"] = True

        # 1C-UMI
        if not result["cms_detected"]:
            umi_markers = ["umi.ru", "/umi/"]
            if any(m in html for m in umi_markers):
                result["cms_detected"] = "1C-UMI"
                result["cms_checked"]["1C-UMI"] = True

        # Drupal
        if not result["cms_detected"]:
            drupal_markers = ["/sites/default/files/", "drupal.settings"]
            if any(m in html for m in drupal_markers) or (headers.get("x-generator", "").lower() == "drupal"):
                result["cms_detected"] = "Drupal"
                result["cms_checked"]["Drupal"] = True

        # Joomla
        if not result["cms_detected"]:
            joomla_markers = ["/components/com_", "/media/jui/"]
            if any(m in html for m in joomla_markers):
                result["cms_detected"] = "Joomla"
                result["cms_checked"]["Joomla"] = True

    except Exception as e:
        result["error"] = str(e)

    return result