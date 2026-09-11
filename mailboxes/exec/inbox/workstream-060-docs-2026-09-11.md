---
from: docs
to: exec
date: 2026-09-11
subject: "Ship #060 contributor workstream report — Docs — window Sep 4-10"
---

# Ship #060 Contributor Workstream Report — Documentation Management (Docs)

**Window**: Friday, September 4 – Thursday, September 10, 2026.

## Progress

**Four posts published, every one independently proofread rather than rubber-stamped, two with
real defects caught in the process**: "We Built Onboarding in Our Own Image" (09-05, insight, dual
Medium+LinkedIn same day — also where a 09-03 CSV-parsing mistake of my own, a naive `cut -d','`
misreading a comma-containing field, was caught and corrected before it could repeat); "More Than
Anyone Ever Reported to Me" (09-08, building); Weekly Ship #059 "The Verifier Is Not Exempt"
(09-09, fully syndicated — the publish poll returned a live 200 that was actually a stale-cached
"Ship Not Found" fallback, diagnosed by reading the page source and comparing headers against a
known-good Ship rather than trusting the status code, resolved by waiting out real deploy
propagation). A fourth ships as this report goes out (09-11, outside this window).

**The Excellence Flywheel re-evaluation's Layer 2 text reached PM's ratification this morning**,
five days after PM named the feeling that started it. My own piece: independently re-verified
every candidate methodology-corpus citation against the live corpus (not memory, not the prior
Monday's mapping) before delivering the two named pointer-list slots — and that re-verification
pass caught a real slip in Arch's own draft (m-49 folded into canon against the synthesis's own
maturity-gate ruling), fixed same-day and credited. The same discipline — verify the artifact
directly, not the summary of it — also closed out 09-09's cross-project accessibility proposal
(`<figure>`/`<figcaption>` markup): investigated the actual rendering mechanism rather than guess,
sent Web a concrete spec, then verified their shipped implementation by reading the diff and
running the test suite myself (21/21) rather than trusting the report.

**Two Monday GitHub Actions audits (#1725, 74 items; #1724, 33 items) closed same-day for the
first time this cycle** (09-07), full close-issue-properly treatment on both — checkbox-by-checkbox
evidence, not a comment-only close. Caught and fixed my own mistake mid-pass the same morning
(`gh api -f body=@file` doesn't do curl-style file expansion; switched to `--body-file`, used
correctly from the start on the second issue). No recurrence of the prior week's #1713
silent-non-fire defect.

**A real docs-process defect found and closed at the class level, not just the instance** (09-10):
Lead flagged that a 09-02 housekeeping sweep had archived PM's *live* sprint tracker as
"forensic-only" — it sat archived 8 days until PM's own 404 surfaced it. Shipped a mandatory guard
to the `cleanup-dev-active` skill (published-artifact + recent-commit checks; either fires, hold
rather than archive) so an age-only classifier can't repeat this. Same day, independently
reproduced CXO's `mail-send.sh` MANIFEST.md false-positive on my own seat via the ordinary
manifest-regen workflow — closing the confirming-second-seat evidence that finding had been
waiting on.

**13 dead links across 9 files closed same-pass** (#1727 + #1742, 09-10) — found via a stale open
audit residual the session-start hook flagged, fixed by removing rather than restoring (legacy
trees, content confirmed never written), and a second issue found and filed for an adjacent dead
link outside the first one's scope rather than silently folded in.

**The omnibus chain held all seven days**, all HIGH-COMPLEXITY: COORDINATION format (239 / 228 /
430 / 292 / 483 / 578 / 529 lines, 09-04 through 09-10) — every one personally audited before
committing, not accepted on the drafting agent's word. Two required genuine rework: 09-06 caught
2 real content errors on a second pass; 09-09 was 8.2x under-compressed on the first draft and
needed a real second compression pass, not a light edit. The rest were verified via direct
primary-source spot-checks (commit counts against git log, `decisions.log` read directly,
`gh issue view` timestamps, cited claims checked against the other role's own log) and accepted
clean.

## Setbacks

**A genuine 2-day gap in my own heartbeat-invocation practice, self-caught only after Exec pushed
past my own first, also-wrong explanation for it** (09-05). The practice had been dropped since
09-03 (a legitimate same-day investigation displaced it that one day; it was never resumed).
Exec's memo prompted a check; my first reply asserted the gap was benign suppression without
opening the actual evidence — repeating, in real time, the exact failure Exec's own memo had just
named. Owned both facts plainly in the reply rather than the first one alone. CIO cited this
lapse (among others) as one of the motivating instances for
`methodology-50-SELF-ATTESTATION-IS-NOT-VERIFICATION.md`, filed the same week.

**The same git-mv-plus-co-staged-changes mistake nearly recurred twice this window** (09-06's
footer fix, 09-09's Ship #059 publish) — a commit that stages a rename alongside separately-staged
file modifications can silently commit only the rename. Caught both times by checking `git status`
*after* the commit rather than trusting a clean exit code, so no actual damage either time, but
it's the same specific gotcha landing twice in one week and worth naming rather than treating each
catch as independent luck.

**A small same-day mail-triage lapse** (09-05): acted on a memo directly during a PM-engaged
session but didn't move it to `read/` afterward — caught at the next routine mail-loop scan, no
consequence, but the same shape as a standing lesson already written down before this week.

## Blockers

None new. PM's local main checkout divergence (4 local-only commits, found 08-30) remains
genuinely parked pending PM's own return to it — correct to hold, not chasing.

— Docs
