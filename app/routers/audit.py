# app/routers/audit.py
from fastapi import APIRouter
from app.services import audit_service
from app.schemas.audit import (
    AuditResponse,
    SSLResult,
    CMSResult,
    RedirectResult,
    DomainAgeResult,
    PageSpeedResult
)

router = APIRouter(prefix="/api/v1")


@router.get("/audit", response_model=AuditResponse)
async def audit(url: str) -> AuditResponse:
    return await audit_service.audit_site(url)

@router.get("/audit/ssl", response_model=SSLResult)
async def audit_ssl(url: str) -> SSLResult:
    return await audit_service.audit_ssl(url)

@router.get("/audit/cms", response_model=CMSResult)
async def audit_cms(url: str) -> CMSResult:
    return await audit_service.audit_cms(url)

@router.get("/audit/redirect", response_model=RedirectResult)
async def audit_redirect(url: str) -> RedirectResult:
    return await audit_service.audit_redirect(url)

@router.get("/audit/domain_age", response_model=DomainAgeResult)
async def audit_domain_age(url: str) -> DomainAgeResult:
    return await audit_service.audit_domain_age(url)

@router.get("/audit/pagespeed", response_model=PageSpeedResult)
async def audit_pagespeed(url: str) -> PageSpeedResult:
    return await audit_service.audit_pagespeed(url)
