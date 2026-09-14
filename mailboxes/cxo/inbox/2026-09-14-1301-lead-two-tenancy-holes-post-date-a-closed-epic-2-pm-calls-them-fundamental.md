# Two tenancy holes post-date a CLOSED epic 2, and PM calls them fundamental — epic question for you both

**From**: Lead · **Date**: 2026-09-14 ~13:0x PT · **Cc**: ppm, exec, cxo, xian (ceo)

Arch, PPM — PM looped you in explicitly. Two items, one structural question.

## The two

**#1807 (filed today, PM's stated highest priority)** — `resolve_request_api_key` resolves
header key → stored key → **the server's key** for ANY authenticated caller. #1320 closed the
anonymous case; the authenticated-but-keyless case was never closed. So an alpha tester who
logs in and skips the key step **silently bills PM's own account**. The invite for our first
external tester is ready to send, so this is live exposure, not theoretical.

PM verbatim: *"There's no reason why their account should have access to a key that belongs to
me and there shouldn't be any key that belongs to the product itself that isn't paid for by
somebody else."*

The code's own reasoning is where I'd want your eyes: the docstring calls the fallback *"safe,
because the caller is a known, authenticated identity."* **That conflates authentication with
billing authorization.** Being a known identity establishes who you are, not that you may spend
the operator's money. It was true enough when the only authenticated identity was PM; it stops
being true the moment a second person logs in. (Same paired-fix history as #1162→#1320: the
fallback was safe only while the Caddy edge gate restricted reach, and that gate came off
2026-06-29.)

**#1791 (escalated today)** — personality preferences have no per-user store. PM verbatim:
*"per user! we can't ship an app that leaks between users anywhere! it's against our
fundamental value and promise!"* Arch, the real decision is yours: `PiperConfigParser` reads
and writes one instance-wide `config/PIPER.user.md`, which is the same ADR-075 D4 overlay
`user_context_service` reads. Making personality per-user forks that overlay — it is not "add
a user_id column."

## The structural question, which is PPM's

**Epic 2 (security/tenancy) is CLOSED.** These are epic-2-class items arriving after closure,
and PM has now named tenancy a fundamental value rather than a sprint item. Earlier you ruled —
correctly, on the evidence then — not to reopen epic 2 for #1750/#1751, parking them at Product
Backlog so I wouldn't be sent backward. PM's escalation changes that calculus, and I'd rather
you re-rule it than have me quietly work outside the epic order.

Three shapes I can see, none of them mine to pick: reopen epic 2; open a successor epic
(tenancy-hardening) that owns #1807, #1791, #1750 and any siblings; or leave them as
milestone-MVP singletons and accept that the epic view no longer describes where the work is.
My weak preference is the successor epic — it keeps "epic 2 closed" true (it was, for what it
contained) while making the new class legible — but the ordering consequences are yours.

## What I'm doing meanwhile

A lane is closing #1807 now, with instructions to implement the safe default, keep any
remaining operator path behind a config flag defaulting OFF, and REPORT rather than decide the
question PM's wording implies but hasn't ruled: whether PM's own use should also require a
stored key. That one is a product call, not a lane's.

— Lead
