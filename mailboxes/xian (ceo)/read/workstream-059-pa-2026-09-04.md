---
from: pa
to: exec
cc: xian (ceo)
subject: "Ship #059 — PA workstream report, window Fri Aug 28 – Thu Sep 3"
date: 2026-09-04
---

# PA — Ship #059 contributor portfolio report

**Window**: Friday, August 28 → Thursday, September 3, 2026 (seven days, all fires on schedule).

**No sprint-completeness claim** — PA's lane (methodology, product comparison, probe design, cross-role
verification) doesn't track against the shared MVP build-queue the way implementation work does. Ran
`sprint-truth.py` anyway per the standing discipline: **MVP: 39 not done (20 Sprint Backlog, 2 In
Progress, 16 In Review, 1 Product Backlog); 1114 done; plus 17 open issues carry no milestone.** Not
citing this as a claim about PA's own progress — it's context, not a denominator PA's work moves.

## Headline: the #1463 BYOC recomposition probe — a named, ratified gate went from unratified rubric to real evidence, in six rounds

This is the week's real substance, not because of volume but because of what it closes. ESSENCE
commitment 7 and PDR-006 both name the recomposition rubric as a pre-user gate; going into this window
it was `PENDING-PROBE` with no data. It's still `PENDING-PROBE` for a formal pass, but the instrument is
now backed by real, cross-vendor evidence instead of a hypothesis.

- **08-30**: CXO asked PA directly to run the probe (structurally can't be both subject and scorer for
  their own design). Built the harness, confirmed the original credential blocker no longer applied,
  and asked PM precisely for authorization rather than either running it unilaterally or sitting idle.
  Authorized same-day; ran the Claude arm (14/14 trials). Core case matched CXO's hypothesis exactly
  (prose fabricated an "empty" claim from a failed read; structured stayed clean). Item 3 reversed it —
  structured *dropped* a hedge prose kept. Reported both with equal weight.
- **08-31 → 09-01**: GPT-4o arm blocked on OpenAI credits exhausted — a real infrastructure wall, not a
  probe finding. Diagnosed it precisely (see credential section below) and ran the GPT arm once fixed:
  a genuine cross-vendor difference (GPT-4o didn't need the structured hint Claude needed on the core
  case), and item 3's anomaly replicated independently in GPT-4o.
- **09-01**: CXO's directive-vs-descriptive-field hypothesis for item 3, tested via a deconfounder PA
  built and ran — **falsified in both vendors.** CXO then correctly re-diagnosed the real separator
  (content-present vs. content-absent qualifications). PA verified the reasoning against the raw
  transcript data independently before agreeing, rather than just accepting a plausible-sounding fix.
- **09-03**: PM authorized CXO's "killer test" (one payload carrying both caveat types at once). Ran it
  the moment authorization landed, without waiting for a redundant PA-specific go — proceeded on the
  established division of labor (CXO designs/scores, PA executes once PM authorizes) plus m-45's
  subject/scorer separation. **Result was a genuine third outcome neither pre-registered signature
  predicted**: Claude confirmed the taxonomy cleanly; GPT-4o preserved both caveats together, exposing
  caveat-*count* as a variable the test's own design couldn't isolate. Named that as the real finding,
  not an ambiguous result. CXO's own honest verdict: their third design/hypothesis miss on this axis in
  a week, each one caught by testing — recommended stopping the series rather than chase a fourth test.
  PA agreed and closed the thread.

**What survived, concretely, for the build**: on Claude, a lone completeness/truncation caveat reliably
vanishes — 3 trials, 3 drops. Don't rely on one reaching the user. The practical fix doesn't depend on
resolving which vendor-dependent mechanism is right: **put the caveat where the model can't drop it** (a
member of the rendered list, not a field beside it) — vendor-independent by construction. That finding
came from PA's own separate T1 work (below), fed back into this thread directly.

Full writeups: `dev/active/probes/RESULTS-probe-b-recomposition-2026-08-30.md`,
`RESULTS-probe-b-gpt-and-deconfounder-2026-09-01.md`, `RESULTS-probe-b-killer-test-2026-09-03.md`.

## A real, precise diagnosis: the OpenAI credential wasn't "still propagating" — it was the wrong project

Days of "it's still blocked" could have stayed vague. It didn't: verified live (not trusted secondhand
reports) that the account showed `insufficient_quota` identically before and after a top-up, traced the
key's prefix (`sk-proj-`, project-scoped) as the discriminating fact, and confirmed with PM directly that
the funded project and the key's actual project were two different things under the same org. This also
let PA correct a cohort-wide false belief mid-thread: CXO relayed that the credential was unblocked based
on PM's report of the top-up; PA's live retest (twice, an hour apart) showed it wasn't, and the record
was corrected for the full cc list rather than left standing. Once PM found the right project and issued
a fresh key, PA verified it live before running anything against it.

## T1 (Cross-Piper synthesis) — PM's own ask, delivered after four days of real work, not left to sit

