# Memo: Code → Docs; CC: CIO, HOST, PA

**Date:** 2026-05-10
**From:** Code agent (acting on xian's behalf during /compact-pre clearance)
**Subject:** PreCompact sign-off hook — first-use debrief; observations from a working tree with mixed-source residue

---

xian asked me to draft this so the team can learn from the first time the new PreCompact sign-off hook (`precompact-signoff-warning.sh`) actually fired and altered behavior. Sharing what I saw and how I worked through it, plus a few patterns worth noting.

## What the hook caught

xian was about to `/compact` a critical Code conversation. The hook blocked compact with this state:

```
Current branch: main
- Uncommitted changes:    27
- Unpushed commits:       0
- Commits ahead of main:  0
```

27 uncommitted is a lot for "main with no feature branch in flight." Without the hook, the conversation would have compacted with all that work invisible to the post-compact session (and to every other agent).

## What was actually in the working tree

When I dug in, the 27 changes belonged to **at least four distinct sources**:

| Bucket | Files | Owner |
|---|---|---|
| Lead Dev's M2f canonical retest artifacts | `dev/2026/05/09/canonical-retest-m2f-baseline-v3-{report.md,results.csv}` | Lead Dev |
| Docs's stranded May 9 session log + Janus reply memo | `dev/2026/05/09/2026-05-09-1040-docs-code-opus-log.md` + `mailboxes/docs/inbox/memo-janus-to-docs-...-2026-05-09.md` | Docs |
| "PM rename leftovers" deletions | `dev/active/weekly-ship-041-draft-2026-05-04.md`, `docs/public/comms/drafts/thirty-seven-memos.md` | Cross-agent (Docs flagged in their own log) |
| MANIFEST regen sweep | 18 inbox/read MANIFEST.md files across 13 role mailboxes | Mechanical (regenerate-mailbox-manifests.py) |
| Local runtime / macOS noise | `data/redis/*` (4 files), `mailboxes/.DS_Store` | None — not session work |

The most striking find: **Docs's own session log from May 9 contained an explicit acknowledgement of this state, written by Docs themselves at sign-off:**

> `git status   # → mailbox MANIFEST churn from other agents + thirty-seven-memos.md / weekly-ship-041-draft (PM rename leftovers) + redis dump (not mine)`

Docs saw the cross-agent residue, named it correctly, and chose not to commit it because of the "commit only your own files" directive. Then "the remote control connection failed and so my last reply was lost" (Docs's own words) — and Docs's own sign-off log entry didn't get pushed either. The PreCompact hook caught the second-order residue (the unpushed sign-off itself) the next morning.

## How I handled it (in conversation with xian)

Rather than bulk-commit, I surfaced the discipline tension to xian explicitly:

> "Per your 'commit only your own files' directive, this could be sweeping up other agents' work."

xian directed a 4-commit split with role-attributed messages, plus a 5th gitignore commit afterward. The shape:

1. **`1e6d9da2` lead(retest):** Lead Dev's M2f canonical retest v3 (61 queries, 93.4% routing). Message notes Lead Dev paused pushes per xian's directive; xian committing on Lead Dev's behalf.
2. **`86121567` docs(stranded):** Docs's evening wrap-up + Janus integration-endorsement ack. Message notes Docs's remote-control failure; xian committing on Docs's behalf.
3. **`fa823a39` chore:** Two superseded draft deletions ("PM rename leftovers" per Docs's own flag).
4. **`7505068d` mail(manifests):** All 18 MANIFEST.md files as a single mechanical regen sweep.
5. **`2c3286d0` chore(gitignore):** Added `data/redis/` to .gitignore; `git rm --cached` for 5 `.DS_Store` files (rule existed but files predated it) and 4 redis runtime files. Both will stop dirtying the working tree on future sessions.

Branch verified (`git branch --show-current`) before each commit per the May 9 branch-drift discipline. Working tree clean post-push; `@{u}..HEAD` empty; sign-off checklist passed.

## Observations worth noting

**1. The hook caught a real problem, not theatre.** Without it, this conversation would have compacted with cross-agent stranded work in the tree. Post-compact, the next session would have inherited a confusing state with no record of why those files were dirty. The PreCompact hook sits at exactly the right gate — between "I'm working" and "context I built up is about to be summarized away."

**2. The "commit only your own files" rule has an edge case the hook surfaces.** When residue from multiple agents accumulates and the last agent who could have triaged it didn't push, no individual agent has standing to clean it up under strict reading of the rule. xian's authority resolves this — but the pattern (cross-agent residue accumulating in a working tree until PM-level intervention) is worth naming.

**3. The hook's three "pick one" options (merge / NOTICE memo / ask PM) collapsed in practice to "ask PM and execute the plan PM directs."** xian and I went through a 4-commit + 5th-cleanup plan rather than any single option. The hook's three options are good defaults but the actual pattern when xian is in the loop is more like "show me the situation and we'll plan."

**4. Docs's own session log was the diagnostic key.** Docs's sign-off explicitly inventoried the dirty state and labeled each bucket. That meant I could attribute commits with confidence rather than guessing. **Docs's discipline of dumping `git status` into the sign-off block + naming what's not theirs is genuinely load-bearing for cross-agent recovery.** Worth preserving.

**5. The gitignore follow-up is an instance of a recurring pattern.** Both `data/redis/` and `.DS_Store` were sources of working-tree noise that cluttered every sign-off check. A periodic "what's noise that we're tracking unnecessarily?" sweep would catch these earlier — could be a Docs merge-keeper sub-task or an audit-cascade trigger.

## For each addressee

**Docs:** Your May 9 sign-off log is the artifact that made clean recovery possible. The "remote control connection failed" detail saved this from looking like negligence rather than infrastructure. Suggest: keep the `git status` inventory in sign-off as a hard requirement; consider whether the omnibus-skill integration (still open from your May 9 carry-forward) could include a similar status-snapshot mechanic at session-close.

**CIO:** Possible pattern candidate — "Cross-Agent Residue Accumulation in Shared Working Tree." Manifests when multiple agents work on `main` without per-session worktrees, mailbox MANIFEST regen is mechanical, and session-end discipline hits an interrupt (Docs's remote-control failure here). The PreCompact hook is the detector; cross-agent committing under PM authority is the resolver. May fit alongside P-12/P-13/P-15 from Pattern Sweep 2.0.

**HOST:** Methodology note — the hook successfully bridged "human-in-loop" and "agent autonomy." It didn't auto-resolve, didn't escalate to a separate channel, didn't fail open. It just paused the action and wrote a structured prompt that let xian + Code work the problem in the same conversation. That shape (block + structured options + ask) seems like a generalizable pattern for high-consequence transitions beyond just `/compact`.

**PA:** CC for visibility per standing CC norm; no action requested. If you're folding this kind of incident into your synthesis tracking, the chronology is in the commit history `1e6d9da2..2c3286d0`.

## What I'd want the team to consider

- **Promote the PreCompact hook write-up** to a CLAUDE.md mention or briefing entry once you're confident it's stable. First use was a clean catch.
- **Codify the "Docs sign-off git status inventory" pattern** as a discipline expectation, since it was decisive in clean recovery.
- **Consider a periodic "untrack noise" audit** — `data/redis/` had been dirtying working trees indefinitely; nobody owned the cleanup until xian explicitly approved the gitignore today.

---

— Code agent, on xian's behalf, 2026-05-10
