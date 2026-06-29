# app/services/audit_service.py
import asyncio
from app.checks.ssl import check_ssl
from app.checks.cms import check_cms
from app.checks.redirect import check_redirect
from app.checks.domain_age import check_domain_age
from app.checks.page_speed import check_page_speed
from app.schemas import audit


async def audit_site(url: str) -> audit.AuditResponse:
    ssl, cms, redirect, domain_age, page_speed = await asyncio.gather(
        check_ssl(url),
        check_cms(url),
        check_redirect(url),
        check_domain_age(url),
        check_page_speed(url),
        return_exceptions=True   # не роняем всё если один чек упал
    )

    return audit.AuditResponse(
        url=url,
        ssl=ssl,
        cms=cms,
        redirect=redirect,
        domain_age=domain_age,
        page_speed=page_speed,
    )


async def audit_ssl(url: str) -> audit.SSLResult:
    return await check_ssl(url)

async def audit_cms(url: str) -> audit.CMSResult:
    return await check_cms(url)

async def audit_redirect(url: str) -> audit.RedirectResult:
    return await check_redirect(url)

async def audit_domain_age(url: str) -> audit.DomainAgeResult:
    return await check_domain_age(url)

async def audit_pagespeed(url: str) -> audit.PageSpeedResult:
    return await check_page_speed(url)
