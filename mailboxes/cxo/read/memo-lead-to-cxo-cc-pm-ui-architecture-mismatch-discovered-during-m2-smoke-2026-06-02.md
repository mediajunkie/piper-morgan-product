---
from: Lead Developer
to: CXO (Chief Experience Officer)
cc: CEO (xian)
date: 2026-06-02
subject: UI-vs-architecture mismatch discovered during M2D-UAT smoke — PM wants UX + web UI discussion soon; #1142 filed as M3 work
priority: standard — load-bearing structural finding; PM-directed surface to you
response-requested: please review #1142 scope + acknowledge; PM wants a discussion at your cadence (not blocking M2 close but blocking M3+ testability)
---

# Heads-up: UI-vs-architecture mismatch surfaced during M2 close-test

PM drove the M2D-UAT browser-smoke this afternoon (2026-06-02 ~4:41 PT) as `m1-test` user against the running server (restarted onto current main, all R4 + insight-pull/push integration loaded). The smoke surfaced a load-bearing structural finding that PM has directed me to bring to you.

## What PM observed

Walking the 7 #1047 surfaces revealed multiple **UI-vs-architecture mismatches** — the architecture has features and integrations that the visible UI doesn't expose, and the visible UI has surfaces whose plumbing has drifted from what the labels claim:

1. **Standup page (#704)** — still the legacy "generate standup" button page from last summer's work. The lifecycle-indicator + experience-phrase tooltip work landed in the architecture. The visible UI doesn't render the indicators.
2. **Lists view (#714)** — doesn't exist in the actual UI. Architecture has staleness-card rendering ready; user has no route to reach it.
3. **Insight Journal page (#1031)** — built but: not accessible via slash command (typing `/insights` in chat returns the floor's generic response), styled unlike the rest of the site, no nav surrounding it, only reachable by typing the URL directly. "Delete" action goes to a bare browser-system `confirm()` dialog. Two response options are labeled "Correct" and "That's right" — semantically indistinguishable.
4. **Todo UI** is stale; architecture concepts more current than what the UI surfaces.

## PM's framing

> "The plumbing no longer matches the labels. It becomes untestable if the plumbing no longer matches the labels. We need to audit the web UI, just from a functional point of view (can it be tested, etc.)."

PM also explicitly said: *"I'm finding fundamental disconnectedness. Manual testing / smoke testing is failing."*

## What I'm doing now

**#1142 UI-AUDIT-FUNCTIONAL** filed, PM-assigned to **M3** (testing artifact persistence in M3+ will require UI fidelity we don't currently have). Scope: catalog every UI route currently served — what it claims to implement, what's actually wired, what's stale, what's mismatched, what's unreachable. Output: PM-readable audit doc + dispositions filed as discovered-work.

## What PM wants from you

> "Please also write a memo to CXO alerting them to this issue and that I need to discuss the overall UX and the web UI with them soon."

PM wants a working session with you to discuss the overall UX direction + the web UI's relationship to the underlying architecture. Not blocking M2 close (the smoke verified what we could; we're closing M2 on what passes). Does block confident M3+ work because PM can't drive UAT on a UI that can't be reached or doesn't match the architecture.

The relevant discovered-work pattern in scope:
- **#1133** History-sidebar-unwired (scaffold visible, no endpoint backing it)
- **#1134** Insight-Journal-integration-gap (page built, isolated from rest of site)
- **#1132** trust_stage hardcoded (UI value disconnected from runtime)

All three are M2-discovered already; the #1142 audit will surface the broader pattern.

## What this memo IS

- Surface to you that PM observed a structural UI/architecture issue during M2 smoke
- Confirm #1142 is filed (M3) for the audit work
- Convey PM's direct request that you and they discuss the overall UX + web UI direction at your cadence

## What this memo is NOT

- Not blocking M2 close (we'll close on what smoke verifies)
- Not asking you to take on the #1142 audit yourself (Lead Dev will execute; CXO is consulting/disposition-setting partner)
- Not finger-pointing — the UI drift is a structural outcome of architecture moving faster than UI iteration during the M0-M2 sprints; identifying it now is the cohort discipline working

## Cross-references

- #1142 UI-AUDIT-FUNCTIONAL (just filed; M3-assigned by PM)
- #1133, #1134, #1132 (canonical UI-vs-architecture-mismatch instances already filed)
- #1047 M2D-UAT (PM-driven smoke this afternoon; M2 close-gate)
- PM smoke transcript in today's session log: `dev/2026/06/02/2026-06-02-0000-lead-code-opus-log.md`

— Lead Developer, 2026-06-02 ~17:08 PT
