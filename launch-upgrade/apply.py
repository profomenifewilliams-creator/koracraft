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
    trust_old = '<div class="hero-trust"><div class="avatar-stack">'
    idx = html.find(trust_old)
    if idx == -1: raise SystemExit("Hero trust anchor missing")
    close = html.find('</div>', html.find('</p>', idx))
    # Insert proof row directly after the hero-trust component.
    end = html.find('</div>', close + 6)
    # The closing div following the paragraph closes hero-trust; add after that.
    if end == -1: raise SystemExit("Hero trust closing anchor missing")
    proof = '\n        <div class="hero-proof-row" aria-label="KoraCraft marketplace values"><div><span class="proof-icon">✳</span><span><strong>Craft first</strong><small>Made with intention</small></span></div><div><span class="proof-icon">↗</span><span><strong>Meet the maker</strong><small>Shop more personally</small></span></div><div><span class="proof-icon">◈</span><span><strong>Make it yours</strong><small>Discover custom work</small></span></div></div>'
    html = html[:end+6] + proof + html[end+6:]
    home.write_text(html)
css = css_path.read_text()
if marker not in css:
    css_path.write_text(css + "\n" + Path(__file__).with_name("excellence.css").read_text())
js = js_path.read_text()
js_marker = "KoraCraft Studio Edition 02: lightweight progressive motion"
if js_marker not in js:
    js_path.write_text(js + "\n" + Path(__file__).with_name("excellence.js").read_text())
print("KoraCraft Studio Edition 02 assets applied.")
