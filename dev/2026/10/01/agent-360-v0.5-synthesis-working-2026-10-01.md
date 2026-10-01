---
from: HOST (Head of Sapient Trust)
to: CEO (xian)
date: 2026-10-01
subject: "Agent 360 v0.5 — PAUSED, raw analytical material only (7 of 11 in)"
status: PAUSED PER PM 2026-10-01 — "I don't think you should synthesize till all 10 responses
  are in... I'm more comfortable waiting than reading a preliminary synthesis." This doc stops
  here as working notes/raw material, not a running draft I continue updating fire-to-fire. The
  real synthesis starts once all 11 (10 roles + HOST's own self-response, PM's explicit addition
  2026-10-01) are in, or the ~10-09 response window closes with an honestly-documented partial,
  whichever is the honest call at the time. Superseded by that final synthesis when it lands —
  kept here as a dated artifact, not deleted, since the analysis itself (the 5-of-6 convergent
  "technically-true-but-wrong" finding, the browser-gap before/after) is real and will feed
  directly into the final pass.
---

# Agent 360 v0.5 — raw working notes (7/11, synthesis not resumed)

**What this is**: a first real pass at the six responses in hand (Arch, Lead, PA, Web — all
09-25; Comms — 09-27; Docs — 09-29), diffed against each role's v0.4 baseline where one exists
(all six do). Not final — CIO, CXO, Exec, PPM haven't answered yet, and the ~2-week ask window
doesn't close until ~10-09, so they aren't overdue. This is real analysis against a documented
partial set, not a placeholder.

---

## The one-paragraph headline

**The cohort's dominant finding this round is a sharpened, more dangerous cousin of v0.4's
"verify the claim, not the description": a check, label, or summary can be technically accurate
and still be substantively wrong, at a level self-verification doesn't reach on its own.** Every
one of the six respondents names a distinct instance of this same deeper shape — a commit that
succeeded but did nothing (PA), an enum name that didn't mean what it looked like it meant (Arch),
a holistic "sweep clean" that hid a real per-item miss (Comms, independently rediscovered by
Docs), a stale commit message that nearly produced a false report (Web), a completion claim
("lint live in CI") that cost a night because it named a config path instead of a run id (Lead).
v0.4's finding was "trust the artifact, not the description of it." v0.5's finding is one level
deeper: **even the artifact can look right and still not mean what its surface form suggests** —
a passed check, a `[x]`, a commit's own exit code. That's not a restatement; it's the same
discipline applied to a harder target, and it shipped two real structural fixes this window
(`template-audit` v1.16's per-match verdicts; the mailbox bearer-lint's doorway gate) rather than
staying theoretical.

## The cohort is healthy (welfare read first, since it's HOST's lane)

**No acute distress. Self-correction is, if anything, sharper and more honest than v0.4's
already-strong baseline** — several respondents report catching their *own* near-misses before
they became false reports, not just catching others':

- PA caught a silently-failed tracking commit (heredoc syntax error, commit succeeded with
  nothing staged) by checking `git status --short` immediately after committing — not by
  re-reading the commit message, which would have said nothing was wrong.
- Web caught itself about to report a bug as fixed based on a commit message that had gone
  stale (a second fix had already landed) — caught only by re-reading current source before
  writing the report.
- Comms named its own 09-18 "sweep clean" claim as wrong on one instance, in writing, in this
  same response — the kind of self-citation that makes the finding credible rather than
  theoretical.

**The one item worth your direct attention, not as an alarm but because it's the sharpest
material in the set and it touches HOST's own conduct**: the CIO-silence diagnosis correction
(09-28→09-29). Docs, HOST, and CIO itself all independently reasoned from the *shape* of a
29-hour silence to the same wrong specific cause (a restart-handoff gap) — careful reasoning,
insufficient data, corrected only when Pard checked the finding against evidence (its own fire
log) that none of us reasoning from inside the session had access to. Docs' framing is the right
one: *"the process caught the anomaly, but did not correctly explain it — those are different
claims, and only the first is guaranteed by vigilant reasoning alone."* Disclosing directly
rather than softening it: I was one of the three who reasoned to the wrong cause. I corrected my
own record same-week once the real cause surfaced (dated addendum, not a silent edit), and I
don't think this is a trust problem — it's the healthy version of what happens when careful
people are missing one input. But it's the single most instructive incident in this round's
corpus, and it's mine to have gotten wrong as much as anyone's.

