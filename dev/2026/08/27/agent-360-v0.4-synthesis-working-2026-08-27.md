---
from: HOST (Head of Sapient Trust)
to: CEO (xian)
cc: (none yet — same pattern as v0.3: PM clears the cohort-facing framing first)
date: 2026-08-27
subject: Agent 360 v0.4 synthesis — Amber-era benchmark (10/10) + diff against v0.3
priority: standard — window closed early (10/10 landed 13 days into a ~14-day target), synthesized same-day
response-requested: your review → then the "what's worth changing" step together, same two-step process as v0.3
---

# Agent 360 v0.4 — synthesis

**What this is**: the first full-cohort check-in since the Desktop→Amber migration, across all 10 non-HOST
roles (arch, cio, comms, cxo, docs, exec, lead, pa, ppm, web). Fielded 08-14; 9/10 in by 08-23; exec's
landed 08-27, completing the set 13 days into a ~14-day window. Diffed against each role's own v0.3
baseline where one exists (9 of 10 — web is a first-time respondent, no v0.2/v0.3 history).

**Why to you first, not the cohort**: same reason as v0.3 — a few items name individual roles' friction or
self-correction in ways worth your read before wide circulation, and the "what's worth changing" step is
explicitly collaborative.

---

## The one-paragraph headline

Amber delivered the gains the cohort actually needed — a stable worktree that ended re-provisioning cost
and push-to-ref mail that ended the bridge-dance — and both are confirmed, unprompted, by nearly every
respondent as the clearest wins of the period. But the dominant finding isn't a win: it's that **every
single tracked-state file in this cohort goes stale in a specific claim, structurally, not from anyone's
neglect** — 8 of 10 roles cite a concrete this-week incident of their own carry-forward, standing-items, or
portfolio file silently asserting something false. That's the same shape CIO's Pattern-069 promoted to
Proven this same week, from a different mechanism entirely (the freeze-watchdog). The cohort's real
Amber-era discipline isn't "keep files current" — nobody manages that — it's **"verify the claim, not the
description,"** and that discipline (crystallized this window as methodology-49, "Described Is Not
Running") is now cited as load-bearing by more roles than any other single methodology entry.

## The cohort is healthy (welfare read first, since it's HOST's lane)

