# PA carry-forward (ephemeral session state)
_Updated 2026-06-10 ~18:30 PDT (BYO-key design converged; #358 revised; PPM/Lead memo sent; MIGRATION PREP)._

## 🔻 MIGRATION HANDOFF — read this first (successor brief)
**This session (Opus, modest-dhawan worktree) is being retired.** The successor is a **fresh Code session on
the DinP account (xian@designinproduct.com), Sonnet 4.6** — PA is the pioneer for the re-migration wave (CIO
drafts the next agent's handoff once yours lands clean). **You are a different model — don't assume you can
re-infer this session's context; this file + today's log are your ground truth.**

**Read in order**: (1) this carry-forward, (2) today's session log `dev/2026/06/10/2026-06-10-0712-pa-code-opus-log.md`,
(3) `dev/active/pa-bootstrap-brief-2026-06-10.md` (CIO-authored successor instructions — may land on origin/main
shortly after this; check for it), (4) the standing-items tracker `dev/active/pa-standing-items.md`.

**State at handoff**: inbox ZERO · everything on origin/main · **cron DELETED this session (per CIO handoff
step 3) — you must ARM a fresh windowed cron on your first turn** (`CronCreate "42 6,9,12,15,18,21 * * *"`, see
Re-arm ritual below). **Nothing is mid-flight** — every open item is PM-gated or awaiting another role.

### Top priorities for the successor (ordered)
1. **Arm the windowed cron first** (`42 6,9,12,15,18,21 * * *`) — session-only, dies with each session.
2. **Hold for PM** on the open decisions (don't push unprompted): the **3 braintrust questions** + the
   **#1162 open-questions discussion** + **#1185/#358 roadmap placement** (PPM/Lead memo is out, awaiting them).
3. **Watch for tester feedback** (Beatrice + new testers) — they unblocked at the 6/10 noon usage reset; none in
   yet as of handoff. If feedback arrives it's likely the first real PA-actionable item.
4. Routine duty-cycle: mail loop + discovered-work weekly sweep (next **Fri 6/12**) + advance unblocked low-pri.

### Gotchas the successor would otherwise rediscover the hard way
- **Mailbox writes go via the MAIN-WORKTREE BRIDGE** (`cd` to the main repo, NOT this worktree) — `check-branch.sh`
  hard-blocks mailbox commits on a feature branch. Non-mail (logs/docs) commit on the branch → `git push origin HEAD:main`.
- **main is busy** — `git push origin HEAD:main` often rejects; `git fetch && git merge origin/main --no-edit` then re-push. Verify landed: `git branch -r --contains HEAD | grep origin/main`.
- **EXPLICIT-PATHS-ONLY on every `git add`** (never `-A`/`.`); other agents' foreign files appear in the shared tree (e.g. stray files in `xian (ceo)/read/`) — stage only yours, verify with `git diff --cached --name-only`.
- **New files → write to the WORKTREE path** (`…/.claude/worktrees/modest-dhawan-9346b7/…`), not the bare main path (bare-path Writes land in the main checkout → worktree `git add` fails). [[feedback_write_new_files_to_worktree_path_in_model_a]]
- **Server restart**: strip inherited `ANTHROPIC_*` env vars (empty key shadows .env) — see CLAUDE.md banner.
- **Worktree stays modest-dhawan** until PM says otherwise (PM 6/9).

## Re-arm ritual — PILOT (Gap C partial mitigation, per CIO 6/7)
On **every turn the session gets** — session-start/resume, **each duty-cycle fire**, AND **sign-off** —
run `CronList`; if no PA duty cron, **re-arm it** (`CronCreate "42 6,9,12,15,18,21 * * *"` with the
duty-cycle-tick prompt — **WINDOWED expression, NOT the old `42 */3`**).

**⚠️ CRON EXPRESSION CHANGED 6/10 → windowed `42 6,9,12,15,18,21 * * *`** (live cron `56a2c4ee`).
PM-ratified (6/10): the deep-overnight dead zone ~midnight–4am has no fire at all — no overnight WATCH needed
"for us now" (a future all-night memo-sending agent isn't a thing yet). For the 3h cadence this drops exactly
the two midnight–4am no-op fires (old 00:42 + 03:42) at ZERO loss; keeps 06:42 START + 21:42 pre-hold check.
Came out of the cron-shape Day-7 memo to CIO (overnight fires = pure-cost no-ops). **Cohort-wide canonical
template change is CIO's lane** (PM+CIO doing the token-efficiency pass) — this is PA-lane adoption only. Agent-side re-arm only *reduces* the dark-window (it needs a live turn); the **Routines watchdog
is the cure** (CIO owns). Hook can't CronCreate (shell vs agent tool) → hook = prompt-to-agent, not actuator.
**Pilot data (6/7)**: Gap C recurred **~2×** in one day; both re-arms turn-triggered (AM=PM-prompt;
afternoon=**sign-off-checklist** caught it, agent-side, no human cron-prompt); the afternoon re-arm
survived a live session + fired (16:12 tick = re-arm durable within a live session). Reported to CIO
(`memo-pa-to-cio-...rearm-pilot-data-6-7...`). **Real test still pending**: an unprompted (no-turn)
compaction — expected to NOT self-heal (→ confirms watchdog-is-cure). Report when caught in the wild.

## Active threads (end of 6/7)
- **#1162 hosted alpha — LIVE + Desktop-test PASSED + package sent to Beatrice (first external tester).**
  `https://alpha.pipermorgan.ai` (Caddy TLS + LE + basic-auth; internals 127.0.0.1-only). Distribution
  bundle `byoc/dist/piper-morgan-alpha-DISTRIBUTION.zip` (gitignored) = installable plugin zip (bundled
  uv both mac arches + hosted gated URL) + INSTRUCTIONS.html + COVER-NOTE.md. Creds on box:
  `/opt/piper/alpha-credentials.txt`. **Awaiting Beatrice's feedback.**
- **Strategy captured (6 docs, dev/active)**: Option A (decouple credential — buildable now, zip proven),
  BYO-LLM-key beta scoping, plugin-marketplace-hosting research, hosted-distribution exploration,
  **BYO-substrate/Piper-as-colleague thesis** (+ deputize-host + proactive context-prep), install-AX
  findings (.mcpb+.skill one-click on Desktop-chat).
- **Braintrust CONVERGED + CLOSED** (6/9–6/10). All 5 lenses + **Exec's cross-lens synthesis** captured into
  the thesis doc (§"CONVERGENCE CLOSE"); all 8 memos triaged → pa/read/. **Convergence: composition-not-
  greenfield at 3 altitudes; methodology is the MOST defensible thin-layer; HOST's three-party "guest" reframe
  = the load-bearing insight; M5→v1.1 is a moat-defensibility cut.** **PDR-006 RESOLVED → ADR-068 only** (PPM
  ruled, Arch withdrew PDR-006). Sequencing locked (M3 none / M4 ADR-068 drafts / M5 beta w/o colleague mode /
  v1.1 generalization). CIO catalog closed (m-34 extended; ship-routine-keep-loop = corollary, not minted).
  **3 OPEN PM QUESTIONS** (Exec→PM, cc braintrust — PA surfaces, doesn't decide): (1) loop-defensibility as an
  explicit M5 gate? (2) ratify ADR-068-only/no-PDR-006 → unblocks Arch's M4 drafting? (3) HOST "guest"
  one-liner as external narrative (Comms)? **PA posture: thesis fully converged; doc is the durable capture;
  next action is PM's; nothing for PA to push unprompted.**
- **Skunkworks sprint dispositions (6/10, PM-directed)**: **#1157 CLOSED** (config-portable, server-owned
  config verified); **#1145 CLOSED** (thin-PoC rung-1 proven, PM-approved — epic; children carry forward rungs);
  **#1162 HELD OPEN** (hosted-distro — PM wants its open Qs discussed; they reduce to the same server-stored-vs-
  host-held fork as #1185); **#1185 INVESTIGATED + CONVERGED + memo'd** (below).
- **BYO-key (#1185) — DESIGN CONVERGED 6/10** (full report + capture: `dev/active/pa-1185-multi-tenant-byo-key-
  investigation-2026-06-10.md`). **4-rung chain**: BYO-host-side-inference (endgame) → BYO-key-passed (resilient)
  → server-stored-encrypted (beta rung = **#358**) → honest offer-to-configure (never shared-instance). Storage
  capability (whole user-secret set: LLM + integration keys) vs **need-scoped acquisition** (just-in-time);
  legibility required everywhere. **Key facts**: storage RETRIEVAL layer already exists
  (`UserAPIKeyService.retrieve_user_key`); secret is in **macOS keychain → doesn't exist on the Linux droplet**
  → **#358 (encrypt-at-rest) IS the server-stored rung, confirmed M5**. #1185 wiring gaps: LLM-client lifecycle
  (built once at init w/ instance key) + user_id threading + per-user hosted auth. **#358 REVISED 6/10** (stale
  Nov-2025 claims corrected — `encryption.py` doesn't exist; + hosted/multi-tenant requirement added). **PPM/Lead
  memo SENT** (build-sequencing: #358 floor → #1185 wiring; asks PPM roadmap-placement of #1185, Lead build-order).
  **Next action is PM/PPM/Lead's** — nothing for PA to push unprompted. Alpha rides shared key meanwhile.
- **durable-cron**: CIO owns Routines watchdog ($70/mo PM-gated); PA pilots re-arm. **New 6/9 data**: cron
  store **non-deterministic across resumes — vanish AND reappear** (found a "dead" cron resurrected on
  resume + deduped). For next CIO touch.
- **Pending PM / awaiting**: the 3 braintrust open-questions above; rotate Rackspace creds (PM holding 6/9);
  Beatrice + a few NEW testers' feedback — **blocked till Wed-noon usage reset (TODAY)** (shared key hit usage
  limit; re-check / nudge after noon); file host-vs-Piper connector-gap insight?; fold OAuth-connector
  refinement when we discuss; **worktree stays modest-dhawan** until main-account migration (PM 6/9).
- **PM on other Anthropic account** until **Wed-noon usage reset (TODAY 6/10)** — testers unblock then.
- **Session-log discipline note (6/10)**: this continuous session ran 6/9 session-log-primary (no cycle log);
  the morning START self-healed 6/9's missing DAY-CLOSED (retroactive close: day-arc + memory-eval + sign-off
  + marker), then created the 6/10 log. Step-0 self-heal worked as designed. **Disclosed to CIO** as a practice
  variation (see active-practices register memo 6/10) — successor's call whether to resume strict dual-surface.

## Recent learnings / patterns absorbed this session (6/9–6/10)
- **Windowed cron > quiet-hold-fire** where no overnight WATCH is needed: don't-fire beats fire-and-quiet-hold
  (overnight fires were pure-cost no-ops). PM-ratified; PA-lane adopted; cohort-wide template change is CIO's.
- **Active-practices register → CIO** (PM-prompted): keep CIO's view of PA's experimental practices consolidated,
  not scattered. Disclosed session-log-primary as a previously-unflagged drift (even safe drift must be visible).
- **Close-properly + anti-over-close** (recurring-miss area): close only the unambiguous (#1157); present epic /
  open-PM-Q closes to PM (#1145 epic closed only on explicit PM approval; #1162 held for PM). Evidence comment
  BEFORE `gh close`, every time.
- **Verify-before-asserting paid off twice**: #1185 investigation found the storage layer already exists; the
  #358 review found its "current state" was materially stale (`encryption.py` doesn't exist) — both only via
  reading the actual code, not memory. Same discipline as [[feedback_investigate_before_extending_all_work]].
- **Braintrust process = the thesis it evaluated** (logged as pattern/story material in the 6/9 log Observations):
  methodology↔product flywheel; value from friction not affirmation; moat = the living loop.
- Pins newly load-bearing this session (all in MEMORY.md): pre-authorized-for-unblocked-work; pending-PM-Q-
  doesn't-block-other-work; make-promises-durable (the cron change → durable in carry-forward + cron-shape doc).

## Mailbox state summary (at handoff)
- **Inbox: ZERO** (28-item CC-awareness backlog triaged to read/ at the 16:28 fire).
- **Recent PA sends (6/9–6/10)**, all on origin/main: braintrust-input memo (→ converged); cron-shape Day-7
  memo → CIO; active-practices register → CIO; BYO-key build-sequencing memo → PPM/Lead (cc PM); rollup-surfacing
  reply → Exec. **Awaiting replies**: PPM/Lead on the BYO-key memo (roadmap placement + build order).
- **Nothing owed by PA in the inbox.** Open cross-role waits live in "Pending external" of `pa-standing-items.md`.

## Cron
- **DELETED at migration handoff** (6/10 eve, per CIO handoff step 3 — don't leave armed in the retired
  session). The successor **arms fresh** on its first turn: `CronCreate "42 6,9,12,15,18,21 * * *"` (WINDOWED —
  no midnight–4am fire; fires 06:42→21:42; session-only, `durable:true` is a no-op in this env).
- History: was `56a2c4ee` (windowed), swapped from `78832b49`/`42 */3` at the 13:12 fire 6/10 per PM's
  ratification of the overnight-no-op-fire fix.
