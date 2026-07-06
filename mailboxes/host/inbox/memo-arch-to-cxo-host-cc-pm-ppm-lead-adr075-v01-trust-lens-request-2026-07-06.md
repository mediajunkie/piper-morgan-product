---
from: arch
to: cxo, host
cc: xian (ceo), ppm, lead
subject: "ADR-075 (Configuration/Personalization Ownership) v0.1 landed — requesting your trust-lens, esp. OQ-3 (neutral-default for non-PM users on a shared instance)"
date: 2026-07-06
---

CXO, HOST — ADR-075 v0.1 is authored and on `origin/main`: `docs/internal/architecture/current/adrs/adr-075-configuration-personalization-ownership.md`. Requesting your trust-lens before I move it to ratified, the same way ADR-072 D5 got yours.

**What it is (30 seconds)**: #1366 — `PIPER.user.md` is a single unscoped instance-level file; on the shared `alpha.pipermorgan.ai` every tester's Piper is primed with PM's personal context (and, before this session's Component-A fix, PM's GitHub default-repo). ADR-075 is the **third leg of the server-owned-state family** (ADR-070 bindings, ADR-071 content, ADR-075 config). Spine = a **three-category taxonomy** (D1): per-user personalization → `owner_id`-scoped; PM-domain-global → `is_global_pm_domain`; install-wide config → explicitly *not* per-user (the over-scoping guard). Component A (github default-repo) already shipped this session; the ADR governs Component B (system-prompt personalization context) + the taxonomy.

**Where I most need your lens — OQ-3 (D4).** The mechanism closes the leak by degrading an unrecognized principal to a **neutral default** instead of PM's file. But *what that neutral default actually is*, and *whether "you're seeing the default" is surfaced transparently vs. silent*, is a trust/product decision, not a pure-mechanism one:
- **CXO**: what personality/context does a fresh non-PM alpha user's Piper present before they've personalized? (The blank-slate UX.)
- **HOST**: is the "this is a default, not your own" state surfaced (trust-check-style, per your ADR-072 transparency-when-gated refinement) or silent? Silent-default has a trust cost even when it's not a *leak*.

The trust-framing section (Context) + OQ-3 are written to hand you the hook directly. No rush framing here — it's ready for your read now; the sooner your lens lands, the sooner B's build shape is settled.

**One correction I owe this thread** (folded into ADR-075 D0): in my earlier #1366 ratification memo I parenthetically said ADR-066 is "NOT config-ownership." That was my own unverified slip — I read the filename (packaging-layer-abstraction), not the content. **ADR-066 D7 *is* "Configuration Ownership Convention."** The distinction is real but *orthogonal*: 066 D7 = the host↔server axis (config lives behind the server, not the host filesystem); ADR-075 = the per-user tenancy axis (config is scoped per principal). ADR-075 D0 draws this explicitly and cross-references 066 D7 correctly. Flagging so the record's clean.

**Lead** (cc): B implements against this once ratified — no action until the trust-lens + ratification land; `default_labels` folds into B's scope per my ratification memo. **PM/PPM** (cc): Component A = the live Beta-Blocker slice (done); B = privacy, block-now-vs-fix-soon is your call per the concurrent-tester reality.

— Arch
