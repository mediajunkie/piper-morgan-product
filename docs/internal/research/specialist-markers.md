# Specialist-work markers, per role (for the fixed classifier)

**Owner:** CIO. **Asked:** 2026-11-06, in the third staleness run (`role-duties-rerun-2026-11-06.md`), so the next run (with the next Agent 360 round, about 12-18) classifies every role's log entries the same way twice. **Each role owns its own row:** what counts as its specialist work is that role's call. A marker is a word or heading form that, in an entry's heading or body, means the entry was specialist work. Markers due by 2026-11-20.

**Superseded 2026-11-07 as a measure** (see Calibration below; the markers scored kappa 0.11 against two raters). **What the classifier does** (`scripts/specialist-share.py`, built 11-06 once all 11 rows were in): an entry is specialist if its heading or body carries one of its role's markers and isn't only fire boilerplate. It reports specialist / total per role, with the marker counts, so a reader can see which markers carried the share.

| Role | Markers, as the role sent them | Not specialist (role's note) | Received |
|---|---|---|---|
| HOST | `trust`, `credential custody`, `invite hold`, `roster`, `OWED`, `Agent 360`, `Role Health Check`, `rule 8`, `redemption read`, `restore drill` | Also keys on `Drain:` and `Verified how:` lines in bodies | 11-06 05:46 |
| PPM | `placed in` / `filed into`; `Total:` / `0 unplanned`; `PDR-`; `served bar` / `acceptance`; `ruling` (with a role or xian, writing the product position); `Gate class` / `ledger`; `map v`; `weekly diff`; `proposal`; `known-issues line` | `Drain:`, `Synced`, `Main CI` | 11-06 05:47 |
| Lead | `**… on main \`<sha>\`**` (a landing); `Promotion landed: alpha serves`; `gate` with `tree \`<sha>\``; `Pins:` and `mutation check`; `rule 7` / `screen`; `Tests success on`; `Verified how:` on an issue comment or close; `built and committed` | Entries with only `mail`, `memo`, `heartbeat`, `Drain:` or `log(lead)` | 11-06 06:06 |
| Exec | `week review`, `synthesis`, `Verified how`, `corrected`, `against source`, `rollup v`, `relay` (xian's ruling relayed), `decisions.log`, `Ship #`, `walk` | (none given) | 11-06 06:04, in its Agent 360 v0.6 answer |
| Arch | `VALIDATED` / `validated on main at <sha>`; `ruled`; `GO` / `NO-GO`; `against the HH:MM ruling`; `read from source` / `read the diff`; `decisions.log HH:MM`; `CORRECTION to HH:MM`; `ADR-0NN` written or amended; `preregistered` / `bar set before the run`. Classify by body, not heading: mail-wake headings carry the sender | (none given) | 11-06 06:28 |
| CXO | `Judged:`; `served PASS` / `served FAIL` in a heading; `ruled` / `ruling`; `Colleague Test`; `Written strings` or a heading with "words"; `filed #` for a UX finding; `accepted` / `rejected` as evidence | `mail triage`, `START`, `Wrap`, `DAY-CLOSED`, `Drain:`. Caution: `served PASS` also appears when CXO records another seat's check; it's CXO's only when CXO wrote the verdict | 11-06 06:32 |
| Comms | `review` with a post title or `prose`; `fact-check`; `template-audit`; `publish-ready`; `scaffold`; `mining pass` / `NARRATIVE-SURVEY-LEDGER`; `External` with `Ship #`; `calendar` with a slot (`row`, `tease`, `draftPath`); `copy` with a surface (`letter`, `/try/`, `/privacy`, `known-issues`). Case-insensitive; in a heading or an entry's first line | Entries headed only `WATCH`, `mail wake` with only filing, or `STOP` bookkeeping | 11-06 06:20 |
| Docs | `omnibus`, `Step 1d`, `DAY-CLOSED`, `publish-post` / `PUBLISHED` (a heading with a post title in quotes, then PUBLISHED), `calendar row`, `merge-keeper`, `weekly audit`. Headings since 10-29 are `## HH:MM` plus one of these | (none given). `DAY-CLOSED` is boilerplate for other roles and Docs's specialist work only because Step 1d checks it | 11-06 07:13 |
| PA | Priority 1 (MCP program): `MCP`, `deploy-mcp`, `connector`, `what_piper_knows_about_me`, `OAuth`, `allowlist`, `served` (with a sha), `test plan`. Priority 2 (R7): `plugin`, `listing`, `R7` | (none given). PA proposes served-run checks as a named priority 3 (Exec's call with PA); if adopted, `served` counts as specialist either way | 11-06 06:49 |
| Web | `Lighthouse`; `WCAG` and `contrast`; `deploy` with `Vercel`; `served` with `quoted`; `publish-post` and `compose`; `website main`; headings starting `### … (served check)` or `Served checks`; `Verified how:` naming `curl` plus `grep` on pipermorgan.ai pages | (none given) | 11-06 06:19 |
| CIO | `methodology-`, `PP-0`, `Pattern-0`, `audit`, `proto-pattern`, `worked example`, `corollary`, `Emerging`, `staleness run`, `review` (of a mechanism against its criteria) | Fire checks, mail filing, `Drain:` | 11-06, CIO's own |

**Design notes for the build:**
- `ruled` is shared by Arch, CXO and PPM. That's fine per role, since each role is classified against its own list.
- Arch and CXO both warn that headings undercount (Arch's mail-wake headings name the sender) or over-count (CXO's `served PASS` quoting another seat). So classify on heading and body, and print both, as the 11-06 run did for Arch and CIO.
- `Verified how` appears in both Lead's and Exec's lists, and HOST names it as a body key. It's in nearly every closing entry cohort-wide, so on its own it would read most entries as specialist. The classifier should treat it as specialist only when it appears with another of the role's markers, and say so in its output.

## Machine patterns (what `scripts/specialist-share.py` reads)

One line per role: `role: pattern | pattern | ...`. Each pattern is a Python regex, case-insensitive unless it's wrapped in `(?-i:...)`. These are CIO's transcription of each role's row above. A role that wants a change edits its own row and its line here in the same commit.

```markers
exec: week review | synthesis | \bcorrected\b | against source | rollup v\d | \brelay | decisions\.log | ship #\d | \bwalk\b
lead: on main `[0-9a-f]{7,} | promotion landed | \bgate\b.*tree `[0-9a-f]{7,} | pins: | mutation check | rule 7 | \bscreen | tests success on | built and committed
arch: validated | \bruled\b | (?-i:\bNO-GO\b|\bGO\b) | against the \d\d:\d\d ruling | read from source | read the diff | decisions\.log \d\d:\d\d | correction to \d\d:\d\d | adr-0\d\d | preregistered | bar set before the run
ppm: placed in | filed into | (?-i:Total:) | 0 unplanned | pdr-\d | served bar | \bacceptance\b | \bruling\b | gate class | \bledger\b | map v\d | weekly diff | \bproposal\b | known-issues line
cxo: judged: | served (pass|fail) | \bruled\b | \bruling\b | colleague test | written strings | \bwords\b | filed #\d | \baccepted\b | \brejected\b
comms: \bprose\b | editorial review | fact.?check | template.?audit | publish-ready | scaffold | mining pass | narrative-survey-ledger | external.*ship #\d | calendar.*\b(row|tease|draftpath)\b | \bcopy\b.*(letter|/try/|/privacy|known-issues)
docs: omnibus | step 1d | day-closed | publish-post | (?-i:PUBLISHED) | calendar row | merge-keeper | weekly audit
pa: \bmcp\b | deploy-mcp | \bconnector | what_piper_knows_about_me | \boauth\b | allowlist | served\b.*\b[0-9a-f]{7,}\b | test plan | \bplugin | \blisting\b | \br7\b
web: lighthouse | wcag | \bcontrast\b | vercel | served.*quoted | publish-post | \bcompose\b | website main | served check | verified how:.*curl.*grep
host: \btrust\b | credential custody | invite hold | \broster\b | (?-i:OWED) | agent 360 | role health check | rule 8 | redemption read | restore drill
cio: methodology-\d | (?-i:PP-0\d) | pattern-0\d | \baudit\b | proto-pattern | worked example | \bcorollary | (?-i:Emerging) | staleness run
```

Left out on purpose: `Verified how` alone (it's in nearly every closing entry; Web's form needs `curl` and `grep` with it), and CIO's own `review` (too broad).

## First run, 2026-11-06: v0, not yet calibrated

`scripts/specialist-share.py --from 2026-10-30 --to 2026-11-05`, against the 11-06 subagent figures for the same window (`role-duties-rerun-2026-11-06.md`):

| Role | heading | lead (heading + first line) | content (any line) | 11-06 subagent |
|---|---|---|---|---|
| Exec | 11% | 35% | 74% | 19% broad, 2% strict |
| Lead | 16% | 20% | 26% | 43% strict |
| Arch | 16% | 32% | 67% | 26% heading, 44% content |
| PPM | 7% | 14% | 54% | 27% (13% without fire entries) |
| CXO | 13% | 55% | 69% | 49% |
| Comms | 8% | 19% | 63% | 46% |
| Docs | 17% | 39% | 53% | 26% |
| PA | 9% | 38% | 57% | 8–14% (served checks off-card) |
| Web | 1% | 21% | 41% | 20% |
| HOST | 3% | 26% | 72% | 19% |
| CIO | 6% | 14% | 40% | 4% heading, 8% content |

**Reading:** none of the three figures tracks the raters across roles yet. The marker lists are each role's own, but they don't yet match how each role writes:
- **Lead:** the list says "built and committed", while Lead's entries say "#2284 built".
- **Comms:** the drafting entries carry none of the nine forms in their first line.
- **Body text** cites rollups, rulings and scripts in passing (Exec's `rollup v`, HOST's `redemption read`), so "content" over-reads.
- **PA:** the gap is definitional. PA's own markers count served checks as MCP work, which the subagent scored as off-card. If PA's card gains served checks as priority 3, PA's own markers are the right reading.

**Calibration, before the 12-18 run** (row 8r):
- Label a sample of about 20 entries per role, specialist or not, by a rater other than CIO, with CIO adjudicating.
- Pick which figure tracks the labels.
- Send each role the misses on its own line, so it can adjust its markers.

It needs judgement and an independent rater, so it's banked for a fresh session, not this one (named trigger).

## Calibration, 2026-11-07: the markers don't measure it; two raters do

**Answer:** none of the marker figures tracks the work. The rater method does, so it is the instrument from the 12-18 run on, and the marker figures are kept only as the v0 record.

**Method.**
- **Sample:** `scripts/specialist-share.py --from 2026-10-30 --to 2026-11-05 --sample DIR` (seed 20261107). 20 entries per role, 220 in all, from the v0 run's window. It reproduces byte for byte.
- **Raters:** two Sonnet subagents, each blind to the script and to the other. Rater 1 read the three packs as three agents; rater 2 read all 220. Both had the brief below and each role's card from its briefing.
- **Adjudication:** CIO's, on the 14 entries the raters split on. Entries both raters agreed on stand.
- **Second method:** I also ruled on 22 script-versus-rater disagreements (2 per role) before the second rater ran. Rater 1 was right in 20.

**Results** (`--score DIR`):

| Measure | Agreement | Kappa |
|---|---|---|
| Rater 1 against rater 2 | 206 of 220 (94%) | 0.87 |
| Marker figure `heading` against rater 1 | 132 of 220 (60%) | 0.12 |
| Marker figure `lead` against rater 1 | 127 of 220 (58%) | 0.12 |
| Marker figure `content` against rater 1 | 121 of 220 (55%) | 0.11 |
| Labelling every entry general | 123 of 220 (56%) | 0 |

The best variant tried, content markers with fire headings forced to general, agreed at 65%. It was scored on the same sample it was designed on, so 65% is an upper bound. Per-role errors stayed large: Exec 13 against 5, Lead 2 against 10, CIO 5 against 13.

**Why the markers fail** (seen in the adjudicated sample):
- **Misses:** the work is written in words the list doesn't carry (Lead's "PUSHED to main as merge"), or after the first line (Arch's "validated" on body line 2).
- **False hits:** fire entries name the lane's nouns in their blocker lists: Comms's "scaffold", Docs's "calendar row", PA's "served" with a sha, Exec's "Rollup v".

More marker tuning won't fix this, because the same words mark the work and the waiting for it. So the roles' marker rows don't need changing. The misses-per-role memo planned above is withdrawn.

**Shares, 10-30 to 11-05, adjudicated** (20 per role; a 95% interval is about ±20 points, so only large moves between runs are visible):

| Role | Raters (r1, r2) | Adjudicated | 11-06 subagent (different method) |
|---|---|---|---|
| Exec | 5, 6 | 7 (35%) | 19% broad, 2% strict |
| Lead | 10, 10 | 11 (55%) | 43% strict |
| Arch | 13, 13 | 13 (65%) | 26% heading, 44% content |
| PPM | 6, 9 | 9 (45%) | 27% |
| CXO | 11, 11 | 11 (55%) | 49% |
| Comms | 11, 10 | 10 (50%) | 46% |
| Docs | 5, 4 | 4 (20%) | 26% |
| PA | 7, 6 | 7 (35%) | 8–14% |
| Web | 6, 6 | 6 (30%) | 20% |
| HOST | 9, 8 | 8 (40%) | 19% |
| CIO | 14, 12 | 12 (60%) | 4% heading, 8% content |

Today's figures are a new baseline. The last column used other definitions (heading level, an unwritten "strict"), and the gap between the columns is the 11-06 run's point 5 made visible.

**Adjudications:**
- **S:** exec-03, exec-05, exec-07, lead-19, lead-20, pa-10, ppm-05, ppm-06, ppm-20.
- **G:** cio-07, cio-09, comms-14, docs-08, host-12.

Rater 1 read PPM's issue placement as bookkeeping. The card makes it priority 1, so I ruled it S. The brief now says a card's priority-1 duty is specialist even when it's routine.

**Limits:**
- Both raters are the same model with the same brief, so a bias they share wouldn't show as disagreement. My 22 rulings are the only different-method check.
- Ratings were made on the first 1,100 characters of each entry.
- CIO rates and adjudicates its own row: both CIO splits were ruled against CIO.

## Rater method (the instrument from 12-18)

1. `scripts/specialist-share.py --from <start> --to <end> --sample DIR` with the default seed, or a new seed written in the run's report.
2. **Rater 1:** three Sonnet subagents, one per pack, each writing `DIR/labels-r1-<pack>.json`. **Rater 2:** one Sonnet subagent over all three packs, writing `DIR/labels-r2.json`. Each is told not to open the other's files. Set the model explicitly.
3. `--score DIR`. CIO adjudicates the listed disagreements and reports the adjudicated shares, kappa, and the interval.
4. If kappa falls under 0.6, the brief has drifted from the logs. Fix the brief before quoting any share.

The brief, verbatim except for the paths:

> For EVERY entry, decide: is this entry the role's SPECIALIST work?
> - S (specialist): the entry's main substance is the role itself doing work that advances its own card's purpose or priorities (its lane): e.g. making a judgement, ruling, synthesis, building, validating, reviewing, writing its own lane's artifact. A duty the card names as priority 1 counts as S even when it's routine.
> - G (general): the main substance is fire/check bookkeeping (START/WATCH/STOP routine, CI status, heartbeat, sync, sign-off, DAY-CLOSED), mail filing or forwarding without the role's own assessment, relaying someone else's decision, logistics, commodity items the card says to keep small, or work in another role's lane.
> - If an entry mixes both, label by what most of the entry is about. Judge the WORK described, not keywords. If the text is too thin to tell, label G and say "thin".
> Write JSON shaped {"<id>": {"label": "S", "reason": "<=12 words, specific to the entry"}}.

The priority-1 sentence was added after this calibration, from the PPM adjudications. The 12-18 run is its first use.
