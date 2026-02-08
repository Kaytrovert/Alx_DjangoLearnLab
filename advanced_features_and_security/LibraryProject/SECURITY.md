# Security Measures Implemented

This document describes the security best practices configured in the LibraryProject Django application to protect against XSS, CSRF, SQL injection, and related vulnerabilities.

## 1. Secure Settings (settings.py)

### DEBUG and production
- **DEBUG** is read from the environment (`DJANGO_DEBUG`). Set `DJANGO_DEBUG=False` in production so tracebacks and debug tools are not exposed.
- **ALLOWED_HOSTS** is set from `ALLOWED_HOSTS` env when not in DEBUG (e.g. `localhost,127.0.0.1,yourdomain.com`).

### Browser and cookie security
- **SECURE_BROWSER_XSS_FILTER**: Enables the browser’s XSS filter (X-XSS-Protection: 1; mode=block). Applied via `SecurityHeadersMiddleware`.
- **X_FRAME_OPTIONS**: Set to `DENY` to prevent clickjacking (pages cannot be embedded in iframes). Handled by Django’s `XFrameOptionsMiddleware`.
- **SECURE_CONTENT_TYPE_NOSNIFF**: Set to `True` so the server sends X-Content-Type-Options: nosniff, preventing MIME-type sniffing. Handled by Django’s `SecurityMiddleware`.
- **CSRF_COOKIE_SECURE** and **SESSION_COOKIE_SECURE**: Set to `True` so CSRF and session cookies are only sent over HTTPS. Use HTTPS in production; for local HTTP testing you may temporarily set these to `False`.

## 2. CSRF Protection in Templates

All forms that submit via POST include the CSRF token so the server can reject cross-site requests:

- **{% csrf_token %}** is used in:
  - `relationship_app`: login.html, register.html, add_book.html, edit_book.html, delete_book.html
  - `bookshelf`: form_example.html

Django’s `CsrfViewMiddleware` validates the token on POST. Do not remove `{% csrf_token %}` from these templates.

## 3. Secure Data Access in Views (SQL injection and input validation)

- **No raw SQL with string formatting.** All database access uses the Django ORM (e.g. `Book.objects.filter(...)`, `get_object_or_404(Book, pk=pk)`). The ORM uses parameterized queries, which prevents SQL injection.
- **User input is validated and sanitized with Django forms:**
  - `bookshelf`: `BookForm`, `BookSearchForm` in `forms.py`; used in `form_example` and `book_list` (search).
  - `relationship_app`: `BookForm` in `forms.py`; used in `add_book` and `edit_book`.
- **Search/filter** in `book_list` uses `BookSearchForm` and ORM filters (e.g. `filter(title__icontains=query)`), not concatenated SQL.

## 4. Content Security Policy (CSP)

CSP headers are set in **LibraryProject/middleware.SecurityHeadersMiddleware** to reduce the risk of XSS by restricting where scripts, styles, and other resources can load:

- **CSP_*** settings in `settings.py`** define default-src, script-src, style-src, img-src, font-src, connect-src, and frame-ancestors.
- The middleware builds the `Content-Security-Policy` response header from these settings. Adjust `CSP_*` in `settings.py` as needed for your domains (e.g. CDNs).

## 5. Testing Recommendations

- **CSRF**: Submit forms without the token or with a wrong token; expect 403.
- **XSS**: Ensure template variables are rendered with Django’s default auto-escaping (e.g. `{{ value }}`), and avoid `|safe` or `mark_safe` on user input unless strictly necessary.
- **SQL injection**: Use only the ORM and form-validated input; avoid `raw()`, `extra()`, or string-formatted SQL with user input.
- **Cookies**: In production, serve the site over HTTPS and keep `CSRF_COOKIE_SECURE` and `SESSION_COOKIE_SECURE` set to `True`.
