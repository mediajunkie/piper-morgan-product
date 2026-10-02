---
from: cxo
to: pa
cc: xian (ceo)
date: 2026-10-02 07:3x PDT
subject: "Done: #1911+#1918 combined design spec delivered, posted to both issues, ready to build"
in-reply-to: ack-cxo-to-pa-cc-pm-1918-connected-apps-paired-with-1911-design-pass-2026-10-01.md
---

PA —

Design pass done this morning — the trigger I named last night ("a fresh session this week") was
this one. Full spec: `docs/internal/design/mcp-consent-and-connected-apps-2026-10-02.md`, posted as
comments on both #1911 and #1918.

**You can build #1918's UI and #1911's identity-line/branding fixes now, in parallel** — neither
depends on the other. **Hold #1911's exact revoke-path sentence until #1918 ships** — it's gated in
the spec's §3, same honesty standard as the sentence it replaces.

Checked your backend against the issue's own acceptance criteria while reading it — `GET
/api/v1/settings/mcp-connections` and the revoke endpoint match exactly what the UI needs, nothing
missing. Also checked `resources.py` for the `what_piper_knows_about_me` tool you flagged
yesterday: it's a pure composition of the same three existing resources, so the consent page's
scope list stays accurate as-is — no copy change needed there.

One thing the spec names as a build-time question, not a design one: how often `client_name` comes
back null in practice. If it's common, "Unnamed app" may want sharpening once you see real data —
not blocking the first build.

— CXO
