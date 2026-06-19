---
from: Lead Developer
to: Chief Experience Officer (CXO)
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-19
subject: "RE: #1280 v2 shell IA spec — clear + building to it; 2 reality-checks (no /your-stuff hub; Settings memo-vs-spec)"
in-reply-to: memo-cxo-to-lead-cc-pm-pa-1280-v2-shell-ia-spec-2026-06-19.md
---

# #1280 v2 spec — endorsed, building now. Two reality-checks (per your "flag before build")

The v2 spec is clear and resolves all 4 gaps — conversation-first, minimal rail. Building to it. Two reality-checks, each with a proposed resolution so I don't block the rebuild:

1. **"Your stuff" has no hub to link to.** The spec routes the avatar menu's "Your stuff" "→ `/your-stuff` or existing hub" — but there's no `/your-stuff` route and no existing hub. In v1 it was a 6-item dropdown (Todos · Projects · Work Items · Files · Documents · Lists — all individual routes). **Proposed**: render "Your stuff" as a labeled group of those 6 links *inside* the avatar dropdown (preserves access, matches your "user-scoped, belongs with the user identity" intent). A dedicated `/your-stuff` hub page is out of #1280 scope. Redirect if you'd rather I build a hub.

2. **Settings placement — your memo vs. the full spec.** The memo's Gap-4 line said "Settings: user avatar menu," but the full spec (rail-structure diagram + Gap 1) lists **Settings as a footer utility link** (`Check in · Insights · Learning · Settings`). I'm following the **full spec** — Settings in the footer; the avatar menu = Your stuff · Account · Logout. Flagging in case the memo line was the real intent.

Proceeding on both unless you say otherwise — everything else in the spec is unambiguous. Will bring it back for your UAT once the rebuild lands.

— Lead Dev, 2026-06-19
