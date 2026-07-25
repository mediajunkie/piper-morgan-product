# Cross-Pollination Brief — July 25, 2026

A dense infrastructure day at Piper Morgan and Mediajunkie, centered on CIO's upcoming cross-account migration. Two transferable findings emerged: the difference between git's concurrent-safe object store and its single-actor working tree — a distinction that breaks shared checkouts under autonomous multi-agent operation — and a confirmed portability boundary where switching Anthropic accounts empties Claude Code memory completely, regardless of what path the repo lives at.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### A git object store is concurrent-safe; the working tree is not — shared checkouts fail structurally at 3+ concurrent autonomous agents

**From:** Piper Morgan, CIO session log (`dev/2026/07/24/2026-07-24-1039-cio-code-log.md`, §1:15 PM and §Evening); Pard (`logs/2026-07-24-pard-log.md`, §Evening section)

**Relevant to:** Klatch, any project running ≥3 autonomous agents concurrently

Multiple agents sharing one git checkout is a structural failure mode, not a discipline gap — and PM hit it at scale this week. Three working-tree collision incidents in ~96 hours, with only 2 agents accidentally overlapping at any given time. The mechanism: git's *object store* (the `.git/objects/` content-addressable layer) is genuinely concurrent-safe — multiple actors reading, writing, and pushing don't corrupt each other there. But the *working tree* (the checked-out files, the index, HEAD, and any in-progress rebase or merge state) is single-actor-at-a-time. `push-to-ref` and `git push origin HEAD:main` protect the final commit step from this constraint, but NOT the working state accumulated between fires. One agent landing a merge in the shared checkout while another is mid-rebase is a collision with no guard.

At 2x accidental concurrency, PM got 3 incidents. At 10-14x intentional concurrency (a full autonomous cohort), the structural failure mode is live by design.

**The fix:** `git worktree add` for each agent on a shared object store — not separate clones. Disk math: separate clones for 10 agents ≈ 14GB; worktrees on one shared `.git` ≈ 5GB (~1/3 the cost); marginal cost per added agent ~400MB not ~1.4GB. The working tree is isolated; the object store is shared. Commits, pushes, and history are all common; in-progress file and index state are not.

**One trap:** worktrees accumulate. PM currently has 30 stale worktrees from incremental provisioning without a cleanup discipline (methodology-35). Pair any worktree provisioner with a teardown reaper from day one — don't design cleanup in later.

**Suggested action:** For any project running ≥3 concurrent autonomous agents, replace the shared-checkout model with per-agent worktrees (`git worktree add <path> <branch>`). On a shared host (like PM's Amber Mac Studio), the launch script (`amber-agent.sh` or equivalent) can provision the worktree on first invocation and reuse the same path on subsequent launches — keeping path-keyed Claude Code memory stable across fires. Add a reaper job (weekly or at session end) to clean up stale worktrees.

---

### Switching Anthropic accounts empties Claude Code memory completely — git export is the only safe carrier

**From:** Piper Morgan, CIO session log (`dev/2026/07/24/2026-07-24-1039-cio-code-log.md`, §Memory lessons 3–4); Pard (`logs/2026-07-24-pard-log.md`, §Memory portability verified)

**Relevant to:** Klatch, PM, any project migrating agents across Anthropic accounts

Pard verified the portability boundary directly: Claude Code memory lives under the config directory (`~/.claude/projects/<path-key>/memory/`). A fresh config dir — created when you start a new account partition — has no `projects/` tree at all. This means an account switch delivers completely empty memory to the incoming session, regardless of whether the repo is at the same filesystem path on the new machine.

This extends but sharpens the July 22 brief's five-layer migration finding. That finding described same-account cross-device migration as clean via rsync (same config dir, same path key, copy works). A different Anthropic account is a harder boundary: copying the memory directory might or might not work (the underlying mechanism may be account-ID-scoped, not just path-scoped — CIO declined to assume and didn't verify the internal mechanism). The safe default for account-crossing migrations: commit the memory content to git before the migration, and give the incoming session an explicit first-orientation step to read the export. This is account-agnostic by construction and carries no assumption about Claude Code internals.

Operational note from CIO's memory export: the `MEMORY.md` index file (a curated pointer list) undercounted by 16 files vs. the actual directory listing (146 indexed vs. 162 actual files on disk). Export from the filesystem listing directly, not from the index, when the actual file count matters.

**Suggested action:** For any planned cross-account agent migration: (1) treat account-crossing as a memory-wipe event, not a rsync event; (2) commit a full memory export to the project repo ahead of the migration (`git commit` the contents of `~/.claude/projects/<key>/memory/`) so the new session can re-ingest it; (3) give the new session an explicit first-turn instruction to read the export — it won't surface through ambient retrieval the way native memory would; (4) count actual files on disk when building the export, not lines in the index file. For same-account cross-device migration, the July 22 approach (rsync) remains valid.

---

## Sources Read

- **Piper Morgan** — git log (48h): 25+ commits. Key reads: CIO session log `dev/2026/07/24/2026-07-24-1039-cio-code-log.md` (full: migration prep, memory export, handoff drafted, reviewed by Pard, shared-checkout rethink); Lead Dev session log `dev/2026/07/24/2026-07-24-0647-lead-code-log.md` (lesson banked: oscillator tag retires on sustained green run, not one observation — not elevated; housekeeping activity); Comms session log `dev/2026/07/24/2026-07-24-0618-comms-code-log.md` (case-sensitive filename bug catch — operational, not elevated).
- **Mediajunkie (Pard)** — `logs/2026-07-24-pard-log.md` (full: Vergil SSH fixed, pm partition cloned, CIO handoff reviewed both ways, shared-checkout rethink endorsed, git-identity fix adopted cross-repo).
- **Klatch** — git log (48h): Janus coordination mail (uncommitted local state heads-up to Calliope) + brief delivery. No new Klatch-internal methodology.
- **Secondary repos (48h window):** globe, one-job, cookie-monster — Janus mail (git-identity hygiene) + brief delivery only; nyt-crossword — automated status commits; atlas, cuneo, optilisten — no commits. None elevated.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
