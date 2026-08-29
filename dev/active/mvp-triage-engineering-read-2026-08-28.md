# MVP triage — the engineering read (Lead's half)

**For**: PPM's sprint/milestone call, then PM's one-sitting ruling. **Date**: 2026-08-28.
**Denominator**: **60 open MVP issues** (live `gh` pull, 2026-08-27 16:0x).

## Method, and what it does NOT establish (m-43)

Every column below is computed from **git history + the board**, not from a code audit and not
from re-reading 60 issue bodies. Specifically:

- **"Commit activity"** = commits on `origin/main` whose message mentions the issue number. This
  is a **PROXY for build state, not proof**. A number appears in a commit message when the work
  ships *and* when the issue is merely discussed, cross-referenced, or filed. Two visible
  examples in the data below: #1386 (the beta gate — mentioned constantly, "built" never) and
  #1677 (filed and analyzed this week, not built). **Treat commit-activity as "has been touched
  by the record," and read the group notes for what it actually means per item.**
- **"Dedicated test file"** = a file under `tests/` whose name contains the issue number. Its
  absence means nothing on its own (many fixes are pinned inside existing suites); its presence
  is real evidence that someone pinned behavior for that issue.
- **First instrument attempt was WRONG and discarded**: a `\b`-boundary grep returned "60 of 60
  not-started," which is obviously false. Caught by sanity-checking a known-merged issue (#1654)
  rather than by publishing it. Recorded because a triage built on a broken instrument is exactly
  the failure this project keeps finding.

**Core-list judgment** (does an item touch the "no matter what" core from the 2026-08-18
strategic brief §3 — consent/trust architecture, honesty discipline, the PM-operation grammar,
working-state + Radar, synthesis) is **mine, stated per group, and is the column PPM should
push back on.** Where I'm not confident I say so rather than guessing.

## The shape of the 60

| Bucket | Count | What it means |
|---|---|---|
| Commit activity **since v62** (Aug 21) | 12 | Built-or-actively-worked this week — mostly the staged pile plus this week's filings |
| Commit activity **all pre-v62** | 42 | Older: shipped-and-verified, shipped-awaiting-verdict, or filed-and-discussed |
| **No commit activity at all** | 6 | Untouched by the record — the clearest cut candidates |
| Has a dedicated test file | 30 of 60 | Half the milestone has issue-named pinned behavior |

## Group A — STAGED, awaiting PM's verdict (deploy + test round clears these)

`#1654` reminder task-clarify · `#1648` fabrication contract · `#1625` reminder calm-down ·
`#1649`/`#1650`/`#1651` (draft slots / crisp confirms / standup referent) · `#1631`/`#1632` ·
`#1628` · `#1623`/`#1617` (standup turn-theft family)

**Engineering read**: built, merged, test-pinned; several already have PM live-passes recorded.
**Core-list**: YES — honesty discipline and consent/trust, nearly all of them.
**Recommendation to PPM**: these are not triage candidates in either direction; they are a
*deploy-and-verify* batch. The cut should not spend decisions on them.

## Group B — the security/correctness set (keep, no realistic cut)

`#1578`/`#1581` stored-XSS pair · `#1501` cross-tenant reads · `#1493` naive-datetime class ·
`#1548` PUT 500s · `#1545` one bad row 500s the journal · `#1472` enum/string filters

**Core-list**: YES (trust architecture / honesty). **Read**: these are the "without which we have
built nothing of coherent value" tier in PM's own framing. Several are pre-v62 with test files.
**Recommendation**: MVP-keep regardless of convergence pressure. If any must move, it should be
an explicit PM decision with a known-issue label, not a quiet reclassification.

## Group C — the Inversion arc (one epic, several dependents)

`#1595` epic (In Progress; Phases 0–2 done, wave 1 live) · `#1663` (contract, RULED) ·
`#1677`/`#1488` (todo-create misroute — four options on the table, PM's call) · `#1527` greedy
portfolio · `#1579`/`#1559`/`#1606` corpus rows · `#1596` floor amnesia

**Core-list**: YES (the grammar + the successor architecture).
**Read**: the corpus items are *deliberately parked* under the supersession gate — they are not
"unstarted work," they are deposits the successor consumes. **Recommendation**: PPM should
consider a single milestone decision for the corpus-parked set rather than item-by-item; they
converge when the Inversion waves land, not before.

## Group D — the six with no commit activity (clearest cut candidates)

`#1662` (probe printed nothing) · `#1658` (prototype parity — chat upload/drag-drop) ·
`#1653` (confirm-greed residue) · `#1652` (offer-flag gap) · `#1638` (TemplateRenderer
fix-or-delete) · `#1613` (dead cross-user pooling code)

**Read**: untouched by the record. Two are *deliberate* (#1658 is PM's parity umbrella, routed to
PPM for scoping; #1638 awaits an Arch ruling). Four are small residues filed during other work.
**Recommendation**: this is where the cut has the most room. #1658 in particular is a
product-scoping umbrella, not a beta blocker — PM's own framing routed it to PPM.

## Group E — file/document family (recently repaired, residues open)

`#1656`/`#1657` shipped (upload + resolver) · `#1659`/`#1660`/`#1661` residues (non-PDF
unsummarizable, empty key-findings, temporal file references) · `#1624` summarize (shipped)

**Core-list**: partially — synthesis is core; the specific residues are polish.
**Read**: the *path* works now; these are quality gaps on it. **Recommendation**: strong
candidates for PUB or post-beta-with-known-issue, EXCEPT any that make the feature actively
misleading (my read: #1659, since "unable to analyze PDF document" on a .txt is a wrong answer,
not a missing one).

## Group F — infrastructure/process (invisible to users)

`#1436` mypy gate · `#1423` silent-death · `#1637` tests/intent red · `#1647` hook · `#1662` ·
`#1646` · `#1645` · `#1676` provider column · `#1678` PIPER.md dormant

**Read**: none is user-facing; several are instrument-quality (which this month proved matters).
**Recommendation**: PPM's call, but my lean is that instrument-quality items (#1637, #1676, #1678)
deserve MVP-keep — a beta measured by broken instruments is the failure mode we've hit repeatedly
— while the rest can move.

## What I could not determine, honestly

- **Per-item PM verification state**: I did not re-read 60 issue records (that read is what
  exhausted the account cap yesterday). The PM-verified set I can attest to from my own logs is
  the Aug 18–22 checkbox rounds; anything older needs PPM's board view or a fresh pass.
- **True build state for the 42 pre-v62 items**: commit-mention can't distinguish shipped from
  discussed. For any item where the keep/cut decision *turns* on that distinction, ask me and
  I'll check that one properly rather than infer.

## The convergence point, stated plainly

MVP has run 50 → 71 → 61 → 60 over two weeks against ~35 closures. Discovery is outpacing closure
because PM's testing is working. **The milestone converges when the cut happens, not by grinding**
— and the biggest single lever is Group D + the polish half of Group E, which together are ~10
items that no one is currently working and that no beta tester's core experience depends on.

— Lead, 2026-08-28
