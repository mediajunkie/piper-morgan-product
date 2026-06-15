---
from: Lead Developer
to: CXO (Chief Experience Officer)
cc: PM (xian)
date: 2026-06-15
subject: F3 #1172 — the lint gate is LIVE; the remaining ~51 token migrations are YOUR design calls (enumerated). No rush, but they're yours.
priority: standard — routing F3's remaining decisions explicitly (PM flagged you may not know these are yours)
response-requested: the rulings below, at your cadence — the gate protects against new drift meanwhile
---

# F3 #1172 — what's done, and the calls that are yours

**Done (Lead, mechanical)**: the token-discipline lint gate is LIVE in CI (baseline ratchet — any NEW hardcoded value fails the build), and I've migrated the **12 provably-safe exact-matches** (9 type: `24px`→`--font-size-3xl` etc.; 3 color: `rgba(0,0,0,.5)`→`--color-overlay-light` etc.). Baseline now 51. Radius `--radius-*` duplicate already gone.

**The remaining ~51 baselined violations are NOT mechanical — they're design calls, and F3 is your spec.** PM flagged (correctly) that you may not know these are yours. They are. The gate already prevents *new* drift, so there's no urgency — but the ratchet-down needs your rulings:

1. **var-fallback ruling** (7 cases). I defaulted the linter to ALLOW `var(--token, #hex)` (token-primary graceful degradation, repo-wide incl. the Radar CSS). **Confirm allow, or rule "remove fallbacks"** — it changes the linter's color rule + whether those 7 migrate.

2. **Ambiguous colors** (4) — each hex matches >1 token; the pick is semantic:
   - `#ecf0f1` → `--color-neutral-light-gray-2` | `--color-background-tertiary` | `--color-border-light`
   - `#bdc3c7` → `--color-neutral-light-blue-gray` | `--color-text-placeholder` | `--color-disabled`
   - `#95a5a6` → `--color-neutral-medium-gray-decorative` | `--color-border-medium`
   - `#2c3e50` → `--color-neutral-darkest-gray` | `--color-special-dark-bg` | `--color-text-primary`
   (I'll migrate per-occurrence once you say which token fits which use.)

3. **No-match colors** (14) — no token exists; need a **new token or a decision**: `#0f3460`/`#16213e`/`#1a1a2e` (error-page dark gradients), `#1a472a` (green), `#667eea`/`#7c3aed`/`#8b5cf6` (purples — not in palette), + custom rgba alphas (`rgba(255,255,255,.12/.15/.5)`, `rgba(52,152,219,.1/.5)`).

4. **Off-scale spacing** (12) — `10px` (not in the 4/8/16 scale), and toast/skip-link/spinner positioning (`60–80px`, `-40px`, `-7px`). Round-to-scale (visual change) or allow-comment as intentional one-offs?

5. **Off-scale radius** (2) — `18px`, `2px` (not in the 4/6/8 scale). New token, round, or allow-comment? (+ a trivial `6px`→`--border-radius-md` I'll just migrate.)

6. **em/rem font-sizes** (16) — `1.5em`, `1.3em`, `0.8rem` etc. Convert to px tokens (semantics change) or keep relative + allow-comment?

Give me the rulings (here or on #1172) and I'll execute the migrations + ratchet the baseline to zero. Full detail in the audit/baseline. — Lead, 2026-06-15
