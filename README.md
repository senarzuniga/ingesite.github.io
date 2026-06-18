# senarzuniga.github.io
Ingecart Site

Media Hub — local sync & deployment
----------------------------------

This repository includes a lightweight Media Hub that lets you:

- Sync videos from your local OneDrive folder (default: `C:\\Users\\Inaki Senar\\OneDrive\\INGECART\\VIDEOS web`) into the repo
- Serve a video gallery at `/public/videos/` and in the site's `#solutions` section
- Trigger a local sync from the website (the page attempts to call a local helper server)
- Send notification emails when videos are played or downloaded via a Netlify serverless function (requires SendGrid)

Quick start (local sync server)

1. Create a virtualenv and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the local server (this exposes `http://localhost:8600`):

```powershell
python scripts/video_sync_server.py
```

3. From the website (open `index.html`), clicking the **Actualizar videos** button will call the local server to sync files from your OneDrive folder into `assets/videos/` and `public/videos/` and will push a commit to `main`.

Serverless email notifications (Netlify)

The site includes a Netlify function `netlify/functions/notify_event.js` that will send an email via SendGrid if `SENDGRID_API_KEY` is configured in the Netlify dashboard. Configure the following environment variables in Netlify:

- `SENDGRID_API_KEY` — SendGrid API key (optional)
- `EMAIL_TO` — recipient address (defaults to `cgo@ingecart.es`)
- `EMAIL_FROM` — from address for messages

If `SENDGRID_API_KEY` is not set the function returns 204 and the frontend will fall back to attempting a local event call to `http://localhost:8600/event`.

Notes

- The local sync script performs `git add`/`commit`/`push` so ensure your local environment has git configured and an authenticated remote (e.g., cached credentials).
- Large video files may take time to copy and push — be patient.
- Browser security may block calls from a secure (HTTPS) page to `http://localhost`; if that happens, run the local site over HTTP or use the sync script directly:

```powershell
python scripts/sync_videos.py
```

