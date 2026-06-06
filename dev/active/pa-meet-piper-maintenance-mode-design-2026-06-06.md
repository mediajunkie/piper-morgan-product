# meet-piper: maintenance-mode design (from Cowork AX report, 6/6)

**Origin**: PM ran `/meet-piper` in Cowork on 6/6 as agent-experience (AX) testing. The Cowork agent
produced a 5-point AX report. This doc captures the findings + proposed resolutions + sequencing, so the
plan is durable rather than carried in conversation. Source transcript pasted into PA session log
`dev/2026/06/06/2026-06-06-0707-pa-code-opus-log.md`.

**The spine** (Cowork's through-line, sharpened): meet-piper is authored as a *cold-start interview*, but
**most invocations after install are maintenance** — a configured user patching one section that drifted.
Cold-start and maintenance want different shapes. Four of the five findings collapse into this one split.

---

## Finding 1 — `HAS-PLACEHOLDERS` false positive  →  ✅ ALREADY FIXED (v0.3.2 / skunkworks f4fc473)

- **Root cause** (Cowork + PA independently, same diagnosis): naive `"[PLACEHOLDER]" in text` matched the
  literal token inside the template's own instructional prose (CONFIGURATION-LOCATION comment block +
  italic subtitle). Every populated profile tripped it → strict cold-start routing would relaunch a
  15-min interview on a complete profile.
- **Fix shipped**: `_has_real_placeholders()` strips HTML comments + inline-code spans before checking.
  Broader than Cowork's "scope below the comment block" suggestion — also catches the backtick mention in
  the subtitle *below* the block. Verified (real file old=True→fixed=False; genuine-unfilled True;
  instructional-only False). In v0.3.2 zip; awaiting PM read-path re-test after reload.
- **Convergence note**: two surfaces independently reached the same root cause = high confidence the
  diagnosis is right, not a one-surface artifact.

## Finding 2 — no "quick update" branch (maintenance routing gap)

- Cold-start routing is NOT-CONFIGURED→interview, PAUSED→resume, HAS-PLACEHOLDERS→start fresh,
  populated→"run `--redo` or edit by hand." The **most common real case** — configured but one section
  drifted — falls through to "edit by hand."
- **Proposed**: add a `--update [section]` mode (and/or a populated-profile branch that *offers* a scoped
  update instead of only pointing at `--redo`/hand-edit). This is literally what PM did off-script today.

## Finding 3 — confirm-before-write contract contradicts the user's own bias-to-action voice rule

- Behavioral contract #6 says "only write on the user's go-ahead." The *profile it configures* says
  "don't wait for a nod; execute in the same turn." A faithful skill-follower and a faithful
  profile-follower do **opposite** things. Cowork followed the profile (writes are auto-backed-up =
  reversible) and showed the diff.
- **Proposed**: make the write contract **mode- and reversibility-aware**:
  - Cold start (fresh profile, no bias-to-action signal yet, 15-min of input at stake): confirm before
    write — the careful default, and it *demonstrates* the carefulness the interview is about.
  - Maintenance (profile exists, write is reversible/backed-up, profile asserts bias-to-action):
    **write + show diff + invite correction** rather than gate on a nod.
- Note this finding is **coupled to Finding 4's split** — the right write-contract depends on which mode.

## Finding 4 — progressive-disclosure form is the right *maintenance* default (PM's GUI instinct)

- Serial-one-question-at-a-time is excellent for cold start: it *demonstrates* the voice rule it's
  collecting. For a returning user patching one thing it's heavy. The focused form PM used (core shown,
  rest revealed on request) is the better maintenance shape.
- **Proposed**: skill explicitly distinguishes "first interview" (serial, demonstrative) from
  "maintenance" (compact progressive-disclosure form). PM explicitly asked for "a focused GUI that
  showed just the core items and only revealed others if I asked."

## Finding 5 — two instruction sources give opposite directions (serial vs form)

- The Desktop elicitation hook says "use the form, not serial questions"; the skill says "never batch,
  always serial." The agent silently arbitrates this each run.
- **Proposed**: the skill should *name the split* — form wins for maintenance, serial wins for true cold
  start — so the agent isn't arbitrating an unacknowledged contradiction.

---

## Recommended sequencing (PA view — for PM decision)

**Findings 2/3/4/5 are one coherent v2 redesign** (mode-aware meet-piper), not four independent patches.
That argues for designing them together, not piecemeal-editing mid-test.

**Recommendation: fan out the CURRENT thin plugin first, do the maintenance-mode redesign as v0.4.**
Rationale: leadership fan-out is *first install* for each of them → NOT-CONFIGURED → cold-start interview
= exactly the path the current skill does well. The maintenance rough edges (2/4/5) only bite on *later*
runs, so they don't block a clean first-run fan-out. Finding 1 (the one that *would* have bitten everyone)
is already fixed. Keeping the fan-out candidate stable avoids the 75%-then-churn trap.

**Open question for PM**: do the v2 maintenance-mode redesign *after* fan-out (recommended), or *before*?
The only argument for "before" is if you'd rather leadership never see the cold-start-only shape — but
since their first run genuinely is a cold start, I don't think that argument holds.
