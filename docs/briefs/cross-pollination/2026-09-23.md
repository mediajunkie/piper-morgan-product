# Cross-Pollination Brief — September 23, 2026

Two findings from Klatch's ongoing mutation-testing work, both about reading values from source files by text pattern. Piper Morgan had a busy day — Fly infrastructure migration completed, cohort-wide carry-forward spring-cleaning — but nothing that rises to a transferable insight. Globe shipped its scrubber Phase 1 (15 era keyframes, Explore mode); not brief-worthy by this brief's bar.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. In Node.js ESM modules, `dotenv.config()` runs too late to reach constants read at module top level — Klatch Round 253

**From:** Klatch (Daedalus/Theseus)
**Relevant to:** Any project using TypeScript or Node.js ESM with dotenv

In CommonJS Node.js, `require('dotenv').config()` runs where you put it, before subsequent `require()` calls. In ESM, `import` statements **hoist**: every import in the file evaluates before any statement, including the `dotenv.config()` call that follows them. So a database module that reads `process.env.KLATCH_DB` at module top level — `const DB_PATH = process.env.KLATCH_DB ?? defaultPath` — has already frozen that value to `undefined` by the time dotenv runs. A `KLATCH_DB=…` line in `.env` is silently inert.

Klatch found this because a `KLATCH_DB` value set via `packages/server/.env` (which is found before the repo-root `.env` by the server's `findEnv()` walk) worked fine, while the same value in the repo-root `.env` didn't reach the database path. Three-arm probe driven end-to-end (Round 253): value assigned to `process.env` after the module is imported is honoured; caller-supplied value beats `.env`; `.env` alone at the module-loading entry point is inert.

The fix: read env vars inside functions (lazy reads, evaluated at call time), or use a package-local `.env` that the server's path resolver finds first.

**Suggested action:** If your ESM project uses dotenv and a module-level constant that reads `process.env`, audit whether that read actually receives the value from `.env` — or whether it received whatever was in the environment at module import time. The symptom is silent: the default value kicks in without any error.

---

### 2. A doc comment that quotes a constant's declaration is read as the declaration by text-matching tools — Klatch Round 255

**From:** Klatch (Argus/Daedalus)
**Relevant to:** Any code-analysis or code-patching tool that extracts numeric constants from source files by pattern

Klatch's source-constant reader used a regex that matched the first occurrence of `const NAME = …` in byte order. The codebase uses a house style of quoting the declaration in the doc comment directly above it — `// const FINGERPRINT_LINE_CAP = 50 * 1000` above `const FINGERPRINT_LINE_CAP = 50_000`. The reader matched the comment, not the declaration, returning `50` instead of `50000`. Because the comment was the *first* match, all downstream checks passed.

The compound failure is what makes this worth noting. The error thrown by the numeric reader recommended a different function call as the fix — and that second function also read through the same comment-first reader, returning an identically wrong result. Then the *write path's* post-write verifier re-read through the same reader to confirm the patch succeeded — it confirmed what it had just written into the comment, leaving the real declaration unchanged. Three separate callsites, same wrong reader, each one confirming the others. The problem is in the instrument, so instrument-based verification cannot see it.

Fix (Round 255): mask comments before pattern-matching for constant declarations (`maskComments()` now strips block and line comments before the regex runs). The issue was latent rather than live in the shipped code — no file currently has a comment-shadowed numeric constant — but three live probes call through the reader and any new doc comment in declaration syntax above a constant would have been silently misread.

**Suggested action:** Any tool that extracts values from source code by matching declaration patterns should strip or mask comments before matching — and should verify its results by round-tripping through something that cannot be fooled by the same comment a reader would find. A verifier that re-reads through the same component it just patched cannot detect that component's own errors.

---

## Sources Read

- **Klatch**: `scripts/probe-round253-…`, `scripts/probe-round255-…`, `packages/server/src/__tests__/round253-…`, `packages/server/src/__tests__/round255-…`, commit log 2026-09-22
- **Piper Morgan**: session logs (Arch, Docs, Exec) from 2026-09-22; commit log 2026-09-22
- **Globe**: `logs/2026-09-22-tessera-log.md` — Phase 1 shipped (scrubber keyframes + Explore mode); not brief-worthy
- **One Job, Weather, Mediajunkie, NYT Crossword**: cross-pollination brief deliveries and duty-cycle fires; no brief-worthy content

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
