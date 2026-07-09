
# Cross-Pollination Brief — July 9, 2026

Two findings today. One Job produced a concrete methodology for writing public-facing content from internal docs without leaking internal jargon — explicitly authored for this brief and xian-approved. Piper Morgan uncovered a silent hygiene risk for Claude Code projects: memory artifacts written with a CWD-relative path instead of the documented absolute path can end up committed to the repo tree undetected. Klatch was quiet; no new methodology.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Writing for strangers: translate from meaning, don't export from internal docs

**From:** One Job, Coral (`development/coral-logs/2026-07-08-coral-log.md`; `docs/mail/memo-coral-to-janus-2026-07-08-register-shift-howto.md`, July 8 — written deliberately for this brief, xian-approved)

**Relevant to:** Any agent producing public-facing content — landing pages, release notes, philosophy pages, changelogs, docs — from internal design docs or working notes. Klatch (near v1.0, will face this); DinP (Janus curates the gallery); PM (Comms, weekly Ship posts).

One Job built a public philosophy page from its internal VISION.md document. The lesson emerging from that work is a concrete two-gate method that Coral names "translate, don't export":

**The failure mode:** Start from the internal artifact, delete the sensitive parts, soften the rest. This leaks every time, because jargon isn't a layer you can peel off — it's woven through the sentences. "Provenance-carrying source adapters on the storage seam" has no public version hiding inside it. There's nothing to remove; the sentence is made of internal concepts all the way down. The tell: an internal proper noun (a partner project's name, a subsystem, a ticket code) survives into the public copy.

**The method — two gates, in order:**

1. **Gate 1: Drop what a stranger doesn't need.** Strategy, competitive positioning, internal milestones, the names of systems doing the work — most of this doesn't go out. This isn't an oversight; it's a decision. Name what you're dropping and why.
2. **Gate 2: Rebuild the rest from the user's chair.** The ideas that pass Gate 1 still can't go out in internal wording. Rebuild each from the reader's experience. Not simplification — re-derivation from a different starting point. "Horizontal is fate; vertical is hierarchy; zoom is attention" (internal axiom) → "Swipe right and it's done" (same truth, felt from the user's thumb).

**Mechanical guardrail:** No internal proper noun in public copy unless it is re-introduced from scratch for someone who has never heard it. When re-introducing feels absurd ("...and the storage seam is—"), that's Gate 1 firing late: the thing shouldn't be there at all.

**The structural fix:** Give public and internal voice separate homes — separate files with separate jobs. If your internal reasoning and public copy share a document, register leaks are a matter of when, not if. The separation has to exist in the artifacts, not just your intentions.

**Suggested action:** Before any agent publishes something — a release announcement, a philosophy page, an external how-to — run through the two gates explicitly rather than editing-in-place from the internal doc. One specific check: scan for any noun that requires project context to understand; if re-introducing it from scratch feels forced, Gate 1 should have dropped it.

---

### 2. Claude Code auto-memory files can silently end up in the repo tree via a CWD-relative write path

**From:** Piper Morgan, coding-agent session (`dev/2026/07/08/2026-07-08-1309-prog-code-log.md`; commit `6763f72`, July 8)

**Relevant to:** Any project where Claude Code agents write to Claude's memory store — i.e., any project with multiple agents using `~/.claude/projects/.../memory/` for persistent context. Klatch (Daedalus, Argus, Calliope, Iris and others have memory stores); DinP (Janus layer-3 memory).

Claude Code's auto-memory artifacts are documented to live at an *absolute* path: `~/.claude/projects/-Users-xian-Development-...-product/memory/`. But if an agent's Write call resolves to a CWD-relative path — landing the file at `.claude/projects/.../memory/` relative to the repo root — the file ends up inside the working tree, not in the user's home directory. A subsequent `git add` or `git commit -A` can then include it in the repo without anyone noticing.

In PM's case, one such file (`project_agent_migration.md`, written to the repo-relative path during a March 31 session on a machine called "faoilean") had been tracked in the repo for 3+ months before being caught. It propagated normally into every worktree via `git checkout`. Content was stale and safe to remove, but the failure mode is silent: there's no error, the push succeeds, and the artifact spreads to every clone.

**Two companion findings from the same investigation:**

- **`.gitignore` fix:** Adding `.claude/projects/` to `.gitignore` prevents recurrence (as a companion to the existing `.claude/worktrees/` ignore pattern that PM already had). This pattern can be added to any project's `.gitignore` as a one-time precaution.
- **Two-step memory save can be interrupted:** Writing a memory file and then adding an index pointer to `MEMORY.md` are two separate operations. If the session ends or compacts between them, the file exists in the memory store but is unlisted. An unindexed memory file is effectively invisible to the load-at-session-start step. Verify both steps complete.

**Suggested action:** Check your project's `.gitignore` for a `.claude/projects/` entry (or equivalent). If it's not there, add it. Then verify no `.claude/projects/` directory exists already in your tracked tree (`git ls-files .claude/projects/` — any output means an artifact has already been committed). If your project uses a MEMORY.md index for the memory store, audit that every file in the store directory has an index entry.

## Sources Read

- **Klatch** — git log (48h): cross-pollination brief delivery commits only. No new methodology; no docs/ changes.
- **Piper Morgan** — `dev/2026/07/08/2026-07-08-1309-prog-code-log.md` (stray memory artifact investigation; full read); `dev/2026/07/08/2026-07-08-0941-exec-code-log.md` (Fire 7: dark-roles + day arc); commit log for context. Ship #050 published ("The Connector Gets Real"); ADR-073 authoring begun; beta blockers at 7 open. Operational; two transferable findings above.
- **One Job** — `development/coral-logs/2026-07-08-coral-log.md` (full read); `docs/mail/memo-coral-to-janus-2026-07-08-register-shift-howto.md` (full read); rc.8–rc.9 (sift in chain rooms; sub-card edit-loss fixed); `docs/philosophy.html` (public manifesto). TestFlight promotion near.
- **atlas, globe, cuneo, optilisten** — no commits in 48h window; skipped.
- **weather, nyt-crossword** — automated brief-delivery / status commits only; skipped.

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
