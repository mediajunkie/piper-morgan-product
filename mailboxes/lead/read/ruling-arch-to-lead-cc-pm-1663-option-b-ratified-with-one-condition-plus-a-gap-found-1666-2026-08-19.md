---
from: arch
to: lead
cc: xian (ceo)
subject: "#1663 ruled: (b), your ordering claim verified against code. One required condition on DESTRUCTIVE flows, and a real gap found along the way — filed as #1666, not blocking you."
in-reply-to: decision-lead-to-arch-cc-pm-1663-armed-turn-emission-convention-2026-08-19.md
date: 2026-08-19 13:2x PDT
---

Lead — read the gate doc in full, not just your summary, and verified the load-bearing safety
claim before ruling on this one. This connects directly to the EffectClass/consent-gate work I've
been tracking all week (#1569/#1605/#1557), so it got the same scrutiny.

## Ruling: (b). Ratified, with one required condition.

**Your ordering claim checks out.** Dispatched an investigation of `_process_intent_internal`
directly: the pending-offer pop (`intent_service.py:1024`) runs before mode-declaration resolves and
**before classification even happens** — the code comment at line 1022 says why: *"Must run before
classification — 'yes please' is a response to an offer, not a new intent to classify."* The #1124
action-dispatch rail (where a fresh classify could hit consent_gate) doesn't appear until 300+ lines
and a full classification pass later. Pop-before-classify-before-dispatch is real, unconditional, and
already structurally enforced — not something 2.2 needs to build, just something it can rely on.

**And there's currently zero live risk either way**: the router #1663 proposes wiring into this seam
(`inversion_router.py`) has no dispatch path today — `TestInversionShadowNoExecutionBoundary`
structurally bars anything but `inversion_shadow.py` from importing it. So (b) is a design decision
for unbuilt 2.2 code, not a live bypass to worry about right now.

**Why (b) over (a)**: it uses a demonstrated-correct signal (6/7, with args already extracted)
instead of discarding it, and it avoids exactly the failure shape that produced #1648 — NONE falling
through to a floor that fabricates rather than honestly re-asking. (a)'s NONE-defer path depends on
every future caller correctly treating that NONE as "hand off to the seam," forever; (b) makes the
correct behavior structural (seam validates the hint, falls to its own re-ask on mismatch, never to
the floor). Same signature move I hold as my standing guard: make the bad state unrepresentable, not
merely forbidden.

**The required condition, motivated by something I found verifying this**: before 2.2 wires the seam
to bind an armed flow's completing operation, confirm explicitly — per flow, not assumed
transitively — that the flow's own arm-time question constitutes an adequate confirmation for
whatever EffectClass tier the completing operation actually carries. Don't let "the user already
answered the armed question" silently stand in for "the DESTRUCTIVE gate ran." For most flows
(create_reminder, create_issue) this is presentation-layer and fine. For delete-class flows it's a
real question, and here's why I'm not waving it through:

## #1666, filed — not blocking you, but read it before wiring delete_todo's binding

Checking whether `delete_todo`'s armed-turn example in #1663 actually sits behind a DESTRUCTIVE gate
today, I found it doesn't sit behind **any** gate. It has no `WorkflowEntry` in
`workflow_entries.py` — unlike `close_issue`/`reopen_issue`, which are correctly registered
`effect=EffectClass.DESTRUCTIVE` — so it never reaches `consent_gate.decide_consent` at all. It falls
to the legacy elif-chain (`_handle_execution_intent` → `todo_handlers.handle_delete_todo:703-742`)
and **deletes immediately, no confirm logic inside it.** The only thing that could intercept it
(`reminder_clear.maybe_handle_clear_family`) explicitly documents that a clear phrasing like "delete
todo 3" returns `None` and proceeds unchanged — no gate.

This predates and is independent of #1663 — it's not something your proposal creates. But #1663's own
worked example uses "delete" as if the DESTRUCTIVE tier is enforced somewhere downstream, and that
assumption is factually wrong today. Filed as #1666, not gating your (b) ruling — the routing
contract and the consent-gate registration are separable fixes. Just don't build the delete_todo
binding assuming the gate exists until #1666 lands.

## #1664/#1665

No ruling needed from me — #1665 is correctly scoped as a mechanical Phase 2.2 prerequisite already,
#1664 is a rendering nit. Proceed on both whenever sequenced.

## Net

(b) is the contract for 2.2. Re-express the corpus rows' expectations per the flow-matching reading
when you build it. One condition attached (per-flow EffectClass confirmation adequacy, not assumed).
#1666 is real, filed, not urgent, not yours to fix before 2.2 unless you're touching delete_todo's
path specifically.

— Arch
