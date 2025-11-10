from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.http import HttpResponse


# Cache the static HTML/CSS content at import time so every request does not
# need to hit the filesystem.
BASE_DIR = Path(__file__).resolve().parent.parent
PORTAL_DIR = BASE_DIR / "web-portal"
STATIC_FAVICON_PLACEHOLDER = "{% static 'img/favicon.svg' %}"
STATIC_LOGO_PLACEHOLDER = "{% static 'img/logo.svg' %}"


def _load_portal_source() -> tuple[str, str]:
    html_source = (PORTAL_DIR / "index.html").read_text(encoding="utf-8")
    css_source = (PORTAL_DIR / "app.css").read_text(encoding="utf-8")
    return html_source, css_source


PORTAL_HTML: str | None = None
PORTAL_CSS: str | None = None
PORTAL_HTML_MTIME: int | None = None
PORTAL_CSS_MTIME: int | None = None


def _get_portal_source() -> tuple[str, str]:
    """
    Return cached HTML/CSS, refreshing automatically when the source files change.
    """
    global PORTAL_HTML, PORTAL_CSS, PORTAL_HTML_MTIME, PORTAL_CSS_MTIME

    html_path = PORTAL_DIR / "index.html"
    css_path = PORTAL_DIR / "app.css"
    html_mtime = html_path.stat().st_mtime_ns
    css_mtime = css_path.stat().st_mtime_ns

    if (
        PORTAL_HTML is None
        or PORTAL_CSS is None
        or PORTAL_HTML_MTIME != html_mtime
        or PORTAL_CSS_MTIME != css_mtime
    ):
        html_source, css_source = _load_portal_source()
        PORTAL_HTML = html_source
        PORTAL_CSS = css_source
        PORTAL_HTML_MTIME = html_mtime
        PORTAL_CSS_MTIME = css_mtime

    assert PORTAL_HTML is not None and PORTAL_CSS is not None
    return PORTAL_HTML, PORTAL_CSS


def _build_static_url(asset_path: str) -> str:
    """
    Convert a relative asset path into a usable STATIC_URL.
    """
    static_url = settings.STATIC_URL
    if not static_url.endswith("/"):
        static_url = f"{static_url}/"
    if not static_url.startswith(("http://", "https://", "//")):
        static_url = f"/{static_url.lstrip('/')}"
    return f"{static_url}{asset_path.lstrip('/')}"


def render_portal() -> str:
    """
    Inject the CSS into the HTML so Django can return a single document.
    """
    portal_html, portal_css = _get_portal_source()

    inline_css_tag = f"<style>{portal_css}</style>"
    css_link_tag = '<link href="app.css" rel="stylesheet">'

    document = portal_html.replace(
        STATIC_FAVICON_PLACEHOLDER, _build_static_url("img/favicon.svg")
    ).replace(
        STATIC_LOGO_PLACEHOLDER, _build_static_url("img/logo.svg")
    )

    if css_link_tag in document:
        return document.replace(css_link_tag, inline_css_tag, 1)

    closing_head_tag = "</head>"
    if closing_head_tag in document:
        return document.replace(closing_head_tag, f"{inline_css_tag}{closing_head_tag}", 1)

    # Fallback: append styles at the top if head tag missing.
    return f"{inline_css_tag}{document}"


def web_portal(request):
    """
    Serve the FinTrack portal UI directly from Django without separate HTML/CSS files.
    """
    return HttpResponse(render_portal(), content_type="text/html")
