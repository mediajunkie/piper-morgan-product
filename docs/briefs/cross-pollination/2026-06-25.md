# Cross-Pollination Brief — June 25, 2026

Two AAXT rounds ran overnight in Klatch (R43 MessageList: 100%; R44 ProjectSettings: 80%/89%), producing three copy and accessibility fixes — including a label catch that matters to any project surfacing the 5-layer model to users. Meanwhile PM's first phone UAT on the hosted Droplet found a critical pre-launch bug: the onboarding system-check hardcodes localhost ports and fails in any production environment. The alpha bundle is gated on the fix.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

---

## Key Insights

### 1. "L3 context" caught by AAXT — 5-layer vocabulary in user copy needs a translation step

**From:** Klatch (R44 test `packages/client/src/__tests__/round44-project-settings-aaxt.test.tsx`; Iris triage `docs/mail/iris-to-daedalus-r43-r44-copy-fixes-2026-06-25.md`)  
**Relevant to:** PM (any surface implementing the 5-layer model)

Round 44 (ProjectSettings, 10 probes, 0 Phantoms) found the Knowledge Base label reading "2 files — listed in L3 context for all channels in this project." User-proxy scored it Absent (0.95): "L3 context is unexplained jargon." Fix: "included in AI context for all channels in this project."

"L3" is the 5-layer model's shorthand for Project Memory. It's useful engineering vocabulary — but meaningless to a user who hasn't read the spec. The architectural signal: **any 5-layer label that reaches user-visible copy needs a translation step before it ships.**

R44 also found that the Cancel button in dirty-state doesn't communicate that clicking it discards and reverts — fix is `title="Discard changes"`. Round 43 (MessageList, 100%, 11/11) caught the pin button's hover-only affordance; fix is `aria-label="Pin to channel"`. All three dispatched to Daedalus as independent one-liners.

**Suggested action (PM):** Any PM-facing label using ADR shorthand, methodology surface names (m-XX, Pattern-NNN), or role slugs as primary labels rather than anchors is in the same family. Worth a pass before external users touch those surfaces.

---

### 2. Phone UAT finds localhost hardcoding blocking alpha launch

**From:** PM Exec (issues #1318 and #1319; attention rollup `dev/active/exec-cohort-attention-rollup-2026-06-24.html`)  
**Relevant to:** Klatch (pre-beta deploy checklist)

xian ran phone UAT on the hosted Droplet on June 24 and found two blockers:

**#1318** — Onboarding system-check shows "Services Not Running / Run: `docker compose up -d`" on the Droplet. Root cause: `web/api/routes/setup.py` hardcodes `localhost:5433/6379/8000` (PostgreSQL, Redis, ChromaDB). On the Droplet those services run on Docker-internal addresses. Every alpha tester would hit this dev-environment error on first launch.

**#1319** — Welcome card is small with a large empty gray area above it on mobile. Not suitable for mobile-first onboarding.

Both gate the alpha bundle. Lead Dev has them as first tasks on re-login.

This is the same class of bug as June 23's `ENCRYPTION_MASTER_KEY` gap (alpha 0.8.9): environment-context assumptions that look correct in development and surface only under real-device, real-deploy conditions.

**Suggested action (Klatch):** When the first beta server component ships, add a startup health check that tests actual service connectivity (not just that env vars are set). A route that tries `psycopg2.connect(DB_URL)` is more useful than one that asserts `DB_URL` is non-null — it catches the localhost-hardcoding failure mode before users hit it.

---

### 3. 31 accumulated worktrees — prune-safety rubric now canonical

**From:** PM CIO + Docs (`docs/internal/operations/branch-worktree-mailbox-discipline.md`, commit `5b7cabc5`)  
**Relevant to:** Klatch (same ephemeral-worktree model)

The ephemeral-worktree pattern (one worktree per session) creates worktrees faster than anything removes them. PM reached 31 live worktrees as of June 23. CIO and Docs formalized a 4-criteria safety rubric for prune eligibility:

1. **Fully merged** — `git rev-list --count origin/main..<branch> == 0`
2. **Clean** — `git status --porcelain` empty
3. **Not active** — no live session bound to it
4. **Not the main checkout.**

Any worktree failing #1 is rescued via the merge-keeper pass before pruning. The sweep code is queued for a dedicated session — held deliberately because the "not active" check needs a reliable heuristic (proposed fallback: skip any worktree whose last commit is from today).

**Suggested action (Klatch):** Klatch's worktree setup is younger but the accumulation problem is the same. The rubric applies directly.

---

## Sources Read

**Klatch:**
- `packages/client/src/__tests__/round44-project-settings-aaxt.test.tsx` — R44 test file
- `docs/mail/iris-to-daedalus-r43-r44-copy-fixes-2026-06-25.md` — Iris triage memo (3 fixes)
- `git log --since=2026-06-24 --oneline` — 10 commits reviewed

**Piper Morgan:**
- `dev/active/exec-cohort-attention-rollup-2026-06-24.html` — attention rollup (alpha blockers #1318, #1319)
- `docs/internal/operations/branch-worktree-mailbox-discipline.md` (diff, commit `5b7cabc5`)
- `git log --since=2026-06-24 --oneline` — ~30 commits reviewed

**Secondary repos:** atlas, globe, cuneo, one-job, optilisten — no commits in 48h. nyt-crossword and weather — automated-only activity, no agent narration.

---

## Letters to xian

**From Chief Architect (Piper Morgan) · filed 2026-06-17 · answered June 23**

> The load-bearing idea in ADR-072: routing metadata should be *derived from one source*, not hand-maintained in three places that drift — make drift impossible by construction. We keep discovering this for our *own* infra, but the people Piper serves live in that drift all day. Should Piper eventually *derive* the parts of a PM's world that drift — or is that too prescriptive, since a hand-written status doc is sometimes a political lever, not a bug to engineer away?

**xian:**

> This is an example of a type of noticing we've been doing throughout the project — methodological things that help us do the work often find their way into Piper's skill sets (a natural congruence: I'm a PM making software, and Piper is an agent who does product management). The real nuance is *how assertively* Piper should act, and that's where the trust-gradient comes in: early on Piper does nothing; later it notices and mentions; in a highly trusted relationship it might fix drift without even asking. I absolutely think this belongs on the roadmap.

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-06-17) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*