#!/usr/bin/env python3
"""Apply the KoraCraft Studio Edition 02 overlay after extracting the original source archive."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
home = root / "marketplace/templates/marketplace/home.html"
css_path = root / "koracraft_project/static/marketplace/css/app.css"
js_path = root / "koracraft_project/static/marketplace/js/app.js"
marker = "/* KoraCraft Studio Edition 02 — progressive enhancement layer */"
html = home.read_text()

if 'data-excellence-version="2"' not in html:
    replacements = [
        ('<meta name="theme-color" content="#171914">', '<meta name="theme-color" content="#151810"><meta name="color-scheme" content="light"><meta name="application-name" content="KoraCraft Studio Edition">'),
        ("<title>KoraCraft — Africa's Makers. Your Style.</title>", "<title>KoraCraft Studio Edition — Africa's Makers. Your Style.</title>"),
        ('data-backend-auth="1" data-authenticated=', 'data-excellence-version="2" data-backend-auth="1" data-authenticated='),
        ('<h1>Find your style.<br><em>Meet your maker.</em></h1>', '<h1>A world of craft.<br><em>A style of your own.</em></h1>'),
        ('Explore the marketplace <span>↗</span>', 'Explore the collection <span>↗</span>'),
        ('<div class="hero-note"><span>01 / 03</span><span>CRAFT MEETS CULTURE</span></div>', '<div class="hero-note"><span>STUDIO EDITION / 02</span><span>CRAFT MEETS CULTURE</span></div>\n        <div class="kc-float-card kc-float-card-top"><span class="kc-float-icon">✳</span><span><strong>Made with intention</strong><small>Details worth discovering</small></span></div>\n        <div class="kc-float-card kc-float-card-bottom"><span class="kc-pulse-dot"></span><span><strong>Find your kind of craft</strong><small>Explore shoes, clothing & textiles</small></span><b>↗</b></div>'),
        ('This static preview demonstrates the interface; real accounts require the Django backend and configured credentials.', 'Email verification, Google sign-in and payment collection will be introduced in a later release.')
    ]
    for old, new in replacements:
        if old not in html:
            raise SystemExit("Expected KoraCraft template anchor missing: " + old[:90])
        html = html.replace(old, new, 1)

    trust_close = '<span>Local craft. Global possibility.</span></p></div>'
    proof = '\n        <div class="hero-proof-row" aria-label="KoraCraft marketplace values"><div><span class="proof-icon">✳</span><span><strong>Craft first</strong><small>Made with intention</small></span></div><div><span class="proof-icon">↗</span><span><strong>Meet the maker</strong><small>Shop more personally</small></span></div><div><span class="proof-icon">◈</span><span><strong>Make it yours</strong><small>Discover custom work</small></span></div></div>'
    if trust_close not in html:
        raise SystemExit("Hero trust close marker missing")
    html = html.replace(trust_close, trust_close + proof, 1)
    home.write_text(html)

css = css_path.read_text()
if marker not in css:
    css_path.write_text(css + "\n" + Path(__file__).with_name("excellence.css").read_text())

js = js_path.read_text()
js_marker = "KoraCraft Studio Edition 02: lightweight progressive motion"
if js_marker not in js:
    js_path.write_text(js + "\n" + Path(__file__).with_name("excellence.js").read_text())


# Guard against stale DB sockets after Neon/serverless idle periods. The app is
# on a small, scale-to-zero hosting setup, so validate fresh connections and
# avoid carrying them across long idle windows.
settings_path = root / "koracraft_project/settings.py"
settings = settings_path.read_text()
if "conn_max_age=600" in settings:
    settings = settings.replace("conn_max_age=600", "conn_max_age=0", 1)
elif "conn_max_age=0" not in settings:
    raise SystemExit("Expected DATABASE_URL connection-age setting not found")
health_anchor = "    )}\nelse:\n    DATABASES = {\"default\": {"
health_replacement = "    )}\n    DATABASES[\"default\"][\"CONN_HEALTH_CHECKS\"] = True\nelse:\n    DATABASES = {\"default\": {"
if "CONN_HEALTH_CHECKS" not in settings:
    if health_anchor not in settings:
        raise SystemExit("Expected DATABASES health-check insertion anchor not found")
    settings = settings.replace(health_anchor, health_replacement, 1)
old_logging = '''LOGGING = {
    "version": 1, "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"django.security": {"handlers": ["console"], "level": "WARNING", "propagate": False}},
}'''
new_logging = '''LOGGING = {
    "version": 1, "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django.security": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "django.db.backends": {"handlers": ["console"], "level": "WARNING", "propagate": False},
    },
}'''
if old_logging in settings:
    settings = settings.replace(old_logging, new_logging, 1)
elif '"django.request": {"handlers": ["console"], "level": "ERROR"' not in settings:
    raise SystemExit("Expected Django logging configuration not found")
settings_path.write_text(settings)

print("KoraCraft Studio Edition 02 assets applied.")
