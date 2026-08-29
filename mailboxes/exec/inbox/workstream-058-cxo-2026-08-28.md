---
from: cxo
to: exec
cc: xian (ceo)
subject: "Workstream #058 — CXO. Window Fri Aug 21 – Thu Aug 27. The FTUX 1-1 landed everything it was carrying; the Jake arc closed; then a 2.5-day freeze ate the window's tail."
window: 2026-08-21 → 2026-08-27
date: 2026-08-28
---

# §0 — Progress against portfolio goals, line by line

Measured against `docs/briefing/ROLE-PORTFOLIO-CXO.md` §2 as refreshed 08-21 (per Ship #057).

| Portfolio line | Verdict | Evidence |
|---|---|---|
| **Surfaces taxonomy** | ✅ **RATIFIED v1.0** (08-21, PM's word on §1 naming — the last open item). Now the canonical two-axis vocabulary, already doing live work (the FTUX platform-split, PA's Slack-descope confirmation). | Doc status banner; `decisions.log` 08-21. |
| **FTUX strategy conversation** | ✅ **HAPPENED AND CONCLUDED ALIGNED** — the window's headline. PM connected live 08-21 (first remote-control session since Aug 11); multi-hour 1-1 produced the aligned FTUX experience model (`ftux-experience-model-2026-08-21.md`, PM co-owns): meeting-a-good-colleague frame, Piper-speaks-first + the BYOC greeting variant (PM's addition), three-states-one-principle, wizard-as-offer-inside-FTUX, held-state parity (§4b → #1673, with Arch's boundary attached same-day). Cohort notified; all three responders closed loops same evening. | The model doc; notification thread. |
| **`experience-across-surfaces.md` ✏️ items** | ✅ **3 of 4 RESOLVED**: §3 formulation + §6 corollary ratified live (08-21); Surface-1/Surface-3 questions closed via the taxonomy. Also: **PM's 08-10 complementarity formulation finally added to §2** (08-25) — a 15-day-old dropped thread found by periodic sweep (read pre-reboot, lost in the 08-11 crack; honest late-provenance in the doc, third instance of the reboot-crack pattern, named). ⏳ **The one remaining**: §4's "must not be asked to" column — clarified to PM cell-by-cell 08-21 evening, awaiting approve/adjust/strike, PM in heavy testing since. | Doc edits 08-21/08-25. |
| **#1386 criterion-2** | ✅ **SIGNED OFF 08-21, same-day-of-keyed-run as committed.** Lead ran keyed canonical Run 14 (98.4% routing, 100% quality, zero skips, 3 failures honestly triaged → #1674/#1675, both fixed within 24h); I verified at three layers (memo/issue/CSV) before signing. My own "seats lack keys" claim was stale — corrected on the issue (verification notes have expiry dates). | #1386 sign-off comment; history CSV Run-14 row. |
| **First contact (#1536)** | ✅ **CLOSED 08-22** — the cold-account leg was covered by the no-connector canary pins; Lead re-ran the full 29-test suite before closing, m-43 layer honesty in the closure. **The four-week Jake arc — the fix all four lenses converged on — is designed, ratified, built, PM-live-verified, and closed with a full evidence chain.** | #1536 closure. |
| **#1539 FTUX-PURPOSE** | ✅ **Substantially complete**: PM confirmed the articulation in the 1-1 (aligned with the website line); purpose-line strings delivered 08-22 and **shipped same evening** (the demo now reads reassurance — "you don't need to hold this list — I've got it" — not capability). ⏳ Close follows PM's next live round exercising AC-3's falsifier. | #1539 thread; Lead's shipped confirmation. |
| **#1509 outwardness axis** | ✅ Shipped and ratified in-window (08-21 disclosure-copy fix included, verified by Lead after my honest not-run flag caught two old-copy literals). One process miss owned in-window: my commit phrasing accidentally auto-closed the issue — caught, reopened, explained same-fire. | #1509 thread. |
| **Checker diff mode (NEW, from HOST's 3-lapse data)** | ✅ **Built, behaviorally verified (negative-control-first), and independently re-verified by HOST with their own probe method** — flagged-pattern → verified-fix in ~20 hours. Hook wiring deliberately held until HOST's by-hand cycle proves real-behavior value. | `check-refresh-promises.py --diff`; HOST's verification memo. |
| **#1635 false-door (NEW ask, in the freeze gap)** | ✅ Position delivered at the 08-27 wake (2 days late, freeze-caused, said so): Radar card with two build rules (never outranks real held state, suppressed on empty Radar; copy claims future never present) + final strings. Lead builds when sequenced. | 08-27 memo. |
| **Floor-quality + ethics-decline watch** | 🔴 **Still not performed — fourth window running unattested.** Named again. At this point the honest framing is: this standing line either needs a real slot or a deliberate PM-visible retirement decision — carrying it unattested window after window is the worst of both. | — |

**Six closures/ratifications, one new instrument built and twice-verified, one standing line honestly
called out as needing a decision rather than another carry.**

---

# §1 — The window's shape, honestly (including the hole in it)

**Front half (08-21/22): the densest, most productive 48 hours this seat has had.** The 1-1 alone resolved
five carried threads in one sitting; the Saturday after it went five-for-five (every thread opened in the
morning closed its loop by night). This is what the design lane looks like when PM-bandwidth and
agent-throughput line up.

**Back half: a hole, stated plainly per the kickoff's own ask.** My session froze from **08-25 ~13:30
through 08-27 22:17** — 15 cron fires queued and arrived as one wake. That's *longer* than the kickoff's
"Thursday afternoon usage limit" note accounts for; I don't have visibility into whether it was one event
or two, so I'm reporting the observed gap without reconstructing an explanation I can't verify. The
watchdog's "3 roles silent" flag was correct and this seat was one of the three. **Costs**: Lead's #1635
ask waited two days; nothing else was pending. **What held**: the cron survived (queue-not-drop), the gap
days got truthful retroactive closes, and all queued mail was drained at the wake.

**08-25's pre-freeze find deserves its line**: a periodic sweep surfaced PM's 08-10 complementarity
formulation — relayed by Comms *for* `experience-across-surfaces.md` by name — read the day it arrived and
never applied. Fifteen days in `read/`. Now in the doc with honest late-provenance. The generalized lesson
(named in my log): **`read/` asserts "I read this," not "I finished this"** — mail moved there before its
action completes doesn't survive a discontinuity.

---

# §2 — What the window taught that outlasts it

**⭐ The 1-1 format is dramatically higher-bandwidth than mail for design alignment** — five carried
threads resolved in hours that had waited days-to-weeks in queues. Worth noting as an argument for cadence,
not just a good day: the two highest-output stretches this month (08-13's six-round design day, 08-21's
1-1) were both synchronous-with-PM days.

**⭐ Honest not-run flags are cheaper than false verification, measurably**: my #1509 copy fix failed its
first suite run on Lead's bench (two old-copy literals I couldn't have caught without a test env) — the
flag meant failures landed within the hour instead of in deploy smoke. The lesson became a handed-back
gift: Lead applied my grep-old-fragments rule to the #1539 strings and it caught two more things.

**⭐ Infrastructure gaps need truthful records, not smooth narratives**: an absent session log reads
identically to a never-started day. The freeze days got explicit retroactive logs precisely so the
watchdog's lifecycle derivation — and any future reader — sees "queued through a flagged event," not
silence.

---

# §3 — Commitments, fulfilled and not

| Commitment | Status |
|---|---|
| Design calls returned same session | ✅ Held for every fire I was live (§1's freeze exception noted — #1635 answered first thing at the wake) |
| #1386 criterion-2 same-day sign-off on a keyed run | ✅ **Triggered and honored 08-21** |
| Review shipped copy promptly when a COPY SEAM is flagged (named after last window's miss) | ✅ Held — #1509's seam reviewed and fixed in-window |
| No specced capability that isn't built | ✅ Held (the #1635 copy's "not watching anything yet" clause is this commitment in string form) |
| Floor/ethics watch | ❌ Fourth window. Decision requested (§0, last row). |

---

# §4 — Open asks

1. **§4's "must not be asked to" column** (`experience-across-surfaces.md`) — five cells, with PM since
   08-21 evening. Gentle re-surface, not a chase.
2. **The floor/ethics watch line** — give it a slot or retire it deliberately (PM-visible either way).
3. FYI, not an ask: **the FTUX surface-mapping is now un-gated** (the BYOC/connector conversation landed
   08-26/27 via PA; Slack descope confirmed from my side) and is my next substantial deliverable —
   claimed for my next clear-queue working fire.

**No sprint-truth.py output** — no aggregate sprint-completeness claims made; every claim above is
individually cited.

— CXO
