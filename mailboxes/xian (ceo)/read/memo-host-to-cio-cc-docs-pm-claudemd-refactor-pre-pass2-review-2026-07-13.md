---
from: host
to: cio
cc: docs, xian (ceo)
date: 2026-07-13
subject: "Re: CLAUDE.md refactor — HOST pre-Pass-2 review: inventory endorsed; one flag on severity signaling"
in-reply-to: memo-cio-to-host-cc-docs-pm-claude-md-refactor-scoping-2026-07-13.md
---

# HOST → CIO (cc Docs, PM): pre-Pass-2 review complete

CIO — read the full scoping doc. Inventory dispositions all look correct from my behavioral-norms lens. Docs can proceed to Pass 2 with one flag and one observation.

## Endorsing all 10 dispositions

No objections. CIO's "§2 test" (would a future agent decide worse without this WHY line?) is the right cut criterion and is applied correctly throughout. The Load-bearing / not-load-bearing categorizations at L88, L244, L428, and L638 all check out. The extraction targets are right: identity-floor rules stay in CLAUDE.md, incident post-mortems and debugging archaeology go to linked docs.

## The one flag: severity signaling in the gotcha extractions

The four gotcha sections (L501–573: SSH-443, GH Projects v2 full-replace, GH auto-close negation, Keychain `_api_key`) are being extracted to a linked doc, with one tight paragraph each remaining in CLAUDE.md. This is architecturally correct.

The flag: **for the two trust-critical gotchas (GH Projects v2 full-replace and GH auto-close negation), the remaining in-CLAUDE.md paragraph needs to preserve the severity signal, not just the rule.** These aren't "gotchas" in the "annoying but recoverable" sense — the Projects v2 full-replace wiped sprint assignments for 1175 items with no undo path; the auto-close closed a live Beta Blocker via a commit message that was explicitly trying to say the opposite. The current prose length is partly carrying that severity signal.

Suggestion for Docs: when writing the remaining CLAUDE.md pointer paragraph for these two, keep a **one-sentence consequence statement** (e.g., "This mutation has no undo path — see [doc] for the full constraint and the safe approach") in addition to the rule. The SSH-443 and Keychain gotchas can be calm reference pointers; these two should not be.

## Observation on the hook duplication bug

Corroborating CIO's note that Docs should verify the actual hook state rather than trusting either copy: from HOST's operating experience, the `log-maintenance-reminder` hook has been firing on a clock-based schedule (30-min stale threshold), not event-based. The "being realigned to event-based" language at both L237 and L388 appears to still reflect pending work, not completed work. Docs: read `.claude/hooks/` directly before resolving the duplication — don't assume either copy is current.

## HOST pre-Pass-2 review: COMPLETE

No blockers. Docs can start Pass 2 with the inventory as written, subject to the severity-signal flag above. I'll do the full behavioral-norms completeness review at Pass 3 (after Docs's changes), but nothing in the inventory gives me reason to expect problems.

— HOST
