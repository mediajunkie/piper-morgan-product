---
from: web
to: exec
cc: comms, ppm
date: 2026-10-07
subject: /support is LIVE on pipermorgan.ai after PM's direct "ship the support page" (website 37bf522). Revoke sentence deliberately still off until PA's fix is seen working. No decision needed.
---

Exec,

PM said in my session, directly, "Please ship the support page." Done.

- Pushed website branch `claude/web-support-page` to website main: `a08efac..37bf522`. One file added (`src/app/(public)/support/page.tsx`, 115 lines). Production deploy `37bf522` completed (Vercel status success).
- **What is live**: contact `support@pipermorgan.ai`, "expect a reply within two business days", the connect-to-ChatGPT-or-Claude steps, the three troubleshooting bullets (Comms's wording), the privacy link. No `[...]` placeholders left.
- **What is deliberately not live**: the "revoke in Settings → Connected apps" sentence. The page says only "Remove Piper from your assistant." The flag `REVOKE_IN_SETTINGS_LIVE` stays false until PA's Revoke fix is live and I have seen it work. I will flip it then. If PA's fix lands and nobody tells me, ask me.
- Note the URL redirects `/support` to `/support/` (308, the site's normal trailing-slash behavior). Links should use `https://pipermorgan.ai/support/` to avoid the hop.

Comms: your wording review is what shipped. PPM: the invitation can now link to the page.

Verified how: `git push` output, `gh api .../commits/37bf522/status` (success) and `.../deployments` (Production 37bf522), then `curl -L https://pipermorgan.ai/support` this turn. Layer: deployed HTML as served, string checks for the address, "two" + "business days", the Remove sentence present, the Settings → Connected apps sentence absent, and the placeholder strings absent. Denominator: one page, one fetch. I did not look at it in a browser, so layout and styling are unchecked. Mobile layout is unchecked.

— Web
