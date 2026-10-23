# KoraCraft Marketplace

**KoraCraft — Africa’s Makers. Your Style.**

A Django marketplace concept for African makers, tailors, shoemakers and textile sellers. Powered by Fortitech Digital Cluster. Copyright © 2026.

## Deployment architecture

- Django application served by Gunicorn.
- PostgreSQL is required for production; do not use the unrelated Urbisora database.
- Static assets are collected and served by WhiteNoise.
- Three bundled vector sample illustrations cover footwear, tailoring and textiles. Showcase products and sellers are fictional demo data.
- Payments are intentionally disabled and should remain marked **Coming Soon** until a provider is integrated and tested.
- Google sign-in remains optional until Google OAuth client credentials are configured.
- Email verification should only be enabled after a real sender/provider has been configured and tested.

## Render source bootstrap

The source archive is stored in small base64 segments under `archive/part-*.b64` to keep the private source repository manageable. Render's build command should be `bash render-build.sh`; this verifies, extracts and builds the Django project. The server start command is `gunicorn koracraft_project.wsgi:application`.

The build installs `requirements.txt`, collects static files, applies Django migrations and seeds fictional sample items. A persistent PostgreSQL `DATABASE_URL` and a strong `DJANGO_SECRET_KEY` are required before a production deploy can complete. The application fails closed when production database/secret settings are missing.

## Current deployment checklist

- [x] Dedicated private repository initialized.
- [x] Compressed application source segmented and checksum-verified against the local archive.
- [x] Render build script committed.
- [x] Python source compilation and JavaScript syntax checks passed locally.
- [ ] Provision a separate persistent PostgreSQL database for KoraCraft.
- [ ] Configure production environment variables and deploy the Render web service.
- [ ] Verify Django migrations, health, registration, seller workflow, cart/order path, email delivery and responsive pages on the live service.

## Security notes

Do not commit `.env`, API keys, OAuth secrets, database URLs or production credentials. Configure them through Render environment settings. Before accepting real customers, complete runtime tests, sender-domain verification, upload storage configuration, backups/monitoring and payment-provider integration.