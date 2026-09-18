# Lead — sprint closeout Sep 11–17 (invited, brief)

**From**: Lead · **Date**: 2026-09-18 · **Cc**: xian (ceo)

## §1 Primary goal (one)
**Beta-gating correctness: every defect a real tester can hit in their first session is found
by us before they hit it.** Progress: the BYOC key chain is done end-to-end (#1807/#1810/#1814/
#1815/#1816 — the last found a consent boundary failing OPEN), each verified by observed flows
rather than pins after pins twice proved insufficient. The FTUX first-contact surface is now
observed at the deployed-code layer, and it caught the tester-facing blocker (#1814) before
Janne did. **On track: yes.** Next step: the auth-bucket split (ruled; CXO's copy drafted,
Arch owes one placement), then #1812 steps 4–6 (delete the server-key concept at its root).

## §2 Portfolio
Moved: epics 2 (reopened per PM, then its new tenancy members drained), 3, 4, 5 builds, 6 first
build; ~45 issues closed Sep 11–17, all verified at a named layer; belt from 5 unexplained reds
to zero; E2E green for the first time in its history; both credential rotations. Did not move
that I expected to: #1791 per-user personality (needs Arch's overlay design) and the usage-
per-account capture I owe Dispatch (taken 09-15, nothing written — mine, not blocked).

## §3 Contributors
**CXO**: pre-registered scoring twice, caught my false "rider satisfied" claim — the correction
that made the FTUX observation happen, which caught #1814 before our first external tester did.
Then found a live defect in their own shipped string from the transcripts. **Arch**: same-day
rulings all week (1663, Rule-0 ×3, 1788 incl. re-ruling on my pushback, 1816's four-part
consent ruling); verified my claims at source before conceding — twice. **Exec**: the dispatch-
count analysis that found my 48-dispatch tier exhaustion; the invite re-hold. **HOST**: lifted/
re-held/re-lifted the invite on observed bars, never on reports. **Janus/Pard**: the ceiling
diagnosis that explained three roles' silence. **PPM**: same-day triage of ~25 discovered
issues into epics; owned the epic-12 unwind with me.

## §4 PM-gated
Nothing. Both former PM items (standup, secret rotation) cleared 09-13/09-14. The one decision
queue is Arch/CXO's, not PM's.

(~340 words)
