# app/checks/page_speed.py
import httpx
import os
from app.schemas.audit import PageSpeedResult

api_key = os.environ.get("GOOGLE_PAGESPEED_API_KEY")


async def check_page_speed(url: str) -> PageSpeedResult:
    clean = url.removeprefix("http://") \
                .removeprefix("https://") \
                .removeprefix("www.").split("/")[0]

    try:
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as tmp:
            api_url = (
                f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
                f"?url=https://{clean}&key={api_key}&strategy=mobile"
            )
            r = await tmp.get(api_url)

        data = r.json()
        if r.status_code != 200:
            return PageSpeedResult(ok=False, error=data.get("error", {}).get("message", "Unknown error"))

        performance_score = data["lighthouseResult"]["categories"]["performance"]["score"] * 100
        FCP_score = data["lighthouseResult"]["audits"]["first-contentful-paint"]["displayValue"]
        LCP_score = data["lighthouseResult"]["audits"]["largest-contentful-paint"]["displayValue"]
        TBT_score = data["lighthouseResult"]["audits"]["total-blocking-time"]["displayValue"]
        CLS_score = data["lighthouseResult"]["audits"]["cumulative-layout-shift"]["displayValue"]
        SI_score = data["lighthouseResult"]["audits"]["speed-index"]["displayValue"]

        return PageSpeedResult(
            ok=True,
            performance_score=performance_score,
            FCP=FCP_score,
            LCP=LCP_score,
            TBT=TBT_score,
            CLS=CLS_score,
            SI=SI_score,
        )

    except Exception as e:
        print(type(e), e)
        return PageSpeedResult(ok=False, error=str(type(e).__name__ + ": " + str(e)))