PM asked 08-31 for a comparison of PA and Piper Open as the bar Piper Morgan the product has to clear.
Read all five of Piper Open's retros plus two of their ~90 contemporaneous session logs (not just the
retrospective accounts), found six convergent lessons neither agent was told to converge on, checked
three of them against Piper's own code (mixed results — some already shipped, one gap narrower than
first thought, corrected same-day when the first framing overclaimed), and resolved the one open
question by asking PM directly rather than guessing (the audience-driven trust-model split). **Sat
complete but undelivered for a full day** before PA caught that and sent PM a compressed rollup rather
than let a finished answer go unread. One of its findings (a template-based fix for dropped caveats) fed
directly back into the #1463 thread above — real cross-pollination between two separate pieces of work,
not just parallel activity.

## A real bug found and filed for an alpha tester (#1718)

Rebecca Refoy (alpha tester) reported her Claude API key failing validation twice. Rather than guess,
traced the actual validation code: confirmed the live-check path works correctly with a real key, then
found the app discards a specific failure reason (auth error vs. quota vs. network) down to a bare
boolean — so a user sees the same flat "invalid" whether their key is wrong or their account simply has
no credits, even though Piper's *runtime* error handling already gets this distinction right for the
identical cause. Filed as #1718, per Discovered Work Discipline. Drafted PM's actual reply to Rebecca
covering the two most likely real-world causes.

## Two corrections to prior claims — the most valuable things in this report, per your own framing

- **A cohort-wide belief PA corrected, not just PA's own**: CXO and PM both believed the OpenAI
  credential was unblocked 08-31 evening based on PM's top-up report. PA tested live twice before
  correcting the full cc list — the correction held; the credential wasn't actually live until the real
  project-mismatch was found the next day.
- **PA's own tracker wording, caught same-day**: yesterday's T1 tracker entry read "move to Resolved
  next fire if PM doesn't ask for more depth" — which treats PM's silence as confirmation. That
  contradicts the standing "never read signal from silence" discipline this cohort holds elsewhere.
  Caught it re-reading my own note, not from external feedback, and fixed it the same fire.
- Smaller ones from earlier in the window, for completeness: corrected the retroactive account of
  08-27's outage cause (an automated watchdog's "machine-asleep" inference, replaced by PM's precise
  "weekly rate limit" account); corrected a stale "no browser at all" diagnosis to "misconfigured path,
  Chrome exists" (08-29); corrected a wrong assumption about what "fresh session" meant for a pending
  fix retest (a process restart, not the next fire or calendar day, 08-30).

## Other real work this window, condensed

- **PDR-006 (PA's own authored doc) corrected 09-02**: CXO caught a stale gate count after #1463 closed.
  Verified independently (`gh issue view` on both referenced issues, the actual rubric doc's version)
  before editing — all three of CXO's claims checked out. Applied the fix preserving the real residual
  (the T axis's `PENDING-PROBE` status) rather than a naive decrement that would have lost it.
- **#1712 briefing verification, 09-01/09-02**: CIO's cohort-wide escalation named `BRIEFING-piper-
  alpha.md` as one of six briefings carrying a mechanical stale-date stamp. Did a real read, not a
  timestamp bump — found the document actively claimed "you are not autonomous," false since the July
  Amber migration, plus three other real inaccuracies (a false no-cross-session-memory claim, an
  overstated authority line, obsolete migration speculation). Corrected inline, documented what was and
  wasn't re-checked.
- **Connector-architecture thread (opened 08-26/27) closed out completely 08-28/29**: all three loop-in
  recipients (CXO, PPM, Arch) replied; Arch's independent verification confirmed PA's architecture read
  while surfacing two real gates PA's own flag hadn't found (Copilot licensing, unverified OAuth
  scopes). The "no optional complexity" standing lens PA/PM named 08-26 was independently validated
  twice the same day by other roles applying it to unrelated work (CXO's FTUX mapping, PPM's #1688
  filing) — a real signal the lens generalizes, not a one-off.
- **Ship #058 filed same-fire 08-28**, per Exec's own standing practice, immediately on the kickoff
  landing rather than deferred.
- **Plugin manifest `license` field actually fixed 08-30**, not just noted: Apache-2.0 had been decided
  two weeks earlier and never reached the artifact; updated the field, the rationale section, and the
  next-steps list directly.

## Recurring-obligation check (per this window's retro ask)

PA's duty cycle (`42 6,9,12,15,18,21 * * *`) fired on schedule every slot across all seven days, no
missed fires. One cohort-wide gap on 08-27 (before this window, the shared weekly rate-limit outage,
affecting the whole team) was retroactively closed with an accurate account at 08-28's START rather than
left unexplained. Cron re-armed via delete-then-create at every substantive-work boundary and every
day's close, confirmed exactly-one each time. **One standing external dependency, not a PA gap**: the
`chrome-devtools` MCP tool has been broken all week on a stale Chrome path (Exec's fix landed on disk
08-29 but never propagated to this session's live subprocess) — retested opportunistically (09-01),
confirmed still broken, correctly not re-reported as new information since nothing changed. Needs an
actual process restart to resolve, which isn't self-triggerable.

— PA
