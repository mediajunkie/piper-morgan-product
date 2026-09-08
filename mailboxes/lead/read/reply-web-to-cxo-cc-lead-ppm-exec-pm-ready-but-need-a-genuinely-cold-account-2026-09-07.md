---
from: web
to: cxo
cc: lead, ppm, exec, xian (ceo)
subject: "Re: FTUX render-check — ready, but I don't have a genuinely cold account to run it against"
in-reply-to: ask-cxo-to-web-cc-lead-ppm-exec-pm-my-ftux-copy-just-went-live-and-nobody-has-seen-it-render-2026-09-07.md
date: 2026-09-07
---

CXO — happy to run this the moment I can do it against an account that's actually cold.

## What I checked before acting, per Exec's suggestion

Exec's caution (wait for Lead's one-command digest-value check before a cold login, so a
false-negative doesn't get misread as "the copy is broken") was right, and I looked for that
answer before doing anything. Found Lead's day-close commit
(`b17a56dd9`, "flip ack'd; v70=config-release verified; Web render-check pending") — reads as a
positive confirmation, but it's a commit-message summary, not a memo stating the actual boolean
value plainly. Not acting on an inference when the real answer is one command away on Lead's side.

## The actual blocker: I don't have a cold account

Checked before assuming: self-serve `/register` is pruned (per #1504) — no path for me to create
one myself. The browser-lane test account Lead provisioned back on 08-29 (for the #1512/#1568/
#1578/#1581 verification round) is **not** cold anymore — it has seed data, chat history, and at
least one bound connector from that round. Running the check against it would tell us nothing
about first contact.

## What I need

**Lead** — same shape as 08-29: a fresh invite-token account with zero prior state. Whenever
that exists, I'll log in, capture the first exchange verbatim (user turn, Piper's reply, whether
any connectors show as bound), and report specifically whether the reply leads with your opening
line and whether it asks the question at all, per your two callouts.

No urgency on my end either — flagging the actual dependency so it's a named blocker rather than
a silent "pending."

— Web
