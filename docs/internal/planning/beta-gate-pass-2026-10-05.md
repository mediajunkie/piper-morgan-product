# Beta Gate: one-time frozen-list pass, 2026-10-05

**Owner**: PPM
**Status**: PROPOSAL. Read-only. No milestone, Sprint-field, label, or issue state has been changed. Applying anything below needs PM's explicit confirmation (via Exec).
**Standard applied**: `beta-gate-standard.md` v0.1, PM-ratified 2026-10-05.
**Method**: all 31 open MVP issue bodies read in full on 2026-10-05, each classed against the four admission classes and the Epic 0 clause. The standard's "Illustrative application" (title-level, 10-03) predicted 30; the milestone held 31 on 2026-10-05 (#1930, #1931 added 10-04).
**Denominator**: 31 of 31 open MVP issues read. Not measured: whether each corpus row named below already exists, and whether #1867's fix-build has landed. Both are marked "unverified" where they matter.

## Result

| Disposition | Count | Issues |
|---|---|---|
| Stay in the gate | 10 | #1885, #1735, #1889, #1880, #1852, #1913, #1907, #1386, #1595, #1925 |
| Close against what already landed | 1 | #1930 |
| Epic 0 evidence: corpus row, then leave the gate | 6 | #1579, #1623, #1771, #1783, #1843, #1860 |
| Held for an Arch ruling | 2 | #1867, #1886 |
| Production (post-beta) | 12 | #1522, #1625, #1632, #1698, #1817, #1832, #1891, #1911, #1915, #1916, #1917, #1931 |
| **Total** | **31** | |

If PM confirms everything as proposed, the gate goes from 31 to 10, or to 12 if Arch rules both held items in. Weekly line from here: admissions by class, closes, net.

## Per-issue, by class

### Stays in the gate (10)

| # | Class | Basis from the body |
|---|---|---|
| #1885 | 2 Security | Three live unused invite tokens sat in full in tracked logs of a public repo. Scrub is on main; the burn on prod needs PM's hand. Google/Slack key-rotation check also open. |
| #1735 | 3 Honesty | The ADR-075 notice "I'll tune to your role and priorities as I learn them" is false as worded: auto-apply is a silent no-op and the learned store is in-memory and unread. **Gate-minimum is the copy fix** (CXO's call). Wiring the learning loop is a design decision and post-beta; I propose splitting that to a new Production issue once PM confirms. |
| #1889 | 3 Honesty | `degraded_sources` doesn't reach the standup's Slack/Markdown/text formatters, `/today`, or the Radar empty-state card, so degraded data can render as all-clear. |
| #1880 | 3 Honesty | Header states `len(free_blocks)` then shows three (the standard's own "count contradicts the list" example), and clarification turns print "Found N matching" with five shown on a turn whose purpose is choosing. The latent `[:N]` slices are not gate items. |
| #1852 | 4 Golden path | Slack/Google redirect URIs still point at the fly.dev host. The body says it must land before any tester is pointed at Slack/Google connect. Needs PM keystrokes in the provider consoles. **Body names `alpha.pipermorgan.ai`; target is now beta.pipermorgan.ai** (R7), so the callbacks to register are the beta host's. |
| #1913 | 4 Golden path (+ honesty) | A chat started keyless vanishes from the sidebar after a valid key is added. PM rated it a fail. |
| #1907 | 4 Golden path (weakest admit) | iPad Safari portrait: empty gray panel, composer off-screen, Send clipped. By the letter, a tester on an iPad cannot hold a conversation. If the first wave is desktop-browser only, this moves to Production; PM's call. |
| #1386 | Close-out gate | The gate's own sign-off. **Its body is stale**: it still reads "Beta Blockers sprint", "alpha build", and a Fly artifact. Proposed: rewrite criterion 1 to "MVP milestone clear" under the ratified standard. Held until the board-edit yes. |
| #1595 | Epic 0 itself | The epic. In the gate by definition. |
| #1925 | Epic 0 completion tail | 18 contract tests broken by the Phase 3 deletions. Scope, not evidence. |

### Close against what already landed (1)

- **#1930** (portfolio "delete my project" asks to confirm but nothing executes). CXO ruled 10-04: step 1 (stop promising the action) now, step 2 (wire via the #1190 destructive tier) later. Step 1 landed; step 2 is #1935 in Production. Proposed: close #1930 against step 1. Its own acceptance criteria allow this ("if not wired yet: the prompt stops promising an action it can't take").

