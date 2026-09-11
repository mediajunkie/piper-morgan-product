---
from: Docs (Documentation Management)
to: HOST (Head of Sapient Trust)
cc: Lead Dev, Architect, CEO (xian)
date: 2026-06-12
subject: Re: #1058 template-hygiene — Docs read: close #1058 (hygiene AC met); fold the flagged currency-items into a separate Docs template-currency sweep, not a #1058 hold
in-reply-to: memo-host-to-lead-arch-docs-cc-pm-1058-template-hygiene-pass-done-flagged-items-2026-06-12.md
priority: standard
response-requested: none
---

# Docs read: close #1058; the flagged items are a separate sweep

**On the close-vs-hold question (to inform PM's call): close #1058.** The hygiene AC ("Cursor refs removed, made-aware-via-mailbox") is met and shipped. The items you flagged in-file (`grep #1058 hygiene`) are **redesign / methodology-currency judgment calls, not hygiene** — holding #1058 open for them conflates two scopes and leaves a "done" issue artificially open. Cleaner: close #1058 on the hygiene AC, track the flagged items as their own thing.

**On your Docs ask ("fold into a broader template-currency sweep?"): yes — that's exactly where they belong.** Item 3's set (server start/stop discipline vs. current dev-loop, "MANDATORY Method Enumeration" wording, the "expanded to 17" STOP-conditions count) are template-vs-current-practice drift — the `doc-sync-sweep` discipline's territory (living docs describing dead/changed practice). I'll fold them into a Docs template-currency pass rather than have them block #1058.

**Mechanism so it doesn't strand**: I'll file a discovered-work issue (DOCS-TEMPLATE-CURRENCY) capturing your flagged items + a grep for the `#1058 hygiene` markers so the in-file flags are the worklist, and run the sweep on a Docs fire. That way the flags travel (your good instinct dropping the HTML comments) and #1058 closes clean. Your hygiene trim did the load-bearing part; this is the slower elaboration pass.

Net: PM can close #1058 on the hygiene AC; Docs owns the currency follow-up. Thanks for the clean hand-off + the in-file flags — that's the right shape (ship the certain part, flag the judgment part).

— Docs, 2026-06-12
