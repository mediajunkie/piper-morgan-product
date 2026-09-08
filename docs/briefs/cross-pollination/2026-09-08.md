# Cross-Pollination Brief — September 8, 2026

Two findings from Piper Morgan today, both about verification failures that are easy to confuse with adjacent, more-discussed shapes. One adds a third type to the project's verification taxonomy; the other surfaces a real collision risk in how concurrent subagents are launched.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Corrections to the record

### September 6 brief: one-job was not quiet — 27 commits including the App Review submission

The September 6 brief stated that all secondary repositories were quiet. In fact, one-job had **27 commits** in the window, including the largest event in the project's history: **One Job 1.0 submitted to App Review on 2026-09-05** (build 37, `838eabb`). The secondary-source scan ran `git log --since=…` against a stale local HEAD with no prior fetch and no explicit `origin/main` reference — an absence-from-the-mirror reported as an absence-from-the-repo.

The defect was found by Coral (One Job) and root-caused the same day. The sweep's fetch-first / explicit-`origin/main` fix has been in production since the September 7 brief. *Carried from `pending-corrections.md` per Step 2.4.*

### September 7 weekly digest: covered August 24–30 instead of August 31–September 6

The Monday digest published a window heading of "August 24–30" — a window the August 31 digest had already covered — so the week of **August 31 – September 6 was silently dropped** from the weekly digest series. That week included One Job 1.0 submitted to App Review, Klatch's multi-root session scanner shipped and import-tested at real size, PM's methodology-50 filed, and DinP's Colorado proposal locked at $107,280.

The digest prompt was patched on September 7 to compute its window explicitly and refuse to publish if the new window does not start after the previous digest's end date. **The August 31 – September 6 week has not been published**; the next digest run should cover it before resuming normal cadence. *Carried from `pending-corrections.md` per Step 2.4.*

## Key Insights

### 1. "Open the artifact" is a third verification shape, distinct from "described is not running" and "state your bound"

**From:** Piper Morgan (CIO, methodology-52, filed 2026-09-07)
**Relevant to:** Klatch, any project where agents reason from document titles or memory

Piper Morgan's methodology corpus now distinguishes three closely related verification failures:

- **m-49 ("Described Is Not Running")**: a mechanism is documented or believed to exist, but isn't actually live. Fix: add a live check or a behavioral test.
- **m-51 ("A Bounded Search Is Not a Total")**: a result was scoped (first N, a time window) but the scope went unstated. Fix: state the bound at the moment of the claim.
- **m-52 ("Open It — A Summary Is Not Its Contents")**: the artifact is static, present, and readable — no runtime state to check, no tool to run — but the agent reasons from its title, memory, or a summary instead of opening it. Fix: open the artifact.

The discriminator between m-49 and m-52: m-49 is a live-behavior failure (a runtime check is needed); m-52 is a reading failure (the artifact is sitting there; opening it is sufficient). The discriminator between m-51 and m-52: m-51 is about scope ("I searched N, not all"); m-52 is about substance ("I described the artifact's name, not its contents").

Two instances arrived independently in the same week: CXO's miscitation of methodology-45 (reasoned from the pattern's name rather than reading the entry) and Exec's criterion-3 miss on issue #1386 (reasoned from criterion 3's description rather than reading the actual checklist text). The methodology corpus shrank the candidate family from five instances to two through explicit re-examination — the three that fell away were correctly reclassified into m-49 and m-51 rather than padded into a new pattern.

**Suggested action:** When diagnosing an agent's verification failure, ask which shape it is. Did the mechanism not run? (m-49 — add a live check.) Was the scope unstated? (m-51 — state the bound.) Was the artifact not opened? (m-52 — read the file.) The remedies differ; applying the wrong one doesn't address the root cause.

---

### 2. Two background agents sharing a worktree without isolation is a real, previously unguarded collision risk

**From:** Piper Morgan (Docs, 2026-09-07 omnibus)
**Relevant to:** Klatch, any project using the Task tool to spawn parallel subagents

Piper Morgan's Documentation Management role launched two background agents concurrently via the Task tool to audit separate issues (#1725 and #1724). Both shared the role's live working tree without isolation. They succeeded: one detected the other editing a shared file and explicitly deferred. But mutual deference was luck, not design — no guard prevented a collision, and a collision would have meant a silent overwrite or a conflict surfacing only after one agent's work was already committed and that agent was gone.

The Docs role recorded this as a standing lesson: **use `isolation: "worktree"` on Task-tool invocations whenever two concurrent agents have overlapping file scope in the same working tree.** The flag gives each agent a separate copy; writes don't cross-contaminate; merging is explicit and happens after both are done.

**Suggested action:** Before spawning two or more concurrent Task-tool agents that write to the same directory, check whether their file scope overlaps. If it does, pass `isolation: "worktree"` to each invocation. An explicit merge afterward is a much cleaner failure mode than a silent overwrite.

---

## Sources Read

**Klatch:** `docs/logs/2026-09-07-0831-calliope-sonnet-log.md` (Calliope STOP fire, v111 rollup). Rounds 169–170 reviewed (FLOOR_REPORT constant, floor-frequency probe, worktree sandbox boundary). No brief-worthy new content found beyond what yesterday's brief already covered.

**Piper Morgan:** `docs/omnibus-logs/2026-09-07-omnibus-log.md` (11 sessions; methodology-52 filing and concurrent-agent worktree collision are the primary sources for both insights today).

**Secondary repos** scanned against `origin/main --since="48 hours ago"` with `git fetch` first: globe, weather, one-job, nyt-crossword, mediajunkie, and cookie-monster had commits in the window — none brief-worthy (globe/weather/cookie-monster: brief delivery only; one-job: UPDATE-route title fix applying yesterday's Klatch insight, confirmatory not new; nyt-crossword: automated status; mediajunkie: duty-cycle logs). Atlas, cuneo, and optilisten had no commits in the window. Full provenance in front matter.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

