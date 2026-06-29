# app/checks/ssl.py
import asyncio
from datetime import datetime
import ssl
import socket
from app.schemas.audit import SSLResult

context = ssl.create_default_context()


async def check_ssl(url: str) -> SSLResult:
    clean = url.removeprefix("http://") \
                .removeprefix("https://") \
                .removeprefix("www.").split("/")[0]

    try:
        def get_cert(hostname):
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    return ssock.getpeercert()

        cert = await asyncio.to_thread(get_cert, clean)
        issuer_dict = {item[0][0]: item[0][1] for item in cert.get("issuer", [])}
        issuer = issuer_dict.get("organizationName")
        not_after = cert.get('notAfter')
        days_left = (datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')-datetime.now()).days
        alt_names = [host[1] for host in cert.get("subjectAltName", [])]

        return SSLResult(
            ok=True,
            status={'issuer': issuer,
                    'not_after': not_after,
                    'days_left': days_left,
                    'covers_www': f"*.{clean}" in alt_names or f"www.{clean}" in alt_names,
                    'covers_all': [host[-1] for host in cert.get('subjectAltName')]},
        )

    except Exception as e:
        return SSLResult(ok=False, error=str(e))
