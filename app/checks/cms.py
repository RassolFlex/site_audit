# app/checks/cms.py
import httpx
from app.schemas.audit import CMSResult

# Сигнатуры CMS: заголовки, пути, куки, мета-теги
CMS_SIGNATURES = {
    "WordPress": {
        "headers": {"x-powered-by": "WordPress"},
        "cookies": {"wordpress_logged_in", "wp-settings"},
        "body_markers": [
            "/wp-content/",
            "/wp-includes/",
            'name="generator" content="WordPress'
        ],
    },
    "Bitrix": {
        "headers": {},
        "cookies": {"BITRIX_SM_LOGIN", "BX_USER_ID"},
        "body_markers": ["/bitrix/", "BX.ready"],
    },
    "Tilda": {
        "headers": {},
        "cookies": set(),
        "body_markers": ["tilda.ws", "tildacdn.com"],
    },
    "1C-UMI": {
        "headers": {},
        "cookies": set(),
        "body_markers": ["umi.ru", "/umi/"],
    },
    "Drupal": {
        "headers": {"x-generator": "Drupal"},
        "cookies": {"Drupal.visitor"},
        "body_markers": ["/sites/default/files/", "Drupal.settings"],
    },
    "Joomla": {
        "headers": {},
        "cookies": set(),
        "body_markers": ["/components/com_", "/media/jui/", "Joomla!"],
    },
}


async def check_cms(url: str) -> CMSResult:
    clean = url.replace("http://", "").replace("https://", "").split("/")[0]

    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as tmp:
            r = await tmp.get(f"https://{clean}")

        body = r.text.lower()
        headers = {k.lower(): v.lower() for k, v in r.headers.items()}
        cookies = set(r.cookies.keys())

        best_hits = 0
        best_cms = None

        for cms_name, sig in CMS_SIGNATURES.items():
            hits = 0

            # Проверяем заголовки
            for h_key, h_val in sig["headers"].items():
                if h_key in headers and h_val in headers[h_key]:
                    hits += 2  # заголовки — сильный сигнал

            # Проверяем куки
            for cookie in sig.get("cookies", set()):
                if cookie.lower() in {c.lower() for c in cookies}:
                    hits += 2

            # Проверяем тело страницы
            for marker in sig["body_markers"]:
                if marker.lower() in body:
                    hits += 1

            if hits > best_hits:
                best_hits = hits
                best_cms = cms_name

        if best_hits > 0:
            confidence = "high" if best_hits >= 3 else "low"
            return CMSResult(ok=True, cms=best_cms, confidence=confidence)

        return CMSResult(ok=True, cms=None, confidence=None)

    except Exception as e:
        return CMSResult(ok=False, error=str(e))
