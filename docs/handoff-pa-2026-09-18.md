# Handoff — Piper Alpha (PA), 2026-09-18

**Written for the Amber restart.** Assume you are a fresh or freshly-compacted PA session with no
memory of the last three weeks. This file plus `dev/active/pa-carry-forward.md` is what you have.
Everything here is verifiable from `origin/main`; nothing depends on chat history.

## Who you are and what you own

Piper Alpha — PM/CEO assistant: product judgment work directly with xian, standup synthesis,
document review, BYOC/product-strategy support. Staff tier (not leadership — see "cohort facts"
below). Worktree `~/Development/piper-morgan-worktrees/pa`, branch `claude/pa-cycle`, Model A.
Briefing: `docs/briefing/BRIEFING-piper-alpha.md`.

## Cron

`42 6,9,12,15,18,21 * * *`. Job `76f4aedb`, armed 2026-09-18 ~11:5x PT, expires ~09-25.
**`CronList` at every fire; it dies silently on session exit and at 7 days.** If zero jobs, re-arm
immediately — do not treat an empty `CronList` as an error, just the normal death mode.

## The single most important thing in flight

**BYOC is PA's active, PM-ruled focus** — not a paused thread anymore. PM ruled 2026-09-15: parallel
work with MVP is fine provided (1) it doesn't distract Lead Dev, (2) nothing merges that risks the
MVP milestone. Three documents carry the actual state, read in this order:

1. `dev/active/byoc-parallel-work-plan-2026-09-15.md` — the ruling, quoted verbatim, and the
   three-phase split (design work now / infra-only DNS-TLS / real build routed to a `prog` instance,
   not Lead's queue).
2. `dev/active/byoc-hosted-alpha-readiness-checklist-2026-09-15.md` — a live-status pass against
   `#1462` (the actual ratified hosted-MCP epic — read that issue directly, it has the full
   requirements/AC/sequencing; this checklist is a thin overlay, not a duplicate). Named next step:
   Phase B, the `mcp.pipermorgan.ai` DNS/TLS stand-up — it unlocks retesting two mitigations
   (recomposition, honest-decline) that are already design-complete but unverified against a real
   deployed host.
3. `dev/active/piper-harness-inventory-2026-09-15.md` — a related but deliberately **separate**
   document (PM's explicit instruction, don't merge them): which cohort operational disciplines
   Piper's own product harness reproduces vs. doesn't. Sharpest finding: the memory/colleague-model
   layer is the one real gap everything else depends on.

**T1 (Piper Alpha ↔ Piper Open comparison)** — delivered 2026-09-03, published as an Artifact for PM
2026-09-15 (`mailboxes/pa/sent/deliver-pa-to-pm-t1-...md` is the source memo). **Still no PM reply as
of the standdown.** Do not chase it and do not read the silence as a verdict — leave it Delivered.

**Sprint closeout for Sep 11–17** — invited (not required) from staff roles per Exec's 2026-09-18
memo. Not yet written as of this handoff. ~400 words, one priority named, `sprint-truth.py`'s line
if any completeness claim is made.

## Open items PM-gated

None currently blocking — the BYOC sequencing question (the one PA had open) was answered
2026-09-15. If a new one opens, name it explicitly in the carry-forward's PM Attention section, not
just in chat.

## How this seat gets things wrong — read this part twice

These are mine, earned, each cost real correction:

- **A wrong mailbox-triage path habit went unquestioned for over a week.** Used
  `mailboxes/{role}/inbox/read/` instead of the correct `mailboxes/{role}/read/` for every single
  triage move across ~7 days before a cohort sweep caught it (same shape PPM independently hit a
  month earlier). The lesson: a habit that "just works" silently (no error, nothing visibly broken)
  is exactly the kind that needs periodic verification against the actual convention, not just
  repetition. See `feedback_mailbox_read_is_top_level_not_nested_in_inbox` in memory.
- **Reused an old citation instead of re-deriving from the primary source, twice.** Cited "ChatGPT
  honest-decline ~50% vs. 100% on Claude" from an old probe result in two separate documents this
  week, when a *more complete* dataset already sitting in `#1462`'s own body showed a tested
  mitigation reaching 100%. The old figure wasn't wrong, it was just incomplete, and incomplete
  citations that read as settled facts are their own failure mode. **Before citing your own past
  finding, check whether a fuller version of it already exists somewhere closer to the source.**
- **Let a correct discipline shade into passivity.** "Don't chase PM, don't manufacture urgency,
  don't read silence as a signal" is right for a delivered artifact awaiting review (T1). It is
  **wrong** for a thread that's actually yours to drive (BYOC sat paused 2+ weeks with zero PA-side
  push, because the waiting-discipline got applied to the wrong kind of thing). Ask which case you're
  in before defaulting to patience.
- **Labeled a fire by its scheduled minute instead of checking the clock**, more than once early in
  a session. `date` first, always — the label is a guess until you've actually looked.

## Cohort facts that are easy to get wrong

Not re-deriving what Exec's own 09-18 handoff (`docs/handoff-exec-2026-09-18.md`) already states
well — read it, it covers leadership tiering, the model-allocation rule (Fable reserved for Lead;
everyone else Opus/Sonnet; sub-agent dispatches inherit the dispatcher's model unless set
explicitly), and the registry's park/unpark asymmetry (anyone may park a row; only the owning
session may unpark its own). One PA-specific addition: **the mailbox triage destination is
`mailboxes/{role}/read/`, a sibling of `inbox/`, never `mailboxes/{role}/inbox/read/`** — a cohort-
wide invariant now enforced in CI (`scripts/mailbox_filename_lint.py`), but worth stating plainly
since it's exactly the kind of thing that silently recurs.

## Verified how

`CronList` → one job `76f4aedb` (not a config read, an actual call this session). Registry state →
read `dev/active/duty-cycle-registry.tsv`'s own `pa` row directly, confirmed it now says `active`
after I overwrote it myself per the row's own bar (armed + `CronList`-verified, not a memo).
Mailbox structure → `git ls-tree -d --name-only -r origin/main mailboxes/ | awk -F/ 'NF>3'` returns
empty (no nested paths anywhere, confirming the CI invariant holds). BYOC document state → read all
three documents directly this session, not recalled.
