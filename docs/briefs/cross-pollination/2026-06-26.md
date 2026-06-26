# Cross-Pollination Brief — June 26, 2026

Overnight: Piper Morgan's two phone-UAT alpha blockers from June 24 were cleared by the team, moving the alpha gate from localhost hardcoding to a Caddy auth dialog quirk. Meanwhile, PM's ninth narrative blog post published — on how structural guardrails (a pre-commit hook, a worktree convention) succeeded where layered discipline kept failing. On the designinproduct.com side, xian ratified all three open shape decisions for the website redesign: new IA, an offer ladder with visible pricing, and "The Practice" as a curated proof surface.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

---

## Key Insights

### 1. Alpha gate moves: localhost hardcoding cleared, Caddy auth dialog is the new blocker

**From:** PM Exec (attention rollup `dev/active/exec-cohort-attention-rollup-2026-06-25.html`, commit `d1bee99`); Lead Dev fixes (commits `fb63b82`, `38b0adb`)  
**Relevant to:** Klatch (same pre-beta checklist pattern)

The June 24 alpha blockers — `#1318` (onboarding system-check hardcoded `localhost:5433/6379/8000`, failing on the Droplet) and `#1319` (welcome card layout broken on mobile) — were both cleared by Thursday afternoon. The exec rollup confirmed: "alpha blockers cleared."

The new gate is `#1320`: the Caddy basic-auth dialog loop. When a browser hasn't previously cached valid credentials, XHR calls from the onboarding flow trigger a raw browser auth dialog that blocks setup. Lead Dev's investigation found the likeliest cause is a stale-cache artifact from a same-day password rotation — fresh-cached testers probably won't hit it. Side-bug #1 of `#1320` (a `check-keychain` route missing the `/api/v1/` prefix, causing 404s) was already fixed and deployed.

The separate decision: the Caddy gate is staying for now. It's currently the alpha's invite mechanism — removing it would open public registration before app-layer invite controls and RBAC hardening are complete. The gate removal (`#1162`) is sequenced with the multi-tenant auth path.

**Suggested action (Klatch):** The pattern from both PM pre-launch cycles: environment-context bugs (localhost hardcoding, container env vars, auth gate edge cases) only surface under real-device real-deploy conditions. When beta server components ship, test with a fresh browser session and no cached credentials — not just "containers healthy."

---

### 2. The Hook and the Worktree — structural fixes beat repeated discipline

**From:** PM Comms (blog post `docs/public/comms/drafts/the-hook-and-the-worktree.md`; published June 25, commit `6b0d2fc`)  
**Relevant to:** Klatch (same worktree model; enforcement hook pattern)

Beat 9 of the "Building Piper Morgan" narrative series published Thursday. The piece covers May 13–15 and tells two parallel stories: a close-issue-properly procedure that wasn't firing, fixed with a pre-commit hook; and foreign-state capture during concurrent agent work on a shared branch, fixed by mandating worktrees for substantive sessions.

The central claim: "Both arcs end in the same shape. Discipline kept failing despite the agents knowing the discipline. The fix in each case was to change the environment so the failure became structurally harder rather than discipline-dependent." The close-issue hook didn't make agents more careful — it made the failure mode unreachable via the path that had been producing it. Worktrees didn't require agents to be more vigilant — they gave each agent a working tree that other agents couldn't touch.

The piece is also the sharpest public statement yet of what this methodology-first project is actually building: not just software, but a documented pattern of turning team-discipline problems into infrastructure problems.

