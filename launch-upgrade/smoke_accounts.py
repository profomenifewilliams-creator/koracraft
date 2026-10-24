"""Build-time functional checks for buyer/seller onboarding. All test rows are rolled back."""
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.test import Client
from django.urls import reverse

from marketplace.models import EmailVerificationToken, Seller, SellerApplication


HOST = "koracraft-marketplace.onrender.com"
User = get_user_model()


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def register_temporary_account(kind):
    token = uuid.uuid4().hex
    email = f"kc-{kind}-{token}@example.invalid"
    name = "KoraCraft QA " + ("Seller" if kind == "seller" else "Buyer")
    password = "Kc!" + uuid.uuid4().hex + "9Z"
    client = Client()
    response = client.post(
        reverse("register"),
        {"name": name, "email": email, "password": password, "account_type": kind},
        secure=True, HTTP_HOST=HOST,
    )
    check(response.status_code in (302, 303), f"{kind} registration did not redirect: HTTP {response.status_code}")
    user = User.objects.get(email__iexact=email)
    if not user.is_active:
        verification = EmailVerificationToken.objects.get(user=user)
        response = client.post(
            reverse("verify_email", args=[verification.token]),
            secure=True, HTTP_HOST=HOST,
        )
        check(response.status_code in (302, 303), f"{kind} verification did not redirect: HTTP {response.status_code}")
        user.refresh_from_db()

    check(user.is_active, f"{kind} account was not activated")
    check(str(client.session.get("_auth_user_id")) == str(user.pk), f"{kind} registration did not sign the new user in")
    expected_url = reverse("seller_dashboard") if kind == "seller" else reverse("account_dashboard")
    check(response.url == expected_url, f"{kind} registration redirected to {response.url}, expected {expected_url}")

    account_response = client.get(reverse("account_dashboard"), secure=True, HTTP_HOST=HOST)
    profile_response = client.get(reverse("account_profile"), secure=True, HTTP_HOST=HOST)
    check(account_response.status_code == 200, f"{kind} buyer dashboard returned HTTP {account_response.status_code}")
    check(profile_response.status_code == 200, f"{kind} profile returned HTTP {profile_response.status_code}")

    if kind == "seller":
        seller = Seller.objects.get(user=user)
        check(seller.status == "pending", f"new seller workspace should be pending, got {seller.status}")
        seller_response = client.get(reverse("seller_dashboard"), secure=True, HTTP_HOST=HOST)
        check(seller_response.status_code == 200, f"seller dashboard returned HTTP {seller_response.status_code}")
        shop_name = "QA Studio " + token[:9]
        apply_response = client.post(
            reverse("seller_apply"),
            {
                "business_name": shop_name,
                "business_type": "shoes",
                "location": "Abuja, Nigeria",
                "email": email,
                "phone": "08000000000",
                "notes": "Temporary automated onboarding smoke test.",
            },
            secure=True, HTTP_HOST=HOST,
        )
        check(apply_response.status_code in (302, 303), f"seller application did not redirect: HTTP {apply_response.status_code}")
        check(apply_response.url == reverse("seller_dashboard"), f"seller application went to unexpected route: {apply_response.url}")
        application = SellerApplication.objects.get(user=user, business_name=shop_name)
        seller.refresh_from_db()
        check(application.status == "new", "seller application must remain awaiting administrator review")
        check(seller.shop_name == shop_name, f"seller workspace did not sync shop name: {seller.shop_name}")
        check(seller.status == "pending", "seller shop became public before approval")
        seller_response = client.get(reverse("seller_dashboard"), secure=True, HTTP_HOST=HOST)
        check(seller_response.status_code == 200, "seller dashboard failed after application submission")
    print(f"KoraCraft {kind} registration and dashboard check: PASS")


with transaction.atomic():
    try:
        register_temporary_account("buyer")
        register_temporary_account("seller")
    finally:
        # These checks must never leave generated accounts/applications in production.
        transaction.set_rollback(True)

print("KoraCraft account-flow smoke tests passed; temporary data rolled back.")
