# app/checks/domain_age.py
import asyncio
import whois
from datetime import datetime, timezone
from app.schemas.audit import DomainAgeResult


async def check_domain_age(url: str) -> DomainAgeResult:
    clean = url.replace("http://", "").replace("https://", "").split("/")[0]
    bare = clean.removeprefix("www.")

    try:
        # whois — синхронная библиотека, запускаем в пуле потоков
        # asyncio.to_thread — аналог Django's sync_to_async
        data = await asyncio.to_thread(whois.whois, bare)

        creation = data.creation_date
        # whois иногда возвращает список дат
        if isinstance(creation, list):
            creation = creation[0]

        if not creation:
            return DomainAgeResult(ok=False, error="Creation date not found")

        age_years = round(
            (datetime.now(timezone.utc) - creation).days / 365.25, 1
        )

        return DomainAgeResult(
            ok=True,
            registered=creation.strftime("%Y-%m-%d"),
            age_years=age_years,
            registrar=data.registrar
        )
    except Exception as e:
        return DomainAgeResult(ok=False, error=str(e))
