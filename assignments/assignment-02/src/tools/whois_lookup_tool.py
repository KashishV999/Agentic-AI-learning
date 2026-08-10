from __future__ import annotations

from datetime import date, datetime
from typing import Any
from urllib.parse import urlparse

from agents import function_tool
from helper.debug_logging import debug_log, debug_tool_call, debug_tool_result


def _first_value(value: Any) -> Any:
    if isinstance(value, list):
        return value[0] if value else None
    return value


def _format_date(value: Any) -> str:
    value = _first_value(value)
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if value in (None, "", "None"):
        return "Unknown"
    return str(value)


def _normalize_domain(domain: str) -> str:
    candidate = domain.strip().lower()
    if "://" in candidate:
        candidate = urlparse(candidate).netloc or urlparse(candidate).path
    candidate = candidate.split("/")[0].strip()
    if candidate.startswith("www."):
        candidate = candidate[4:]
    return candidate


@function_tool
def whois_lookup_tool(domain: str) -> dict:
    """
    Look up WHOIS information for a domain and return normalized results.
    """
    normalized_domain = _normalize_domain(domain)
    debug_tool_call("whois_lookup_tool", domain=normalized_domain or domain)
    if not normalized_domain or "." not in normalized_domain or " " in normalized_domain:
        debug_tool_result("whois_lookup_tool", status="error", reason="invalid_domain")
        return {
            "status": "error",
            "domain": normalized_domain or domain,
            "message": "Invalid domain format. Provide a domain like example.com.",
        }

    try:
        import whois
    except ImportError:
        debug_tool_result("whois_lookup_tool", status="error", reason="missing_dependency")
        return {
            "status": "error",
            "domain": normalized_domain,
            "message": "python-whois is not installed in this environment.",
        }

    try:
        record = whois.whois(normalized_domain)
    except Exception as err:
        debug_log(f'whois_lookup_tool failed: domain="{normalized_domain}", error="{err}"')
        return {
            "status": "error",
            "domain": normalized_domain,
            "message": f"WHOIS lookup failed: {err}",
        }

    org = _first_value(getattr(record, "org", None)) or _first_value(getattr(record, "name", None)) or "Unknown"
    registrar = _first_value(getattr(record, "registrar", None)) or "Unknown"
    country = _first_value(getattr(record, "country", None)) or "Unknown"
    creation_date = _format_date(getattr(record, "creation_date", None))
    expiration_date = _format_date(getattr(record, "expiration_date", None))

    notes = []
    if org == "Unknown":
        notes.append("Registrant organization unavailable or privacy-redacted.")
    if creation_date == "Unknown":
        notes.append("Registration date unavailable; this weakens recency checks.")
    if registrar == "Unknown":
        notes.append("Registrar could not be confirmed.")

    result = {
        "status": "ok",
        "domain": normalized_domain,
        "registrant_organization": str(org),
        "registration_date": creation_date,
        "expiration_date": expiration_date,
        "registrar": str(registrar),
        "country": str(country),
        "notes": " ".join(notes) if notes else "WHOIS lookup completed successfully.",
    }
    debug_tool_result(
        "whois_lookup_tool",
        status=result["status"],
        domain=normalized_domain,
        registration_date=creation_date,
        registrar=registrar,
    )
    return result
