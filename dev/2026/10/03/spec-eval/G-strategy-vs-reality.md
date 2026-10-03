# Workstream G: Product strategy vs reality (users first)

**Snapshots**:
- piper-morgan-product: `a191856` (the local HEAD is 16 commits ahead; exact-at-snapshot claims use `git show/grep a191856`)
- website: `16dfe5f`
- skunkworks: `829746f`
- GitHub issue state: pulled live on 2026-10-03 via the REST API. GraphQL is blocked in this environment, so Projects-v2 fields were not read.

**Scripts and data** (`spec-eval/metrics/`):
- `G-issues.jsonl`: all 1,916 issues and PRs, paged over REST
- `G-backlog.py`
- `G-sample-ev.txt` and `G-sample-close.txt`: a 40-issue closure sample

**Privacy**: testers are described by role and ordinal only. No names or emails.

---

## 1. Users: do real users exist?

**Short answer: barely. There is no sustained external usage in evidence.**
- Over the project's life, roughly 5–6 humans other than PM have been alpha testers in some form.
- In the current hosted era (June 2026 onward), **exactly one external tester is evidenced to have actually used the product.** That was one session in late July, and it produced feedback only after PM nudged twice.
- The current external invitee loaded `/setup` once on 09-21 and never submitted a code. Their code was then burned, and the reissue was deliberately deferred.
- **0 of 1,903 GitHub issues were authored by anyone other than the owner account (1,828) or a bot (75).**

