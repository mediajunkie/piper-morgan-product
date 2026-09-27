
# Cross-Pollination Brief — September 27, 2026

Three findings today, two from Mediajunkie and one from Klatch. Pard found that a monitoring manifest entry with an unrecognised expected-state silently reported healthy — the checker couldn't interpret its input, fell through both branches, and had been dismissing true positives. A related finding from the same session: verifying a process is foreground is not the same as verifying it can do work; transcript birth — whether the session has written even one file — is a more reliable liveness check than process-state inspection. From Klatch, Daedalus added 99 tooling scripts to the typecheck gate and found three latent bugs that had been invisible because `scripts/` was outside any tsconfig scope.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Ninety-nine tooling scripts were outside the typecheck gate — adding them found three latent bugs — Klatch Round 279

**From:** Klatch (Daedalus, Round 279, 2026-09-26)

**Relevant to:** Any TypeScript project with tooling, test scripts, or infrastructure code in a directory not covered by the main `tsconfig.json`.

Daedalus added `scripts/*.mts` — 99 files — to Klatch's typecheck gate by creating `scripts/tsconfig.json` and chaining `typecheck:scripts` into `npm test`. The first run produced 20 type errors. Three were real defects, not type noise:

- `probe-browse-count-vs-persisted-rows.mts:73`: passed `isHumanTurnBoundary` to `.filter()` by reference, binding the function's index argument to its `opts` parameter. Inert only by luck.
- `probe-browse-endpoint-second-corpus.mts:518`: dereferenced a nullable value on a path an adjacent arm guarded — the arm was wrong, the null check was not.
- `probe-round253:183`: deleted a key off an object TypeScript inferred as `{ PORT: string }`, which the typechecker correctly rejects.

The remaining 17 errors were type noise (missing declarations, unannotated parameters) cleared with hand-written `.d.mts` shims. None of the three defects had ever been flagged because no typecheck had ever run against `scripts/`.

Daedalus also noted: adding the gate drove Round 245 red immediately on first contact — `gate-line.mts`, a new file, had been added to the coverage floor but not to the probe's module census. The gate caught its own blind spot.

**Suggested action:** Check whether your tooling, test, or infrastructure scripts are included in any `tsconfig`. A common pattern is for `src/` and `test/` to be well-covered while `scripts/` or `tasks/` accumulates unchecked code. Adding a dedicated `scripts/tsconfig.json` — using the same compiler options as your main config for comparability — and chaining it into your test command costs little and has already found real bugs in at least one project. (Klatch `scripts/tsconfig.json`; commit `724371e5`.)

