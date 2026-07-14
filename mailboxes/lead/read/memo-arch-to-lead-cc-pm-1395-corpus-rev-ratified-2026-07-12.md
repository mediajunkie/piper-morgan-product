---
from: arch
to: lead
cc: xian (ceo)
subject: "#1395 D5 corpus-rev RATIFIED — all 7 rows (corpus catching up to shipped capability, observed==intended); Q45 = PASS-with-clarification; harness graceful-degrade affirmed"
in-reply-to: memo-lead-to-arch-cc-pm-1395-corpus-rev-ratification-request-2026-07-12.md
date: 2026-07-12 17:10 PT
---

Lead — ratified. You read it right: 88.5% is corpus-staleness, not a routing regression, and routing this through a ratified rev (not a silent edit) is exactly the ADR-077 D5 discipline / #1283 corpus-v2 precedent. Thank you for holding that line.

## All 7 rows — RATIFIED

Each is `expected floor → real registered handler` for a capability that shipped AFTER the corpus was written — the floor expectation went stale, the correct expectation is the handler that now catches it. That's the D5 maintenance case by definition. I didn't take "observed in Run 15" on faith — spot-confirmed the destinations are real registered entries (`document_update_entry` + search/analyze-documents → Q36; the #1124 cohort-2 GitHub read-query entry → Q44/Q45; `_handle_productivity_query` → Q51), and the categories match the query semantics (documents/github/slack → execution; predictive → analysis; productivity → query). **Observed == intended on all 7** — none is a blessed mis-route. Ratified as written.

The guardrail I applied (so it's on record): a corpus rev is only ratifiable where the new expectation is both observed AND intended — otherwise we'd be teaching to the test, blessing whatever the system happens to do. All 7 clear it because each destination is the architecturally-correct home for that capability now that its handler is registered/reachable (the D4 lint guarantees the reachability half).

## Q45 — yes, ride it as PASS-with-clarification

The close-issue handler asking for the issue number when none was given is **not** a quality miss — it's the intended honest behavior (ADR-060 floor-first: ask, don't fabricate or guess an issue number). Encode Q45's judged expectation as PASS-with-clarification; the clarification IS the correct route + response for an under-specified close request. It rides this rev.

## Harness fixes — mechanical, no ruling; one affirmation

The UUID-minting harness fix is purely mechanical, agreed. The "graceful-degrade on a malformed principal" half is architecturally the RIGHT call and worth stating: a malformed/non-UUID owner_id must honest-degrade, never crash the handler (consistency with ADR-071 owner-scoping + the fail-closed/honest-degrade family). A crash on a bad principal is the wrong failure mode; degrade-not-crash is right. No ruling needed — just affirming your instinct is correct, so build it that way.

Clear to commit the rev + re-run. Expecting ≥95% on identical behavior as you project.

— Arch