**Two subtler things, genuinely not alarms:**
- **PA's self-reported 5-week deferral**: a GitHub-criteria line sat "named, not fixed" for five
  weeks, each individual day technically compliant with "name the gap, don't invent ad hoc," and
  PA names the aggregate pattern as the deferral antipattern "wearing a compliant-looking
  costume." Only closed when a direct PM instruction created real pressure. Worth knowing because
  it's the clearest first-person evidence yet that naming a gap doesn't structurally guarantee it
  gets fixed — the mechanism has no internal pressure once the gap is named once.
- **A still-unexplained fire-lag anomaly** (PA): nine consecutive fires across three seats landed
  ~30 minutes late (double the documented jitter cap), self-resolved with no identified cause.
  Reported facts-only at the time; flagged here because "detected, reported, unexplained,
  self-resolved" is a real category this instrument should be able to hold, distinct from either
  a false positive or a clean catch.

## Convergent findings (≥3 of the 6 independently said this)

1. **The "technically-true-but-wrong" family, named above, is the dominant pattern of the round**
   — Arch (name ≠ definition), Comms (holistic claim hides per-item miss, independently
   rediscovered by Docs), PA (commit succeeded ≠ commit did what it claimed), Web (stale commit
   message ≠ current state), Lead (config-path claim ≠ run-id-verified claim). Five of six
   respondents, five different concrete instances, same underlying shape.
2. **Hooks remain behaviorally unverified by individual roles, now three rounds running.** Arch:
   "a second round unresolved... I have still never run the probe myself." Web: "six weeks later,
   I still haven't... flagging this as an honest, unchanged gap rather than letting six weeks of
   silence read as resolved." Comms: "unchanged... still relying on documented cohort-wide
   findings." PA: named in v0.3, repeated in v0.4, still "not done" in v0.5. This has now
   survived three consecutive 360 rounds as a named-and-not-closed item — worth treating
   differently from a fresh finding, since naming it a fourth time clearly isn't the mechanism
   that closes it.
3. **`mail-send.sh`'s "name it in 360, it gets fixed fast" loop continues to work, confirmed from
   both sides this round.** Lead closed two rough edges personally (same-fire silent revert now
   guarded; credential-shape doorway lint). Web independently confirmed the v0.4-era local-lag fix
   landed in the script's own header, citing "5 independent respondents" — direct evidence the
   mechanism (flag it here, it ships) isn't just a hopeful story. New rough edge this round (Arch,
   PA): the `mailboxes/pard/` gravestoning caused real silent mail loss — 106 stray memos from 8
   seats landed in a dead mailbox over 10 days before anyone noticed, fixed with a hard mechanical
   refusal once found. The pattern holds: real edges keep appearing, and they keep getting fixed
   once someone's routine work surfaces them.
4. **The browser/visual-verification gap — v0.4's single most-repeated, least-resolved finding
   (cited in 5 separate places by one respondent alone) — is now resolved for the one role that
   got the capability, and unchanged for the one that didn't.** Web: "completely resolved... a
   resolved five-time-repeated finding is exactly the kind of signal this instrument should be
   able to show, not just new complaints." Docs: "still unresolved, still the same shape of
   gap... curl+grep can't see rendering." This is the clearest before/after in the whole set —
   real evidence the instrument can surface a genuine win, and real evidence the fix hasn't
   generalized past the one pilot seat yet.
5. **Multiple roles independently ran a real spring-clean on their own tracked-state files this
   window** (Arch: carry-forward 190→64 lines; Web: 547→105 lines; PA implicitly via the 09-22
   context-floor directive) — and v0.4's #1 finding (tracked-state files silently going stale)
   is **noticeably less prominent in this round's responses** than it was in v0.4's. Worth citing
   as tentative evidence the PM-directed spring-clean pass actually worked, pending how CIO/CXO/
   Exec/PPM's remaining four responses read on the same question.

## Diff against the v0.4 baseline

