# app/checks/redirect.py
import httpx
from app.schemas.audit import RedirectResult


async def check_redirect(url: str) -> RedirectResult:
    clean = url.removeprefix("http://") \
                .removeprefix("https://") \
                .removeprefix("www.").split("/")[0]

    www_url = f"http://www.{clean}"

    try:
        # follow_redirects=True здесь, чтобы собрать цепочку
        async with httpx.AsyncClient(timeout=8, follow_redirects=True) as cl:
            r = await cl.get(www_url)

        # history содержит все промежуточные ответы
        chain = [str(resp.url) for resp in r.history] + [str(r.url)]

        # Редирект www->bare есть если:
        # 1. Цепочка длиннее 1 шага
        # 2. Итоговый URL без www
        has_redirect = len(r.history) > 0 and "www." not in str(r.url)

        return RedirectResult(
            ok=True,
            has_www_redirect=has_redirect,
            redirect_chain=chain
        )

    except Exception as e:
        return RedirectResult(ok=False, error=str(e))
