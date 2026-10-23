# KoraCraft Marketplace

**KoraCraft — Africa’s Makers. Your Style.**

A Django marketplace for African makers, tailors, shoemakers and textile sellers. Powered by Fortitech Digital Cluster. Copyright © 2026.

## Deployment architecture

- Django application served by Gunicorn.
- PostgreSQL is configured as a separate KoraCraft database; do not use the unrelated Urbisora database.
- Static assets are collected and served by WhiteNoise.
- Three bundled sample illustrations cover footwear, tailoring and textiles. Showcase products and sellers are fictional demo data.
- Payments remain disabled and should display **Coming Soon** until a provider is integrated and tested.
- Google sign-in remains optional until Google OAuth client credentials are configured.
- Email verification is disabled until a real sender/provider is configured and tested. Password-based registration is available without verification during initial launch.

## Render deployment

This repository is private. Before deploying, authorize the Render GitHub App to access `profomenifewilliams-creator/koracraft` at https://github.com/apps/render/installations/new. In the installation's repository access list, select this repository and save the change. This grants Render read access so it can clone the source; it does not make the repository public.

The Render Blueprint is `render.yaml`. The build command is `bash render-build.sh`, which verifies and extracts the segmented source archive, then runs `build.sh`. The server command is `gunicorn koracraft_project.wsgi:application`; health checks use `/health/`.

Set `DATABASE_URL` in Render's Environment settings using KoraCraft's separate PostgreSQL connection string, and keep it secret. Render's Blueprint generates `DJANGO_SECRET_KEY`. Keep `DJANGO_DEBUG=False`. Do not set payment secrets; checkout payment collection is not enabled.

The build installs dependencies, collects static files, applies migrations and seeds clearly fictional sample products. A successful build is not a substitute for live smoke tests.

## Current deployment checklist

- [x] Dedicated private repository initialized.
- [x] Compressed source archive segmented and validated against the local archive.
- [x] Render build script and Blueprint committed.
- [x] Python source compilation and JavaScript syntax checks passed locally.
- [x] Separate KoraCraft PostgreSQL database provisioned on Neon (free plan), not Render; no Render paid database was created.
- [ ] Authorize Render GitHub access to this private repository.
- [ ] Create and deploy the Render web service with the database connection in service secrets.
- [ ] Verify migrations, health, signup/login, seller workflows, cart/order paths, email delivery and responsive pages on the live service.

## Before accepting real customers

Do not commit `.env`, API keys, OAuth secrets, database URLs or production credentials. Configure secrets only in Render environment settings. Complete live runtime tests, sender-domain verification, persistent seller/product upload storage, backups/monitoring and payment-provider integration before accepting real customers.