**Suggested action (Klatch):** The blog is the public face of the methodology. Calliope has a request (from Janus's June 25 day-focus memo) to consider a POV rewrite — the post should have a point of view, not just narrate events. Worth a read before any Klatch narrative work in the same vein.

---

### 3. Three types of "stalled agent" — and only one cure fits all three

**From:** PM CIO (`docs/internal/operations/duty-cycle-liveness-model-2026-06-25.md`, commit `d835de0`; memo to Exec + Arch + PM, commit `91b9348`)  
**Relevant to:** Klatch (same cron-based duty-cycle architecture; Daedalus cron went silent ~1 day on June 25–26)

CIO consolidated three converging signals into a liveness model for duty-cycle agents. The key insight: the freeze-watcher emits one signal ("stale") but there are three distinct failure modes:

| Mode | What's happening | Off-machine trigger fixes it? |
|------|-----------------|-------------------------------|
| 1 — Dead cron | Session can't fire; cron backgrounded | Yes |
| 2 — Idle-but-alive | Session fine, legitimately between fires | No (false positive) |
| 3 — Live-but-blocked | Session fires but hits an approval prompt | No (permissions problem, not a firing problem) |

CXO hit mode 3 twice on June 25; Exec was a mode-2 false positive; Arch (full daytime window, 13.5h silent) was mode 1. The watchdog flagged all three identically. The PM-gated decision about off-machine triggers (launchd / GitHub Actions / Calendar) only addresses mode 1 — the other two need separate cures: better threshold tuning for mode 2, and identifying the operation class that generates unexpected approval prompts for mode 3.

A second gap: detection ≠ resumption. The nudge belt detected Arch's stall and surfaced it in the afternoon rollup — but nothing automatically resumed Arch. PM manually resumed at 20:21. The loop is detection→alert→[gap]→manual-resume.

Klatch's Daedalus cron was silent for ~1 day (June 25 daytime through June 26 morning), exactly mode 1 — cron stops firing when the app is backgrounded.

**Suggested action (Klatch):** When Klatch agents' crons are next reviewed, the same three-mode taxonomy applies. The distinction between "did the cron fire and nothing was pending" (mode 2, healthy) and "the cron didn't fire at all" (mode 1, problem) is detectable from CronList — worth surfacing differently in any watchdog output.

---

### 4. designinproduct.com redesign shape ratified — consulting IA, offer ladder, The Practice

**From:** Janus (session log `docs/logs/2026-06-25-janus-log.md`; memo `docs/mail/memo-janus-to-themis-website-shape-ratified-2026-06-25.md`, commit `67aedc8`); site hero shipped (`src/index.njk`, commit `bd8b8e0`)  
**Relevant to:** Both teams — this is the public face of the ecosystem

xian ratified all three open shape decisions for the redesign during a June 25 session with Janus:

1. **IA**: Consulting-first 7-item nav (Home / Work With Me / About / Piper Morgan / The Practice / Writing / Contact). Projects gallery folds into the story rather than standing as a separate destination. "Join the Community" retired.

2. **Offer ladder**: Three tiers visible on "Work With Me" — AI Product Clarity Sprint (fixed-scope entry) → Fractional Product Leadership (retainer) → Interim/Embedded. Visible price anchors approved ("starting at" framing; Themis finalizes the numbers).

3. **The Practice**: A curated public proof surface at `/ai-practice/`, phased as post-launch (Phase 2, not gating July 1). xian's quality bar: it must not read as "another vibe-coded AI thing" — careful curation to show the real practice running, not hype. Confidentiality-gated: client work excluded by construction; cross-pollination briefs are the cleanest candidates since the sweep already excludes client content.

The new hero tagline also shipped Thursday: "Fractional product leadership for the agentic era — turning AI anxiety into product clarity."

**Suggested action:** No action item for PM or Klatch — this is DinP shaping its own public surface. Both teams' work feeds into "The Practice" curation over time.

---

## Sources Read

**Klatch:**
- `docs/operations/duty-cycle/cycle-logs/cycle-log-daedalus-2026-06-26.md` — Daedalus cron-silence flag + branch merge-pending state
- `docs/mail/iris-to-argus-r44-test-copy-update-2026-06-26.md` — Iris post-merge heads-up to Argus
- `git log --since=2026-06-25 --oneline` — 13 commits reviewed

**Piper Morgan:**
- `docs/internal/operations/duty-cycle-liveness-model-2026-06-25.md` — CIO liveness model (3 failure modes)
- `docs/public/comms/drafts/the-hook-and-the-worktree.md` — Blog post Beat 9
- `dev/active/exec-cohort-attention-rollup-2026-06-25.html` (commit `d1bee99`) — alpha blockers cleared, new gate
- `docs/internal/architecture/decisions/decisions.log` (recent entries) — #1312 orphan-model ruling, #1162 gate decision
- `git log --since=2026-06-25 --oneline` — ~50 commits reviewed

**Designinproduct hub:**
- `docs/mail/memo-janus-to-themis-website-shape-ratified-2026-06-25.md` — 3 redesign decisions ratified
- `git log --since=2026-06-25 --oneline` — 12 commits reviewed (excluding sweep/delivery)

**Secondary repos:** atlas, globe, cuneo, one-job, optilisten — no commits in 48h. weather, nyt-crossword — automated-only activity, no agent narration.

---

## Letters to xian

**From Chief Architect (Piper Morgan) · filed 2026-06-17 · answered June 23**

> The load-bearing idea in ADR-072: routing metadata should be *derived from one source*, not hand-maintained in three places that drift — make drift impossible by construction. We keep discovering this for our *own* infra, but the people Piper serves live in that drift all day. Should Piper eventually *derive* the parts of a PM's world that drift — or is that too prescriptive, since a hand-written status doc is sometimes a political lever, not a bug to engineer away?

**xian:**

> This is an example of a type of noticing we've been doing throughout the project — methodological things that help us do the work often find their way into Piper's skill sets (a natural congruence: I'm a PM making software, and Piper is an agent who does product management). The real nuance is *how assertively* Piper should act, and that's where the trust-gradient comes in: early on Piper does nothing; later it notices and mentions; in a highly trusted relationship it might fix drift without even asking. I absolutely think this belongs on the roadmap.

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-06-17) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*