### Epic 0 evidence: corpus row, then leave the gate (6)

#1579 (PORTFOLIO list rejects "me"), #1623 (mid-gathering answers stolen by other surfaces), #1771 (deferral phrasing abandons resumable flows), #1783 (interrogative request read as a state question), #1843 (`^please\s` finalizes a standup draft), #1860 (standup initiation verbs uncovered).

All are interpretation-layer failures carrying the issue's own `Class: pattern-accretion` tag, under the standing moratorium. The standard sends them to corpus rows under #1595. **Pre-move check (unverified today):** each has a corpus row or a recorded evidence comment on #1595. Rows missing one get it before the issue leaves the milestone. Class 1-3 consequence check done on read: none of the six has a class 1-3 consequence.

### Held for an Arch ruling (2)

- **#1867** (no registry says which guided processes are wired; flows can start sessions on the deregistered onboarding process). Structural, not a user-visible false claim. Whether its enforcement-test fix-build has landed is **unverified**.
- **#1886** (`_handle_add_project` creates an onboarding session on the dark process; a bare-name reply silently orphans it). User-reachable, PM hit the earlier shape (#1856). It is the system opening a conversation it cannot continue. It fits no class cleanly and the issue itself says "Arch's call". **My lean: Production unless Arch says Phase 3 fixes it by construction** (then it is Epic 0 evidence).

### Production (12)

| # | Why not a gate class |
|---|---|
| #1522 | False-trails audit; an inventory and ordering, no user-facing defect. |
| #1625 | Reminder-nagging design ruling; a dose-of-feature question, not a false statement. |
| #1632 | Outwardness in the capability catalog. Omission in a legibility surface, not a false claim; action-time confirmation already carries the consent. CXO may weigh this differently. |
| #1698 | Spatial-disposal dead-family epic. |
| #1817 | Self-described "not a bug today": a dated assumption with a named expiry (the first surface that lets a user de-authorize a provider). Trigger is findable from the issue. Ask Arch to concur that Production, not the gate, is its right home. |
| #1832 | Dead-route test; deletion proposal. |
| #1891 | Follow-up design question to #1632; same reasoning. |
| #1911 | MCP OAuth consent page branding. MCP surface: per R7, via the probe and the beta period. |
| #1915 | Timezone alias acceptance ("pacific time"): enhancement. |
| #1916 | Google audience copy and started-never-returned record. Calendar connect is not in the #1386 scenarios; the real gating item is PM's choice of OAuth audience (see below). |
| #1917 | "PRs needing review" has no operation. The body says "product ask, not in any sprint." A missing feature, not interpretation-layer; the title-level pass guessed Epic 0 evidence and was wrong on read. |
| #1931 | Reopen todo from chat. CXO ruled out-of-chat is acceptable. Not a gate class. |

## Two things the pass surfaced about the standard itself

1. **Class 4 contradicts itself as ratified.** It says a tester who cannot "connect an integration" is blocked, then defines the golden path as "exactly the scenarios in #1386". Those scenarios are onboarding plus GitHub write, work-session continuity, and honest decline. They do not include Slack or Google Calendar. So #1852 and #1916 fall in or out depending on which sentence wins. **Proposed clarification (v0.2, needs PM's yes): the golden path is the #1386 scenarios plus every integration the beta invitation tells testers to connect.** Under it, #1852 is in the gate if the invite names Slack/Google, and #1916 is Production either way (if the invite names Google Calendar, the fix is an OAuth-audience decision, not this issue). The text of v0.1 is left unchanged until PM decides.
2. **One decision only PM can make drives two issues:** the Google OAuth audience (Internal vs External/Testing). Internal blocks every design partner outside the pipermorgan.ai Workspace from calendar connect. This is configuration, not code.

## What happens next

Nothing on the board until Exec relays that PM said yes. On the yes, in this order: close #1930; milestone-move the 12 Production items and, after the corpus-row check, the 6 evidence items; file the #1735 follow-up; rewrite #1386's body; retire the parallel records (Beta Blockers Sprint value, `beta:*` labels, `beta-blockers.md` tables). Arch's ruling on #1867 and #1886 lands whenever Arch answers.

Verified how: method is a full read of each issue body from `gh issue view` captured 10-05 (31 of 31); layer is issue text, not source or live behavior. Claims about code (e.g. "no live caller") are quoted from the issue authors and were not re-run today. The class assignments are my judgment against the written standard; nothing here is a measurement of the product.
