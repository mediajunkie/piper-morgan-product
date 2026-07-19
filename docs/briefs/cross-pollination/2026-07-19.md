
# Cross-Pollination Brief — July 19, 2026

Two findings from different corners of the ecosystem this window. Piper Morgan's Tier-3 cleanup sprint named a distinct failure class — code that lies when reached rather than merely being unreachable — and Dispatch documented a subtle MCP task-launch behavior where a client timeout does not mean the server-side session failed to start.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### "Fabricated" code — reachable but returning plausible-wrong results — is a distinct cleanup class from dead code

**From:** Piper Morgan, Architect + Lead Developer (Tier-3 cleanup sprint, issue #1436, decisions.log 2026-07-18)
**Relevant to:** Klatch, One Job, any project doing code-quality cleanup sprints

During PM's Tier-3 cleanup sprint, the Architect named a class of code that's worse than unreachable dead code: code that can be reached in production but returns plausible-looking fabricated results rather than honest errors. Dead code is silent; fabricated code is actively misleading. The through-line the Architect called out: "fabrication-removal, not dead-code cleanup — code that LIES when reached."

Concrete examples found in PM's codebase:
- **The sleeper** — a flag-gated path in the MCP resources layer was live from the production file-repository, and when the flag was on it returned *simulated* file-search results rather than real ones. No crash, no obvious signal — it would have silently served fabricated data in a beta deployment. Fixed by first severing the live-path dependency (honest-degrade), *then* deleting the fabricated machinery.
- `recovery_strategies` — returned fake "Matched file..." results in its fallback path instead of an honest empty result.
- `token_blacklist.revoke_user_tokens` — returned a success-shaped silent `0` on every call (stub never raised; callers assumed it worked). Fixed to `raise NotImplementedError` explicitly.

The cleanup discipline that emerged: before deciding to delete a piece of cold code, ask not just "is this reachable?" but "if it IS reached, does it tell the truth?" Fabricated code that's reached silently in production can cause worse failures than code that crashes, because it never triggers an obvious error signal.

**Suggested action:** When doing a Klatch or One Job code audit, look for prototype-era code that returns canned or simulated data on any non-error path — demo modes, stub implementations, partial wiring. For each: (1) sever any live-data dependency before deleting; (2) if keeping the stub, make it raise loudly rather than returning a plausible empty result. The distinction between `return []` (plausible, silent) and `raise NotImplementedError("not yet wired")` (loud) matters once the code is reachable from a real user path.

---

### MCP task-launch timeouts can be client-side-only — the server session may already exist

**From:** Dispatch-DinP (standards/SESSION-RESILIENCE-OPS.md, 2026-07-18)
**Relevant to:** Any agent team using Cowork's `start_code_task` for unattended or scheduled sessions

When `mcp__dispatch__start_code_task` returns a timeout error ("MCP error: timed out after 180s"), the task may have been created on the server-side even though the client call didn't confirm it. Observed twice in a single session on 2026-07-18. Retrying without checking first spawns a second concurrent session pointed at the same repository — two agents racing on commits.

The safe pattern, now documented in Dispatch's SESSION-RESILIENCE-OPS.md: **list before you launch**. After a timeout, call `list_sessions` (or equivalent) and look for a session with a matching title and working directory that's running or idle. If a match exists, resume it with `send_message` rather than starting a new task. Only launch fresh when there's genuinely no match.

The session that hit this had a safety net — each duplicate session independently verified nothing had changed and declined to take destructive actions — but that's not reliable as a general backstop. The check is cheap; duplicate racing agents are not.

**Suggested action:** Any Klatch, Piper Morgan, or DinP process that uses `start_code_task` for scheduled or unattended work should add a list-then-check step before treating a timeout as a clean failure. The session-existence check costs one tool call and prevents a class of concurrent-session race that's otherwise invisible until you see duplicate commits or conflicting git state.

## Sources Read

- **Piper Morgan** — git log (48h): 50+ commits. Key read: Architect decisions.log entries 2026-07-18 (Tier-3 Family-1 through Family-3 rulings; `# nie-ok:` mechanism; spatial committed-theory review convened). Lead Dev session activity: fabrication removal executed across Families 1, 2, 4, 6; collection reaches 11,774/0 errors for first time in sprint. Transferable finding (fabrication class) elevated; other activity (family-by-family execution, specific ratchet counts) sprint-internal completions.
- **Klatch** — git log (48h): brief delivery commits only. No Klatch-internal methodology this window; skipped.
- **Dispatch** — git log (48h): 4 commits. Key read: SESSION-RESILIENCE-OPS.md update (start_code_task timeout behavior). Activity-log entry for "Mechanical First, Then Read" Medium/LinkedIn cross-post: publication event only, not reported. Stale-screenshot hazard doc (Medium/LinkedIn specific, not cross-relevant).
- **Secondary repos quiet (48h window):** atlas, cuneo, optilisten (no commits); globe, one-job, weather (brief delivery only); nyt-crossword (automated status commits); mediajunkie (no commits); cookie-monster (brief delivery only).

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
