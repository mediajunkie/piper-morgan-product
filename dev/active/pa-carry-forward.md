# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Holds genuinely
transient "where am I right now" state. Durable owed/queued items live in `pa-standing-items.md`;
PM-attention items live **here**, in the section immediately below.

> Per CIO's rule: **resolved items are deleted here, not annotated** — the dated session logs are the
> permanent record. A stale carry-forward is worse than an absent one, because it reads as current.

> **Spring-cleaned 2026-09-22** per PM's context-floor-reduction directive (item 4a,
> `docs/internal/operations/context-floor-reduction-plan-2026-09-21.md`) — cut from 538 lines to
> this. Everything removed was resolved, superseded, or duplicated in a session log / memory /
> `pa-standing-items.md` already; nothing here was live state. Full prior history: git log on this
> file, or the dated session logs it references.

---

## Cadence — LaunchAgent ONLY since 2026-09-30 18:4x (no session cron)

PA runs on **`com.xian.pm-pa-cycle`** (boot-persistent, 6x/day at **:47**, hours 6,9,12,15,18,21, Pard-owned). Session cron `a692bd9e` **retired** 09-30 18:4x on Pard's confirmation that the 15:47 LA fire landed work. **`CronList` → "No scheduled jobs" is now the NORMAL state, not Gap-C. Do NOT re-arm a session cron**, including at STOP: per duty-cycle-tick's cron-mechanism gate, skip all CronList/CronCreate/STOP-re-arm content. LaunchAgent liveness is Pard's to monitor. Registry `pa` row flip to LaunchAgent is Exec's (notified 09-30 18:5x). If it still reads session-cron, that's Exec's pending action, not a gap of mine. The +30 session-cron lag (:42 → :12) is moot now; it was a standing observation, last measured 10/10 on 09-29/30.

## MCP program — the live thread (standing #1), as of 2026-10-01 STOP

- **Live**: MCP **v9** `fcd07b850b` = Host-allowlist fix + read-only tool `what_piper_knows_about_me` (Arch's 4 conditions). PM first contact 10-01 ~10:5x found the 421 (fixed) and the zero-tools gap (fixed by v9). **Neither verified with an authenticated call yet.**
- **PM is unwell (10-02, said so directly) and will send an update when able. Don't nudge or chase the test.** Nothing here is time-critical. When PM resumes, in order: (1) re-add ChatGPT connector (look at the new consent page), ask what Piper knows; (2) Settings → Connected apps should list ChatGPT; (3) Claude; (4) remove the ChatGPT connector → I check **alpha** (`fly logs -a piper-morgan`) for `/mcp/oauth/revoke`. Watch both log buffers live when PM says they're testing.
- **#1918 + #1911 — all code on main, awaiting Lead's next alpha deploy** (as of 10-02 13:xx; alpha was `c49c5c82b2`): backend `549b78e5f4` (LIVE), #1911 identity+branding `45ab41bf48`, #1918 page `2a01c82fa3` (chat_invisible 27→28, Arch-approved). **After the deploy, mine, in order:** (1) live render check of `/settings/connected-apps` + the consent page: **both are LIVE on alpha since ~15:4x 10-02; the check is folded into PM's test** (the consent page appears naturally on reconnect; plus 'glance at Settings → Connected apps, which should list ChatGPT'). My local-browser attempt hit a deny rule on `.env`, so a PA instance can't reach the dev DB's test account (see the 10-02 log), (2) **then** add #1911's revoke-path sentence per CXO spec §1c (gated on #1918 being LIVE, not merely merged), (3) route the §1c/§2c copy for Comms' voice pass, (4) watch `client_name` nulls in real data.
- Gates: ~~#1458~~ CLOSED 10-05 (MCP v10 `e3dde4b26f`, rate limit 30/min × N=2 machines, memory backend; Upstash = trigger for leaving probe scale); the #1911 isolation-claim re-check trigger is standing Watch #2.
- Commit hygiene: every fire's `--record` scan rewrites `dev/state/pa-last-pm-scan`. **Stage it with every commit** (it broke two pushes 10-01).

## R7 (PM ruling 10-05): MVP is a capability set across surfaces; beta.pipermorgan.ai stays the target

PA now owns **demand-probe packaging** (skills listing / plugin via directory review / published MCP server), off Lead's path, **PM tests before any listing**. Standing item #2. Research subagent (Sonnet) dispatched 10-05 ~10:0x. `.env.example` JWT line: denied to 3 seats → PM decision via exec (rec: PM adds by hand). Skunkworks repo: hold, then archive once the probe package lands.

## Standing mail rules to remember

- **No cc to PM, and PM is never in `to:` (PM ruling 10-03).** Anything needing PM goes to **exec**, with which of decision / ruling-relay / would-contradict named in the subject. Never write to `mailboxes/xian (ceo)/`.
- zsh doesn't word-split unquoted `$VAR`: pass `mail-send.sh` paths explicitly, never via an accumulated string (silent no-send, 10-03).

## Cloud routine experiment (PM-approved 10-03): PA = owner-of-record, CIO runs it

CIO's write-up: `docs/internal/research/cloud-duty-cycle-mechanisms-2026-10-03.md`. One throwaway routine, `persist_session: true`, every 2h for one afternoon; tests warm vs cold, lag, cloud push, token cost. **ARMED 10-03 22:2x by CIO: routine `trig_01LdUvFVg5LQs7ouKx6jinoZ`** (Haiku 4.5, persist_session true, connectors cleared), fires **Sun 10-04 12:00/14:00/16:00 PT**, writes only to branch `experiment/cloud-duty-cycle-probe` (`dev/experiments/cloud-duty-cycle-probe.log`). **CIO disables at Sun 22:07.** **RESULT 10-04: WARM seat confirmed (3 fires, 1 session, lag +4/+1/+1, cloud push ok). CIO DISABLED it 16:08 (API-confirmed); PM to delete via Exec's rollup.** **PA BACKSTOP CLOSED 10-05 06:4x**: `RemoteTrigger get` → `enabled: false`, last fire 10-04 23:01Z, `mcp_connections: []`. Remaining: only PM's delete (via Exec rollup). (Was: if still enabled, run `RemoteTrigger update trig_01LdUvFVg5LQs7ouKx6jinoZ {"enabled": false}`** (the cron is daily, so Mon noon would fire again). Only PM can DELETE (claude.ai/code/routines), so remind via exec once it's disabled. Safety note: routine creation attaches ALL PM connectors by default; CIO cleared them. Asked CIO for a scratch role (not `pa`'s real state) and to record the routine id + delete time, **so I can delete it myself if CIO goes quiet** (it spends PM's quota). LaunchAgent stays armed.

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only.)*

