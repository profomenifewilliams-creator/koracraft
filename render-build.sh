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
chmod +x build.sh
./build.sh
python manage.py shell -c 'from django.test import Client; client = Client(); paths = ["/", "/shop/", "/seller/apply/", "/categories/", "/makers/", "/how-it-works/", "/login/", "/register/", "/cart/", "/health/"]; results = [(path, client.get(path, secure=True, HTTP_HOST="koracraft-marketplace.onrender.com").status_code) for path in paths]; print("KoraCraft HTTPS route smoke check:", results); failures = [(path, status) for path, status in results if status >= 500]; assert not failures, "HTTPS route smoke check failed: " + repr(failures); redirects = [(path, status) for path, status in results if status in (301, 302, 307, 308)]; assert not redirects, "Unexpected redirects in HTTPS smoke check: " + repr(redirects)'
