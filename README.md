# RKB Facebook Page Manager

A Meta-approved multi-account, multi-page Facebook publishing dashboard.

## MVP features

- Meta OAuth login
- Discover connected Facebook Pages
- Text, photo, and video publishing
- Same or per-page captions
- Instant and scheduled publishing
- SQLite persistence
- Post status and retry
- Page-level publish reports

Only Meta Graph API-supported operations are exposed. Unsupported page features are reported as unsupported instead of being simulated.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000`.

Use an HTTPS public URL for Facebook OAuth in production. Configure the exact OAuth redirect URI in the Meta app and `.env`.

## Required Meta setup

Create a Meta app, enable Facebook Login, and request permissions through Meta App Review where required. Typical permissions for this MVP include:

- `pages_show_list`
- `pages_read_engagement`
- `pages_manage_posts`
- `pages_read_user_content` if reading/reviewing Page comments or existing posts is required

Publishing access must be granted for each Page. Meta can reject or limit publishing based on app mode, permissions, Page eligibility, account status, and API rate limits.
