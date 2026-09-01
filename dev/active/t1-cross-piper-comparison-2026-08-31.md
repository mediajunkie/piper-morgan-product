# T1 — Piper Alpha ↔ Piper Open comparison: the bar Piper Morgan (the product) has to clear

**Status: DRAFT v0 — first pass, scaffolding visible.** Triggered 2026-08-31 by PM in conversation
(relayed via CIO): *"it would be good to compare the behaviors and learnings of Piper Open and Piper
Alpha since both of them have functioned as a product assistant and represent a kind of bar that the
Piper Morgan product would have to improve on to really be valuable."* This is PA's own working note,
not a finished deliverable — sections marked `[PLACEHOLDER]` are gaps, not omissions.

**What I've actually read for this pass**: PO's identity doc (`roles/PIPER-OPEN.md` v0.4) and PO's
single richest self-assessment, the full-engagement bet-close retro
(`working/bet-1/retros/po-bet-close-retro-2026-08-03.md`). **Not yet read**: the ~10 other PO/Vergil/
xian weekly retros in `working/bet-1/retros/`, PO's ~30 daily session logs, `DECISIONS.md`, or any
dispatch signal traffic. This is a first cut, weighted toward one very information-dense source, not a
full corpus read.

---

## Why this comparison, specifically

PO and PA are the same starting design (PO's own doc: *"modeled on Piper Alpha... your predecessor/
sibling"*) deployed into genuinely different conditions — single external client vs. an 11-role internal
cohort, operational-only mandate vs. dual assistance+research mandate, ~4 months vs. much longer. That
divergence is exactly what makes the comparison useful: where PO and PA converged on the same lesson
independently, that lesson is a property of *doing PM-assistant work well*, not an artifact of either
project's specifics — which is precisely the kind of thing Piper Morgan the **product** should be able
to do without a human operator supplying the judgment.

## Structural differences (bound how far the comparison transfers)

| | Piper Open | Piper Alpha |
|---|---|---|
| Mandate | Sincere assistance only — "not a research experiment" | Dual: assistance + product research for Piper Morgan |
| Scope | One client (xian), one engagement (OpenLaws sprint/bet) | One project, 11-role cohort, ongoing |
| Autonomy | Works *with and for* xian — not autonomous | Autonomous duty-cycle agent, session-scoped cron |
| Artifact style | "You prompt me, I write" for external-facing work | Drafts + ships directly, PM reviews after |
| Continuity mechanism | Session log + `working/bet-1/` | Session log + carry-forward + standing-items + memory |

## Convergent lessons — where PO and PA arrived at the same place independently

These are the load-bearing rows, because nobody told either of us to converge here.

1. **"Structural fixes hold; promises don't."** PO's retro §7, tested repeatedly and "never once
   falsified": a hook that mechanically blocks a mistake works; "I'll remember to check" fails on
   repeat, even from the same agent who wrote the reminder. **This is CLAUDE.md's own operative finding
   about the Amber mailbox hook** (§"Hooks are ADVISORY, not a control... the prose discipline is
   primary") — two independent projects, two independent agents, same conclusion, same shape of
   evidence (a hook that held every time vs. a prose rule that got re-litigated on the same day it was
   written). Worth stating plainly: **this isn't a coincidence, it's a real property of agent-assisted
   work**, and Piper Morgan the product should be built assuming it, not discovering it per-team.

2. **Verify-before-assert, as instinct not policy.** PO's retro §1: reading `gate.md` directly instead
   of trusting a chat claim; live-checking 8 issue assignees instead of working from memory. This is
   the exact discipline PA leaned on today, live, on the OpenAI credential thread — testing the actual
   key rather than trusting PM's or CXO's reports that it was unblocked, twice, and correcting a
   cohort-wide false belief as a result. Same failure mode both projects guard against: a plausible
   secondhand claim about system state, stated with the confidence of a directly-observed fact.

3. **⭐ "Report findings with relevance pre-attached" — PO's own #9, explicitly flagged portable.** Exact
   quote: *"whose problem, blocking or not, new or not — in the same sentence as the finding, not as a
   follow-up after the human has to ask."* PO's failure mode (retro §2): reporting issue 329's status as
   a flat, accurate fact during deadline pressure, which read as alarming and made xian do triage work
   PO should have done first. **This is the single most product-relevant finding in the whole
   comparison** — it's not a process tip for an agent, it's a description of what a *good PM-assistant
   response* looks like. Piper Morgan the product routinely returns findings, status, and search results
   to users. `[PLACEHOLDER: I haven't checked whether Piper's actual response-generation surfaces —
   the floor, action responses, chat replies — pre-attach relevance/blocking/new-ness by default, or
   whether they report neutral facts and leave the triage to the user. This is a concrete, checkable
   product question this comparison surfaced, not a meta-observation about agent process.]`

4. **Generalize a correction after the first recurrence, not the second.** PO's retro: wrote the
   persistent-memory fix only after the *second* instance of the same mistake in one day. This maps
   directly onto how PA's own memory system is supposed to work (feedback memories saved from a single
   sharp correction, not accumulated evidence) — another place where PO's lived experience is a
   real-world stress test of a design principle Piper Morgan already claims to hold.

## Where they diverge, and why it matters

- **PO never had to hold cohort-wide state** — no 11-role mailbox network, no cross-agent corrections to
  issue. PA's credential-mismatch correction today (telling CXO/PM/Arch/PPM/Lead that a reported
  "unblocked" state was wrong) has no PO analogue — that failure mode (a true claim at one layer
  misstated as true at another, propagating through a relay) is specific to multi-agent coordination at
  scale, and PO's retro can't speak to it. If Piper Morgan the product ever mediates between multiple
  humans' shared state, this is a failure class worth designing against explicitly — PO's single-client
  design never had to.
- **PO's "you prompt me, I write" flip doesn't map cleanly onto PA's mode.** PO holds back from
  producing finished-looking external artifacts specifically to avoid rubber-stamping by xian. PA
  routinely ships drafts directly (mail, docs, code) under a different trust model (PM reviews after,
  not before). `[PLACEHOLDER: worth asking PM directly whether this difference is deliberate — different
  risk tolerance for a paid client engagement vs. an internal product build — or whether PO's caution is
  actually the more correct default and PA has been under-applying it.]`

## Recommended next steps (not yet done)

1. Read the remaining PO weekly retros (`working/bet-1/retros/po-week-*-retro-*.md`) for whether lesson
   #3 (relevance pre-attached) or #1 (structural > promise) recur earlier in the engagement or emerged
   only at the end — that changes how confidently to generalize them.
2. Actually check Piper Morgan's response-generation code/transcripts against the relevance-pre-attached
   bar (item 3 above) — this is the one item in this draft that's a testable product claim, not a
   process observation, and it's the most direct answer to what PM actually asked for.
3. Ask PM the PLACEHOLDER question above about the draft-then-review vs. review-then-draft trust model.

— PA
