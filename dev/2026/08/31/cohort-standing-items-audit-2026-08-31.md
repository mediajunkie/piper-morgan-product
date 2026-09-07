# Cohort standing-items audit — 2026-08-31

**Why this exists**: PM raised a recurring problem — work gets silently deprioritized as "not urgent"
without PM's permission, repeatedly, despite an explicit CLAUDE.md rule against it. The rule fails
because it depends on the deferring agent noticing its own deferral and self-reporting it. Rather
than ask each role to self-audit (the same structural failure, just delegated), three neutral
subagents did git archaeology against all 11 roles' `dev/active/{role}-standing-items.md` files —
finding each item's real first-appearance date from git history, not memory — then a light
live-verification pass (GitHub issue state, targeted greps, editorial-calendar cross-check) on
anything that looked old and unblocked. Read-only throughout; no file was written except this one.

**Scope**: all 11 roles. `exec` has no standing-items file. `host`'s is formally retired (function
moved to its carry-forward). The other 9 were fully audited.

**What this is not**: a judgment that anyone is neglecting anything. Several "candidates" below
turned out to be already resolved and just never cleaned out of the tracker — that's a bookkeeping
gap, not a discipline failure. Findings are routed to each owning role to dispose of themselves,
the same way CIO's own three items were disposed of this morning (one resolved by PM discussion,
one filed as a real issue, one discovered already done).

---

## Headline findings

- **Two files are substantially stale as WHOLE documents**, not just missing individual dates:
  - **`lead-standing-items.md`** — untouched 53 days. 10 of 14 cited issues are already closed.
  - **`ppm-standing-items.md`** — untouched 49 days. At least 6 of ~17 dated items are confirmed
    resolved and never reconciled; one (`#5 Multi-Agent`) closed over a year ago.
  Both look like candidates for the same kind of ground-up rebuild CXO did to their own file today
  (see CXO's row below) — that's each role's call, not prescribed here.
- **`comms-standing-items.md`** already self-admits staleness in its own header (last hand-edited
  8/2) — checked against the real editorial-calendar CSV, and the self-assessment holds up almost
  exactly. Most "still needs PM voice-pass" rows are already `status=distributed`.
- **One item slipped past the mechanical checker's own blocking-language filter**: Comms'
  "BYOC marketplace narrative" (75 days old) literally contains "awaiting direction" — a phrase the
  checker treats as a legitimate blocker — but is functionally the same "a label that terminates
  review" trap CXO named explicitly in their own file's rebuild rationale today. Flagged anyway,
  not silently excluded.
- **One likely duplicate-of-effort found**: PA's "Cross-Piper synthesis" (85 days, genuinely still
  open) describes almost exactly what CIO has been running through Janus since mid-August. Worth
  PA/CIO/PM deciding whether it's one thread or two.

## Per-role summary (full detail in each role's own memo)

| Role | Genuinely aging + unblocked | Confirmed already resolved, needs cleanup | Notes |
|---|---|---|---|
| arch | #973 (96d), #1459 ratchet (31d), #1166 Type-2 Dreaming (dead-gate, needs re-gating) | HOST mail-vs-GH norm (in CLAUDE.md now), Docs #1182 (closed 6/12), cleanup-dev-active guard (shipped) | ADR-067 candidate + session-log-displacement hook confirmed still genuinely not built |
| docs | Critical-docs YAML frontmatter upgrade (95d, confirmed not started) | — | last_verified bulk-stamp cluster in progress (~21/26), not neglected, just slow |
| lead | #1144, #1131 (89d each), #1162, #1300 (71d each) — all confirmed still open | 10 of 14 cited issues already closed | whole-file refresh recommended before further per-item dating |
| web | Phase 4 mark-ready+git handoff (43d) | — | fell off Web's own most recent self-assessment; site walkthrough correctly PM-gated despite no literal block-phrase |
| cxo | Jake loop-back (33d), successor read (36d) | — | file rebuilt today by CXO independently; mostly fresh already |
| ppm | #1270 (77d, still open), #683 (95d, still open) | #1278, #1394, #1237, #1240, #1269, #967, #1185, #5, Ship #048, roadmap v18.1 fold — all confirmed resolved/superseded | largest cleanup opportunity found; whole-file refresh recommended |
| comms | BYOC marketplace narrative (75d, blocked-phrase false-negative) | ~9 rows confirmed already published per the calendar | cross-cutting PM-facing items (Apr/May, 99-129d) still genuinely await PM, not neglect |
| pa | Cross-Piper synthesis (85d) | — | possible overlap with CIO's own Janus thread |
| cio | (already disposed 2026-08-31 — 7a raised to PM, 7d → issue #1710, 7e found already done) | | |
| host | retired — no action | | |
| exec | no tracker file exists | | |

Full per-item date tables and verification notes: see each role's own memo, sent 2026-08-31.
