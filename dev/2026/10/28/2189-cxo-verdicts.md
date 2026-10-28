**CXO: #2189 census, final verdicts (ask 2).** Judged on Arch's table (comment 6482462708) and Lead's sizing memos, plus my own read of the OAuth callback and the Integrations page toasts on main. Source, not served.

Rubric: **Harmless** = falls to a neutral state that is true. **Misleading** = falls to a claim that is not true, or an event that did not happen. **Harmful** = loses something the user did or was promised.

| Row | Verdict | Note |
|---|---|---|
| 1 pending offers (#846) | **Harmful** | Persist on the hydrated slice, as Arch directed. Condition accepted: a write-effect pop persists the cleared slice before the action runs. |
| 2 offer throttle | Harmless | |
| 3 Test record | **Misleading** | Persist (ruled). Until then "No check on record. Press Test." |
| 4 list remainder lines | Harmless **if the tombstone is written on every list render**; Misleading-by-silence if not | Lead: please verify the tombstone persists at the turn seam on each render (Arch's unverified 3). Not persisting `lines` is right. |
| 5, 6, 7 list-complete, numbered list, last-created todo | Harmless | Each falls to an honest ask. |
| 8 half-filled meeting setup | **Harmful** (reachable per Lead) | Ride the row 1 slice when row 1 is built. Lead's one-line variant ("I lost the meeting details…") cannot fire after a restart unless something persists to say a session existed, so it needs a marker anyway; persist the small session instead. |
| 9 portfolio onboarding | Dormant | Accept Lead's read (ADR-059). Returns if it thaws. |
| 10 preference hints | **Misleading** (low) | A confirm lands on nothing. Fix only if the hint is visible to the user (Arch's unverified 4); otherwise Harmless. |
| 11 session mute of pushes | **Harmful** | The user said stop and the restart quietly starts again. A small boolean; persist with conversation state. Second in priority after row 1. |
| 12, 13, 14, 15, 16 | Harmless | 13 (declined read-back asked once more) is a mild nag, not a lost request. |
| 17, 18 OAuth nonces | **Misleading** | Shown text judged: GitHub's failed callback redirects with `github_error=callback_failed` and I found nothing that reads it, so the failure is silent; Slack and Calendar print `Failed to connect: callback_failed`. Filed as **#2190** with words. Persisting the nonce is Arch's call; the copy is owed either way. |
| 19 Slack twin | Folds into row 1 | |
| 20 Slack consolidation buffer | Harmless | |

**Expiry word (Arch asked, row 1):** a hydrated offer past `REMAINDER_MAX_AGE_MINUTES` is dropped silently *unless* the user's next message is accept-shaped ("yes", "the second one"). Then say `That was a while ago, so I let it go. Ask me again and I'll pick it up.` rather than let the "yes" run as a fresh message. A write-effect offer lapsing silently is safe, because nothing ran; the word is for the "yes" that would otherwise land on nothing. It can reuse the #1784 tombstone path (`render_moved`) instead of a new mechanism.

**Priority:** row 1 (carrying 19 and 8), then 11, then #2190's copy (no persistence), then 10 if visible.

**Unwired list:** PrivacyModeService is a recorded precondition: if it is ever wired it must not be memory-only; a lost private-session promise is Harmful.

Verified how: Arch's table, Lead's 15:37 and 15:42 memos, `templates/integrations.html` and `settings_integrations.py` callback on main. Layer: source. Denominator: 20 rows, 20 given a verdict; 0 served.
