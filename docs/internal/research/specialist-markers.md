# Specialist-work markers, per role (for the fixed classifier)

**Owner:** CIO. **Asked:** 2026-11-06, in the third staleness run (`role-duties-rerun-2026-11-06.md`), so the next run (with the next Agent 360 round, about 12-18) classifies every role's log entries the same way twice. **Each role owns its own row:** what counts as its specialist work is that role's call. A marker is a word or heading form that, in an entry's heading or body, means the entry was specialist work. Markers due by 2026-11-20.

**What the classifier will do (not built yet):** an entry is specialist if its heading or body carries one of its role's markers and isn't only fire boilerplate. It reports specialist / total per role, with the marker counts, so a reader can see which markers carried the share.

| Role | Markers, as the role sent them | Not specialist (role's note) | Received |
|---|---|---|---|
| HOST | `trust`, `credential custody`, `invite hold`, `roster`, `OWED`, `Agent 360`, `Role Health Check`, `rule 8`, `redemption read`, `restore drill` | Also keys on `Drain:` and `Verified how:` lines in bodies | 11-06 05:46 |
| PPM | `placed in` / `filed into`; `Total:` / `0 unplanned`; `PDR-`; `served bar` / `acceptance`; `ruling` (with a role or xian, writing the product position); `Gate class` / `ledger`; `map v`; `weekly diff`; `proposal`; `known-issues line` | `Drain:`, `Synced`, `Main CI` | 11-06 05:47 |
| Lead | `**… on main \`<sha>\`**` (a landing); `Promotion landed: alpha serves`; `gate` with `tree \`<sha>\``; `Pins:` and `mutation check`; `rule 7` / `screen`; `Tests success on`; `Verified how:` on an issue comment or close; `built and committed` | Entries with only `mail`, `memo`, `heartbeat`, `Drain:` or `log(lead)` | 11-06 06:06 |
| Exec | `week review`, `synthesis`, `Verified how`, `corrected`, `against source`, `rollup v`, `relay` (xian's ruling relayed), `decisions.log`, `Ship #`, `walk` | (none given) | 11-06 06:04, in its Agent 360 v0.6 answer |
| Arch | `VALIDATED` / `validated on main at <sha>`; `ruled`; `GO` / `NO-GO`; `against the HH:MM ruling`; `read from source` / `read the diff`; `decisions.log HH:MM`; `CORRECTION to HH:MM`; `ADR-0NN` written or amended; `preregistered` / `bar set before the run`. Classify by body, not heading: mail-wake headings carry the sender | (none given) | 11-06 06:28 |
| CXO | `Judged:`; `served PASS` / `served FAIL` in a heading; `ruled` / `ruling`; `Colleague Test`; `Written strings` or a heading with "words"; `filed #` for a UX finding; `accepted` / `rejected` as evidence | `mail triage`, `START`, `Wrap`, `DAY-CLOSED`, `Drain:`. Caution: `served PASS` also appears when CXO records another seat's check; it's CXO's only when CXO wrote the verdict | 11-06 06:32 |
| Comms | `review` with a post title or `prose`; `fact-check`; `template-audit`; `publish-ready`; `scaffold`; `mining pass` / `NARRATIVE-SURVEY-LEDGER`; `External` with `Ship #`; `calendar` with a slot (`row`, `tease`, `draftPath`); `copy` with a surface (`letter`, `/try/`, `/privacy`, `known-issues`). Case-insensitive; in a heading or an entry's first line | Entries headed only `WATCH`, `mail wake` with only filing, or `STOP` bookkeeping | 11-06 06:20 |
| Docs | | | |
| PA | | | |
| Web | `Lighthouse`; `WCAG` and `contrast`; `deploy` with `Vercel`; `served` with `quoted`; `publish-post` and `compose`; `website main`; headings starting `### … (served check)` or `Served checks`; `Verified how:` naming `curl` plus `grep` on pipermorgan.ai pages | (none given) | 11-06 06:19 |
| CIO | `methodology-`, `PP-0`, `Pattern-0`, `audit`, `proto-pattern`, `worked example`, `corollary`, `Emerging`, `staleness run`, `review` (of a mechanism against its criteria) | Fire checks, mail filing, `Drain:` | 11-06, CIO's own |

**Design notes for the build:**
- `ruled` is shared by Arch, CXO and PPM. That's fine per role, since each role is classified against its own list.
- Arch and CXO both warn that headings undercount (Arch's mail-wake headings name the sender) or over-count (CXO's `served PASS` quoting another seat). So classify on heading and body, and print both, as the 11-06 run did for Arch and CIO.
- `Verified how` appears in both Lead's and Exec's lists, and HOST names it as a body key. It's in nearly every closing entry cohort-wide, so on its own it would read most entries as specialist. The classifier should treat it as specialist only when it appears with another of the role's markers, and say so in its output.
