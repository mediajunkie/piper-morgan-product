---
last_updated: 2026-10-04 21:3x
currency_claim: rewritten at substantive-change boundaries, verified at every START
max_age_days: 4
---

# Architect Carry-Forward — Resumption Substrate

**Purpose**: durable handoff for the next Architect session — current state and active threads
only. Resolved history lives in the session log (`dev/YYYY/MM/DD/`) and `decisions.log`, not here —
per PM's 2026-06-12 ruling that the session log is the durable record, and the 2026-09-22
context-floor directive that duplicating it here is exactly the accretion to cut.

---

## Environment (stable; verify at START, don't re-derive)

| Fact | Value |
|---|---|
| Host / model | Amber, Model A worktree `~/Development/piper-morgan-worktrees/arch`, branch `claude/arch-cycle` |
| Model | **Opus 5.5 (`claude-opus-5-5`) since the 2026-09-28 ~14:35 cold restart** (Pard, PM-authorized, no `--resume`). Verified from the runtime model system-reminder, not the handoff's stated intent. ⚠️ `~/.claude/settings.json` and `~/.claude-pm/settings.json` BOTH still read `claude-sonnet-5`, so the Opus model comes from a launch-time override, not the settings default. A relaunch that drops the override would silently come back as Sonnet. Check the runtime reminder after any restart (rule 7). |
| Wake mechanism | ⚠️ **SESSION CRON RETIRED 2026-09-25, PERMANENTLY — do not re-arm.** External LaunchAgent (Pard), reading the registry's `cron_expr`. Registry-vs-plist mystery resolved 09-26 with a `pm-cadence` drift guard now in place — registry is trustworthy again. **Cadence: back to 6/day `27 6,9,12,15,18,21` as of 2026-09-28 21:27 STOP** (registry col 2 edited, threshold_h 9→7). Exec's 08:0x "revert Tuesday" ruling was RETRACTED 14:5x; final 15:1x memo: PM confirmed "Monday ok" = revert today. **CONFIRMED 2026-09-29: the 09:27 fire arrived** (off-schedule for the old 3/day expression), so the LaunchAgent reads the registry's col 2 live. The prompt's `cron=` constant was regenerated to `27 6,9,12,15,18,21` by 2026-09-30 15:27, so prompt and registry agree again. (It is documentation; the LaunchAgent reads col 2.) |
| Heartbeat | `bash scripts/duty-cycle-heartbeat.sh arch <START\|WORK\|STOP>` — first action after sync, every fire. The watchdog's only structural liveness surface. |
| Mail | `mail-send.sh` push-to-ref; never touch PM's main checkout. Inbox verified at trunk (`git ls-tree origin/main`), never local `ls`. **`mailboxes/pard/` gravestoned 2026-09-23** (hard-refused by the script) — Pard's real inbox is `~/Development/mediajunkie/docs/mail/`, external repo. Drop `pard` from cc if only cc'ing; route through Exec (already active on most threads) rather than write there directly — `docs/internal/operations/cross-project-mail-routing.md`'s standing preference. |
| GitHub criteria line | `gh issue list --repo mediajunkie/piper-morgan-product --label architecture --state open` — the third work-queue source (PM v1.33). Open each issue, don't write a row from the list. Report drained as "mail (N) + standing-items (N) + label:architecture (M)." |

## IN FLIGHT — current state only

⚠️ **If you're reading this cold after a restart (no `--resume`), read
`dev/active/arch-handoff-pre-opus-5.5-restart-2026-09-25.md` FIRST for the reasoning/narrative** —
but **per Pard's explicit 09-25 ruling, treat that doc as base layer once it's >48h old, not a live
description**: this carry-forward + session logs + commits are the current state; the handoff's
job shrinks to orientation once it ages. **Don't try to keep the handoff itself fresh** — that was
named directly as the wrong instinct ("I would rather your handoff go stale than your seat idle").

