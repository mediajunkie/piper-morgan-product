# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Holds genuinely
transient "where am I right now" state. Durable owed/queued items live in `pa-standing-items.md`;
PM-attention items live **here**, in the section immediately below.

> Per CIO's rule: **resolved items are deleted here, not annotated** — the dated session logs are the
> permanent record. A stale carry-forward is worse than an absent one, because it reads as current.

---

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only — rewritten 2026-08-04 fire 3.)*

**Beta target: MOVED BACK A MONTH from 2026-08-09** (PM, 08-08 10:10 PT, in-conversation with Lead,
verbatim: *"I am going to move the beta date back a month. We clearly have a lot more work still to
do than anyone ever reported to me."* — `decisions.log:1242`). No new fixed date recorded as of this
fire; 08-08's Fundamentals-First ruling governs the moved-beta month's priority order
(Understanding-Layer Inversion first, surface polish deferred). The 08-09 line this replaced was two
days stale.

- ⏱️ **TEN SECONDS: open `https://pipermorgan.ai/privacy` in a browser** and say whether a real policy
  renders. URL returns **200**; **server-rendered text is 29 characters.** Undecidable from this
  session (see correction below); matters because Anthropic rejects *"missing or incomplete"* policies
  and review may fetch without JS.
- 🟢 **CORRECTED 08-29 — the 08-13 "no browser at all" diagnosis was wrong in a specific, now-understood
  way, not just stale.** Exec found `.mcp.json`'s `chrome-devtools` server pointed at
  `/Applications/Google Chrome.app/...`, which doesn't exist on Amber — that's a **misconfigured path**,
  not an absent browser. A real, working Chrome (Playwright's Chrome for Testing) was on disk the whole
  time; the tool just couldn't find it. Exec repointed the config. **Tested live rather than assumed
  fixed**: my own session still fails with the exact old broken path in the error — the `.mcp.json` edit
  is correct on disk but doesn't reach an already-running session's MCP subprocess. Reported to CIO/Exec
  (`mailboxes/pa/sent/pa-to-cio-cc-exec-pm-chrome-devtools-fix-not-live-in-running-sessions-2026-08-29.md`)
  so "still fails today" isn't misread as the fix not working. **Retested 08-30 — still the old path,
  same exact error.** Corrected my own framing: "next fresh session start" does NOT mean the next
  duty-cycle fire or the next calendar day — this whole multi-day conversation is one continuous
  Claude Code process, so every fire so far has shared the same pre-fix MCP subprocess. Only an actual
  process restart (a genuine new session, not a new fire within this one) will pick up the config.
  Not self-triggerable or predictable from in here — just retest opportunistically whenever a real
  restart happens, and don't re-report "still fails" as new information unless something changes.
  ⚠️ Exec separately flagged the fix is fragile anyway (version-pinned to a rotating Playwright
  directory) — CIO owns that residual, not PA.
- ✅ **RESOLVED 08-30 — plugin manifest `license`**: `Apache-2.0`, decided 2026-08-13 (commit
  `a4547d7c4`), reached PA only today via Exec's finding that a two-week-old decision never got
  routed to the artifact carrying it as `TBD`. Copyright holder confirmed PM-ruled 08-29: Christian
  Crumlish. Updated `dev/active/plugin-manifest-draft-2026-08-05.md` directly (not just this note) —
  the manifest's `license` field, its "Open, and not mine to decide" section, and its next-steps list
  all now reflect the resolved state, plus PM's own rationale (Apache's patent grant + trademark
  carve-out, real protection is trademark + `docs/legal/values.md`, not the license itself) so a
  future reader doesn't have to re-derive it from the adoption commit.
- 🔴 **BYOC/conversational-layer conversation — 08-26 positions all landed; 08-27 continued live with
  PM on connector architecture. Thread STILL PAUSED, not closed — no explicit wrap either day.** Full
  08-26 detail: `dev/2026/08/26/2026-08-26-0712-pa-code-log.md`. Condensed status:
  - **Positions 1-3 (BYOC sequencing, Radar/Files first-party, freeze multi-provider LLM)**: all
    ACCEPTED 08-26, unchanged since. Position 1's PPM-coordination condition **discharged 08-27**
    (#829/#1462 reconciliation, PPM closed #829 same-day — see below).
  - **⭐ "No optional complexity" — NAMED PRINCIPLE, now recorded in `decisions.log` (2026-08-27
    entry) and given a standing-lens proposal**:
    `docs/internal/product/no-optional-complexity-standing-lens-proposal-2026-08-27.md`. Two layers:
    (1) does a proven single case justify this scope item at all — the original 08-26 connector-gate
    audit; (2) NEW 08-27 — does an implementation's SHAPE actually match its claimed architecture, or
    does it just look aligned. Layer 2 came from PM's own 08-27 follow-up push on connector strategy.
  - **Connector architecture — VERIFIED, not just discussed, 08-27**: GitHub, Slack, Notion all now
    ship official vendor-hosted remote MCP servers (`api.githubcopilot.com/mcp/`, `mcp.slack.com/mcp`
    GA 2026-02-17, `mcp.notion.com/mcp`) — PM's "other products don't agonize like this" instinct is
    correct and verifiable. Checked Piper's own `services/mcp/consumer/` adapters against it:
    `github_adapter.py` is mostly real MCP (8 live `call_tool()` sites) but talks to a **self-hosted**
    `github-mcp-server` instance rather than GitHub's own official endpoint (a config-level
    simplification candidate per ADR-070's own server-ref resolver — flagged to Lead/Arch, not decided
    here). `slack_adapter.py` and `notion_adapter.py` are connector-**contract shims with ZERO real
    MCP calls** underneath (grep-verified) — all actual data ops are bespoke REST, same shim shape as
    Calendar. PM's fear about "hack-ish prototyping" is confirmed for 3 of 4 connectors, not all 4.
  - **Connector-gate audit (08-26) + PM's live follow-up (08-27) — still not PM's final call**:
    GitHub — hard requirement, no argument. **Slack — PA's recommendation: Fast Follow** (weakest
    architecture fit of all four *and* already excluded from CXO's ratified FTUX set *and* already
    fail-closed since #1481/#1484 — three independent reasons, not one). Notion — keep in Production
    as-is; ripping it out for architectural purity now would be the same scope-creep instinct in
    reverse. Calendar — still genuinely uncertain, a Lead/PPM usage-data question.
    **PM said "I'll decide re connectors" — this is a recommendation on the table, not a settled
    answer. Don't presume the outcome in future work.**
  - **Backlog audit (08-26)**: read all 60 open MVP-milestone issues directly. Pattern barely shows up
    as individual tickets — one live instance found and now resolved (#1572, see below). #1522 (PM's
    existing false-trails/dead-code audit) stays a distinct failure mode (accidental vs. deliberate-
    premature-breadth) — cross-referenced in its comments 08-27, not merged.
  - **Owed items, ALL FOUR NOW EXECUTED as of 08-27**:
    1. ✅ **#829/#1462 PPM reconciliation** — PPM closed #829 same-day, independently re-verified
       against PDR-006's own text, found a second signal (child #829 outranking parent epic #828's
       Fast Follow milestone). Nothing further owed.
    2. ✅ **Diagram content fixes + rev2** — `dev/active/pdr-006-architecture-2026-08-10-rev1.html`:
       surface-primacy correction moved to `decisions.log`, ChatGPT capability chip updated (Agent
       Plugins 1.0.0), plus **rev2 added 08-27**: a BYOC-sequencing section (Position 1's phrasing +
       the #829 discharge) and a "Connector shims vs. real MCP" section encoding the verified finding
       above, explicitly marked as pending PM's connector-milestone call, not settled. Republished to
       the same artifact URL, favicon 🏗️ (unchanged from 08-27's first republish).
    3. ✅ **#1572 rescoped** — decoupled the Slack-tz-capture half (the one live "premature breadth"
       instance from the backlog audit) from the real, unconditional browser-tz-at-login bug fix.
       Title + a full comment explain the split; Slack-tz tracked as a future issue once the milestone
       call lands, not silently orphaned.
    4. ✅ **#1522 updated** — added a cross-reference comment naming the connector-shim finding as a
       related-but-distinct failure mode from that issue's own scope (accidental complexity).
  - **RATIFIED 2026-08-27 (same day, later in the conversation): "I approve your recommendations."**
    Slack → Fast Follow, confirmed. Executed immediately, not left as a ruling sitting in chat:
    Production milestone (#9) description updated (three connectors: GitHub/Calendar/Notion); epic
    #1440 retitled + commented with full rationale; five Slack-specific Production issues moved to
    Fast Follow (#1364, #1481, #1500, #1503, #1497); #1514 (spans all four connectors) left in
    Production with a scope note rather than moved wholesale; #1572's Slack-tz half filed as new
    issue **#1686** (Fast Follow) now that the milestone call is final. **Loop-in memo sent to PPM,
    CXO, Arch (cc PM)** per PM's direct ask —
    `mailboxes/pa/sent/pa-to-ppm-cxo-arch-cc-pm-slack-descoped-connector-architecture-2026-08-27.md`
    — one open question per recipient (PPM: roadmap coherence, same shape as #829; CXO: pure
    confirmation against their already-ratified FTUX exclusion; Arch: the GitHub self-hosted-vs-
    vendor-hosted `github-mcp-server` config question, flagged not decided).
  - **CXO replied 08-27 evening — confirmed, one nuance, no action needed**: Slack was already outside
    the ratified F-Integrations set (GitHub/Calendar/Notion), so the gate catching up is convergence
    not conflict. One thing worth keeping in mind, not an edit: the taxonomy's §4 rule ("re-evaluate
    Slack cells as a batch if #1481 clears") still holds, but its trigger moved further out now that
    #1481 is Fast Follow rather than Production. PPM and Arch haven't replied yet as of 08-28 morning —
    nothing to chase.
  - **PM corrected the gap-cause 08-28 morning**: not "machine-asleep" (the watchdog's inference) —
    "the entire team hit the weekly rate limit yesterday afternoon around 2:00pm... reset until
    10:00pm... a known issue, a fairly good maxing out of available resources across the length of a
    week." Fully accounts for PA's own gap; corrected in the 08-27/08-28 session logs; saved as
    standing memory (`project_weekly_rate_limit_outage_pattern`) so future gap-diagnosis doesn't
    re-derive this.
  - **PM restated PA's role vs. Exec vs. PPM, 2026-08-28** (unprompted, "it's been a while since I
    restated that"): PA is *"a close product apprentice focused on the product"* — hands-on product
    thinking with PM directly, helping set the bar for what Piper should do and what makes Piper
    *Piper*. Exec is the broad coordination/proxy surface; PPM holds actual product-management
    decision authority (*"my agentic proxy leadership role in charge of the product lens"*). Overlap
    is deliberate, not a bug — *"we use it well to triangulate and debate our way to good
    solutions."* Saved as standing memory (`feedback_pa_role_vs_exec_vs_ppm`) since this kind of
    clarification is easy to let drift again.
  - **PM confirmed BYOC is explicitly PA's to drive** as it moves from skunkworks to primary roadmap.
    Also previewed (NOT started) a next topic: shipping small, useful product pieces on a tighter
    cycle, MVP-thinking applied harder, Skills as the precedent — motivated by PM's own *"I'm envious
    of people who have been continuously shipping... building a ship in the bottle with almost no
    users."* Explicitly PM's call when to start, not a deadline — PA gave an honest readiness read
    (current in-flight load is light, ready when PM is). Saved as standing memory
    (`project_byoc_pa_driving_and_shipping_small_things_preview`) so this doesn't get lost if the
    conversation gap widens before it starts.
  - **Direct validation of the standing-lens proposal, 08-28 — now twice in one day**: CXO applied the
    "no-optional-complexity" lens (named 08-26, credited explicitly as "PA's/PM's lens") as the FIRST
    move on FTUX surface mapping, not a trim-after-the-fact — cut ~40 speculative cells to 2 live ones
    plus one real gap (`docs/internal/design/ftux-surface-mapping-2026-08-28.md`). PPM then answered
    CXO's §5 consult using **the same core-list test from this week's MVP triage cut** — filed the
    empty-state interview as its own MVP issue (#1688) on the reasoning that it's an honesty-discipline
    extension of #1536's own AC3, not "differentiator work getting a pass by default." Both cc'd to
    PA, no action needed — just a good outcome worth having on record: the lens is compounding across
    roles, not a one-off.
  - 🟢 **CONNECTORS.md v1 (living core doc #5), 08-30 — PA's 08-27 connector-reality finding is now
    permanent, cited architecture, and this diagram artifact is superseded on connector status
    specifically.** Arch authored, Lead maintains going forward
    (`docs/internal/architecture/CONNECTORS.md`). The Slack row's governing-decisions cell cites
    **"PA's 08-27 connector-reality finding"** by name alongside #1481/#1484 and the descope memo
    trail. The table formalizes exactly what PA found (GitHub real MCP, Notion/Calendar honest
    shims, Slack dead/descoped) plus ESSENCE's standing test (backend holds a grant only for
    no-user-present work) as a per-connector, actively-maintained source of truth — not something
    PA needs to keep parallel-maintaining in `dev/active/pdr-006-architecture-2026-08-10-rev1.html`.
    **Going forward: point anyone asking about connector status to CONNECTORS.md, not PA's diagram**
    — the diagram did its job (surfaced the finding, drove the Slack descope) and that job is now
    done; no need to keep it current on this specific axis. Also codifies a rule directly downstream
    of CXO's #1463 trace: *"hedges ride the payload, not a prompt"* for the MCP tool layer.
  - **Arch replied 08-28 evening — architecture read confirmed, thread now fully closed**: investigated
    independently (checked the code AND looked up GitHub's actual hosted-endpoint contract) rather than
    just accept PA's framing. Confirmed config-level per ADR-070 Amendment A's own design — no ADR
    amendment, no resolver rewrite needed — and confirmed the tool-name coupling holds across a swap
    (GitHub's hosted endpoint is built using the OSS `github-mcp-server` as a library, same tool
    contract). **Two real, non-architectural gates found that PA's original flag hadn't surfaced**:
    (1) GitHub's hosted endpoint requires the authenticating user hold a Copilot license — enforced at
    GitHub's edge, not config-tunable, so a global default flip would silently fail for any user
    without a seat; (2) whether Piper's stored OAuth grant scopes are valid against the hosted endpoint
    is unverified — needs an empirical connect-and-call test, not just docs-reading. Net ruling:
    architecturally sound, not yet a safe default flip; routed the actual rollout call to PPM (whether
    it's worth pursuing given the licensing gate narrows who benefits) rather than deciding it
    unilaterally. Not blocking anything. **PPM now owns that follow-on question, not PA.**
  - **PM ruled 08-29 — final answer, question fully closed**: *"nice catch. I don't want to limit it
    to Copilot licensees if we don't have to."* Piper stays on self-hosted `github-mcp-server`; the
    hosted-endpoint flip is rejected on the licensing gate alone, not a technical barrier — Arch's
    "it's config-level and cheap if economics change" finding is explicitly preserved for a future
    revisit, not discarded with the decision. Second-order effect: the OAuth-scope empirical test
    (Arch's gate 2) comes off the critical path entirely, since it was only needed to de-risk a flip
    that isn't happening. Nothing owed by PA, PPM, or Arch on this going forward.
  - **Thread status — genuinely fully resolved as of 08-28 evening**: all three loop-in recipients
    (CXO, PPM, Arch) have now responded; every question raised in the 08-27 memo has a home.
  - 🔴 **MAJOR NEW CONTEXT, 08-29 — ESSENCE.md v0.1 is now the fixed point for the next BYOC
    conversation with PM.** PM+Arch ran a full "Architectural Review 2026" (9 discovery legs, a
    docs-blind 491-module census, clean-room paper-rebuild test) and PM ratified a genuinely
    load-bearing set of decisions same-day (`docs/internal/architecture/ESSENCE.md`,
    `docs/internal/architecture/reviews/2026-08-architectural-review/`). Arch's cohort-wide
    broadcast explicitly named PA: *"no action owed. PA — the BYOC convergence discussion you're
    steering with PM now has the essence doc as its fixed point."*
    - **All NEW build effort goes to the MCP/BYOC path, effective now** — not a future fork per
      08-26's "one track that forks once the shared foundation is done," but the live sequencing
      decision as of today. **Web-chat is explicitly in maintenance mode**: bugs fixed, nothing new
      built. This is an acceleration/sharpening of Position 1, not a contradiction of it.
    - **A new, sharper connector rule** (ESSENCE commitment #6): *"Piper's backend holds a grant
      only where it must act without the user present (standup generation, background reflection,
      document mirroring); in-conversation reads of third-party services belong to the host's own
      connectors."* This is a more precise successor to the 08-27 shim-vs-real-MCP finding — it
      suggests Piper shouldn't be building its own in-conversation connector reads at all in the
      target architecture, only holding grants for background/no-user-present work. Worth bringing
      into the next BYOC conversation explicitly, not just filed away.
    - **Connector status list matches PA's own 08-27 finding almost verbatim**, now official: GitHub
      real MCP (load-bearing); Calendar honest SDK shim; Notion REST, held grant now governed by
      **Bet 003** (the new scope-bet-gate mechanism — a named, PM-ratified justification, not just
      "cheap to maintain"); **Slack descoped to Fast Follow, adapter dead** — exactly PA's
      recommendation, now load-bearing architecture doc language.
    - **Not PA's to act on** — none of the four reorientation workstreams (Socialize/Docs-reform/
      Code/presumably a fourth) name PA as owner; CXO+PPM are the "directional trifecta" who must
      read-and-respond on ESSENCE by Wed 09-02, not PA. PA's job is to bring this into the next BYOC
      conversation with PM as context, not to execute on the review itself.
  - ✅ **RESOLVED 08-30, caught stale 09-08 — the milestone/beta-definition question (PPM's reading a
    vs. b) was decision (2) of the same-day ESSENCE ratification, not left open.** Sat in this file as
    "still awaiting PM's actual ruling" for 9 days after being ratified — Exec's 09-08 re-verification
    sweep caught it, not a re-check PA ran itself; verified directly against `decisions.log:1761`
    rather than take Exec's framing on faith (Exec's own memo only flagged decisions 1/3 as resolved
    and asked PA to confirm decision 2's status — checking the source directly showed all three
    landed in one ruling, decision 2 being the one actually in PA's lane).

    **The ratified model, verbatim**: *"MILESTONE RECONCILIATION: MCP work STAYS in the Production
    milestone, FRONT-LOADED — MCP-path completion is the PUBLIC-BETA GATE. PM's full model restated
    as law: MVP closure ends alpha and starts invitation-only private beta (v0.9.0); PUB sprint
    front-loaded; public beta requires MCP path complete; Production milestone closure = 1.0.0."*
    Matches reading (a), which both PPM and Arch had leaned toward. #1688 moved MVP → Production-front
    (MCP-path new build, not web-chat convergence); PPM tasked with executing the board move and
    refreshing a citable release-model doc. **Bring the resolved model into the next BYOC conversation,
    not the open question** — the framing this file carried until today was wrong by 9 days.
  - ⭐ **PA's July Probe-A sequencing insight paid off concretely, 08-30 — worth having on record.**
    CXO's #1463 BYOC recomposition-rubric work traced the #1425 honesty class in running code and
    found the structured half (`source_failed`) already exists and travels end-to-end
    (`first_contact.py`, `context_assembler.py`); only the *rendering* half is a chat-specific floor-
    prompt instruction with no BYOC analogue. CXO credited PA's 07-30 framing twice — *"your July
    sequencing call was right and is the reason this is actionable rather than academic"* and *"this
    is your July sequencing point paying off concretely... we got the answer for one class without
    needing the probe at all, by reading code."* Ask went to Lead (emit `source_failed` as a
    structured field in #1688's tool output) — cheap, doesn't need the probe, doesn't block anything.
    No action for PA; triaged. ⚠️ **The next two sentences were stale at the point of this re-read too
    — a second cascade from the same fix, caught in the same pass**: this used to say the recomposition
    probe "is still needed... still gated on the credential question" and that the milestone question
    below was "PM's ruling pending." Both wrong as of today — the probe series is `SERIES PERMANENTLY
    CLOSED` (see the entry right below this one) and the milestone question is resolved (see above).
    Corrected in place rather than left for a third pass to catch.
  - **Thread status, restated**: the connector-architecture sub-thread is fully closed (see above); the
    #1463 probe series is closed (see below); the milestone/beta-definition question is resolved (see
    above). PM signaled the next topic is "the BYOC skunkworks project itself, next steps" — still PM's
    timing to initiate, now with ESSENCE.md and the ratified milestone model as its fixed points, not
    open questions to bring in.
- ✅ **#1463 recomposition probe (Probe B) — SERIES PERMANENTLY CLOSED, 08-30 through 09-03, CXO's call.**
  Six rounds across four days: Claude-only run (08-30), GPT arm + first deconfounder (09-01, after a
  billing project-mismatch delay), the directive-vs-descriptive hypothesis falsified in both vendors,
  CXO's correct re-diagnosis (content-present vs. content-absent, verified against raw data), and a
  final PM-authorized "killer test" (09-03) that produced a genuine third outcome — Claude confirmed the
  taxonomy cleanly, GPT-4o preserved both caveats together, revealing caveat-*count* as an uncontrolled
  variable CXO's own design couldn't isolate. **CXO recommended stopping rather than run a fourth test**
  (their third design/hypothesis miss on this axis in a week, each one caught by testing) — PA agreed.
  **Durable product fact that survived the whole series**: on Claude, a lone completeness/truncation
  caveat reliably vanishes (3-for-3) — don't rely on one reaching the user; the practical fix (put the
  caveat where the model can't drop it, a rendered list member rather than a field beside it) doesn't
  depend on resolving which vendor-dependent explanation is right.

  **Seventh round, 09-06, and the practical fix got tested rather than left as an argument.** PM
  authorized CXO's design (a caveat as a list member, not a sibling field) to ride the killer test's
  approval on 09-02 — it sat authorized-and-unbuilt for four days (a two-sided miss: PA never built it,
  CXO never chased it) until Exec's standing-authorization memo re-surfaced it. Built and ran it: clean
  pass, both vendors, first try — the first design across seven rounds where a completeness caveat held
  in both Claude and GPT-4o. CXO's ruling: **don't extend, hand to Lead as-is** — the practical question
  is answered and further testing would serve CXO's curiosity about generality, not Lead's actual need.
  Named a real trigger for future extension (Lead hits a second class-B case and the member trick fails)
  rather than leave it open-ended. Rubric now v0.6 with the mechanism and PA's name on it — verified
  directly rather than taken on CXO's word. Full writeups: `dev/active/probes/
  RESULTS-probe-b-recomposition-2026-08-30.md`, `RESULTS-probe-b-gpt-and-deconfounder-2026-09-01.md`,
  `RESULTS-probe-b-killer-test-2026-09-03.md`, `RESULTS-probe-b-member-candidate-2026-09-06.md`.
  **Nothing further owed from PA on #1463 — genuinely closed this time, with a tested answer, not just
  a recommendation to stop.**

### Fully resolved 08-06→08-08, deleted per CIO's rule (see git history if you need the trail)

#1481 held by PM ruling; #1484 + #1482 both deployed and verified live in v30 (08-07); #1463's retest gate
identified as blocked on #1462 (unbuilt), not a deployment, and CXO now owns notifying-on-ship; the
"is a Saturday beta deliberate" question — moot, PM named 08-09 directly.

### Closed / no PM action

- ✅ **PDR-006 RATIFIED** (2026-07-31); epic **#1462**; gates **#1458**, **#1463**.
- ✅ **Probe A complete and stood down** — refusals survive as **failure-shaped payloads** (6/6 both
  providers); structured fields help but are **not sufficient** on GPT. ⚠️ **CORRECTED 2026-08-08 (CXO's
  finding, verified independently)**: the retest gate isn't waiting on a **deployment** — `services/mcp/
  server/` doesn't exist in `main` or the artifact. **It's unbuilt, not undeployed** — blocked on **#1462**
  (the epic), not a hostname. CXO retests same-day once #1462's server package lands; tell them when it does.
- ⚠️ **"Delete" means SOFT delete** — five live *"cannot be undone"* claims on reversible paths
  (**#1482**, CXO owns copy, HOST owns the trust ruling).

## Active state — 2026-09-01 (mid-day, updated fire 15:45)

- **Role**: PA · **Host**: Amber · **Account**: xian@pipermorgan.ai · **Model**: Opus 5 (1M)
- **Worktree**: `~/Development/piper-morgan-worktrees/pa` · branch `claude/pa-cycle`
- **Session log**: `dev/2026/09/01/2026-09-01-0645-pa-code-log.md` — today's, still open. Full arc so
  far: OpenAI credential resolved live with PM, #1463 probe closed out end-to-end (both vendors +
  deconfounder), CXO's item-3 resolution verified and replied to, T1 (Cross-Piper synthesis) advanced
  across five passes including a self-correction on the code-check finding.
- **Cron**: `42 6,9,12,15,18,21`, job `0a39909f` (re-armed 08-31 ~22:xx via delete-then-create for
  substantive T1 work; unchanged since). 🔴 **First action any new session: `CronList`.** Empty = not
  cycling.
- **Inbox**: 0 as of 15:45 fire.
- **Standing discipline (from 08-15's correction, still active)**: re-verify carried-forward claims
  against their live source before citing them in an external report, not just at routine
  carry-forward-hygiene time. Habit, not yet mechanical.
- **Connector-architecture thread: PERMANENTLY CLOSED** — every sub-question now has a final,
  PM-ratified answer, and PA's own finding is now cited in `CONNECTORS.md` as permanent architecture.
  Nothing owed, nothing to chase on this thread specifically.
- **#1463 probe: CLOSED, see the collapsed entry above.** No open external dependency remains.
- **T1 (Cross-Piper synthesis) — genuinely active, DRAFT v0.** Draft:
  `dev/active/t1-cross-piper-comparison-2026-08-31.md`. All 5 PO retros + 2 session logs read; 3 code
  files checked (found a mixed picture, corrected same-day from an initial overclaim). Still open: a
  fuller response-surface audit (action confirmations, search-result formatting) and one question
  posed directly to PM (draft-then-review vs. review-then-draft trust model) — not yet answered.
- **BYOC's next phase still waits on PM's own timing**: "the BYOC skunkworks project itself, next
  steps" plus the shipping-small-things preview, with `docs/internal/architecture/ESSENCE.md` (v1.0,
  ratified 08-30) as its fixed point. Read it fresh before that conversation resumes, not from memory.
- **Privacy-policy check: retested 09-01, still failing on the same known-stale chrome-devtools MCP
  path** (`/Applications/Google Chrome.app/...` doesn't exist on Amber; a real fix needs an actual
  process restart, not yet observed). Not new information — don't re-report unless it changes.

🔔 **STEP 5b — HEARTBEAT: emit it IMMEDIATELY AFTER `date`, BEFORE the git fetch/merge, and WITHOUT
`--if-quiet`** *(ordering fixed 2026-08-05: my heartbeat had five commands incl. fetch+merge in front of
it, so my timestamp was **wake + git-op time**, inflating my dispatch number and its spread. Satisfied
HOST's "date first" ask while defeating its purpose.)* *(adopted 2026-08-04, deliberately
diverging from the memo's specified invocation)*.
```
scripts/duty-cycle-heartbeat.sh pa WORK        # no --if-quiet
```
**Why the divergence — TIMING, not visibility.** `--if-quiet` asks *"committed within 6h of **now**"*
while the belt asks *"alive **at 06:46**"* — **a commit only proves liveness at the instant it lands**,
and the suppressing commit can **postdate** the sweep it excuses (arch: log 07:01, sweep 06:46).
**No threshold value fixes a predicate evaluated at the wrong instant** (1h suppresses identically). A
wake row is the only signal that can precede a sweep; the end-of-fire one is intrinsically too late.
⛔ **DO NOT repeat my retracted claim that suppression makes a role "invisible."** It doesn't — verified at
`duty-cycle-freeze-check.sh:62-70`, the belt takes `max(ct, ct2, ct3)` = role-tagged commit / session-log
commit / heartbeat tsv, so **a committing role is already covered by the first two** and an empty surface
on a working day is *correct*. I had the mechanism right and the consequence wrong (Arch made the same
error; HOST made its mirror image — checked *what* the belt reads, not *when*).

🔴 **AFTER ANY CONFLICTED MERGE, BEFORE PUSHING** *(new 2026-08-08, real incident — Arch's own broad-
staging-hook remediation deleted 17 files from `main` during a merge)*: run
`git diff --diff-filter=D --name-only <merge-sha>^2 <merge-sha>` — **`^2`, not `^1`.** During a conflicted
merge, `git restore --staged <path>` resolves to **HEAD's** version; for a file new on the incoming side,
HEAD has none, so the result is **deletion**, and concluding the merge carries it to `main`. **Never run
`git restore --staged` mid-merge.** Retroactively audited my one real conflict this week (0b6b36b2,
decisions.log, 08-07) — clean, no deletions. Now `one-command-checks.md` #8.

⛔ **NEVER `grep -c "DAY-CLOSED"` TO DECIDE CLOSE STATE** *(bit me 2026-08-05)*. My 8/04 log returned **2**
and was **not closed** — one match was a continuity reference to the prior day, the other was **my own
prose about the freeze-check's DAY-CLOSED skip.** ⭐ **Writing ABOUT the marker creates a false marker**,
and the roles most likely to write that prose are the ones working on the watchdog. Use the anchored
pattern from `duty-cycle-freeze-check.sh:99`. **A count is not a marker.** ⛔ **GENERAL FORM (3 instances on 08-05): any audit for a retracted claim MATCHES ITS OWN CORRECTIONS** — the better a correction states what it corrects, the more certainly it defeats the search for what it corrected. **Line context, never a count.** ⚠️ **Hit TWICE on 2026-08-05, two unrelated files** — the second time my own *correction note* quoting old text made `grep -c` report the retracted claim as still live. **Writing ABOUT a marker creates a match for it. Verify with line context, never a count.**

⏱️ ~~**YOUR DISPATCH CONSTANT IS +30m16s..+30m20s**~~ — ⛔ **RETRACTED-SHAPE CLAIM, corrected 08-08.**
CXO generalised **within-seat stability is a property SOME seats have, not a property of the system** —
their own seat looked identical to mine (stable, +30-band) for 7 fires, then swung to +2 on 08-08.
**Mine has NOT swung — 13 consecutive fires through and including that exact morning, +30m15s..+30m22s**
— but per CXO's own caveat, *"nothing distinguishes genuinely stable from hasn't-swung-yet."* **Report the
series, never a fitted constant**: `08-07: +22,+17,+19,+18,+15,+17s · 08-08 07:12: +20s`. No claim about
tomorrow.
⚠️ **My claim that git-ops inflated this was PRE-REGISTERED AND FALSIFIED 8/05** — moving the heartbeat
ahead of fetch/merge left it unchanged. **So the ~3s arch/pa gap may be REAL and my advice to discard it
is unsupported.**
⛔ **Never label a fire by its scheduled minute** — Arch and I both did, and both had to correct it.
**Commits/heartbeat-tsv timestamps are the evidence; the label is a guess.**

⚠️ **KEYCHAIN**: use `/Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python` — any other
binary **HANGS** on a GUI dialog rather than failing; `SIGALRM` will not save you.

⚠️ **SEARCH PREDICATES** — CXO's `grep "Aug 8"` against a log storing **ISO**; PA searching
**`web/templates`** (1 file) instead of **`templates/`** (63). **The search that finds NOTHING is the one
that most needs its predicate audited.** Real template root is `templates/`.

⛔ **SOURCE VOCABULARY IS NOT SOURCE VERIFICATION** *(new 8/4, cost two false claims — one in a legal
document)*. `disconnect.py`'s docstring says *"#358 grant **revoke**"* for what is a **local** grant-store
row deletion. I carried that verb into two artifacts. **A comment using a strong verb for a weak operation
hands you the strong verb, and the audit trail looks clean because you can cite the file.** Citing a file
proves you read it, not that you read what it does.

## Open threads PA owns
✅ **Ship-055 — FILED 08-07** (`mailboxes/exec/inbox/workstream-055-pa-2026-08-07.md`), same fire, after Exec corrected the deadline framing (write now, not by Saturday — a deadline gives license to delay).


1. 🟢 **Tool-annotation spec — UNBLOCKED, complete enough to hand to Lead.**
   `dev/active/tool-annotation-spec-2026-08-04.md`. **Next actor is Lead, not PA.**
   ✅ **Arch ruled**: condition 3 does **NOT** reach the workflow registry — **nothing leaves the catalog,
   build ONCE**. `readOnly` ≠ `resource` (orthogonal axes: *addressable context vs invoked operation* is
   not *does it mutate*). ✅ A defaultless registry field satisfies condition 2, and Arch flagged
   **"don't let defaultless get softened in review — it's the whole thing"** (4 of 5 `WorkflowEntry`
   fields are already defaulted).
   ✅ PPM: `close_issue` = `WRITE` — **DESTRUCTIVE = destroys information unrecoverable through the product**.
   ✅ CXO: **the irreversible part of a reversible operation goes in the same sentence as the reversibility
   claim** (a recomposing client LLM drops trailing caveats, and keeps the *reassuring* one).
   ✅ **Registry alias count CORRECTED**: not 31→12 (that's the literal dict, **one of five writers**) but
   **103 aliases → 38 entries**, 2.71 names/op — re-derived independently, matches Arch exactly.
   **Catalog must dedupe by entry identity; aliases are classifier surface and must not leak outward.**
   ✅ All **26 cohort handlers screened → all READ** (3 ambiguous hand-checked). ⚠️ **A screen, not an
   audit**; `_handle_learn_pattern` is the one to re-check first.
   ⬜ **Open for Lead**: the ~15-site breaking change. ⬜ Unscreened: `meeting` (offer-only),
   `run_todo_query_workflow` (separate module).
   ✅ **Plugin manifest DRAFTED** (`dev/active/plugin-manifest-draft-2026-08-05.md`) from the fetched
   reference. **The item is far smaller than scoped**: manifest is *optional*, **`name` is the only
   required field**, unrecognized fields are warnings. ✅ **The gap I flagged is CLOSED and was MINE** — plugins
   DO support remote MCP (`http`/`sse`/`ws` with `url`, `headers`, **`headersHelper`**). No shim owed.
   ⭐ **`headersHelper` supplies dynamic per-request auth headers → it is the carrier for Arch's
   condition 1.** ⛔ My miss: the answer was in a page dump I already had; **`-i sse` matched "pa·sse·d"
   and the noise filled my `head -8`, evicting line 691. NEVER `head` a search you'll draw a NEGATIVE
   conclusion from.** ⛔ Draft is NOT at `.claude-plugin/plugin.json` — that path
   would make this repo a plugin for every agent.
   ⬜ Other Phase 0 items: **`claude plugin validate` dry-run is MIS-SCOPED** — verified 8/05: `claude` is
   not on PATH or at common install paths, **and no plugin manifest exists** (`coordination/manifest.json`
   is the async-prompt-queue tracker, unrelated). **The real item is "author a plugin manifest, THEN
   validate"** — a build task, not a command. · public docs page · ChatGPT 5-positive/3-negative test cases.
2. ⚠️ **PRUNED 09-08 — abandoned, not confirmed-closed.** The old tool-name-routing "Probe B" (situation-
   vs-object-shaped names, upstream of a 12-tool catalog, PM-gated on spend that was never asked for).
   Its own spec file (`dev/active/phase0-client-llm-probe-spec-2026-07-30.md`) no longer exists on disk
   — checked directly rather than assumed still there — and no trace of this thread anywhere in five
   weeks of subsequent work (the catalog/#1124 work, ESSENCE, #1463's own — unrelated — "Probe B," the
   connector architecture). Consistent with the 08-11 prune's own disposition for items with no
   corroborating evidence: pruned as abandoned, not verified resolved. If it resurfaces, it'll come from
   a fresher source (PM, a GitHub issue, Lead), not from this stale row.
3. **#1458** — pre-live cross-caller state isolation; blocks multi-tenant serving. Re-verified 09-08:
   still `OPEN` on GitHub, matches this row exactly. Not started; belongs with the implementation epic.
   PPM: don't let epic optimism compress it — the failure is silent and cross-tenant.
5. **Architecture-diagram discussion** — PM-requested, awaiting a time. `pa-standing-items.md` #2.
   Prep, don't pre-empt: PM asked to discuss, not for a revision.
6. ✅ **#1485 — RESOLVED, re-verified 09-08.** `gh issue view` shows CLOSED 2026-08-13, a month ago,
   clean — no evidence anywhere since of a trimmed AC or unaddressed class. Nothing further to watch.
