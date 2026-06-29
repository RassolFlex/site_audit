from pydantic import BaseModel
from typing import Optional


class SSLStatus(BaseModel):
    issuer: Optional[str] = None
    not_after: Optional[str] = None
    days_left: Optional[int] = None
    covers_www: Optional[bool] = None
    covers_all: Optional[list] = None


class SSLResult(BaseModel):
    ok: bool
    status: Optional[SSLStatus] = None
    error: Optional[str] = None


class CMSResult(BaseModel):
    ok: bool
    cms: Optional[str] = None  # "WordPress", "Bitrix", None если не определено
    confidence: Optional[str] = None  # "high" / "low"
    error: Optional[str] = None


class RedirectResult(BaseModel):
    ok: bool
    has_www_redirect: Optional[bool] = None
    redirect_chain: Optional[list[str]] = None
    error: Optional[str] = None


class DomainAgeResult(BaseModel):
    ok: bool
    registered: Optional[str] = None   # дата строкой "2015-03-21"
    age_years: Optional[float] = None
    registrar: Optional[str] = None
    error: Optional[str] = None


class PageSpeedResult(BaseModel):
    ok: bool
    performance_score: Optional[float] = None
    FCP: Optional[str] = None
    LCP: Optional[str] = None
    TBT: Optional[str] = None
    CLS: Optional[str] = None
    SI: Optional[str] = None
    error: Optional[str] = None


class AuditResponse(BaseModel):
    url: str
    ssl: SSLResult
    cms: CMSResult
    redirect: RedirectResult
    domain_age: DomainAgeResult
    page_speed: PageSpeedResult
