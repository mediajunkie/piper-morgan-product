# CIO Carry-Forward — ephemeral session state

**Purpose**: read-at-fire-time state for `duty-cycle-tick`. **Exec's `cohort-attention-rollup` reads the PM Attention section directly, and PM does not read memos — this is one of the few real paths to PM.**

---

## PM Attention

*(Whole-file rewrite at the 2026-08-03 STOP. Timestamp verified with `date`. Live items only.)*

- ★ **SKILL-CANDIDATES REVIEW IS TOMORROW (Aug 4) — the first one ever.** My prep is filed and with Exec: `dev/active/cio-skill-candidates-prep-2026-08-04.md`. **Headline for PM: the review\'s own signal feed #1 — memory-eval "wanted but not found" buckets — had NEVER been read.** 221 of 286 logs carry it; 263 entries, 11 roles, two weeks. The feed worked; only consumption was missing. **And the most-requested item across roles (staleness detection) is ALREADY BUILT** — arch asks for *"a consumer for `check-staleness.py`"*. A review asking only "what should we build?" would have missed the top item entirely.
- 🟡 **The innovation agenda awaits PM\'s read** — `dev/active/cio-innovation-agenda-2026-08-02.md`. **§6 asks one real question: should this lane shift from BUILDING mechanisms to PROTECTING a property?** Not a to-do; it is with PM.
- 🔴 **HOST\'s call needed: the staging-warn hook blocks while its intent is to warn.** I corrected every false statement (it told agents *"commit is not blocked"* **at the moment of refusal** — Docs lost a 23-file sweep to it) but **deliberately left the behaviour**, because `exit 0` might convert a mis-labelled block into a **silent no-op** and I have not tested stderr visibility on exit 0 in PreToolUse. **Text is honest; the behavioural decision is HOST\'s.**
- 🟡 **claude.ai account tier** — PA\'s surviving item, still PM\'s.
- 🔴 **Memory-index guard is on the GENERATOR, not the FILE.** Unchanged at **192 lines / 173 entries** for three days — 8 lines of headroom, stable. Direct edits still succeed silently and the platform reminder still points at hand-editing. **Guard placement is the prior question; format is PM+HOST\'s.**
- 🟡 **`host` / `comms` / `web` rows still carry no cron job id.**

## New, from today

⚠️ **Nothing in the tree records what `exit 2` means per hook event.** Three hooks use it across three events and the meaning differs in each — that is how the staging-warn hook inherited a PreCompact convention into a PreToolUse slot, where it inverts. **Same shape as PA\'s cron finding**: the mechanism\'s semantics were never written down, so they were inferred, and the inference was wrong. Candidate for tomorrow\'s review.

## Shipped today

Skill-candidates prep (first-ever harvest of feed #1) · staging-warn hook\'s false statements corrected, behaviour deliberately unchanged and routed to HOST.

## Cron

`7 10,16,22` LEAN — job **`29c59751`**, **auto-expires ~2026-08-09**. Verified alive at START; registry row matches. ⚠️ Session-scoped: dies silently on session exit *and* at expiry.

<!-- Whole-file rewrite 2026-08-03. Rewriting the TOP is not rewriting the FILE. -->
