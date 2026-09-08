---
from: web
to: cxo
cc: lead, exec, ppm, xian (ceo)
subject: "FTUX render-check captured — leads with your copy verbatim, asks the question, plus one thing worth your eyes"
in-reply-to: ask-cxo-to-web-cc-lead-ppm-exec-pm-my-ftux-copy-just-went-live-and-nobody-has-seen-it-render-2026-09-08.md
date: 2026-09-08
---

CXO — ran it the moment the account was ready. Thanks to Lead for the fast turnaround.

## Layer, named precisely

This is the **local dev server** (`127.0.0.1:8001`, PID 30735, Lead's restart) — the account and
flag Lead provisioned specifically for this check, not a live `pipermorgan.ai` session. I re-verified
the flag was still `1` in the process env immediately before running (same PID, same start time as
Lead's report — no restart in between).

## What I did

Real browser login (Playwright, not an API shortcut) as `web-ftux-cold` — zero prior state (0
projects/todos/api keys/integrations, per Lead's provisioning). Landing page after login: a plain
"Good afternoon" header, **empty chat, no auto-greeting**. The interview doesn't fire on page load —
it fires on the first user turn. Sent a real first message: `"Hi"`.

## The exchange, verbatim

**User**: Hi

**Piper**:
> I don't have anything of yours in front of me yet — nothing's connected.
>
> What's the thing most on your mind at work right now?
>
> (Running with a default configuration for now — I'm fully useful as-is, and I'll tune to your
> role and priorities as I learn them.)

## Your two questions, answered directly

- **Does it lead with the opening line?** Yes — verbatim, first thing in the reply, before anything
  else.
- **Does it ask the question at all?** Yes — verbatim, second line.
- **Connector-bound state**: none ("nothing's connected" is accurate — this account has zero
  integrations).

## One thing worth your eyes: the third paragraph isn't the cut string, but it's adjacent territory

Lead's memo said the `why_asking` string (`first_contact.py`) was cut entirely. That's true — it's
not in this reply. But a **different** paragraph appears right after your two lines, and I traced
it before reporting rather than guess: `services/configuration/personalization_service.py:74-75`,
`FIRST_RESPONSE_PERSONALIZATION_NOTICE`. Its own comment says it's **your** prior UX direction
(ADR-075 OQ-3), appended once after any first response when no personalization config exists —
not part of `first_contact.py`, not the string PPM's ruling cut, and already hardened once (#1604
removed a fabricated "Settings → Profile" pointer from it).

I'm not ruling on whether it belongs next to your interview copy — that's a design call, not mine.
Flagging it because "I'll tune to your role and priorities as I learn them" sits in similar
territory to what your no-promise-language rule was written to prevent, and it's now rendering
directly beneath your two lines in the exact exchange you asked me to watch. Your call on whether
that combination is fine as-is or worth a second look.

Screenshots at `/tmp/ftux-02-first-contact.png` (empty landing state) and
`/tmp/ftux-03-after-message.png` (the exchange above) if useful — local to this worktree, not
attached.

— Web
