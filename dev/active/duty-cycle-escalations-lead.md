# Lead Developer — Duty-Cycle Escalations

Items raised during cycle fires that need cross-agent or PM attention. Living doc — append-only with disposition tracking.

**Format**: timestamp · target · status · brief · disposition (when closed)

---

## Open

- **2026-05-27 ~10:30 AM PDT · PM · #1122 disposition** — Multi-turn antecedent regression diagnosed. Surprise finding: not a regression; gap introduced by late-2025 structured-dispatch decomposition (no entity memory existed in July 2025). 3 fix options (A narrow / B medium = recommended / C broad post-M2). Report: `dev/active/1122-investigation-2026-05-27.md`. Comment posted: gh issue 1122. Awaiting PM choice of fix scope + AAXT-coverage decision + bisect-frame disposition.
- **2026-05-27 ~10:35 AM PDT · PM · #1081 live smoke** — NOTION-SLACK-XREF infrastructure verified green (19/19 unit tests pass; webhook_router → spatial_adapter → response_handler wired end-to-end). Only outstanding AC is live PM-UAT smoke — Slack message with Notion URL flowing through real Slack API. Smoke recipe posted to gh issue 1081. Cannot be driven by agent; awaiting PM at-keyboard window.
- **2026-05-27 ~10:25 AM PDT · PM · GH Actions stuck run** — UPDATE: Step A (Settings toggle) tried 2:23 PM — failed. Step B (Phase 1+2 push as volume-reduced trigger) merged 2:31 PM via commit `f372ce793` — stuck run still queued, scheduled workflows not yet fired post-merge. Auth refresh confirmed `workflow` scope; DELETE 403 is state-based not scope-based (only `completed` runs deletable). Path forward: wait ~1-2 hours to see if scheduled events recover post-volume-reduction, OR GitHub Support ticket per Docs's draft language. Phase 1+2 itself successful: filters working as designed (only the 5 workflows whose allow-list includes `.github/workflows/**` fired on the merge push, exactly as planned).
- **2026-05-27 ~10:25 AM PDT · Arch · GH Actions paths-filter sanity-check** — Requested Architect sanity-check on Docs's proposed `paths:` filter taxonomy (services/tests/web/python vs. docs/mail/log vs. config) before Phase 1 commits land. Cross-cutting filter taxonomy will inherit through all future workflows; want it shaped right once. Sent in lane-accept memo above.
- **2026-05-27 ~12:38 PM PDT · PM · #1081 disposition post-#1129 discovery** — Slack inbound structurally unmounted since 2025-10-01 (CORE-GREAT-2D); #1081 live-smoke AC could not pass; filed #1129 SLACK-INBOUND-STRUCTURAL absorbing #1107 with PM-picked path C (Socket Mode rebuild). PM disposition needed on #1081: drop from M2 close-gating (close as superseded-by-#1129) or keep open as post-M2 re-verification tracker?

## Resolved

(None yet.)

## Notes

- **Format discipline**: terse single-line entries, link to memo / issue / commit if disposition needs detail elsewhere.
- **Escalation tiers**:
  - **PM**: requires CEO decision (scope, priority, ratification)
  - **Cross-agent**: requires another lead's input (Arch on classifier work, CIO on methodology codification, etc.)
  - **Cohort-wide**: requires multi-role coordination (governance, discipline, infrastructure)
- **Closure**: move from Open → Resolved with disposition (link to memo or commit). Don't delete entries.
