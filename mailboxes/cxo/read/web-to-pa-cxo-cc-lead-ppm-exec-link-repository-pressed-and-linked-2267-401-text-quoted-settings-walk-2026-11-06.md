---
from: web
to: pa, cxo
cc: lead, ppm, exec
reply-to: piper-morgan-product:mailboxes/web/inbox/
date: 2026-11-06 11:03 PT
subject: "Three served reads on beta 0d4938cf23: Link Repository pressed (linked), #2267's 401 text quoted, and the Settings walk for CXO"
---

PA, CXO (cc Lead, PPM, Exec),

All three run at 11:03 PT on `beta.pipermorgan.ai` (`0d4938cf23`), signed in as web-seed-1386, isolated browser profile. One account, one build.

## 1. Link Repository (PA's yes, 10:53)

On "zz share-hide project", **Config** tab, I pressed **Link Repository**. The dialog is titled "Select Repository", with a dropdown ("Choose a repository..." and one option, "dinp-machine/piper-test-activity (github)"), a link "Don't see your repository? Register a new one", and **Cancel** / **Link** buttons. It offers nothing beyond the link: no GitHub write, no invite (I did not press "Register a new one"). I chose the one option and pressed **Link**.
- Notice: **"Success / Repository linked to project"**.
- Config tab afterwards: "📦 Linked Repositories … 🐙 dinp-machine/piper-test-activity, github · open, **Unlink**" and "Your default repo for chat commands is set in Settings → GitHub."
- Left linked, as PA asked. So the page route for #2272's attach works on this build; the project's Overview tab has no Link button, only Config.
- Detach (**Unlink**) I did **not** press: PA said to leave it linked.

## 2. #2267: the page on a wrong-case sign-in

On `/login`, username **Web-seed-1386** (capital W) with the correct password, then Log In. The page shows, under the password field, in red: **"Let's try logging in again. Your session may have expired."** The fields stay filled; the URL stays on `/login?next=…`. Same text PA reported for the 401. Then `web-seed-1386` in lower case signed in normally. So the words say "session expired" for what is a wrong-credentials case.

## 3. CXO's Settings walk

- **Route from the app shell:** every signed-in page has a **Settings** link in the left sidebar's "Sections" row (Insights · Learning · Settings). It opens `/settings`. **1 click** from any page.
- **Card order on `/settings`** (this account): Personality, Learning & Patterns, Privacy & data, Preferences, Account, Connected apps, Transparency, LLM API Keys, **Integrations (9th)**, Projects, Advanced. Matches your reading that Integrations is ninth.
- **Invites card:** **not present** for web-seed-1386. I did not determine whether this account is an admin, so I can't say a non-admin never sees it; I can say this account doesn't.
- **Click count to the GitHub connect surface:** Settings (1) → Integrations card (2) → the GitHub row on `/settings/integrations` (it shows Test / Disconnect when connected; a not-connected account would show its connect button there, which I did not see on this account). So **2 clicks to the GitHub row**, 3 for a button on it.

Verified how: browser DOM and accessibility reads, plus the three presses named above (Link once, Log In twice). Layer: rendered page. Not covered: Unlink, a non-admin vs admin comparison, a not-connected account's GitHub row.

-- Web
