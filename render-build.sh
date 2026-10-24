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
python manage.py shell -c 'from django.test import Client; client = Client(); paths = ["/", "/shop/", "/seller/apply/", "/categories/", "/makers/", "/how-it-works/", "/login/", "/register/", "/cart/", "/health/"]; results = [(path, client.get(path, HTTP_HOST="localhost").status_code) for path in paths]; print("KoraCraft route smoke check:", results); failures = [(path, status) for path, status in results if status >= 500]; assert not failures, "Route smoke check failed: " + repr(failures)'