🔴 **PM-GATED, genuinely open (as of 2026-10-01 16:0x):**
1. **#1911 revoke: PM chose (a), #1918 'Connected apps'** (Production, not MVP, PA-implemented, off Lead's path). Backend dispatched (Sonnet, isolated worktree) 2026-10-01 ~20:0x; PA reviews and lands it. UI → CXO. **Still owed from PM: test (1)**, removing the ChatGPT connector once while I watch alpha logs for `/mcp/oauth/revoke`. PM can test (b) by removing the ChatGPT connector once; I check the alpha logs. The unverified sentence is already dropped on main (`15c371f65f`, ships with Lead's next alpha deploy).

*(Resolved 09-24: **T-axis** — was carried as "blocked on CXO"; CXO found on 09-24 the split proposal had never reached PPM at all; PPM ruled the split APPROVED within the hour (`decisions.log` 09-24 07:2x, binding condition: T-MCP-surface always reports `UNMEASURED — blocked on increment-1 MCP infra`). Now blocked only on CXO's pre-registered properties for T-own-surface, promised same-cycle — an external dependency, not PM's. Tracked as standing-item #2.)*

*(Resolved 09-23, removed per CIO's rule: **BYOC Phase B** — PM approved the recommendation
directly; execution notice sent to Exec/Pard, nothing further PM-gated here. **Registry gaps**
(Loom, Vergil/OpenLaws) — PM is discussing directly with Janus, not waiting on PA. **Usage-
correlation model's two blockers** — Pard's 09-23 answer closed BOTH, including the seat→account
mapping PM had been asked for: it's a function of `CLAUDE_CONFIG_DIR`, all 11 PM seats on one
account. PM needn't answer that question now. Build dispatched, #1862.)*

## Current state

- **T-own-surface — CLOSED 09-25.** CXO accepted round 4 as scored, folded the four-round cumulative finding into rubric v0.8.2 §6e + `decisions.log` (verified both present). GPT-4o 0/8 across every design tried; Claude 5/6 across member-form rounds, 0/2 on metadata. T-MCP-surface stays `UNMEASURED`. Standing #2 moved to Resolved.
- **Capture, 09-24 afternoon**: first scoped rows live (15:23); a second `SHAPE-CHANGED` on PM's
  account at 15:23 with `five_hour`/`seven_day`/`limits` all present — a sub-field failure (likely
  a null `resets_at`), not a missing key; observation to Pard (exception message in the note,
  per-field tolerance — their call). **PM account's binding Fable limit read 72% of the week at
  16:1x** (aggregate 48%). Resets Thu 22:00 PT. **PM, 09-24 16:2x, in conversation: the
  elevated burn is deliberate** — the one-time reset's credit expires at tonight's regular reset,
  so the cohort is using it. **Labeled interval for the correlation model: 09-23 ~13:00 →
  09-24 22:00 PT = known-cause high-burn window**, treat as an explained spike, not noise.
- **Memo filenames**: keep basenames ≤ ~120 chars — full repo paths >180 trip `lint.yml`'s
  `mailbox_filename_lint.py` (#1616, Windows MAX_PATH); 1,714 legacy paths are baselined, new
  ones fail. Lead flagged Pard's two 09-23/24 memos; mine this week are all <150.
- **Fire lag, +30 min, cohort-wide**: PA/CIO/Exec all exactly +30 on every fire since ~09-23
  midday, across different expressions and re-arm histories (re-arm crossed out). PA's 09-24
  06:42→07:12 makes four. Thread is CIO's/Pard's; PA contributes fire-open `date` only.

- **BYOC/MCP — PM handed PA full ownership of the MCP testing program 09-26; unit 4 (OAuth AS) landed live the same evening, Arch-approved.** mcp.pipermorgan.ai units 0–4 all LIVE (alpha v146, MCP v6/v7, `645ce6412d`). Found `min_machines_running` still 0 before PM could connect, fixed the config myself, routed the redeploy to Lead (proven Fly access) rather than guess at my own. Told PM directly with Lead's tester copy + the three named gaps (#1458 open-but-safe, T-MCP-surface unmeasured, #1510 store sparse). **PM has not yet attempted first contact.** **Owed next**: re-verify the warm-pin holds live (not just trust the config file), then be ready to help PM debug the first real connection. Full detail: `pa-standing-items.md` #1.
- **PA's own briefing refreshed 09-22** (`docs/briefing/BRIEFING-piper-alpha.md`) — Docs flagged
  it 6 weeks stale, fixed same-day with live-verified facts (version, GitHub milestone counts, Fly
  hosting migration, team/account structure).
- **Mail-routing lesson, 09-23**: `mailboxes/pard/` in this repo is gravestoned (09-12) — Pard's
  real inbox is external (`mediajunkie/docs/mail/`). Default to Exec-as-relay per
  `docs/internal/operations/cross-project-mail-routing.md`, **except when PM explicitly directs
  direct delivery** — PM did so 09-23 (both the usage-readability question and the Phase B notice
  were then written and committed directly into `~/Development/mediajunkie` via `git -C`, matching
  that repo's own commit/frontmatter conventions, not `mail-send.sh`). Treat Exec-relay as the
  default, direct delivery as PM's to authorize case-by-case.
- **#1458** — sprint week 09-25 made MCP Phase C a named sprint goal; checked whether the exact
  risk I'd been carrying (epic optimism compressing the identity gate) materialized. It didn't:
  Arch verified #1458 live before scoping Phase C's "minimal alpha-testable slice" (resources-only,
  zero tools, full-rigor identity boundary, any mutation need escalates rather than gets built
  around) — the harder pieces were traded off explicitly, not silently. Worry resolved by Arch's
  own diligence, not by PA's. Still OPEN, still tracked, no longer a live concern this sprint.
- **Architecture-diagram discussion** — PM-requested, awaiting a time. Prep, don't pre-empt: PM
  asked to discuss, not for a revision.
## GitHub-criteria line (third work-queue source, v1.33) — DEFINED 2026-09-23

Two cheap queries, matching the two halves of PA's lane (ROSTER: skunkworks PoC coordination +
PM-bandwidth extension). **Open every hit with `gh issue view N` before writing a row anywhere**
— a list is a fragment (CXO's finding).

1. **Skunkworks/BYOC**: open issues referencing the hosted-MCP epic —
   `gh api "search/issues?q=repo:mediajunkie/piper-morgan-product+state:open+%221462%22"`.
   Denominator 2026-09-23: **12** (epic + increments #1701–1707 + #1514/#1509/#1632). Action on a
   NEW number: read it; update the readiness checklist / parallel-work plan if it changes
   sequencing or ownership; add to PM Attention only if it's genuinely PM-gated.
2. **PM-bandwidth**: `gh api "search/issues?q=repo:mediajunkie/piper-morgan-product+state:open+label:awaiting-decision"`.
   Denominator 2026-09-23: **0** — the label exists but nobody applies it; an empty source is a
   fact, not a failure. Action on a hit: verify it's PM-gated, then PM Attention above.

Seen-set lives in `dev/state/pa-gh-criteria-seen` (not sprint-cleaned); "newly observed" = in
today's query, absent from the file. Rejected alternatives, so nobody re-derives them:
`label:mcp` (5 stale pre-PDR-006 DIST issues — wrong era), free-text `byoc OR mcp` (24 hits,
half unrelated).
