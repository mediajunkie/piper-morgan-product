# Architect Carry-Forward — Resumption Substrate

**Purpose**: durable handoff record for the next Architect session (duty-cycle-tick + PM-ratified single-log discipline 2026-06-12 + escalations-doc FOLD 2026-06-17). PM-attention items ride here.

**Consolidated 2026-08-15 06:5x PT** — named trigger from 08-14's STOP note ("if tomorrow is quiet, that pass is the right next move"). Folded 08-11→08-14's settled daily notes into the summary below; **re-verified every "Owed by me"/"For PM" item against `gh issue view` live rather than carrying 07-29/08-04 claims forward** — result: `#1430`, `#1419`, `#1433`, `#1484`, `#1466` are all **CLOSED** and were still sitting in this file as open asks. The entire old "For PM" section is now stale/resolved and has been removed (see note where it lived). This is exactly the failure mode the file's own prior staleness-warnings predicted — worth remembering the warnings were right, not just fixing the result.

---

## Environment (verified 2026-07-29, still accurate)

| Fact | Value |
|---|---|
| Host | **Amber** (`pipermorgan.ai` account) — cohort migrated 2026-07-25/26 |
| Worktree model | **Model A** — stable per-agent path, reused every session. **The path is load-bearing** (Claude Code keys per-path state; a fresh path silently orphans accumulated state) |
| Worktree | `/Users/xian/Development/piper-morgan-worktrees/arch` |
| Branch | `claude/arch-cycle` |
| Cron | **`27 6,9,12,15,18,21`** (6×/day, offset :27), job **`4c9a63ff`**, re-armed at 08-21 STOP via delete-then-create (prior `d6d05551`). **Session-only — dies with the session.** Empty `CronList` → re-arm this expression. Full reboot/park story (macOS 26.6, 08-11): `docs/handoff-arch-2026-08-11.md` §1 |
| Registry row | **`active`** in `dev/active/duty-cycle-registry.tsv`, kept in sync at every re-arm |
| Memory | shared cohort pool, keyed to the git **common** dir — shared by construction with every role |
| Mail | `scripts/mail-send.sh` push-to-ref from this worktree. **Never** touch PM's main checkout working tree (HARD RULE — PM saves uncommitted work there) |

**Hooks** (settled 2026-07-29, still current): a real `.git/hooks/pre-commit` gate is installed in the shared common dir and delegates to `check-branch.sh` — *any* commit that would place a `mailboxes/` path into a non-`main` branch commit is refused, however staging was expressed. The advisory PreToolUse layer stays too (HOST ruled, on measurement, against retiring it — `--no-verify` + prior-call staging is UNCOVERED by the gate, held only by the advisory layer + `mail-send.sh` being safe by construction). ⚠️ Cleanup wedge: a gate-blocked commit leaves the file staged, and the advisory layer's predicate matches `git commit` **anywhere** in a call — make cleanup calls contain no `git commit` (`git restore --staged <path>` then `rm -f <path>`, separate commands).

---

## Recent history (08-11 → 08-14, condensed from daily notes)

**08-11**: Amber rebooted for macOS 26.6. Cron parked pre-reboot, re-armed post-reboot, verified. Quiet mail otherwise.

**08-12**: Retroactive `DAY-CLOSED` self-heal for 08-11 (two fires queued without a turn — session-specific, not cohort-wide, confirmed via `cohort-freeze-detect.sh`). Otherwise quiet.

