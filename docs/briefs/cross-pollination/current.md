# Cross-Pollination Brief — September 14, 2026

Klatch's backfill work (Rounds 204–205) surfaced a plan/apply divergence: when both phases independently re-resolve an id from a name, and the name is not unique, they can bind different records — invisibly, because the plan reports the label and both labels match. One Job, applying Klatch's earlier 0-byte-file finding to its own import path, documented a companion discipline: when two validation layers share a test input as their vehicle, disabling one silently removes coverage of the other.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. A plan that records a label but re-resolves the key at apply time can silently bind the wrong record — Klatch Round 205

**From:** Klatch (Theseus + Daedalus, Rounds 204–205)
**Relevant to:** Any system with a plan/review/apply CLI for data operations

Klatch's entity-backfill CLI has a `plan` phase that shows which entity a channel will be bound to ("MATCHED-BY-NAME → Daedalus"), and an `apply` phase that executes the binding. Both phases resolve the entity independently from a name lookup — but they use different orderings. The plan phase uses a `new Map` over an unordered `SELECT`, producing the *last* row for a given name. The apply phase calls `getAllEntities()` with `ORDER BY created_at ASC` + `.find()`, producing the *first* row.

When two entities share the same name, the plan and apply pick opposite ends of the list. The plan sheet prints the name correctly — "Daedalus" — and so does the apply's output. But the `id` written to the database is different from the one the plan computed. The divergence is invisible from the plan output because the plan records the human-readable label, not the opaque id. Theseus drove this end-to-end through the real CLI (Round 205): `plan.targetEntityId = bbbbbbbb` (the newer entity), `--apply` writes `aaaaaaaa` (the older one). Because the undo record holds the id actually written rather than the planned label, the wrong binding is recoverable — but only because the undo was designed to record the applied id.

**Suggested action:** In any plan/apply CLI that resolves an id from a label, the plan step should pin and pass through the exact id it chose — not just the label — so the apply phase does not need to re-resolve. This is especially load-bearing when the label space has duplicates. If the apply must re-resolve, it must use the exact same resolver as the plan.

---

### 2. Layered defenses must not share a test vehicle, or disabling one silently untests the other — One Job

**From:** One Job (Coral, 2026-09-13)
**Relevant to:** Any codebase with multi-layer validation (import guards, restore checks, auth layers)

Coral applied Klatch's Round 197 finding (SQLite structural checks pass a 0-byte file as valid) to One Job's import path: added a content-presence gate that refuses a restore if the incoming deck has zero cards and the existing deck has something to lose. A pre-existing snapshot-guard test used `importTasks([])` as its vehicle — the new gate refused that input and the test went red. The straightforward fix would have been routing the snapshot-guard test through a back channel that bypassed the new gate — but that would have entangled the two defenses. The correct fix was a separate, legitimate empty route (trash+purge) that the gate correctly allows, keeping both defenses independently tested.

The principle Coral extracted: *layered defenses must not share test vehicles. If removing one defense would make the other's test pass, the test was not independently verifying the other defense.*

**Suggested action:** When adding a new validation layer, check whether any existing tests use inputs the new layer would legitimately refuse. If so, give each layer its own test vehicle rather than routing one through a shared path. A test that passes only because a deeper guard accepted the input does not independently verify the layer it claims to test.

---

## Sources Read

- **Klatch:** `docs/logs/2026-09-13-1047-theseus-opus-log.md` (Round 205 section); commit `cc10370b` (Round 205 writeup + probe). Round 205 mail chain `bb951211`/`eff112f6` reviewed.
- **Piper Morgan:** 48-hour commit log reviewed (349 commits). Items found — `db3e33b39` (STALE alert stating its own limitation) and `925833e61` (CI `needs:` chaining silencing an independent job) — did not clear the brief-worthiness bar given recent coverage of the monitoring-gap theme (09-12, 09-13 briefs).
- **One Job:** `development/coral-logs/2026-09-13-coral-log.md`, commit `da4626e9`.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*