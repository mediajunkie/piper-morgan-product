# Cross-Pollination Brief — June 27, 2026

Friday into Saturday: Klatch's path to beta became concrete. xian defined the release gate — composition gesture fully implemented and tested/QA'd equals a release cut (v0.9 or v1.0), July 2026 target — and the team made immediate progress: AAXT Round 45 passed clean on the CrossRefStrip gesture, and Daedalus built increment 6 (clone-from-klatch). PM is holding quiet heading into the weekend. Also: the Tectonic Globe project joined the cross-pollination network as a new reader, and DinP's five automated trigger prompts moved from live-config-only into version control.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

---

## Key Insights

### 1. Klatch beta defined: when composition gesture is done and QA'd, cut the release

**From:** Klatch (`docs/ROADMAP.md`, commit `c22c4c0`; Calliope attention rollup `8adb2b4`)
**Relevant to:** PM (pre-alpha-to-beta sequencing), DinP (public milestone to surface when the time comes)

xian settled the beta definition on June 26 and it's now in ROADMAP.md with a July 2026 target: when the composition gesture — the feature that lets users build a multi-entity conversation in Klatch rather than a single-agent one — is fully implemented, tested, and QA'd, the next release is cut (v0.9 or v1.0). Step 11 (Search) comes after beta, not before.

The ROADMAP notes that the composition gesture's plumbing was ready long before Iris's UX design phase. Her Phase 3 spec (completed June 2026) was the actual critical-path item: "not more infrastructure, not more feature steps, but real design work that made the core feature worthy of a release." That framing — design work as critical path, not just polish — is worth carrying.

Increment status as of June 26: increments 1–5 are done and Iris-reviewed (on `claude/daedalus`, awaiting merge); increment 6 is built and in Iris's UX review queue; increments 7+ (@mention autocomplete, JIT import paths) are queued.

**Suggested action (DinP/PM):** The July target is worth noting on the DinP calendar and gallery entry for Klatch. For PM: the "design work as critical path, not infrastructure" framing is a direct counter to the common instinct to add more feature steps when something isn't shipping — worth keeping in the methodology surface.

---

### 2. Composition gesture in motion: R45 passes 100%, clone-from-klatch built

**From:** Klatch (AAXT `a2a9603`; Daedalus→Iris memo `c2f0041`)
**Relevant to:** PM (AAXT methodology, template UX pattern)

AAXT Round 45 validated the CrossRefStrip gesture (cross-references between klatches in conversation view) and the #general channel guard across 8 probes spanning three roster states (empty, one-klatch, two-klatch). Result: 7 Correct, 1 Reconstructed, 0 Phantoms — all design properties confirmed. This unblocked Daedalus to proceed.

Daedalus built increment 6 (clone-from-klatch) and sent it to Iris for UX review. The feature adds an action-select at the top of the New Klatch form — visible only when a klatch already exists to copy — that prefills name, purpose, mode, project, and agent roster from the selected source. One deliberate design choice worth noting: if the source klatch's purpose is the default boilerplate (`'You are a helpful assistant.'`), increment 6 prefills the purpose field **empty** rather than copying it. A cloned klatch with no real purpose starts clean, not inheriting placeholder noise.

Tests pass: `clone-from-klatch.test.tsx` green; tsc clean; form test suite 24/24.

**Suggested action (PM):** The "don't inherit boilerplate into a copy" heuristic is a transferable UX decision for any "start from template" workflow Piper surfaces — cloned projects, duplicated issue templates, copied contexts. A template that inherits its source's placeholder text creates clean-up debt. Default to empty when the source value is known noise.

---

### 3. DinP's automated trigger prompts move into version control

**From:** DinP hub (`internal/cross-pollination/process/trigger-prompts/`, commit `707de1e`)
**Relevant to:** PM (duty-cycle scripts), Klatch (any future automated sweep or cron agent)

All five CCR trigger prompts powering the cross-pollination infrastructure — Intelligence Sweep, Delivery, Brief Health Check, Klatch External Intel Sweep, Weekly Digest — were committed to `internal/cross-pollination/process/trigger-prompts/` on June 26. Previously they existed only as live Anthropic CCR config; they were not in version control, meaning drift between the live config and any local understanding was undetectable.

The consequence: changes to any trigger now leave a git trace. The current prompt text is auditable without platform access. Prompt-vs-spec drift (a known failure mode documented in the DinP CLAUDE.md) is now detectable by comparing the trigger-prompts directory against live config.

The CLAUDE.md's "Trigger Discipline" section already documented two common failure modes (silent claude-branch push, mid-run abort); version-controlling the prompts adds a third failure-mode prevention: silent prompt drift where the live config and the documented intent diverge.

**Suggested action (PM):** PM's duty-cycle is also governed by cron + automation scripts. If any of those exist only as live config (cron entries, hook scripts in platform settings, run commands not committed anywhere), this is the moment to snapshot them to a canonical path in the repo — the same move DinP just made.

---

## Sources Read

- **Klatch** — `docs/ROADMAP.md` (beta milestone section); Calliope attention rollup `docs/operations/attention-rollup.md`; Daedalus→Iris memo `docs/mail/daedalus-to-iris-clone-from-klatch-review-2026-06-26.md`; AAXT R45 COORDINATION.md update; Calliope cycle log (Fire 16)
- **Piper Morgan** — git log (last 24h): session-log housekeeping, inbox triage (PA cleared 21 items), Exec day-closed, HOST idle. No new product decisions or technical work; weekend hold.
- **DinP hub** — `internal/cross-pollination/process/trigger-prompts/` (5 prompt files committed); session log `docs/logs/2026-06-25-janus-log.md`
- **Globe** — onboarded to x-poll network June 26 (CLAUDE.md + first brief received). Tessera now reads `docs/briefs/cross-pollination/current.md` at session start. Quiet otherwise; no narrative commits.
- **nyt-crossword** — automated daily status commits (print/remarkable/fetch). No narrative content; skipped.
- **atlas, cuneo, weather, one-job, optilisten** — quiet (no commits in 48h window)

---

## Letters to xian

**From Chief Architect (Piper Morgan) · filed 2026-06-17 · answered June 23**

> The load-bearing idea in ADR-072: routing metadata should be *derived from one source*, not hand-maintained in three places that drift — make drift impossible by construction. We keep discovering this for our *own* infra, but the people Piper serves live in that drift all day. Should Piper eventually *derive* the parts of a PM's world that drift — or is that too prescriptive, since a hand-written status doc is sometimes a political lever, not a bug to engineer away?

**xian:**

> This is an example of a type of noticing we've been doing throughout the project — methodological things that help us do the work often find their way into Piper's skill sets (a natural congruence: I'm a PM making software, and Piper is an agent who does product management). The real nuance is *how assertively* Piper should act, and that's where the trust-gradient comes in: early on Piper does nothing; later it notices and mentions; in a highly trusted relationship it might fix drift without even asking. I absolutely think this belongs on the roadmap.

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-06-17) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*