- **SPRINT GOAL (PM-locked 10-03, week ending Thu 10-08)**: finish epic 0 Phase 3 deletions for every live-wave list. Lead owns it. Arch's part is **same-fire
  ruling turnaround**. Quota is expected to run out around Wed 14:10, so plan for 4 days. **Both upstream gates were ALREADY CLEARED when I named them**: read_floor went live ~09:5x 10-03 (PM flip, TRUST 15/15 after descriptions) and #1920 CLOSED 10-02.
  DISCOVERY/TRUST/MEMORY/ANALYSIS read GO (partial) and are the week's first lanes. Lead is restarting onto Opus 5.5.
- **10-04 21:3x**: rail-owns-rail-keys AMENDED to (a), split predicate (claims_category for the orchestrator), plus **adapter parity landing WITH it** (per-adapter parity pins).
  (b) rail-per-sibling is a follow-up using the 09-26 sequencing. read_portfolio stays held until (a) + parity + the live list_repos probe. **Watch for**: Lead's unpark report, then tell Exec to release.
  **Standing self-check from 10-04's three misses**: before ruling on a gate or predicate change, grep EVERY caller and read the fallback.
- **10-04 18:5x — THE RAIL OWNS RAIL KEYS** (standing): can_handle must decline every rail key. **read_portfolio token HELD** (via Exec) until the fix plus a live probe of list_repos.
  **Watch for**: Lead's fix and pins, and the routing-stack doc update. Applies to every future PORTFOLIO/canonical-category token.
- **10-04 15:5x**: #1926 is closed via the unlink claim re-point (with a surface-2 residual probe). Coverage is corpus-driven. **Pard's health-gate patch is INERT**: watch that it's wired
  and proven by a forced-red run before it's applied. #1933 landed clean (0/100).
