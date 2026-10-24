#!/usr/bin/env bash
set -euo pipefail
ARCHIVE="$(mktemp /tmp/koracraft-source.XXXXXX.tar.gz)"
trap 'rm -f "$ARCHIVE"' EXIT
if [ ! -d archive ]; then echo 'KoraCraft source archive directory is missing.' >&2; exit 2; fi
cat archive/part-*.b64 | tr -d '\r\n ' | base64 -d > "$ARCHIVE"
tar -tzf "$ARCHIVE" >/dev/null
tar -xzf "$ARCHIVE" -C .
rm -rf archive
# Apply the tracked Studio Edition overlay after extracting the original Django source.
python launch-upgrade/apply.py
python launch-upgrade/v3.py
python launch-upgrade/v4.py
chmod +x build.sh
./build.sh
python manage.py shell -c 'from django.test import Client; client = Client(); host="koracraft-marketplace.onrender.com"; public_paths = ["/", "/shop/", "/seller/apply/", "/categories/", "/makers/", "/how-it-works/", "/login/", "/register/", "/cart/", "/health/", "/makers/demo-obi-leather/"]; public_results = [(path, client.get(path, secure=True, HTTP_HOST=host).status_code) for path in public_paths]; print("KoraCraft public HTTPS route smoke check:", public_results); public_failures = [(path, status) for path, status in public_results if status != 200]; assert not public_failures, "Public route smoke check failed: " + repr(public_failures); auth_paths = ["/account/", "/account/profile/", "/seller/dashboard/", "/orders/"]; auth_results = [(path, client.get(path, secure=True, HTTP_HOST=host).status_code) for path in auth_paths]; print("KoraCraft authenticated route checks (redirects to login expected):", auth_results); auth_failures = [(path, status) for path, status in auth_results if status not in (200, 302, 303)]; assert not auth_failures, "Authenticated route smoke check failed: " + repr(auth_failures)'