**08-13**: Quiet day. Watched (didn't own) the **CXO/PPM #1569/#1605 design thread** run to a clean resolution through 4 rounds — worth remembering as a model of the discipline: PPM caught a real DESTRUCTIVE-vs-WRITE confirm-gate asymmetry against actual `EffectClass` code, not summary.

**08-14 — the week's most substantive day**:
- **Understanding-Layer Inversion Phase 1 ruling.** Lead needed two of my prior conditions decided before tuning. Verified both against source rather than the memo: **ratified** the 62-canonical-operation grammar (independently re-ran `derive_routing_grammar()` live). **Split, not uniform** on the corpus-fix ask — Lead's memo treated two rows as the same shape; `create_issue`'s QUERY-filing was a real artifact, `meeting_time`'s was a **deliberate cited decision (#589)** the memo had mischaracterized. Sent back split; Lead executed both correctly (filed **#1619** for the wider mutation-under-QUERY pattern); **I verified all three completion artifacts before accepting**, catching my own first-pass mistake (checked the generated corpus file instead of its actual source). Thread closed cleanly. **Watch item**: Phase 1 shipped shadow-only; five corpus categories are still REVIEW-only/ungateable, so the validating instrument has its own live measurement gap — don't over-read the 93/93 result as more settled than it is.
- **Ship #056 workstream review**, filed same-evening after PM moved the deadline up. Led with the routing-moratorium→Inversion pivot as the week's central architectural fact; named my own 08-08 merge-drop and 08-09 mailbox-glob incidents without softening them; flagged the merge-aware hook (asked of CIO 3×, still not landed) and the spatial-intelligence PM-gate (open since 07-30) as live risks, both freshly re-verified rather than assumed.
- **Agent 360 v0.4** fielded by HOST — deliberately deferred, tracked in `arch-standing-items.md` with its real ~2-week deadline. Don't let it slide silently.

---

## Standing hard rules — load-bearing, not stale, keep verbatim

### 🔴 Never glob the inbox (2026-08-09, PM-escalated as a TRUST VIOLATION)

**`read/` is a CLAIM ABOUT MY OWN COGNITION.** On 08-08 I moved a memo there **without reading it**, then told PM it didn't exist — PPM's independent search inherited my false framing. PM: *"a real violation of trust."*

⛔ **NEVER `for f in mailboxes/arch/inbox/*.md`.** ✅ **The drain iterates a list I APPEND TO IN THE SAME TOOL CALL THAT DISPLAYS A MEMO'S CONTENTS.** Unread ⇒ never in the list ⇒ **cannot move.**

**Two halves, get both right**: reading (the cognitive act) and pushing (the shared record) are separate failure points — I got each wrong on consecutive days once (08-08: moved without reading; 08-09: read properly but only pushed the MANIFEST, not both sides of the move). **Mandatory verification after every drain**: `git ls-tree -r --name-only origin/main -- mailboxes/arch/inbox/ | grep -vc MANIFEST` — never `ls` the local directory, which can read clean while the trunk is wrong.

**And search for the OBJECT, not a guessed date** — I once searched for "a Lead memo dated 08-09" when the memo was dated 08-08, concluded it didn't exist, and was wrong.

### 🔴 State the scope IN the ruling (2026-08-10)

**Earned three times in one fortnight**: I ratified a direction and a specific clause rode along unratified; I ruled against a spec's copy of a type instead of the landed one; my material sat adjacent to someone else's finding and inherited its apparent scope. CXO's diagnosis: *"Proximity does attributive work. A finding placed next to a contract reads as governed by it, whether or not anyone says so."*

**Three lines, before any ruling ships**: (1) name the OBJECT the ruling is about — the actual file/type, not a description of it; (2) name at least one thing the ruling does NOT cover, especially the adjacent thing a reader would most plausibly assume it does; (3) if ratifying a document, say which CLAUSES — a ratified direction is not a ratified sentence. Same discipline for placement: if something a contract's enforcement can't reach sits next to it, say so in the material itself, not the covering memo.

*(This convention is what caught the `meeting_time`/`create_issue` conflation on 08-14 — Lead's memo violated exactly this pattern, and checking for it is what surfaced the error.)*

---

## Active threads

### Owed by me / watching (verified live 08-15, not carried from stale notes)

- ✅ **Understanding-Layer Inversion, Phase 2.1 gate RULED 2026-08-19 — #1663 (armed answer-turn emission contract), ratified (b).** Gate found the constrained router correctly reads armed-turn bindings 6/7 (e.g. "at 3pm" → `create_reminder` @0.95 with args, on a flow asking a reminder-time question) but the scoring convention expected `route:NONE` — a real contract gap between "router demonstrably understands" and "what the corpus asserts." Verified Lead's load-bearing safety claim against code before ruling, not on trust: `_process_intent_internal`'s pending-offer pop (`intent_service.py:1024`) runs before classification, unconditionally — real and structurally enforced. Ratified **(b)**: seam consumes the router's flow-matching emission as a hint (binds to the armed flow's handler, never fresh-dispatches; falls to the seam's own re-ask on mismatch, never to the floor) rather than **(a)** teaching the router to always emit NONE (which depends on every future caller correctly treating NONE as "hand to the seam" — and NONE's failure mode is the floor, which is #1648's fabrication mechanism). **Required condition attached**: before wiring, confirm per-flow (not assumed) that the flow's arm-time question is an adequate confirmation for its completing operation's EffectClass tier. **Real gap found verifying this, filed separately as #1666** (not blocking): `delete_todo` — used in #1663's own worked example — has no `WorkflowEntry` and never reaches `consent_gate.decide_consent`; it executes immediately via the legacy elif-chain with zero confirm logic. Pre-existing, independent of #1663, but #1663's example implicitly assumed the gate was there. **Watch for**: Phase 2.2's actual build against this contract, and whether #1666 lands before delete_todo's binding gets wired.
- **#1481** (OPEN, Production) — socket-mode Slack DM/mention path binds every sender to the connector owner's principal; `#1466`'s mapping (now closed/shipped) should resolve per-sender identity here too. Not blocked on me; watching for whether it's sequenced.
- **#1459** (OPEN, Production) — `Intent.original_message` dual-surface storage, the thread I raised 07-29. Per 08-14's log: **SPECCED (AC + ratchet shape) but NOT BUILT** — a build task now, not a design question. Not blocked on me; Lead's to sequence.
- **#1462** (OPEN, Production) — Hosted MCP endpoint + plugin distribution EPIC (PDR-006 implementation). The load-bearing risk I flagged in PDR-006 — fail-closed caller-identity, since all ADR-079 owner-scoping sits downstream of it — lives here now, not as a standalone "For PM" ask.
- **PDR-006 ChatGPT success criterion** — last touched 08-02/08-05 (PPM: the criterion is "unmeetable as written" pending a retest CXO gates on `mcp.pipermorgan.ai` existing). **Not re-verified since** — don't assume either way; check before citing.
- **Merge-aware hook** — requested of CIO three times (08-08, 08-09, 08-10). Confirmed still not landed as of 08-14 (git log + mail search). Highest-leverage unfixed item from my own 08-08 incident; stays flagged until it ships.
- **#1633 (`issue_intelligence.py`) — RULED 08-16, watch for Lead's sweep.** Investigated before ruling (not just Lead's framing): zero production callers, a dead config flag, and a prior Phase-0 investigation had already found this exact gap and left it unresolved (`test_standup_data_sources.py:127`'s own docstring). Ruled **DISPOSE**, not complete-the-wiring — this was never started, not 75% done. Flagged two things for the sweep: yesterday's `5d27a2a70` patched a line in this dead file believing it was live; the standup test has a broken import (`IssueIntelligence`, a class that doesn't exist) silently swallowed via `except ImportError`. Ruling posted to GH #1633 and sent to Lead. Not blocked on me now — watch for the sweep landing.
- ✅ **Spatial-intelligence review CLOSED 2026-08-15, scope FINAL 2026-08-16: ALL 11 MODULES.** PM extended disposal from 9 to all 11 same night — the last 2 (`notion_spatial`, cold `slack_adapter`) get the same "superseded prior art" treatment as the other 9, PM: *"ok to also remove any superseded predecessors."* **Execution not yet claimed by me or Lead.** If it lands on me: commit-hash findability must explicitly cover all 11 (PM was explicit this isn't optional) — don't draft a record against the original 9 and forget the extension. L4 phased plan (MVP placeholder #1635 / Beta #1174 unchanged / Production gated on Lead's delivered cost estimate + discovery) unchanged from the 08-15 ruling. My review slice was done 07-30; nothing further owed on the architecture side.
- **Agent 360 v0.4** — tracked in `arch-standing-items.md` with its real deadline (~08-28). Don't answer it rushed.
- ✅ **Surfaces taxonomy consult ANSWERED 2026-08-16.** CXO's v0.1 draft (`docs/internal/design/surfaces-taxonomy-2026-08-16.md`) asked two things: ratified the **F-AuditTransparency split from F-Errors** (ADR-063 checked directly — real routes, real module, own auth model; general error handling has no comparable doc, so they were never one thing). On the platform-axis question, **investigated before answering rather than trusting CXO's "receipts"**: found §3's cited PDR-005 mechanisms (capability-claim layer, client-identifier template dispatch) **don't exist in code** — PDR-005 commits to exactly one template at 1.0, so there's been nothing to dispatch between yet. What IS real (`services/commands/registry.py`'s `CommandDefinition.interfaces`) has the right *shape* but is narrower than the taxonomy (no Notification/Mobile axis, `CommandCategory.SETTINGS` declared-but-unused — the taxonomy's own worked example maps to an empty slot). Ruled: ratify the naming, but say explicitly the platform axis is *decided*, not yet *enforced* — flagged as a real follow-up, not silently assumed done. PPM's MVP-vs-aspirational consult landed same fire (cc, no arch action) — all 7 open cross-matrix cells deferred, one general rule (Slack cells inherit #1481's existing hold) rather than seven separate calls. **Watch for CXO's ratification pass** — my two rulings are inputs, not the close.

### Resolved this pass, confirmed via `gh issue view` — do NOT re-open or re-ask

`#1430` CLOSED · `#1419` CLOSED · `#1433` CLOSED · `#1484` CLOSED (Slack kill-switch shipped) · `#1466` CLOSED (Slack principal mapping shipped, guarded by `tests/test_slack_identity_binding_guard.py`) · PDR-006 itself RATIFIED (PM, 7/31) · the "is Slack inbound a beta surface" question resolved via #1484 shipping the fail-closed gate exactly as recommended.

**The old "For PM" section lived here** (07-29 through 08-04 asks: Slack-beta-scope word, two board-field mismatches, #1430 closure, cron-cadence confirmation, PDR-006 ratification). **Every item on it is now resolved or superseded** per the live check above — removed rather than left to accumulate more silent staleness. If a genuinely new PM-facing ask arises, it gets its own dated entry, not a revival of this one.

---

## Standing guard — the invariant most likely to be accidentally reversed

**ADR-078 D4: the classifier stays stateless.** HOST-endorsed, load-bearing. The pressure to "just give the classifier the conversation history" recurs on every reference-resolution bug — it nearly landed twice. The answer is always: resolve it in surface-1 / the ledger / the pre-classifier. Injecting history also silently disables the classifier cache, so it's two regressions riding one fix.

⚠️ **New pressure point to watch, 2026-08-21**: PM's "held-state parity" principle (**#1673**, audit-scoped, can-wait) — equip Piper with the same durable-state discipline the cohort proves on itself (carry-forward, session logs). Real and worth doing, but if read as "thread more state into the classifier," it's the same D4 violation in new clothes. Attached the boundary to the issue directly: the right shape is async/reconstructive (carry-forward-like, or #1510's `SessionSnapshot` — assembled before the call, consulted by a seam) not live-in-context. Watch when the audit actually starts.

**PM's personal delegation, which is the core of this role**: *"Lead is welcome to map, diagnose, propose, but I rely on you to maintain the architectural integrity of this project."* A STOP does not require having the right answer — it requires protecting the invariant while the right answer is found.

**The signature move**: on every ruling, ask *"can I make the bad state unrepresentable instead of forbidden?"* — derive the model set, derive the mapper surface, derive the tool catalog. A contract that can't drift beats one everyone must remember.
