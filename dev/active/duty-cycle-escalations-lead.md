# Lead Developer — Duty-Cycle Escalations

Items raised during cycle fires that need cross-agent or PM attention. Living doc — append-only with disposition tracking.

**Format**: timestamp · target · status · brief · disposition (when closed)

---

## Open

- **2026-05-27 ~10:30 AM PDT · PM · #1122 disposition** — Multi-turn antecedent regression diagnosed. Surprise finding: not a regression; gap introduced by late-2025 structured-dispatch decomposition (no entity memory existed in July 2025). 3 fix options (A narrow / B medium = recommended / C broad post-M2). Report: `dev/active/1122-investigation-2026-05-27.md`. Comment posted: gh issue 1122. Awaiting PM choice of fix scope + AAXT-coverage decision + bisect-frame disposition.
- **2026-05-27 ~10:35 AM PDT · PM · #1081 live smoke** — NOTION-SLACK-XREF infrastructure verified green (19/19 unit tests pass; webhook_router → spatial_adapter → response_handler wired end-to-end). Only outstanding AC is live PM-UAT smoke — Slack message with Notion URL flowing through real Slack API. Smoke recipe posted to gh issue 1081. Cannot be driven by agent; awaiting PM at-keyboard window.

## Resolved

(None yet.)

## Notes

- **Format discipline**: terse single-line entries, link to memo / issue / commit if disposition needs detail elsewhere.
- **Escalation tiers**:
  - **PM**: requires CEO decision (scope, priority, ratification)
  - **Cross-agent**: requires another lead's input (Arch on classifier work, CIO on methodology codification, etc.)
  - **Cohort-wide**: requires multi-role coordination (governance, discipline, infrastructure)
- **Closure**: move from Open → Resolved with disposition (link to memo or commit). Don't delete entries.
