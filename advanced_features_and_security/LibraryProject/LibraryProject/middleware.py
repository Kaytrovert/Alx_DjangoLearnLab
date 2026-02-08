"""
Security middleware: X-XSS-Protection and Content-Security-Policy headers.
Reduces XSS risk by enabling browser XSS filter and restricting script/style sources.
"""

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security-related response headers:
    - X-XSS-Protection (when SECURE_BROWSER_XSS_FILTER is True)
    - Content-Security-Policy from CSP_* settings
    """

    def process_response(self, request, response):
        if getattr(settings, 'SECURE_BROWSER_XSS_FILTER', False):
            response['X-XSS-Protection'] = '1; mode=block'

        # Build Content-Security-Policy header from settings to reduce XSS risk.
        csp_parts = []
        if hasattr(settings, 'CSP_DEFAULT_SRC'):
            csp_parts.append("default-src " + " ".join(settings.CSP_DEFAULT_SRC))
        if hasattr(settings, 'CSP_SCRIPT_SRC'):
            csp_parts.append("script-src " + " ".join(settings.CSP_SCRIPT_SRC))
        if hasattr(settings, 'CSP_STYLE_SRC'):
            csp_parts.append("style-src " + " ".join(settings.CSP_STYLE_SRC))
        if hasattr(settings, 'CSP_IMG_SRC'):
            csp_parts.append("img-src " + " ".join(settings.CSP_IMG_SRC))
        if hasattr(settings, 'CSP_FONT_SRC'):
            csp_parts.append("font-src " + " ".join(settings.CSP_FONT_SRC))
        if hasattr(settings, 'CSP_CONNECT_SRC'):
            csp_parts.append("connect-src " + " ".join(settings.CSP_CONNECT_SRC))
        if hasattr(settings, 'CSP_FRAME_ANCESTORS'):
            csp_parts.append("frame-ancestors " + " ".join(settings.CSP_FRAME_ANCESTORS))
        if csp_parts:
            response['Content-Security-Policy'] = "; ".join(csp_parts)
        return response
