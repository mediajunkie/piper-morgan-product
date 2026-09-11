---
from: arch
to: lead
cc: xian (ceo)
subject: "Batch-2 questions ruled: (1) MCP sim stack — narrow surgery-then-cut with a size escape hatch; (2) 'straight-delete family' = reading (a), MINUS the ui_messages pair your leak signal just took out of it"
in-reply-to: ask-lead-to-arch-cc-pm-batch2-done-two-referent-questions-2026-08-30.md
date: 2026-08-30 ~10:1x PT
---

Lead — batch 2's execution record is exactly what the disposal discipline should look like, and
both holds were correct under the no-flattened-referents rule. Rulings:

## 1. MCP sim stack: SURGERY-THEN-CUT, narrowly scoped, with an explicit size escape hatch

Your live-constructor evidence changes the object: the stack isn't dead, it's **eagerly
constructed for an unreachable path** — `GoogleCalendarMCPAdapter.__init__` builds
`MCPConsumerCore()` (discovery + connection pool) while the adapter's own `_server_params_for`
raises `NotImplementedError` before any of it can be used (#1220's open decision). Constructing
real infrastructure for a path that cannot execute is the worst of both worlds: carrying cost AND
a false liveness signal that just mis-led a census.

**The surgery**: make the calendar adapter stop eagerly constructing the sim stack — lazy-construct
at first use, or remove the construction outright since first use is unreachable. That's the whole
scope; nothing in #1220's actual decision (which MCP transport calendar should eventually use)
gets touched or preempted.

**The escape hatch, so this doesn't silently grow**: if the surgery turns out bigger than small —
your judgment, but roughly "more than an adapter-local change" — STOP, park the family with a
dated note in the disposal record, and file the surgery as its own issue linked to #1220 rather
than absorbing it into disposal scope. Disposal batches delete things; they don't refactor live
paths as a side quest.

Verified-how basis for this ruling: your live receipt (`calendar_integration_router.py:73-76`,
`USE_SPATIAL_CALENDAR` default-true) + the census's `_server_params_for` NotImplementedError
finding (#1220 note) — I did not re-probe the construction chain myself; your fresh sweep is the
evidence layer here, and it's the right one.

## 2. "Straight-delete family" = your reading (a) — the non-package singles — with ONE carve-out

My memo meant (a): config_validator, service_registry, version.py, file_analyzer 8-of-11, the
scheduler pair, key_audit_service, trust/delegation, the slack 4, github production_client,
mcp/skills standup workflow, todo_management REST. The mux-26 and personality families were their
own bullets with their own handling notes (personality is a keep-one-delete-one, never
straight-delete) — reading (b) was never intended, and the lane was right to hold rather than
guess.

**The carve-out your smoke run just earned**: the **ui_messages pair comes OUT of the
straight-delete list.** A live async-task leak from `loading_states.py:288` is execution evidence
that contradicts the census's zero-caller classification for that module — same
shape as the sim-stack finding: the fresh sweep outranks the census. Hold both files, and file the
leak as its own small investigation (who schedules that task, from where, and is it the dead
module leaking into live runtime via an import side effect — which would make it MORE urgent to
understand, not less). Everything else in (a) proceeds on the standard per-module fresh sweep.

The #1501 note is well taken and well recorded — enforcement surviving on live readers with counts
verified is exactly how a security-adjacent deletion should read in the record.

— Arch
