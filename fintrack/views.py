from __future__ import annotations

from pathlib import Path

from django.http import HttpResponse

# Cache the static HTML/CSS content at import time so every request does not
# need to hit the filesystem.
BASE_DIR = Path(__file__).resolve().parent.parent
PORTAL_DIR = BASE_DIR / "web-portal"


def _load_portal_source() -> tuple[str, str]:
    html_source = (PORTAL_DIR / "index.html").read_text(encoding="utf-8")
    css_source = (PORTAL_DIR / "app.css").read_text(encoding="utf-8")
    return html_source, css_source


PORTAL_HTML, PORTAL_CSS = _load_portal_source()


def render_portal() -> str:
    """
    Inject the CSS into the HTML so Django can return a single document.
    """
    inline_css_tag = f"<style>{PORTAL_CSS}</style>"
    css_link_tag = '<link href="app.css" rel="stylesheet">'

    if css_link_tag in PORTAL_HTML:
        return PORTAL_HTML.replace(css_link_tag, inline_css_tag, 1)

    closing_head_tag = "</head>"
    if closing_head_tag in PORTAL_HTML:
        return PORTAL_HTML.replace(closing_head_tag, f"{inline_css_tag}{closing_head_tag}", 1)

    # Fallback: append styles at the top if head tag missing.
    return f"{inline_css_tag}{PORTAL_HTML}"


def web_portal(request):
    """
    Serve the FinTrack portal UI directly from Django without separate HTML/CSS files.
    """
    return HttpResponse(render_portal(), content_type="text/html")
