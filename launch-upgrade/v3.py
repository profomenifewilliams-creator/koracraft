#!/usr/bin/env python3
"""KoraCraft Studio Edition 03 — page routing, seller form accessibility and motion."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
home_path = root / "marketplace/templates/marketplace/home.html"
base_path = root / "marketplace/templates/marketplace/base.html"
views_path = root / "marketplace/views.py"
urls_path = root / "koracraft_project/urls.py"
css_path = root / "koracraft_project/static/marketplace/css/app.css"
js_path = root / "koracraft_project/static/marketplace/js/app.js"
seller_path = root / "marketplace/templates/marketplace/seller_apply.html"

home = home_path.read_text()
if 'data-excellence-version="3"' not in home:
    home = home.replace('data-excellence-version="2"', 'data-excellence-version="3"', 1)
    home = home.replace('<a class="announce-link" href="#seller"', '<a class="announce-link" href="{% url \'seller_apply\' %}"')
    home = home.replace('<a href="#shop" class="btn-primary">Explore the collection <span>↗</span></a>', '<a href="{% url \'shop_catalog\' %}" class="btn-primary">Explore the collection <span>↗</span></a>')
    home = home.replace('<a href="#seller" class="btn-quiet">I\'m a maker <span>→</span></a>', '<a href="{% url \'seller_apply\' %}" class="btn-quiet">I\'m a maker <span>→</span></a>')
    home = home.replace('<a class="brand" href="#top"', '<a class="brand" href="{% url \'home\' %}"')
    home = home.replace('<button class="icon-btn search-open" aria-label="Search" title="Search">⌕</button>', '<a class="icon-btn" href="{% url \'shop_catalog\' %}" aria-label="Search products" title="Search">⌕</a>')
    home = home.replace('<button class="text-btn login-open">Sign in</button>', '<a class="text-btn" href="{% url \'login\' %}">Sign in</a>')
    home = home.replace('<button class="seller-btn" id="open-seller">Sell on KoraCraft <span>↗</span></button>', '<a class="seller-btn" href="{% url \'seller_apply\' %}">Sell on KoraCraft <span>↗</span></a>')
    home = home.replace('<button class="cart-btn" id="open-cart" aria-label="Open cart">Bag <span id="cart-count">0</span></button>', '<a class="cart-btn" href="{% url \'cart_view\' %}" aria-label="Open cart">Bag <span id="cart-count">0</span></a>')
    home = home.replace('<div class="mobile-nav" id="mobile-nav"><a href="#shop">Shop everything</a><a href="#categories">Categories</a><a href="#makers">Meet the makers</a><a href="#how">How it works</a><button class="login-open">Sign in / Create account</button></div>',
        '<div class="mobile-nav" id="mobile-nav"><a href="{% url \'shop_catalog\' %}">Shop everything</a><a href="{% url \'categories_page\' %}">Categories</a><a href="{% url \'makers_directory\' %}">Meet the makers</a><a href="{% url \'how_it_works\' %}">How it works</a><a href="{% url \'login\' %}">Sign in</a><a href="{% url \'register\' %}">Create account</a></div>')
    home = home.replace('<nav class="desktop-nav"><a href="#shop">Shop everything</a><a href="#categories">Categories</a><a href="#makers">Meet the makers</a><a href="#how">How it works</a></nav>',
        '<nav class="desktop-nav"><a href="{% url \'shop_catalog\' %}">Shop everything</a><a href="{% url \'categories_page\' %}">Categories</a><a href="{% url \'makers_directory\' %}">Meet the makers</a><a href="{% url \'how_it_works\' %}">How it works</a></nav>')
    replacements = [
      ('<button class="category-card cat-shoes" data-filter="Shoes">','<a class="category-card cat-shoes" href="{% url \'shop_catalog\' %}?category=shoes">'),
      ('<button class="category-card cat-tailor" data-filter="Clothing">','<a class="category-card cat-tailor" href="{% url \'shop_catalog\' %}?category=clothing">'),
      ('<button class="category-card cat-fabric" data-filter="Fabric">','<a class="category-card cat-fabric" href="{% url \'shop_catalog\' %}?category=fabric">'),
      ('<button class="category-card cat-custom" data-filter="Custom">','<a class="category-card cat-custom" href="{% url \'shop_catalog\' %}?category=custom">'),
      ('</div></button>\n        <button class="category-card cat-tailor"', '</div></a>\n        <a class="category-card cat-tailor"'),
      ('</div></button>\n        <button class="category-card cat-fabric"', '</div></a>\n        <a class="category-card cat-fabric"'),
      ('</div></button>\n        <button class="category-card cat-custom"', '</div></a>\n        <a class="category-card cat-custom"'),
      ('</div></button>\n      </div>\n    </section>', '</div></a>\n      </div>\n    </section>'),
      ('<button class="filter-tab active" data-filter="All">Everything <span>{{ products|length }}</span></button><button class="filter-tab" data-filter="Shoes">Shoes</button><button class="filter-tab" data-filter="Clothing">Clothing</button><button class="filter-tab" data-filter="Fabric">Fabric</button><button class="filter-tab" data-filter="Custom">Custom-made</button>',
       '<a class="filter-tab active" href="{% url \'shop_catalog\' %}">Everything <span>{{ products|length }}</span></a><a class="filter-tab" href="{% url \'shop_catalog\' %}?category=shoes">Shoes</a><a class="filter-tab" href="{% url \'shop_catalog\' %}?category=clothing">Clothing</a><a class="filter-tab" href="{% url \'shop_catalog\' %}?category=fabric">Fabric</a><a class="filter-tab" href="{% url \'shop_catalog\' %}?category=custom">Custom-made</a>'),
      ('<div class="shop-controls"><label class="search-box"><span>⌕</span><input id="product-search" type="search" placeholder="Search pieces, makers..." aria-label="Search products"></label><select id="sort-products" aria-label="Sort products"><option value="featured">Sort: Featured</option><option value="low">Price: Low to high</option><option value="high">Price: High to low</option></select></div>',
       '<form class="shop-controls kc-shop-route-form" action="{% url \'shop_catalog\' %}" method="get"><label class="search-box"><span>⌕</span><input id="product-search-route" name="q" type="search" placeholder="Search pieces, makers..." aria-label="Search products"></label><label class="kc-sort-label"><span class="sr-only">Sort products</span><select id="sort-products-route" name="sort" aria-label="Sort products"><option value="featured">Sort: Featured</option><option value="price-low">Price: Low to high</option><option value="price-high">Price: High to low</option></select></label><button class="kc-route-search" type="submit">Search ↗</button></form>'),
      ('<a href="#seller" class="btn-lime">Meet the maker community <span>↗</span></a>', '<a href="{% url \'makers_directory\' %}" class="btn-lime">Meet the maker community <span>↗</span></a>'),
      ('<button class="btn-primary" id="seller-join">Start selling for free <span>↗</span></button>', '<a class="btn-primary" href="{% url \'seller_apply\' %}">Start selling for free <span>↗</span></a>'),
      ('<a href="#how" class="btn-quiet">How seller shops work →</a>', '<a href="{% url \'how_it_works\' %}" class="btn-quiet">How seller shops work →</a>'),
      ('<a href="#shop">Marketplace</a><a href="#categories">Categories</a><a href="{% url \'custom_request\' %}">Custom commission</a><a href="#makers">Our makers</a>',
       '<a href="{% url \'shop_catalog\' %}">Marketplace</a><a href="{% url \'categories_page\' %}">Categories</a><a href="{% url \'custom_request\' %}">Custom commission</a><a href="{% url \'makers_directory\' %}">Our makers</a>'),
      ('<a href="#seller">Open a shop</a><a href="#how">How it works</a><a href="#seller">Seller standards</a>',
       '<a href="{% url \'seller_apply\' %}">Open a shop</a><a href="{% url \'how_it_works\' %}">How it works</a><a href="{% url \'how_it_works\' %}#seller-standards">Seller standards</a>'),
      ('<a href="{% url \'contact_us\' %}">Contact support</a><a href="#how">FAQs</a><a href="#top">Safety & trust</a>',
       '<a href="{% url \'contact_us\' %}">Contact support</a><a href="{% url \'how_it_works\' %}#faq">FAQs</a><a href="{% url \'privacy_policy\' %}">Safety & trust</a>'),
      ('<a class="brand brand-footer" href="#top"', '<a class="brand brand-footer" href="{% url \'home\' %}"')
    ]
    for old, new in replacements:
        if old not in home:
            # Anchors may be split by whitespace formatting; make other required fixes fail closed only.
            if old.startswith('</div></button>'):
                continue
            raise SystemExit("Studio Edition 03: expected homepage anchor missing: " + old[:100])
        home = home.replace(old, new, 1)
    # Convert the top categories, maker, and seller anchors to dedicated route links.
    home = home.replace('<a href="{% url \'home\' %}#categories"', '<a href="{% url \'categories_page\' %}"')
    home = home.replace('<a href="{% url \'home\' %}#makers"', '<a href="{% url \'makers_directory\' %}"')
    home = home.replace('<a href="{% url \'home\' %}#how"', '<a href="{% url \'how_it_works\' %}"')
    # Category cards are now anchors; close them as anchors too. Keep the
    # replacement scoped to the category grid so no unrelated buttons change.
    grid_start = home.find('<div class="category-grid">')
    grid_end = home.find('\\n      </div>\\n    </section>', grid_start)
    if grid_start < 0 or grid_end < 0:
        raise SystemExit("Studio Edition 03: category grid boundary missing")
    category_grid = home[grid_start:grid_end].replace('</button>', '</a>')
    home = home[:grid_start] + category_grid + home[grid_end:]
    home_path.write_text(home)

# The shared site header/footer used on all non-home routes also navigates to real pages.
base = base_path.read_text()
base = base.replace('<body data-backend-auth="1"', '<body data-excellence-version="3" data-backend-auth="1"', 1)
if "{% static 'marketplace/js/app.js' %}" not in base:
    base = base.replace("</body>", "<script src=\"{% static 'marketplace/js/app.js' %}\"></script></body>", 1)
base = base.replace('<a href="{% url \'home\' %}#categories">Categories</a>', '<a href="{% url \'categories_page\' %}">Categories</a>')
base = base.replace('<a href="{% url \'home\' %}#makers">Meet the makers</a>', '<a href="{% url \'makers_directory\' %}">Meet the makers</a>')
base = base.replace('<a href="{% url \'home\' %}#how">How it works</a>', '<a href="{% url \'how_it_works\' %}">How it works</a>')
base = base.replace('<a href="{% url \'home\' %}#makers">Our makers</a>', '<a href="{% url \'makers_directory\' %}">Our makers</a>')
base_path.write_text(base)

# Dedicated browse pages and a working sellers directory.
views = views_path.read_text()
if "def categories_page(request):" not in views:
    views += '''

def categories_page(request):
    categories = list(Category.objects.filter(is_active=True).order_by("sort_order", "name"))
    for category in categories:
        category.active_product_count = Product.objects.filter(
            category=category, status="active", seller__status="active"
        ).count()
    return render(request, "marketplace/categories.html", {"categories": categories})


def makers_directory(request):
    sellers = list(Seller.objects.filter(status="active").order_by("is_demo", "shop_name"))
    for seller in sellers:
        seller.active_product_count = Product.objects.filter(
            seller=seller, status="active"
        ).count()
    return render(request, "marketplace/makers.html", {"sellers": sellers})


def how_it_works(request):
    return render(request, "marketplace/how_it_works.html")
'''
    views_path.write_text(views)

urls = urls_path.read_text()
route_marker = '    path("", views.home, name="home"),'
if "name=\"categories_page\"" not in urls:
    if route_marker not in urls:
        raise SystemExit("Studio Edition 03: URL insertion anchor missing")
    urls = urls.replace(route_marker, route_marker + '''
    path("categories/", views.categories_page, name="categories_page"),
    path("makers/", views.makers_directory, name="makers_directory"),
    path("how-it-works/", views.how_it_works, name="how_it_works"),''', 1)
    urls_path.write_text(urls)

# Ship the new pages with the original code bundle, so every build reproduces them.
extra_templates = Path(__file__).with_name("templates")
template_target = root / "marketplace/templates/marketplace"
for name in ("categories.html", "makers.html", "how_it_works.html"):
    source = extra_templates / name
    if not source.is_file():
        raise SystemExit("Studio Edition 03 page template missing: " + name)
    (template_target / name).write_text(source.read_text())

# Seller registration is a dedicated, normally scrollable page—not a clipped modal.
seller = seller_path.read_text()
seller = seller.replace('<section class="plain-card plain-card-wide">', '<section class="plain-card plain-card-wide seller-application-page">')
seller = seller.replace('<p class="plain-intro">Tell us about your business. The team will review your details before approving the shop for public listings.</p>',
'''<p class="plain-intro">Tell us about your business. The team will review your details before approving the shop for public listings.</p>
<div class="kc-seller-step-row" aria-label="Seller application steps"><span><b>01</b> Business details</span><span><b>02</b> Review by KoraCraft</span><span><b>03</b> Set up your shop</span></div>''')
seller = seller.replace('<form method="post" class="plain-form">', '<form method="post" class="plain-form kc-seller-form" autocomplete="on">')
seller_path.write_text(seller)

css = css_path.read_text()
css_marker = "/* KoraCraft Studio Edition 03 — 3D routes and accessible page loading */"
css_source = Path(__file__).with_name("excellence-v3.css").read_text()
if css_marker not in css:
    css_path.write_text(css + "\n" + css_source)

js = js_path.read_text()
js_marker = "KoraCraft Studio Edition 03: routed navigation, skeleton bubbles and card links"
js_source = Path(__file__).with_name("excellence-v3.js").read_text()
if js_marker not in js:
    js_path.write_text(js + "\n" + js_source)

print("KoraCraft Studio Edition 03 applied: full-page seller flow, dedicated browse pages, motion and route loading.")
