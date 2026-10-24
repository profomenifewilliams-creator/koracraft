#!/usr/bin/env python3
"""Studio Edition 04: account-specific dashboards and a cinematic store opening."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
views_path = root / "marketplace/views.py"
urls_path = root / "koracraft_project/urls.py"
base_path = root / "marketplace/templates/marketplace/base.html"
views = views_path.read_text()

def replace_fn(src, name, next_name, body):
    start = src.find("def " + name + "(")
    end = src.find("\ndef " + next_name + "(", start + 1)
    if start < 0 or end < 0:
        raise SystemExit("Studio Edition 04: missing function boundary: " + name)
    return src[:start] + body.rstrip() + src[end:]

helper = '''
def _attach_seller_application(user):
    """Create/link a seller workspace for applications matching this account."""
    application = SellerApplication.objects.filter(email__iexact=user.email).exclude(status="declined").order_by("-created_at").first()
    if not application:
        return Seller.objects.filter(user=user).first()
    if application.user_id != user.pk:
        application.user = user
        application.save(update_fields=["user"])
    location = (application.location or "").strip()
    city, country = (location.split(",", 1)[0].strip(), location.split(",", 1)[1].strip() or "Nigeria") if "," in location else (location, "Nigeria")
    seller, created = Seller.objects.get_or_create(user=user, defaults={
        "shop_name": application.business_name, "business_type": application.business_type,
        "city": city, "country": country, "status": "active" if application.status == "approved" else "pending",
        "is_verified": False, "is_demo": False,
    })
    if not created and seller.status == "pending" and application.status == "approved":
        seller.status = "active"
        seller.save(update_fields=["status", "updated_at"])
    if not created:
        changed = []
        if seller.status == "pending" and application.status == "approved":
            seller.status = "active"
            changed.append("status")
        if seller.shop_name != application.business_name:
            seller.shop_name = application.business_name
            seller.slug = ""
            changed.extend(["shop_name", "slug"])
        if seller.business_type != application.business_type:
            seller.business_type = application.business_type
            changed.append("business_type")
        if seller.city != city:
            seller.city = city
            changed.append("city")
        if seller.country != country:
            seller.country = country
            changed.append("country")
        if changed:
            seller.save(update_fields=list(dict.fromkeys(changed + ["updated_at"])))
    return seller


def _create_pending_seller_workspace(user, display_name=""):
    """Seller accounts get a workspace immediately, before their application."""
    existing = Seller.objects.filter(user=user).first()
    if existing:
        return existing
    name = (display_name or user.get_full_name() or user.username or "Maker").strip()
    first_name = name.split()[0] if name else "Maker"
    shop_name = (first_name + "'s Studio")[:120]
    return Seller.objects.create(
        user=user,
        shop_name=shop_name,
        business_type="other",
        status="pending",
        is_verified=False,
        is_demo=False,
    )


'''
if "def _attach_seller_application(user):" not in views:
    views = views.replace("def register_view(request):", helper + "def register_view(request):", 1)

register = '''
def register_view(request):
    if request.user.is_authenticated:
        return redirect("seller_dashboard" if Seller.objects.filter(user=request.user).exists() else "account_dashboard")
    form = RegisterForm(request.POST or None)
    account_type = (request.POST.get("account_type") or request.GET.get("account_type") or "buyer").lower()
    if account_type not in {"buyer", "seller"}:
        account_type = "buyer"
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            form.add_error("email", "An account with this email already exists. Sign in instead.")
        else:
            name = form.cleaned_data["name"].strip()
            base_username = email.split("@", 1)[0][:120] or "koracraft-user"
            username, index = base_username, 2
            while User.objects.filter(username=username).exists():
                username = f"{base_username[:110]}{index}"
                index += 1
            user = User.objects.create_user(username=username, email=email, password=form.cleaned_data["password"], first_name=name[:150], is_active=not settings.EMAIL_VERIFICATION_REQUIRED)
            if settings.EMAIL_VERIFICATION_REQUIRED:
                request.session["koracraft_new_account_type"] = account_type
                token_record = EmailVerificationToken.objects.update_or_create(user=user, defaults={"token": uuid.uuid4()})[0]
                verification_url = request.build_absolute_uri(reverse("verify_email", args=[token_record.token]))
                try:
                    send_mail("Confirm your KoraCraft email address", f"Hello {name},\\n\\nConfirm your KoraCraft email to activate your account: {verification_url}\\n\\nThis link expires in 24 hours.", settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
                    messages.success(request, "Your account was created. Check your email for the confirmation link before signing in.")
                except Exception:
                    messages.warning(request, "Your account was created but the confirmation email could not be sent. Check email configuration or use Resend confirmation.")
                return redirect("verification_sent")
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            request.session.pop("koracraft_cart_hydrated", None)
            seller = _attach_seller_application(user)
            if not seller and account_type == "seller":
                seller = _create_pending_seller_workspace(user, name)
            messages.success(request, "Welcome to KoraCraft. Your account is ready.")
            if request.POST.get("next") or request.GET.get("next"):
                return redirect(_valid_next(request, fallback="seller_dashboard" if seller else "account_dashboard"))
            if seller:
                return redirect("seller_dashboard")
            return redirect("seller_apply" if account_type == "seller" else "account_dashboard")
    if request.method == "POST":
        messages.error(request, "Please check the registration details and try again.")
    return render(request, "marketplace/register.html", {"form": form, "account_type": account_type, "google_oauth_configured": bool(settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET)})
'''
views = replace_fn(views, "register_view", "verification_sent", register)

verify = '''
@require_http_methods(["GET", "POST"])
def verify_email(request, token):
    record = EmailVerificationToken.objects.select_related("user").filter(token=token).first()
    if not record:
        return render(request, "marketplace/email_verification.html", {"valid_token": False, "expired": False})
    if timezone.now() - record.created_at > timedelta(hours=24):
        record.delete()
        return render(request, "marketplace/email_verification.html", {"valid_token": False, "expired": True})
    if request.method == "POST":
        user = record.user
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])
        record.delete()
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        request.session.pop("koracraft_cart_hydrated", None)
        account_type = request.session.pop("koracraft_new_account_type", "buyer")
        seller = _attach_seller_application(user)
        if not seller and account_type == "seller":
            seller = _create_pending_seller_workspace(user, user.get_full_name())
        messages.success(request, "Your email is confirmed. Welcome to KoraCraft.")
        return redirect("seller_dashboard" if seller else ("seller_apply" if account_type == "seller" else "account_dashboard"))
    return render(request, "marketplace/email_verification.html", {"valid_token": True, "expired": False, "email": record.user.email})
'''
views = replace_fn(views, "verify_email", "resend_verification", verify)

login_fn = '''
def login_view(request):
    if request.user.is_authenticated:
        return redirect("seller_dashboard" if Seller.objects.filter(user=request.user).exists() else "account_dashboard")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"].strip().lower()
        password = form.cleaned_data["password"]
        user = User.objects.filter(email__iexact=email).first()
        authenticated = authenticate(request, username=user.username, password=password) if user else None
        if authenticated and authenticated.is_active:
            login(request, authenticated)
            request.session.pop("koracraft_cart_hydrated", None)
            seller = _attach_seller_application(authenticated)
            messages.success(request, "You're signed in.")
            if request.POST.get("next") or request.GET.get("next"):
                return redirect(_valid_next(request, fallback="seller_dashboard" if seller else "account_dashboard"))
            return redirect("seller_dashboard" if seller else "account_dashboard")
        form.add_error(None, "Those details didn't match an active account. Check them and try again.")
    if request.method == "POST" and not form.is_valid():
        messages.error(request, "Please enter a valid email and password.")
    return render(request, "marketplace/login.html", {"form": form, "google_oauth_configured": bool(settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET)})
'''
views = replace_fn(views, "login_view", "logout_view", login_fn)

apply_fn = '''
def seller_apply(request):
    form = SellerApplicationForm(request.POST or None, initial={"email": request.user.email} if request.user.is_authenticated else {})
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        if request.user.is_authenticated:
            if application.email.strip().casefold() != request.user.email.strip().casefold():
                form.add_error("email", "When signed in, use the email address attached to your KoraCraft account.")
            else:
                application.user = request.user
        if not form.errors:
            application.save()
            if request.user.is_authenticated:
                _attach_seller_application(request.user)
                messages.success(request, "Your seller application is saved. Your seller workspace is ready; public listings unlock after approval.")
                return redirect("seller_dashboard")
            messages.success(request, "Your application is saved. Register with the same email to access your seller workspace.")
            return redirect(reverse("register") + "?account_type=seller&next=%2Fseller%2Fdashboard%2F")
        messages.error(request, "Please check the seller application fields and try again.")
    return render(request, "marketplace/seller_apply.html", {"form": form})
'''
views = replace_fn(views, "seller_apply", "_uploads_have_durable_storage", apply_fn)

seller_dash = '''
@login_required
def seller_dashboard(request):
    seller = Seller.objects.filter(user=request.user).first() or _attach_seller_application(request.user)
    if not seller:
        applications = SellerApplication.objects.filter(Q(user=request.user) | Q(email__iexact=request.user.email)).order_by("-created_at")
        return render(request, "marketplace/seller_dashboard.html", {"seller": None, "applications": applications})
    profile_form = SellerProfileForm(request.POST or None, request.FILES or None, instance=seller)
    if request.method == "POST":
        if request.FILES and not _uploads_have_durable_storage():
            profile_form.add_error(None, "Shop image uploads are paused until persistent storage is configured. You can still update text fields.")
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your shop profile has been updated.")
            return redirect("seller_dashboard")
        messages.error(request, "Please review the shop profile fields and image sizes.")
    products = seller.products.order_by("-created_at")
    order_items = seller.order_items.select_related("order", "product").order_by("-order__created_at")[:30]
    total_orders = seller.order_items.values("order_id").distinct().count()
    has_application = SellerApplication.objects.filter(Q(user=request.user) | Q(email__iexact=request.user.email)).exclude(status="declined").exists()
    return render(request, "marketplace/seller_dashboard.html", {"seller": seller, "products": products, "order_items": order_items, "profile_form": profile_form, "total_orders": total_orders, "has_application": has_application})
'''
views = replace_fn(views, "seller_dashboard", "product_create", seller_dash)

account_fn = '''
@login_required
def account_dashboard(request):
    orders = Order.objects.filter(buyer=request.user).prefetch_related("items", "status_events")[:10]
    addresses = CustomerAddress.objects.filter(user=request.user)
    wishlist = WishlistItem.objects.filter(user=request.user).select_related("product", "product__seller")[:8]
    notifications = MarketplaceNotification.objects.filter(user=request.user)[:10]
    custom_requests = CustomRequest.objects.filter(Q(user=request.user) | Q(email__iexact=request.user.email))[:8]
    seller = Seller.objects.filter(user=request.user).first()
    total_orders = Order.objects.filter(buyer=request.user).count()
    total_spend = Order.objects.filter(buyer=request.user).aggregate(total=models.Sum("total"))["total"] or Decimal("0.00")
    return render(request, "marketplace/account_dashboard.html", {
        "orders": orders, "addresses": addresses, "wishlist": wishlist, "notifications": notifications,
        "custom_requests": custom_requests, "unread_count": MarketplaceNotification.objects.filter(user=request.user, is_read=False).count(),
        "seller": seller, "total_orders": total_orders, "total_spend": total_spend,
    })


@login_required
@require_http_methods(["GET", "POST"])
def account_profile(request):
    if request.method == "POST":
        display_name = " ".join(request.POST.get("display_name", "").split()).strip()
        if not display_name:
            messages.error(request, "Please enter the name you want displayed on your account.")
        else:
            parts = display_name.split(" ", 1)
            request.user.first_name = parts[0][:150]
            request.user.last_name = parts[1][:150] if len(parts) > 1 else ""
            request.user.save(update_fields=["first_name", "last_name"])
            messages.success(request, "Your profile has been updated.")
            return redirect("account_profile")
    return render(request, "marketplace/account_profile.html", {
        "display_name": " ".join(part for part in [request.user.first_name, request.user.last_name] if part).strip(),
    })
'''
views = replace_fn(views, "account_dashboard", "address_book", account_fn)

store_fn = '''
def seller_store(request, slug):
    seller = get_object_or_404(Seller.objects.select_related("user"), slug=slug, status="active")
    products = seller.products.filter(status="active", seller__status="active").select_related("category")
    return render(request, "marketplace/seller_store.html", {"seller": seller, "products": products, "is_own_store": bool(request.user.is_authenticated and request.user.pk == seller.user_id)})
'''
views = replace_fn(views, "seller_store", "product_review_create", store_fn)
views_path.write_text(views)

urls = urls_path.read_text()
if 'name="account_profile"' not in urls:
    marker = '    path("account/", views.account_dashboard, name="account_dashboard"),'
    if marker not in urls:
        raise SystemExit("Studio Edition 04: account URL anchor missing")
    urls = urls.replace(marker, marker + '\n    path("account/profile/", views.account_profile, name="account_profile"),', 1)
urls_path.write_text(urls)

# Bump the shared and home pages while retaining the Studio 03 bubble loader.
for path in (base_path, root / "marketplace/templates/marketplace/home.html"):
    html = path.read_text().replace('data-excellence-version="3"', 'data-excellence-version="4"')
    path.write_text(html)
base = base_path.read_text()
base = base.replace('<a class="text-btn" href="{% url \'account_dashboard\' %}">My account</a>', '<a class="text-btn" href="{% url \'account_dashboard\' %}">Dashboard</a><a class="text-btn" href="{% url \'account_profile\' %}">My profile</a>')
base_path.write_text(base)

template_map = {
    "register.html": "marketplace/templates/marketplace/register.html",
    "account_dashboard.html": "marketplace/templates/marketplace/account_dashboard.html",
    "account_profile.html": "marketplace/templates/marketplace/account_profile.html",
    "seller_apply.html": "marketplace/templates/marketplace/seller_apply.html",
    "seller_store.html": "marketplace/templates/marketplace/seller_store.html",
}
for name, destination in template_map.items():
    (root / destination).write_text((Path(__file__).with_name("templates") / name).read_text())

seller_dashboard_path = root / "marketplace/templates/marketplace/seller_dashboard.html"
seller_dashboard = seller_dashboard_path.read_text()
seller_dashboard = seller_dashboard.replace(
    '<p class="plain-intro">Welcome to {{ seller.shop_name }}. Keep your listings fresh and your customers informed.</p>',
    '<p class="plain-intro">Welcome to {{ seller.shop_name }}. Your products, public storefront, profile and order activity live in one workspace.</p><div class="kc-seller-dashboard-banner"><div class="kc-shop-avatar">{% if seller.logo_image %}<img src="{{ seller.logo_image.url }}" alt="{{ seller.shop_name }} logo">{% elif seller.logo_url %}<img src="{{ seller.logo_url }}" alt="{{ seller.shop_name }} logo">{% else %}{{ seller.shop_name|slice:":2"|upper }}{% endif %}</div><div><strong>{{ seller.shop_name }}</strong><span>{{ seller.city }}{% if seller.city %}, {% endif %}{{ seller.country }} · {{ seller.get_business_type_display }}</span><small>{% if seller.status == "active" %}Your storefront is public{% elif has_application %}Your application is waiting for the marketplace team to review it.{% else %}Your seller workspace is ready. Complete your business application to submit your shop for review.{% endif %}</small></div>{% if seller.status == "active" %}<a class="btn-lime" href="{% url \'seller_store\' seller.slug %}">Open my shop ↗</a>{% elif has_application %}<span class="kc-review-pill">Awaiting approval</span>{% else %}<a class="btn-lime" href="{% url \'seller_apply\' %}">Complete seller application ↗</a>{% endif %}</div>'
)
seller_dashboard = seller_dashboard.replace(
    '<a class="btn-quiet" href="{% url \'account_dashboard\' %}">My buyer account</a>',
    '<a class="btn-quiet" href="{% url \'account_dashboard\' %}">Buyer dashboard</a><a class="btn-quiet" href="{% url \'account_profile\' %}">My personal profile</a>'
)
seller_dashboard_path.write_text(seller_dashboard)

css_path = root / "koracraft_project/static/marketplace/css/app.css"
css_extra = Path(__file__).with_name("excellence-v4.css").read_text()
if "KoraCraft Studio Edition 04 — personal dashboards" not in css_path.read_text():
    css_path.write_text(css_path.read_text() + "\n" + css_extra)
js_path = root / "koracraft_project/static/marketplace/js/app.js"
js = js_path.read_text()
old_guard = "if(!body||body.dataset.excellenceVersion!=='3')return;"
new_guard = "if(!body||(body.dataset.excellenceVersion!=='3'&&body.dataset.excellenceVersion!=='4'))return;"
if old_guard in js:
    js = js.replace(old_guard, new_guard, 1)
elif new_guard not in js:
    raise SystemExit("Studio Edition 04: bubble-loader guard missing")
door_js = Path(__file__).with_name("excellence-v4.js").read_text()
if "KoraCraft Studio Edition 04: account and door entrance" not in js:
    js += "\n" + door_js
js_path.write_text(js)
print("KoraCraft Studio Edition 04 applied: separate account profile, buyer dashboard, seller workspace, linked applications and door-opening shops.")