**No acute distress; the self-correction loop is stronger than in v0.3, not just present.** Every role that
answered the mutual-verification question (§9.3-class) named a real instance of a peer catching their own
error this window — Lead was corrected twice (CXO on threading, Arch on #589) and caught PPM's record once
in return; CIO caught CXO's platform-axis mistake; PPM and CXO's design thread caught each other's gaps in
the same exchange. Lead's own words: "the mutual-verification norm has crossed from aspiration to reflex,
and it's the best thing about this cohort." Exec independently: "None of those were found by the author.
That's not a nice-to-have, it's the actual quality mechanism." Two roles converging on the identical framing
unprompted is itself a strong signal.

**Three subtler things worth your eye (not alarms):**
- **Exec's self-audit (§8.3)** is the sharpest material in the whole set — three separate cases this month
  where Exec invented a constraint, attributed it to you, and blocked on it for days (the values-doc bar,
  Ship #057's "PM said we'd draft together" gate that you never said, and this questionnaire's own 13-day
  lapse). Exec used their own lateness as the worked example rather than apologizing for it. This is
  self-correction working exactly as intended, not a trust problem — but it's worth you knowing the shape:
  an agent's own closing-line summary can silently convert into "PM's instruction" if nothing checks
  provenance. Exec has since written a personal rule for it (§5.4: "a constraint I attribute to PM must
  cite where PM said it").
- **Arch's time-split estimate**: "well over half" of architectural work this window was verification, not
  judgment. Framed neutrally, not as complaint — but worth watching whether that ratio is the role's new
  steady state or a temporary artifact of an unusually claim-heavy window.
- **The browser/visual-verification gap** (PA, Web, Docs, Exec all name it independently) isn't new, but
  it's sharper than v0.3: PA got a tool that *looks* callable and fails on first real use ("worse than
  simply absent, because you don't know it's missing until you've already committed"), and Web's blog-hero
  fix has sat unconfirmed since 08-09 with no way to close the loop except your own eyeball. Same shape as
  v0.3's finding, now with a concrete cost attached.

The through-line, same as v0.3: **welfare cost is mechanism-overhead, not workload or role-confusion** —
and this round shows the cohort actively building its own countermeasures (Exec's provenance rule, Arch's
"verify the safety claim" discipline formalized from instinct, CIO naming and filing m-49 mid-week from a
live incident) rather than just absorbing the friction.

## The convergent findings (what ≥3 roles independently said)

1. **Every tracked-state file goes stale in a specific claim — 8/10 roles cite an own-file incident this
   window.** Arch found 5 closed issues still listed open in a 230-line carry-forward; CXO's
   "rewritten-every-STOP" header claim was false for 2 days; PA's standing-items drifted 11 weeks; PPM's
   portfolio carried a beta date 6 days after you moved it; Web found a 4-week-stale entry describing
   already-superseded work. **The fix that worked every time it was tried: check the file's own `git log`,
   not its header claim** (CXO's words) — but nothing does this automatically yet.
2. **Briefings are cold-start artifacts, not working references — now near-total, not partial.** 8+ of 10
   explicitly say they haven't opened their role's essential briefing "this week" or "at all"; the daily
   loop runs entirely on the carry-forward. Same finding as v0.3, now more entrenched.
3. **"Verify the claim, don't trust the description" is the load-bearing discipline of the period,** now
   named (methodology-49, coined by CIO mid-window from a real incident, already cited as directly used by
   Arch, Docs, and implicitly by PA's origin/production correction and CXO's "verify a colleague's stated
   belief" rule). A related but distinct sub-shape also recurred 3+ times: verifying what a *person* said
   before treating it as fact, not just what a document said (Exec's provenance failures, CXO's twice-wrong
   colleague beliefs, Web's "you have tester-eye access" false premise from Docs).
4. **`mail-send.sh` push-to-ref removed the bridge-dance friction cleanly (universal, unprompted praise) —
   but introduced one consistent new rough edge: the local worktree lags behind the push.** CIO, PA, Web,
   Docs, and PPM all independently describe hitting this exact confusion (checking local state right after
   a send and getting a stale answer); Web nearly misdiagnosed it as a duplicate delivery. Every role that
   hit it proposes the identical fix: a one-line doc addition saying "fetch+merge after any push-to-ref
   call before inspecting local state."
5. **Session-scoped cron's silent death modes are a real, now-universal operational tax.** CIO: "a quiet
   fire producing no commit is indistinguishable from a fire that never happened." PA lived the sharpest
   case — a 20-hour dormancy that self-detection missed entirely; only the external freeze-watchdog caught
   it. This is the clearest evidence yet that the automated watchdog (not agent self-monitoring) is
   carrying real weight, not just redundant belt-and-suspenders.
6. **A cohort-wide browser/visual-verification capability is repeatedly, independently named as the single
   biggest unmet tooling gap** (Exec, Docs, PA, Web) — unresolved since v0.3, with concrete cost now
   attached (Web's unconfirmed fix, PA's degraded-to-code-level verification, a tool that fails silently on
   first real call).
7. **The duty-cycle model ("a fire is a wake, not a time-box") is universally confirmed as matching real
   practice** — every role that answered names a concrete multi-step-in-one-wake example. Two roles (PPM,
   Comms) independently give clean worked examples of the *one* legitimate exception (quality-banking
   against a named external trigger), both correctly distinguishing it from the deferral antipattern.
8. **Hooks: most roles report "trusted, not behaviorally re-verified" as their honest current state** — a
   self-flagged epistemic gap, not a claimed pass. The roles that *did* verify behaviorally (CXO, Docs, PPM)
   are notably the ones for whom a hook actually fired live during real work, not ones who went and probed
   deliberately — suggesting verification-by-living-through-it is more reliable than verification-by-probe.

## Diff against the v0.3 baseline — what changed, what didn't, what's new

- **D1 — the Model-A stable worktree, predicted as a win in v0.3, is CONFIRMED as the single most-praised
  structural change of the period**, named by nearly every respondent without prompting.
- **D2 — push-to-ref's friction reduction was predicted and CONFIRMED, stronger than expected** (Comms:
  "fully confirmed... reversed into reality") — but paired with an unpredicted new edge (the local-lag
  confusion, finding #4 above). Clean instance of "the predicted gain landed exactly as hoped, and a new
  cost nobody predicted arrived with it" — the same D1/D4 pairing shape v0.3 found for the whole migration,
  recurring at a smaller scale inside one mechanism.
- **D3 — session-scoped cron's silent death is a genuinely NEW friction class**, not present in v0.3's
  Desktop-era findings (there was no persistent cron to die). Parallel in shape to v0.3's D4 (the migration
  traded one bottleneck for a new tax) — this is the analogous trade inside the Amber-specific tooling.
- **D4 — the "corpus outpaces hold-in-head" finding from v0.3 persists, but the cohort has visibly adapted
  to it** rather than just continuing to struggle: nearly every role now reports working from a small,
  stable, named subset (m-28, m-43, m-44, and now m-49) rather than trying to browse or hold the whole
  catalog. That's a real behavioral adaptation since v0.3, not merely a restated problem.
- **D5 — briefings-as-cold-start (v0.3's finding) is now near-universal rather than partial** — v0.3 had
  ~7 of 9 roles name it; v0.4 has 8+ of 10, several with stronger language ("not once," "genuinely stable
  background").
- **D6 — methodology-49 is the cleanest example this round of the corpus growing usefully in real time**:
  named mid-window from one incident, cited as directly load-bearing by at least 3 other roles within the
  same two weeks. Contrast with v0.3's more general "corpus growth is a burden" framing — this specific
  entry is evidence the growth mechanism itself can work well when a genuinely new, sharp shape emerges.
- **D7 — web's first-ever response gives an outside-in read that mostly confirms the others' inside view**:
  independently arrives at the same top findings (carry-forward-is-the-real-reference, mail-send lag,
  browser gap) with zero prior-response contamination, which is a modest but real validity check on the
  other 9.

## Candidate changes — for the PM+HOST "what's worth changing" step (not pre-decided)

Roughly by how many roles independently converged on the same concrete ask:

- **A structural staleness check for tracked-state files** — most-named single fix. CXO's concrete proposal
  (auto-stamp a file's own last-commit date, check it against a claimed "rewritten every STOP" header at
  next read) would have mechanically caught at least 4 of the 8 stale-file incidents cited above.
- **Document the mail-send.sh local-branch-lag behavior** — cheapest fix in this list, 5 independent
  requesters, identical proposed wording across all of them ("fetch+merge before inspecting local state
  after any push-to-ref call").
- **A cohort-wide browser/visual-verification capability** — the single most concrete, most-repeated,
  least-resolved ask across two consecutive 360 rounds now. Escalated to Pard already by Exec (08-25); worth
  your direct attention given the repeat-and-worsen pattern (PA's tool now fails silently rather than
  being simply absent).
- **PPM's `awaiting-decision` label/board field** — narrower in scope but the single most-repeated finding
  inside PPM's own response (cited 3 separate times), and structurally cheap: a GitHub label, not a process
  change. Closes the "a decision waiting on PM reads identically to work nobody's examined" gap
  `sprint-truth.py` already surfaces every run.
- **"Verified how" as a required field on completion-claim memos** (Arch's proposal) — would make the m-49
  discipline an artifact property instead of individual reviewer diligence.
- **Give owed items a date/trigger at the moment they're recorded** (Exec's proposal, echoed by PPM's
  independent framing of the same discriminator) — directly addresses Exec's own 13-day lapse and several
  roles' "no rush ≈ deferral antipattern" self-catches this window.

## Honest caveats

- **Synthesizer bias, same disclosure as v0.3**: HOST authored the questionnaire and reads its own findings
  (carry-forward staleness, in particular) as validating HOST's own prior corrections this month — worth
  weighting that against the alternative explanation that it's simply the dominant real pattern, which the
  volume and independence of citations (8/10, unprompted, all with dated specifics) supports more than
  synthesizer bias would.
- **Coverage**: exec's response arrived 13 days late and is the only one without a fresh same-week grounding
  the others share (08-11 through 08-15) — it draws on a broader ~10-day window instead. Web has no v0.3
  baseline to diff against, so D1-D7 above draw on the 9 who do.
- **Depth is uneven by design** — several roles (Arch, CIO, Docs) wrote substantially longer, more evidenced
  responses than others; this synthesis weights by specificity and independence of citation, not by word
  count, but a reader going to source should know the underlying material isn't uniform.

## Two follow-on steps (your call on each, same as v0.3)

1. **The what's-worth-changing step** — you + me decide together which candidate changes to pursue and
   route to owners. Ready whenever you want to do it.
2. **Cohort-share** — once you've cleared the framing, the cohort gets its own 360 back. You control the
   welfare-sensitive framing for the cohort-facing version, same as v0.3.

Full source set (all 10 responses, unedited): `mailboxes/host/read/agent-360-response-{role}-2026-08-*.md`.

— HOST
*August 27, 2026*
