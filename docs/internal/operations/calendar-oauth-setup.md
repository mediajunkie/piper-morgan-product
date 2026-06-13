# Google Calendar OAuth — local setup (one-time)

**Owner:** Lead Dev · **For:** PM (xian) · **Issue:** #1215 · **Added:** 2026-06-13

Piper's calendar integration is **already wired** (#577): Settings → Calendar has a
form to enter a Google OAuth **app credential** (client_id + secret), then a
"Connect with Google" button to authorize. The only missing piece is the app
credential itself — this guide creates it.

## Which Google account

Use **designinproduct.com** (xian's own domain), not Kindsys — it survives losing
the Kindsys account. If designinproduct.com is a Google **Workspace** domain, set
the consent screen to **Internal** (skips Google's test-user limits + verification
review). If it's a plain account, use **External** and add yourself as a test user.

## What the app expects (so the OAuth client matches)

- **Scopes** (read-only — Piper won't modify your calendar):
  - `https://www.googleapis.com/auth/calendar.readonly`
  - `https://www.googleapis.com/auth/userinfo.email`
- **Authorized redirect URIs** — register BOTH exactly (the Settings flow and the
  setup-wizard flow use different callbacks):
  - `http://localhost:8001/api/v1/settings/integrations/calendar/callback`  ← the Settings → Calendar "Connect" flow (the one you'll use)
  - `http://localhost:8001/setup/calendar/oauth/callback`  ← the setup-wizard flow (add for completeness)

## Step by step (Google Cloud Console, signed in as xian@designinproduct.com)

1. **Project** — console.cloud.google.com → project dropdown (top bar) → **New Project** → name it `Piper Morgan` → Create → select it. (Reusing an existing personal project is fine too.)
2. **Enable the API** — ☰ → **APIs & Services → Library** → search **"Google Calendar API"** → **Enable**.
3. **OAuth consent screen** — APIs & Services → **OAuth consent screen**:
   - User type: **Internal** (if Workspace) or **External**. Create.
   - App name `Piper Morgan`; user-support email + developer-contact email = your email. Save & continue.
   - **Scopes** → Add or remove scopes → add the two scopes listed above. Save & continue.
   - (External only) **Test users** → add `xian@designinproduct.com`. Save.
4. **Create the OAuth client** — APIs & Services → **Credentials** → **Create Credentials → OAuth client ID**:
   - Application type: **Web application**.
   - Name: `Piper Morgan local`.
   - **Authorized redirect URIs** → **Add URI** twice → paste the two URIs above (exactly — trailing slashes and `http` vs `https` must match).
   - **Create** → a dialog shows your **Client ID** and **Client secret**. Copy both.
5. **Paste into Piper** — open http://localhost:8001 → **Settings → Calendar** → paste Client ID + Client secret into the credentials form → **Save**. The status should flip to "credentials configured."
6. **Connect** — click **Connect with Google** → choose your designinproduct.com account → approve the read-only calendar + email scopes → you'll be redirected back to Settings with a "Connected" status.

## Troubleshooting

- **`redirect_uri_mismatch`** — the URI in the Google client doesn't byte-match the app's. Re-check both URIs in step 4 (no trailing slash; `http://localhost:8001`, not `127.0.0.1` or `https`).
- **403 `access_denied` / "app not verified"** — you're on an External consent screen in Testing status and your email isn't a test user (step 3) — or just click "Advanced → go to Piper Morgan (unsafe)" for your own app.
- **Still 503 "OAuth not configured" on Connect** — the credential didn't save/where the server reads it. Lead Dev can verify with `IntegrationConfigService().get_google_client_id()`.

## Where the server reads it (for debugging)

`GoogleCalendarOAuthHandler` (`services/integrations/calendar/oauth_handler.py`) loads
client_id/secret with priority **env vars (`GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET`)
> IntegrationConfigService (keychain)**. The Settings form stores to the keychain via
`IntegrationConfigService.store_google_credentials()`, so no env vars are needed.