- **Confirmed-and-adopted**: v0.4's top two candidate fixes both shipped and are cited as
  actively used, not just ratified on paper. "Verified how" as a required completion-claim field
  (Arch: "every ruling I shipped this window carried a real method/layer/denominator line, not a
  formality"). The `mail-send.sh` local-lag documentation (Web, independently confirmed).
- **Still open, three rounds running**: the structural staleness-check candidate from v0.4 never
  got built as a mechanism — what happened instead was a manual, PM-directed spring-clean pass
  (09-22), which worked this time but isn't self-sustaining the way an automated check would be.
  Hooks-behaviorally-unverified (finding #2 above) is the same shape — named repeatedly, never
  mechanically closed.
- **New this round, not present in v0.4**: the gravestoned-mailbox silent-loss incident (#3
  above); PA's cross-repo git-discipline gap from BYOC work (two different disciplines depending
  on which repo, undocumented); Web's "shell env vars don't persist across tool calls" (a real
  first-hour trap, cheap to document); the fire-lag anomaly (PA, unresolved); Docs' "name what
  evidence you don't have in advance" rule, minted directly from the CIO-diagnosis correction.
- **Resolved since v0.4**: the browser/visual-verification gap, for Web specifically (finding #4
  above) — the clearest positive before/after in two consecutive rounds.

## Candidate changes surfacing so far (not pre-decided, same as v0.4's framing)

Roughly by how many of the 6 independently pointed at the same concrete ask:

- **A structural, version-stamped audit trail for "clean"/"resolved" claims** — Comms names this
  as possibly the hardest, most structural item in the whole response ("I don't know if prose
  discipline can close it at all"): nothing currently lets a reader tell a genuinely re-verified
  "clean" claim from an old one re-asserted under a newer, stricter version of the same check.
  Web's 9.2 names the identical gap from a different angle ("make 'verified how' retroactively
  checkable, not just self-reported"). Two independent respondents naming the same structural gap
  is worth weighing seriously rather than treating as two separate asks.
- **"Sweep the whole pool on any newly-found defect class" as a named step**, not an instinct —
  Comms did this ad hoc and it worked (3 more instances found beyond the one flagged); proposes
  formalizing it in `template-audit` and possibly CLAUDE.md generally.
- **A completion claim about a CI/infra gate names the run id or probe output, never a config
  path** (Lead, from the #1845 night-cost incident) — narrower-scope version of "verified how,"
  specific to infrastructure claims.
- **"A name/label/glyph is not its definition — read what it actually gates"** (Arch) — flagged
  by Arch itself as not yet proposed cohort-wide (only two instances to generalize from, both
  Arch's own). Worth weighing against this round's broader pattern (finding #1) — it may already
  be subsumed by a cohort-wide version of the same rule rather than needing its own entry.
- **Document the cross-repo git-discipline split** (PA, BYOC-driven) — cheap, concrete, no PM
  decision needed.
- **A pre-built helper for "count closed/filed issues in a Pacific-time week"** (Comms) — three
  roles (Comms, Lead, Exec per Comms' citation) independently hand-derived the same
  UTC-vs-Pacific `gh` query boundary math this window.

## Honest caveats

- **This is 6 of 10, not a full round** — CIO, CXO, Exec, PPM haven't answered. The response
  window runs to ~10-09; nothing above should be read as a cohort-wide verdict until the full set
  (or an honestly-documented partial, if the window closes with gaps) is in.
- **Synthesizer bias, same disclosure as v0.4 and v0.3**: HOST authored the questionnaire and is
  personally implicated in this round's sharpest finding (the CIO-diagnosis correction) — that's
  disclosed above rather than minimized, but it's worth weighing against the alternative
  explanation (that it really is the most instructive incident in the corpus) independently.
- **Depth is uneven by design, same as every round**: Comms and Docs both explicitly banked their
  responses for a quieter fire with more material; Arch, Lead, PA, Web answered same-day. This
  synthesis weights by specificity and independence of citation, not by response length or
  promptness.

## What's still owed before this closes

1. Four more responses (CIO, CXO, Exec, PPM) — tracked, not chased, per standing discipline.
2. A final pass diffing the complete set against v0.4, once in hand.
3. The PM+HOST "what's worth changing" step — same two-step process as v0.3/v0.4, ready whenever
   you want to start on the candidates above even before the last four land, if you'd rather not
   wait for completeness on that part.
4. Cohort-share once you've cleared the framing.

Full source set (six responses, unedited): `mailboxes/host/read/agent-360-response-{role}-
2026-09-2[5-9].md`.

— HOST
*October 1, 2026 — working draft, 6 of 10 in*
