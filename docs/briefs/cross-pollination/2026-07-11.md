# Cross-Pollination Brief — July 11, 2026

Heavy execution day in Piper Morgan: Fly.io deployment stack live (#1278), field-encryption plaintext-write risk caught and patched (#1387), ADR-070 amended to store logical connector identity rather than topology, and the full sprint LOW-tier backlog (218 issues) resolved. One transferable methodology finding emerged — a structural gap in how scheduled jobs are cleaned up when migrating between scheduling mechanisms.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### Switching a recurring job to a new scheduling mechanism permanently orphans the old one — cleanup must happen in the same session that creates the replacement

**From:** Piper Morgan, CIO (commit `b82b0b8` + `docs(cron-lifecycle)`, July 10; methodology-35 promoted to Proven)

**Relevant to:** Any project running duty-cycle agents or scheduled background jobs, especially where multiple scheduling mechanisms coexist — ephemeral CronCreate vs. persistent scheduled-tasks, different cron shapes, or interval changes across sessions. Klatch (Calliope duty cycle); DinP (Janus + Themis pulse cycles); One Job (Coral / Relay sessions).

When Piper Morgan's Docs role moved their duty-cycle trigger from an ephemeral `CronCreate` job to a `scheduled-tasks` entry (to satisfy a schedule-change request), the new job was created and verified. The old ephemeral job was never deleted. Both then ran independently for an unknown period — two parallel duty-cycle sessions doing overlapping work daily — until Docs noticed two session logs covering the same day's work.

The reason this is structurally harder than other double-fire cases: `CronList`/`CronDelete` only see jobs the *calling session itself* created. `scheduled-tasks` is a separate disk-persistent subsystem with its own listing. Once the migration session ends, neither mechanism can see the other's jobs — so the orphaned predecessor becomes **permanently unreachable**. No subsequent session, and no other mechanism, can delete it. The window for cleanup closes when the session that performed the migration moves on.

**The discipline (the only fix that works):** when migrating a recurring job from one mechanism to another, delete the old mechanism's job as an **explicit, named step of the same migration** — before or immediately after creating the new one, in the same session and turn. Do not defer it to a cleanup pass. Do not assume another session can pick it up later. Verify both surfaces before considering the migration complete.

This instance, combined with the same-mechanism STOP re-arm bug fixed the same day (`fix(duty-cycle-tick): STOP re-arm is delete-then-create, not create-only`) — where creating a new STOP cron without first deleting the previous one also produces two parallel jobs — promoted **methodology-35 (Asymmetric Discipline: creation without paired cleanup)** from Emerging to Proven. The pattern name captures the root cause: creation is visible and memorable; deletion of the predecessor is easy to skip because it's not in the "happy path" mental model of "make the new thing."

**Suggested action:** Audit any scheduled job or cron-style duty cycle for pending mechanism migrations (or past ones that might have left a predecessor). When planning a migration, add "delete old job" as a literal step in the same procedure that creates the new one — before the procedure is considered complete. If a stale predecessor exists and the window has closed, detection is still possible by scanning for duplicate session logs or double-commits for the same role in the same day; the `mcp__ccd_session_mgmt__list_sessions` surface can identify which session owns a stray job, and `send_message` can ask that session to self-clean.

## Sources Read

- **Klatch** — git log (48h): cross-pollination brief delivery commits + one `.gitignore` update (applying July 9 brief suggestion; confirmatory). No new methodology.
- **Piper Morgan** — commit log (48h, full): Fly.io stack live (`2162b6c`–`8fda0c7`); #1387 field-encryption plaintext-write risk caught and patched (`9921a4a`, same day, Arch boundary-check); ADR-070 Amendment A (`30b1cee`, mcp_server_ref stores logical key not topology); sprint LOW-tier 218/218 complete (`d45fd2a`); duplicate-cron root-caused as methodology-35 instance + promoted (`92ed971`, `b82b0b8`); duty-cycle-tick STOP re-arm fixed (`08b2f6b`); briefing-staleness hook uses git commit date not mtime (`76f6b5d`). One transferable finding above; rest operational.
- **atlas, globe, cuneo, optilisten** — no commits in 48h window; skipped.
- **weather, one-job** — cross-pollination brief delivery commits only; skipped.
- **nyt-crossword** — automated status commits; skipped.
- **mediajunkie** — no commits in 48h window; skipped.

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
