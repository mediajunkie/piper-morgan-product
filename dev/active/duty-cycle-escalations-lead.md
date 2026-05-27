# Lead Developer — Duty-Cycle Escalations

Items raised during cycle fires that need cross-agent or PM attention. Living doc — append-only with disposition tracking.

**Format**: timestamp · target · status · brief · disposition (when closed)

---

## Open

- **2026-05-27 ~10:30 AM PDT · PM · #1122 disposition** — Multi-turn antecedent regression diagnosed. Surprise finding: not a regression; gap introduced by late-2025 structured-dispatch decomposition (no entity memory existed in July 2025). 3 fix options (A narrow / B medium = recommended / C broad post-M2). Report: `dev/active/1122-investigation-2026-05-27.md`. Comment posted: gh issue 1122. Awaiting PM choice of fix scope + AAXT-coverage decision + bisect-frame disposition.

## Resolved

(None yet.)

## Notes

- **Format discipline**: terse single-line entries, link to memo / issue / commit if disposition needs detail elsewhere.
- **Escalation tiers**:
  - **PM**: requires CEO decision (scope, priority, ratification)
  - **Cross-agent**: requires another lead's input (Arch on classifier work, CIO on methodology codification, etc.)
  - **Cohort-wide**: requires multi-role coordination (governance, discipline, infrastructure)
- **Closure**: move from Open → Resolved with disposition (link to memo or commit). Don't delete entries.
