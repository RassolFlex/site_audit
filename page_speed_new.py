# app/checks/page_speed.py - Django sync версия (ТЗ)
import requests
from datetime import datetime

import os
API_KEY = os.environ.get("GOOGLE_PAGESPEED_API_KEY", "")
from django.utils import timezone

    """Получение PageSpeed результатов для сайта через Google API (Django sync)."""
    clean = url.removeprefix("http://").removeprefix("https://")
def check_page_speed(url: str):
               .removeprefix("www.").split("/")[0]
        "ok": False, "url": url,
    result = {
        **{"performance_score": 0, "FCP": 0, "LCP": 0,
        "timestamp": timezone.now(), "error": None,
            "TBT": 0, "CLS": 0, "SI": 0},
    }