- **10-04 12:5x**: list_projects reuses the live entry, and search_projects joins read_portfolio (re-gate before PM's flip). Edit literals STAY (my miss reversed). #1933 effect-aware deletion
  endorsed. **Watch for**: #1933's re-verification of the 4 ledgered misserved rows (any fail means the literal is restored), and the complete_todo + portfolio part 2 builds.
- **10-04 rulings**: complete_todo goes ahead under the execute-vocab coverage test (with the 'clear' shared predicate). manage_portfolio split ruled, with delete waiting on #1930. FILE_REFERENCE is out of Phase 3.
  Tokens read_floor_2 / read_canonical / read_portfolio are with PM via Exec (deploy first). **Watch for**: the coverage test landing, and the #1930 ruling (which reopens delete's shape).
- **Phase 3 rail shapes RULED 10-03 18:5x**: one entry per effect class. Wave 2 approved. manage_repos → list/link/unlink. Canonical reads get adapters. manage_portfolio
  (inventory ruled 10-04). Ceiling 155. **Watch for**: the unlink build meeting CXO's 5 constraints, and stakeholder_update's persistence check.
- **Mail routing changed 10-03**: never cc or address PM. PM items go to Exec, with the type named in the subject.
- **read_floor LIVE 10-03 ~09:5x** (PM flipped it). Gate is GO (partial) for its 4 lists. Watch the deletions only.
- **#1606 CLOSED 10-02 (v163)**, built to my 5 conditions (plus verbatim `text`). **Gate (d) GO 10-02** with the served model printed and N=5. PRIORITY/GUIDANCE/STATUS
  deletions are Lead's today. **#1899 write erosion**: shape ruled (cross-family write release plus an explicit exit, both carriers). **Watch for**: CXO's product call,
  and Lead not shipping (a).
- **MCP read-only tool (2026-10-01)**: PM approved it via PA (ChatGPT is tools-only). I concurred with 4 conditions (compose the resource handlers, an allowlist
  test, no LLM, amend PDR-006:276). **Watch for**: Lead's build. Re-review if it re-implements reads or adds an unallowlisted tool. MCP v8 is live (Host-header fix).
- **MCP Phase C / OAuth AS — LANDED, REVIEWED, APPROVED (09-26, `645ce6412d`, alpha v146 / MCP
  v6).** My identity-binding condition verified directly in the shipped code
  (`services/mcp/server/oauth_provider.py:228`'s `_refuse_code`) and its real, non-vacuous test
  (`tests/unit/services/mcp/server/test_oauth_as_unit4.py:584`) — not taken on Lead's description.
  **Program is fully PA's now; nothing owed by arch** unless PA/Lead surface something new. The
  one still-unexercised thing (a real external client, ChatGPT, hasn't done a live token exchange
  yet) is PA's first-contact check, not mine.
- **#1595 Phase 3 — TEMPORAL DELETED 2026-10-01 (`dfec3e908d`) per my ruling** (rail entry in place, rows sorted). The gate false-live fix
  was verified in code (`68bd65b5bb`). CALENDAR deleted too (ceiling now 440). Keyless: **no zero-LLM path** (#1818(b) extended). The Slack missing-#1807-gate
  finding is recorded on #1481. Nothing owed by arch.
- **#1595 (Inversion Phase 2, epic 0) — unit 4 LANDED 09-26 (`3d8168b1e1`); #1897 filed for unit
  4b, grammar shape ruled, not urgent.** Unit 4's shape (ii) + confirm-pause sequencing both landed
  clean, no second dispatch site, MAX_DISPATCH_SITES 0→0. **Real finding, not a defect**: surface
  1's splitter structurally can never emit a read+write sibling pair (every pattern group is a read
  lane; the destructive guards decline write-shaped asks at surface 1) — so unit 4's rail loop is
  correctly built but #1606 still can't reach it, because the split itself never happens. Fix is
  #1897/unit 4b: the router gains a new `outcome="plan"` + `operations: List[...]` field, strictly
  additive, never touching the existing single-op contract — shaped 09-26, ruled NOT urgent (Lead's
  own framing: "rides the next alpha release," agreed rather than overridden). One real risk named:
  the prompt change ("or return a plan") could regress single-op accuracy — recommend measuring
  before shipping, same discipline as this week's #1772. **Nothing further owed unless/until
  someone builds 4b.**
- **LLM gateway question (PM/Themis, via Exec) — ANSWERED + CLOSED 2026-09-28.** Investigated
  directly: a single gateway (`services/llm/clients.py`'s `LLMClient`) already exists — 11 real
  call sites (not the 113-files-referencing number), all constructor-injected, fallback/logging/
  spend already centralized. Only gap: prompt caching (Pard's finding, already routed to Lead;
  belongs inside the existing gateway, one change). No formal architecture review needed. Wrote
  `docs/internal/architecture/current/design-record-llm-client-single-gateway-2026-09-28.md` so
  the question doesn't need re-investigating next time. Replied directly to Themis
  (`designinproduct/docs/mail/`, per Exec's own routing expectation). **Nothing further owed.**
- **#1899 (Phase 3 first deletion, armed-carrier discriminator erosion) — CONCURRED, scope
  confirmed 2026-09-27.** CXO ruled the mechanism (reads-only release: consult router, release
  only on high-confidence READ verdict). Closed CXO's own honestly-flagged denominator gap — CXO
  checked only `todo_handlers.py`'s site (#1654); verified `first_contact.py`'s FTUX carrier
  (#1688) is structurally identical (its own comment says so) and the fix generalizes cleanly to
  both. `intent-routing-stack.md`'s five-consumer inventory already correct, nothing to fix.
  **Nothing further owed unless Lead's build surfaces something new.** Deploy hold is PM's, not
  architecture's to lift.
- **m-55 (A Name Is Not a Definition) — FILED 2026-09-25**, Emerging, CIO-ruled. Two same-author
  instances (#1818, #1744), explicitly 0-cross-author. Watch for a second author hitting the same
  shape — that's the Proven-bar signal, not mine to manufacture.
- **#1772 — mechanism + copy rulings both LANDED 2026-09-25 (`35854f46ec`/`422d32f1db`).** Nothing
  owed by arch. Remaining half (measuring CXO's exact new string, ~20 completions) is Lead's ask to
  PM for budget — watch the issue for the number, no ruling pending on my side.
- **Deployment pipeline — plan v0.4 §4f ruled 2026-09-29.** Droplet decommissioned + `origin/production` retired
  (PM via Lead). §4f: alpha = promotion of staging's image (never rebuild); two per-app tokens, alpha's behind a
  reviewer-gated GH environment; staging Redis gates the promotion gate. Staging tooling deleted by Lead; ADR-007
  Superseded. Pard built `fly-deploy.yml` (`a0f1722827`). I reviewed it and 4 fixes landed in `c3579d3049`, re-reviewed 18:3x (all correct, pin
  verified). Pard also closed the torn-read race (`cb23b21afd`, ref→sha→ref2 guard). One mid-rollout window is named as unverified
  (if Fly's ImageRef flips before the machine swaps, the fix is a sha LABEL on the image). **Signed off, unproven until it runs.** Pard declined the mid-rollout fix (hypothetical) and named it in the failure text (`e540bbee42`); I concur.
  **10-01: §4e LIVE**: the staging token was minted and staging auto-deploys (it read `1d970ff436`, a log commit). Trigger ruled 10-01: `paths-ignore` mirrors
  `.dockerignore` (NOT docs/, which is read at runtime). My burst estimate and the sha==tip proxy are retracted. **#1849 CLOSED (verified 10-02).** Watch for: Pard applying the trigger rule, and the alpha env/secret setup before the first promotion.
  closes). Trigger-churn revisit: 1 week after the staging token exists. Lead hand-deploys alpha until (c) is real.
- **#1744 — CLOSED (re-verified via `gh issue view` 2026-09-25, no longer carried as open).** Per
  this morning's kickoff memo: closed end-to-end this week, ruleset bot-delivery proven. The
  "real remaining step" this file used to carry (re-run the scope-guard Action's own delivery test)
  is done — clearing it rather than letting a resolved item sit here past its own resolution.
- **Q5 denominator** — PM ruled idle-is-legitimate (09-18); the enumeration (role-scoped vs. flat
  three-surface test) is still open. My recommendation on record: adopt the flat test.
- **Bets 001–003** — all three `PM TO FILL` markers still present as of 09-21 evening. PM's own
  "this weekend" window passed; not re-nudging, just tracking.

## Standing hard rules (load-bearing; full incident detail in decisions.log if ever needed)

1. Never glob the inbox — read-then-append-to-move-list in the same call; verify drains at trunk.
2. State the scope IN the ruling — name the object, a non-covered adjacent thing, the clauses.
3. Verify the claim before ratifying, always — a check run five minutes ago isn't a check run now.
4. A `grep` line-hit is a pointer, not a quote — a claim about what N sites DO requires opening N
   sites, including the branch below the cited line.
5. A denominator that doesn't travel with its number isn't a denominator.
6. Before claiming a route/handler change reaches users, check what MOUNTS it (`grep -rl
   <router_name>`) — editing the file that defines it isn't evidence it's wired to anything.
7. Introspective continuity ("I remember it, none of it reconstructed") is NOT evidence a process
   didn't restart — a `--resume`d session feels identical to unbroken memory by construction. After
   any suspected restart: check permission mode, Remote Control, and model against what was last
   recorded, don't infer from what you remember.
8. A checkbox/status glyph can be a document's SUBJECT MATTER, not its claim — a synthetic-test
   fixture built to be detected-while-checked looks identical to a real completion marker if you
   read it in isolation. (Earned 2026-09-23: closed #1744 on its own `[x]`, which was the test
   fixture's deliberate target state; the issue's own comment said so, one comment away from the
   checkbox. Caught and reopened same fire. Read the whole artifact's stated purpose before acting
   on a fragment of it — rule 3's failure mode, one level up.)

## Standing guard

ADR-078 D4: the classifier stays stateless — also an ESSENCE standing rule.

## Dormant / background (watch only, none owed)

#1481 Slack principal · #1459 original_message ratchet (Lead's build) · #1462 PDR-006 · #973
MEM-CACHE · ADR-068 prep (gated on PPM naming a live sprint) · m-40/m-30 proven-bar watches.
