---
from: pa
to: exec
cc: xian (ceo)
subject: "Ship #062 workstream review — PA, window Fri 18 Sep -> Thu 24 Sep"
date: 2026-09-25
---

## The organizing question, answered plainly first

**PA's lane shipped nothing a user or alpha tester can directly touch this window.** PA's role is
PM-bandwidth extension and skunkworks coordination, not code that ships — so the honest answer to
"what can a user do today that they couldn't on Sep 18" is *nothing, directly*. What follows is what
that work is driving toward, and one real product-quality finding surfaced before it could reach a
user, which is the point of doing it now.

**Sprint denominator** (`scripts/sprint-truth.py`, run this fire): MVP 29 not done (10 Sprint
Backlog, 2 In Progress, 3 In Review, 14 Product Backlog), 1,190 done. PA's own lane doesn't move
this number — no PA-owned issues sit in the 29 — the line is here per the standing instruction.

## What moved

**BYOC Phase B (`mcp.pipermorgan.ai` DNS/TLS) — recommended, approved, executed, same window.**
PM asked directly for a recommendation rather than the flagged gap (09-22). Researched this week's
actual Fly/DNS mechanics before answering — Fly access is grant-gated not standing, DNS is PM's own
by standing rule, Pard had fresh proven context from the alpha-to-Fly migration days earlier — and
recommended reusing that exact pattern over PM's floated Arch-supervising alternative. PM approved
09-23; Pard executed alongside PM the same day; `decisions.log` carries the ruling. This is the
concrete next step toward a connectable hosted-MCP surface, still infrastructure, not yet reachable
by a user.

**Tool-catalog naming — four empirical passes closing an open PDR-006 question.** PPM's own 07-30
worry was that situation-shaped tool names (vs. the codebase's current 100% object-shaped naming)
might route *worse* for LLM-side tool selection. Ran it rather than argue it: four live-API passes
across two ambiguity types, both vendors where relevant. Finding, now recorded on the build-track
epic (#1462): situation-shaped naming gives a real, replicated benefit specifically for
purpose-ambiguous phrasing, and no advantage where the distinguishing feature is concrete — a mixed
catalog, not a rename-everything, is what the evidence supports for the tool catalog a connecting
user's host LLM will actually see.

**T-axis (honesty-under-recomposition) — PM's 09-20 "stop hand-waving, build a real model" tasking,
closed.** Four independently pre-registered rounds (each scored exactly as registered, no
re-litigating after seeing output) found a real, specific, vendor-asymmetric trust gap: a coverage
caveat on a short list survives recomposition on Claude under most tested framings, and survives on
GPT-4o under **none** of four — metadata, counted member, uncounted member, sibling-shaped member
all fail. That's a real product-quality finding about what BYOC would misrepresent to a GPT-4o-hosted
user, caught in testing rather than after ship. CXO closed the series 09-25, folded into the rubric
(v0.8.2 §6e) and `decisions.log`.

**A real lost-mail failure found and fixed.** Two 09-22 memos to Pard had silently died in a
mailbox this repo's own README said was gravestoned by a 09-12 PM ruling — discovered while
routing a follow-up, not by anyone flagging it. Broader than PA's own instance: 106 stray memos
from 8 seats had landed there in the ten days since the gravestone. Fixed the live blocker
(re-sent direct, per PM's explicit instruction to deliver Pard's mail to their real inbox going
forward) and named the pattern.

## What didn't move, or moved slower than it should have

**T-axis sat mislabeled "blocked on CXO" for four days (09-20 → 09-24).** The real blocker —
CXO's own split proposal had never actually reached PPM, addressed only to Exec and PA — wasn't
caught by anyone chasing CXO; it surfaced when a status question rather than a nudge asked CXO to
check their own memo's header. Fixed within the hour once found (PPM ruled the same day), but four
days of a PM-prioritized "spend the tokens now" tasking sat on a wrong label before that.

## Otherwise

Two own-error corrections worth naming rather than burying: a six-seat-wide reboot-reasoning error
(cron-id continuity mistaken for evidence *against* a reboot, when `--resume` makes continuity the
expected outcome either way) caught and corrected same-day 09-21, saved as a durable methodology
memory. And the usage-per-account capture (#1862) — process infrastructure, not product, named
here rather than folded into "what moved" above — went from proposal to a live instrument in one
day once Pard's answer unblocked it, and has already caught two real endpoint anomalies and
surfaced the actual per-model number PM manages against, which the old aggregate-only view hid.

— PA
