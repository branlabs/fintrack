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

# Cache each HTML asset individually so we can serve different shells.
PORTAL_HTML_CACHE: dict[str, tuple[str, int]] = {}
PORTAL_CSS: str | None = None
PORTAL_CSS_MTIME: int | None = None


def _get_html_source(html_filename: str) -> str:
    """
    Return cached HTML for the requested page, refreshing the cache when needed.
    """
    html_path = PORTAL_DIR / html_filename
    html_mtime = html_path.stat().st_mtime_ns
    cached = PORTAL_HTML_CACHE.get(html_filename)

    if cached is None or cached[1] != html_mtime:
        html_source = html_path.read_text(encoding="utf-8")
        PORTAL_HTML_CACHE[html_filename] = (html_source, html_mtime)
        return html_source

    return cached[0]


def _get_css_source() -> str:
    """
    Return cached CSS, refreshing automatically when the source file changes.
    """
    global PORTAL_CSS, PORTAL_CSS_MTIME

    css_path = PORTAL_DIR / "app.css"
    css_mtime = css_path.stat().st_mtime_ns

    if PORTAL_CSS is None or PORTAL_CSS_MTIME != css_mtime:
        PORTAL_CSS = css_path.read_text(encoding="utf-8")
        PORTAL_CSS_MTIME = css_mtime

    assert PORTAL_CSS is not None
    return PORTAL_CSS


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


def render_portal(html_filename: str = "index.html") -> str:
    """
    Inject the CSS into the HTML so Django can return a single document.
    """
    portal_html = _get_html_source(html_filename)
    portal_css = _get_css_source()

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


def investment_portal(request):
    """
    Serve the investment shell so the UI chrome stays consistent.
    """
    return HttpResponse(render_portal("investment.html"), content_type="text/html")