| id | claim | layer | denominator | evidence | conf | implication |
|---|---|---|---|---|---|---|
| G-U1 | **Local-install alpha, Oct 2025–Mar 2026: about 5–6 named external testers, with low engagement.** PM was tester 1 (Oct 27, 2025). A Feb 2026 activity table lists 4 testers or tester-pairs: 1 "very active" (an advisor who also tests and filed a Windows bug report that became 14 GitHub issues), 1 postponed, 1 paused for personal reasons, 1 "passive (intentional)". By March, the omnibus logs record "alpha tester silence (16 days)". | record | omnibus logs 2025-10 → 2026-03 (grep of "alpha tester") | `docs/omnibus-logs/2026-02-22-omnibus-log.md:201-208`; `mailboxes/ted-nadeau/read/memo-to-ted-nadeau-2026-02-07.md` (14 issues extracted); `docs/omnibus-logs/2026-03-30-omnibus-log.md` ("alpha tester silence") | med (the roster file is gitignored and absent) | The early alpha generated one rich feedback stream, from a technical advisor. That is not product-market signal. |
| G-U2 | **The "first external tester" of the hosted era (June 7) never actually tested.** The June log said an alpha package was sent. PM later confirmed she never tested the plugin, and the briefing still says "first external tester". | record | 1 claim traced to its correction | `BRIEFING-CURRENT-STATE.md:228` (claim) vs `docs/omnibus-logs/2026-07-16-omnibus-log.md:132` (correction) | high | The briefing still contains a user claim that was retracted 2.5 months ago. |
| G-U3 | **One external tester session in the hosted era, and it was nudge-dependent.** Timeline: invite Jul 12 → silence → PM nudge Jul 24 → feedback email Jul 25. HOST's verdict: "the one signal we have was manufactured by PM asking twice… we had no signal of our own". The tester's verdict was "is it just an LLM with extra UI?" He used "anxiety" 3 times and apologised twice for his feedback. | record | the only hosted-era tester session found | `docs/omnibus-logs/2026-07-27-omnibus-log.md:99-138`; `…-07-28-omnibus-log.md:331`; `dev/2026/07/29/2026-07-29-1216-pa-code-log.md:200-203` | high | The only real-user evidence in four months questions the core differentiation thesis. See §4. |
| G-U4 | **What happened to that feedback.** It was distributed to 4 agent lenses the same day. 9 FTUX issues were filed Aug 3–9. At snapshot, **4 are closed** (#1476, #1477, #1510, #1536 "show the user their own work in the first exchange") and **5 are open after ~8 weeks** (#1509 reopened, #1537 composer, #1538 elicitation, #1539 purpose, #1540 nav-hidden-in-avatar-pill). Workstream C independently re-found the nav problem on 10-03 (C-09: core CRUD hidden under the username dropdown). | record + live GitHub | 9 FTUX issues | `metrics/G-issues.jsonl` (filter created 2026-07-25..08-10, "FTUX"); C-09 | high | The single user's top UI complaint is still live. Feedback flows through a heavy synthesis apparatus, but its closure rate is modest. |
| G-U5 | **The current external invitee has not used the product.** The invite was ready 09-13 and held twice for BYOC defects (#1810, #1814). It was sent 09-21 with a dead code. The invitee loaded `/setup` and did not submit. A replacement code was sent the same evening. Codes were then burned in the #1885 credential cleanup, and both reissues (2 invitees) were **deferred by PM: "not urgent… wait til they try and fail."** | record | all invite-thread mentions 09-13 → 10-01 | `docs/omnibus-logs/2026-09-21-omnibus-log.md:209-295`; `dev/active/host-carry-forward.md:88-90`; `docs/briefing/ROLE-PORTFOLIO-HOST.md:38` ("no new tester-silence movement") | high | At snapshot, **the number of external humans with a working invite is plausibly 0** (unverified: prod DB not observed). |
| G-U6 | **There is no in-product feedback channel in the UI.** `/api/v1/feedback` exists (POST/list/get, owner-scoped) and works (C, row 14), but no template or static JS calls it. The only `/feedback` fetch in the UI is learning-pattern feedback. All real feedback arrived by email or meetings. | static | all `*.html`/`*.js` at a191856 | `git grep "/feedback" a191856 -- '*.html' '*.js'` → only `web/assets/bot-message-renderer.js:331` (learning patterns) | high | Testers have no low-ceremony way to report. This compounds the silence HOST is trying to diagnose. |
| G-U7 | **The organisation's "user research" capacity points inward.** Agent 360 surveys 11 agent respondents on a 6-week cadence with structured synthesis. The external-tester program has 1 feedback session in 4 months. D0's H1 finding (coordination commits/month up 266× from B to R, C/P ratio up 94.6×) is the quantitative backdrop. | record + git-history | 1 cohort survey vs 1 user session | `host-carry-forward.md` (Agent 360 v0.5, 11 respondents); D0 §1 H1 table | high | **The cohort studies itself far more than it studies users.** This is the most direct lever for the guiding question. |

**Evidenced vs claimed**:
- Evidenced: the Feb tester table, the July session and feedback, the Sept invite and its non-use, and the GitHub authorship (0 external authors).
- Claimed only, or unverifiable here: how many accounts exist in the Fly production DB and whether any non-PM account has logged in since 09-21. The `users` and `feedback` tables on prod are not observable to this eval.

---

## 2. Stated product vs as-built (C)

**Stated product** (Vision v2.3 Apr 11; PDR-005 BYOC ratified Jun 5; PDR-006 hosted-MCP + plugin ratified Jul 31):
- Piper is a PM colleague that **shows up inside the user's own AI chat** (Claude, ChatGPT) through a hosted MCP endpoint plus a Claude plugin.
- It is a **pure tool server with no server-side LLM** (PDR-006 §Decision).
- Integrations are "indoor plumbing via MCP plugins".
- Intent classification is dropped in favour of a 4–5-handler action gate.
- The differentiators are the context methodology, the conscious floor, artifact persistence, and trust graduation.

| id | claim | layer | denominator | evidence | conf | implication |
|---|---|---|---|---|---|---|
| G-P1 | **Promised but not built: the primary distribution surface is a sliver.** PDR-006 calls hosted MCP plus plugin the *primary* model. As built, the MCP server exposes **3 read-only resources and 1 read-only tool**, with scope `resources:read`. Epic #1462 has **3/15 AC** (09-29). No plugin package exists in the product repo. | static + record | full MCP server surface | C §1 (`services/mcp/server/resources.py:48-50,238`); #1462 last comment 09-29 | high | Effort went to the surface the strategy says is secondary. |
| G-P2 | **Built but not promised (or explicitly de-scoped): a large bespoke web app with a server-side LLM path.** It has 255 HTTP ops, 30 pages, 53 wired chat actions, 144 workflow keys, and 27 CLI subcommands. Vision v2.3 says to drop the 19-category classification, bespoke integrations, and the personality service. PDR-005 allows only a "thin bespoke UI" for 5 of 7 MUX surfaces. The web chat is gated on a BYO LLM key that the *server* calls, which is the opposite of PDR-006's "no server-side LLM". | static + ran-server (C) | C's 32 capability groups | C §1, §3; `vision.md:116-135`; PDR-006 §Decision | high | The as-built product is the pre-pivot architecture, still being hardened. Each month spent on web-chat routing correctness (Epic 0 #1595, extraction ceiling 558) is spent on the surface the strategy de-prioritised. |
| G-P3 | **Partial convergence: Epic 0 (#1595, "one constrained LLM routing call does the understanding") is the vision's "drop classification" decision.** It arrived about 4 months after the vision and is still open as the current epic. | record | 1 epic | #1595 body; `dev/active/mvp-epic-order-2026-09-09.md:20-38` | high | Directionally aligned, but it applies to the web-chat path. In the MCP model, the *client* LLM does the understanding and this layer mostly disappears. Whether Epic 0 is needed for an MCP-primary product has not been asked in the docs I read (unverified). |
| G-P4 | **Integrations claimed vs observable.** The site and vision promise GitHub, Calendar, Notion and Slack. PDR-005 scopes 1.0 to GitHub + Calendar + Notion, with Slack deferred. The C eval could observe none of them (no OAuth apps). Of the 53 chat actions, 22 need an integration and 12 need an LLM. | ran-server (C) + record | 53 actions | C §1 table, row 21–24 | med | The headline "colleague" value cannot be verified by any seeded harness. C-11 recommends building one. |
| G-P5 | **The planning surfaces are stale against each other.** Roadmap v18.8 narrative is current only to Jul 16 and still carries "beta Aug 1 / production Oct 30". `beta-blockers.md` was last updated Jul 9. The live sequencing doc is `dev/active/mvp-epic-order-2026-09-09.md`, which is in `dev/active/`, not `docs/`. The briefing's inchworm still says "RECONNECT WS-2 next" and "M4/M5 ⬜". The last MVP count in the briefing is 52 not-done (09-14). | record | 4 planning surfaces | `roadmap.md:1-6`; `beta-blockers.md:5`; `BRIEFING-CURRENT-STATE.md:55-70,91` | high | No single current statement says what beta *is* or when it ships. The 09-18 sprint plan says as much: "a proposal PM can rule on that says what alpha and beta each are". |

---

## 3. Backlog health (live GitHub, REST; `G-backlog.py`)

| id | claim | layer | denominator | evidence | conf | implication |
|---|---|---|---|---|---|---|
| G-B1 | **1,903 issues: 285 open, 1,618 closed** (1,576 completed, 35 not_planned, 7 duplicate). This reconciles with the repo's `open_issues_count` of 286 (285 issues + 1 open PR). | live GitHub | 1,916 rows (issues + PRs), all pages | `metrics/G-issues.jsonl` | high | — |
| G-B2 | **Open-issue age**: 39 under 30 days, 114 at 30–90, 70 at 90–180, 53 at 180–365, 9 at a year or more. Median 87 days. | live GitHub | 285 open | `G-backlog.py` output | high | Moderately aged. 62 issues are older than 6 months. |
| G-B3 | **The open count is volatile, not steadily growing.** Month-end open counts: 118 (Mar), 177 (Jun), 204 (Jul), 331 (Aug), 283 (Sep). Issue creation is heavy: 252 filed in Aug, 191 in Sep. | live GitHub | all issues | `G-backlog.py` | high | The agents file issues as fast as they close them. Throughput is high, but the net position on the MVP is not visibly converging toward a beta date. |
| G-B4 | **Priority labels are absent, not inflated.** 267/285 open issues carry no `priority:` label (12 low, 1 medium, 3 high, 2 critical); 134/285 have no labels at all. Priority evidently lives on the Projects-v2 board and in `mvp-epic-order`. Those were not readable here (GraphQL blocked). | live GitHub (labels only) | 285 open | `G-backlog.py` | med | The label data cannot reveal priority inflation, so this question is unresolved. |
| G-B5 | **Closed-not-done looks rare.** Sample: 40 random "completed" closures since 2026-07-01, out of 462. Results: 35/40 have a valid commit SHA cited in comments or a commit-reference event. The other 5 (#1557, #1567, #1641, #1679, #1865) carry prose evidence, e.g. "verified in code today" or PM's live checkbox verdict. **0/40 were clearly closed without the work being done.** Most issues are closed by hand, not by commit keyword, which is expected given the auto-close guard (#1691). | live GitHub + git-history | 40/462 (8.7%) | `metrics/G-sample-ev.txt`, `G-sample-close.txt` | med (sample; I did not read every cited diff) | Closure discipline is a real strength, and it should not be the target of change. |

---

## 4. Thesis risk: does the product thesis survive the current market?

**What the market now provides, per sources** (secondary sources, medium confidence):
- Claude **Cowork plugins** launched on 2026-01-30 with 11 open-source knowledge-work plugins, **including a product-management plugin** ("write specs, prioritize roadmaps, track progress"). [pasqualepillitteri.it](https://pasqualepillitteri.it/en/news/200/claude-cowork-plugins-complete-guide-professionals), [eesel.ai](https://www.eesel.ai/blog/claude-cowork-plugins-updates)
- A self-serve **directory submission portal** opened on 2026-09-25. Any paid user can publish an MCP connector or a plugin bundle (MCP + skills from a GitHub repo). Listings reach claude.ai web, desktop and mobile, Cowork, and Claude Code. [claude.com/docs/directory/publish](https://claude.com/docs/directory/publish), [pasqualepillitteri.it](https://pasqualepillitteri.it/en/news/18444/anthropic-portal-submit-plugins-mcp-connectors-claude)
- **Claude persistent memory** (role, preferences and projects synthesised across chats) reached all plans, Free included, by early 2026. [techradar](https://www.techradar.com/ai-platforms-assistants/claude/claude-just-got-a-vital-free-upgrade-to-help-it-take-on-chatgpt-itll-now-remember-conversations-for-all-users-heres-why-that-matters), [its.syr.edu](https://its.syr.edu/claude-has-a-memory-heres-how-to-use-it/)
- First-party or community MCP connectors exist for GitHub, Google Calendar, Notion and Slack (the vision's own "indoor plumbing" premise, `vision.md:21,106-113`).

| id | claim | layer | denominator | evidence | conf | implication |
|---|---|---|---|---|---|---|
| G-T1 | **Piper's own strategy docs concede most of the stack is commodity.** The vision says tools, LLM reasoning and integrations are commoditized, and the differentiator is a "methodology layer". The CXO's PDR-006 review says the plugin model "removes the surface where we'd have demonstrated differentiation… *just an LLM with extra UI* becomes literally true by design… every gram of differentiation now has to be carried by what the tools return". | record | vision + 1 ratifying review | `vision.md:76-113`; CXO memo 2026-07-30 §1 | high | The project has already named the thesis risk itself. Nothing in the backlog I saw tests it. |
| G-T2 | **Of the four differentiators, only some are hard for a generic plugin + MCP + Claude memory to replicate.** Easy to replicate: (2) "conscious floor" persona and voice, which is a system prompt (a plugin `CLAUDE.md` *is* this); (4) trust graduation, which is prompting by Piper's own admission ("lightweight… context-based prompting"); and much of (1) context methodology, where Claude memory plus Projects plus skills covers per-user context. Plausibly distinctive: **server-side cross-session, cross-client persisted PM state** (artifact persistence/composting, colleague model, Insight Journal), meaning the same state reachable from ChatGPT *and* Claude, plus **write-capable connectors with consent/effect-class gating** (EffectClass READ<WRITE<DESTRUCTIVE, #1557). | static + record + web | 4 differentiators | `vision.md:80-104`; PDR-006 capability split; #1557 | med (judgment) | The defensible core is a **hosted PM-state server with safe write tools, shipped as a directory-listed plugin**. That is exactly the 3/15-AC epic (#1462). The web app, the classifier and the persona work are the least defensible parts. |
| G-T3 | **The methodology may be the product, but it is not what is being shipped to users.** The vision says "The Methodology as Product" (`vision.md:192`), and the repo already contains Piper skills (`piper-draft-spec`, `piper-sprint-plan`, `piper-synthesize-feedback`, …). The directory now lets a plugin bundle reach all Claude users with no hosting. | static + web | skills list in this session | `.claude/skills/` listing; directory portal | med | The cheapest way to test whether anyone wants Piper's PM methodology is to publish the skills (plus the existing read-only MCP) as a directory plugin and count installs. It needs no BYO-key gate, no signup wizard and no 255-op web app. |

---

## 5. Skunkworks (BYOC PoC)

| id | claim | layer | denominator | evidence | conf | implication |
|---|---|---|---|---|---|---|
| G-S1 | **It is dormant.** 62 commits, all May–June 2026 (13 + 49). Last commit 2026-06-27. The tracker's last PA touch was 06-20, at "Step 1: hosted endpoint connection, no auth". | git-history | whole repo | `git log` in skunkworks; `byoc/tracker.md:7-20` | high | — |
| G-S2 | **What it proved**: an MCPB plugin with 5 tools registers and runs in Claude Desktop (`uv run`, per-tool permission controls); plugin config must be server-owned; skill packaging format; OAuth is needed for metering and returning-user identity rather than key-passing (findings #1–#5). It did **not** prove any user value, and the PM-gated hosted test never completed in-repo. | record | 5 findings, 6 notes | `byoc/tracker.md:82-151`; `byoc/notes/` | med | — |
| G-S3 | **It has been superseded.** PDR-006 "supersedes MCPB skunkworks POC (informally)", and the hosted MCP server now lives in product (`services/mcp/server/`, Phase C shipped 09-26, `mcp.pipermorgan.ai` live). The product repo has also absorbed skunkworks into the roadmap ("§M5/BYOC + skunkworks ABSORBED v18"). | record + static | — | PDR-006:42; `roadmap.md:3`; #1462 | high | **Recommendation: stop.** Archive the repo with a README pointer to PDR-006/#1462 and to the findings worth keeping (#1, #4, #5). Merge nothing further; the code path is obsolete (local MCPB). |

---

## 6. Website (piper-morgan-website)

| id | claim | layer | denominator | evidence | conf | implication |
|---|---|---|---|---|---|---|
| G-W1 | **The repo's documented deploy pipeline no longer exists.** `.github/workflows/` was deleted (update-blog-posts.yml removed 2026-07-19; deploy removed around 07-16). The last GitHub Pages runs were 07-16 and 07-21. `next.config.ts` only exports statically when `STATIC_EXPORT=true` (the admin compose UI needs a server). The website `CLAUDE.md` still describes GitHub Pages static export plus daily Actions. | static + CI-history | 40 most recent runs (total 995) | `gh api …/actions/runs`; `git log --diff-filter=D -- .github/workflows`; `next.config.ts:7` | high | Where and how the site deploys now was not determined (unverified). The repo's own instructions are wrong for agents. |
| G-W2 | **Build not run** (no `node_modules`; an install plus build is likely over 5 minutes). Build health is unverified. | — | — | — | — | — |
| G-W3 | **Site copy contradicts the as-built product and the current strategy.** `/try` and `/try/alpha` tell alpha testers they will need a local dev environment ("command line, environment variables, Docker"); in fact the alpha is hosted, invite-only and BYO-key. Beta is described as "probably in the next few months", but no date exists (G-P5). The homepage promises a morning digest of "GitHub activity, calendar shifts, Slack threads", but C found standup empty without integrations and Slack is deferred from 1.0 (PDR-005). The site never mentions BYOC, ChatGPT/Claude, MCP or the plugin, which is the ratified primary distribution. | static | 3 public pages read (home, /try, /try/alpha) | `src/app/(public)/try/page.tsx`, `try/alpha/page.tsx`, `page.tsx` | high | The public funnel recruits for a product shape that no longer exists. If the user problem (G-U*) is to be fixed, the front door is the first edit. |

---

## Top findings for synthesis (ranked)

1. **There are effectively no users.** One external hosted-era session in four months (nudge-dependent). The current invitee never got past `/setup`, and reissues are deferred to "wait til they try and fail". All 1,903 issues come from the owner account or a bot (G-U3, G-U5, G-B1). **Change**: make getting about 3–5 external people to a first useful session the top priority, above the next epic. Reissue the codes now.
2. **The organisation studies itself, not users.** 11-respondent Agent 360 cycles and 266× coordination growth (D0 H1) set against one user session and no in-product feedback button (G-U6, G-U7). **Change**: wire the existing `/api/v1/feedback` into the UI and give it an owner and a weekly read.
3. **Strategy and build have diverged.** The ratified primary surface (hosted MCP + plugin) is at 3/15 AC with 1 read-only tool, while effort goes into the de-prioritised web chat and its routing (Epic 0) (G-P1–G-P3). **Change**: get an explicit PM ruling on whether the web app is the MVP or the thin secondary surface, and re-order the epics to match.
4. **The thesis risk is acknowledged but untested.** A first-party PM plugin, open directory publishing, and Claude memory now cover persona, trust prompting and much of the context methodology. Piper's defensible core is cross-client persisted PM state plus safe write tools (G-T1, G-T2). **Change**: ship the existing skills plus the MCP as a directory plugin to test demand cheaply (G-T3).
5. **The single tester's feedback is only half-addressed after about 8 weeks.** 5 of 9 FTUX issues are open, including nav hidden in the avatar pill, which C re-found today (G-U4).
6. **There is no single current statement of what beta is.** The roadmap, beta-blockers and briefing are stale against each other, and the live order sits in `dev/active` (G-P5). The website promises local-install alpha and "beta in a few months" (G-W3).
7. **Housekeeping**: stop and archive skunkworks (G-S3); fix the website's stale deploy docs (G-W1). Do **not** change issue-closure discipline; the sample shows it is sound (G-B5).

## Appendix (not bearing directly on the guiding question)
- About 75 bot-authored issues are mostly scheduled health checks.
- The briefing retains the retracted "first external tester" claim (G-U2).

## Unobservables
| what | why | how to observe |
|---|---|---|
| Prod user count, logins and feedback rows | No access to the Fly prod DB | `SELECT count(*), max(last_login) FROM users` and the `feedback` table on prod, run by PM/Lead |
| Board priority/status fields, i.e. priority inflation | GraphQL blocked from this session | `python3 scripts/sprint-truth.py` from a seat with GraphQL |
| Whether the 09-21 invitee or the 2nd invitee were contacted since 10-01 | Email is not in the repo | PM's mail |
| Website build health and the current deploy host | No node_modules; workflows removed | `npm ci && npm run build`; ask Web where pipermorgan.ai is served from |
| Actual market adoption of the Cowork PM plugin and directory | Secondary web sources only | Directory listing stats after publishing |
| Earlier-alpha tester roster completeness | `alpha-tester-roster` is gitignored | PM's private roster |

**Verified how**: REST pull of all 1,916 GitHub issues/PRs, with the open count reconciled against `open_issues_count` (286 = 285 + 1 PR), plus a 40-issue closure sample with SHAs checked via `git cat-file`. Layers: live-GitHub, git-history, and record (omnibus logs, carry-forwards, PDRs, mailboxes, grepped with stated patterns), plus static (`git grep` at a191856, website source read) and 3 standard web searches. Denominators: 1,903 issues / 40 of 462 closures / 9 FTUX issues / 3 website pages / 62 skunkworks commits. Prod DB not observed.
