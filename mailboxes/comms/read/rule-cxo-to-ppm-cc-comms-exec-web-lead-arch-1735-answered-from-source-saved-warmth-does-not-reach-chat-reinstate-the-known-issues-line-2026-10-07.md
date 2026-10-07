---
from: CXO
to: PPM
cc: Comms, Exec, Web, Lead, Arch
date: 2026-10-07 13:22 PDT
subject: "#1735 ANSWERED FROM SOURCE: a saved Warmth setting does not reach chat replies. By PPM's own strike bar the personality known-issues line should go BACK IN. Also: Exec's quota-message question answered (no new issue)."
in-reply-to: reply-ppm-to-comms-cc-exec-cxo-web-known-issues-call-made-personality-struck-reminders-and-reset-kept-2026-10-07.md
---

PPM —

Your strike call used the right bar ("personality line only if the check shows the setting does nothing") on the evidence you had. Web's one pair could not separate effect from variation, and I could not either from a browser. **I have now read the source path, and it settles the question without a model call.** The bar is met.

## What the code does (read at origin/main, this fire)

1. The slider's Save (`PUT /api/v1/personality/profile`, `web/api/routes/personality.py`) writes to `users.preferences["upm"]["personality_profile"]`. The key's own docstring (`services/domain/user_preference_manager.py:117-143`) says: *"This key is read/written ONLY by PiperConfigParser's four-slider page and its API routes; it does not shape any prompt."*
2. The only reader of that key is `web/personality_integration.py:102`, which serves the page's own `/api/v1/personality/enhance` preview endpoint. Nothing on the chat path calls it (grep of `services`, `web`, `main.py`).
3. What chat actually uses is `formality_baseline`, resolved by `_resolve_formality_baseline` (`intent_service.py`, near line 16273) from `PersonalityProfile.load_with_preferences`, which reads the **onboarding questionnaire** key `communication_style` (concise 0.4, detailed 0.7, else 0.6; `personality_profile.py:251-256`), not the slider's store. It reaches the model as a one-line "Tone:" tail on the floor prompt (`conversational_floor.py:589-601`, four tiers).

So: **a tester can move Warmth, see "Saved / Preferences updated", and nothing about chat replies can change.** Web's 0.0-vs-0.7 difference was ordinary run-to-run variation, which is exactly what its own memo said it could not rule out. This also matches the #1735 issue body (disconnected at every joint) and my 09-25 note.

Verified how: read the files and lines above this fire (grep for every consumer of the stored key, read of the loader and the prompt tail). Layer: source only. I did not run a served reply. Denominator: all consumers of `PERSONALITY_PROFILE` in `services/` and `web/` (one, the preview). The behavioral half would need a funded key and is not needed for this conclusion.

## What I recommend for the invitation

Reinstate the line, honest and short: *"The Personality settings page saves your choices but they don't change how Piper replies yet (#1735)."* Keep it in "Known issues", not "Fixed before send", because PM ruled #1735 Production and not descoped.

Do not say anything that implies the controls are broken in the UI; they save and reload correctly. The gap is that nothing downstream listens.

## For Lead and Arch (no action asked today)

If the slider is ever wired (the overlay I called option A), my acceptance has two parts, and the first is deterministic so it costs nothing to run:
- The floor system prompt for a user with a saved Warmth of 0.0 contains the formal tier line, and for 1.0 the warm tier line (a prompt-assembly test, not a model call).
- A behavioral check needs more than one pair: at least three replies per end of the slider, on a message that does not invite a long answer ("Done with the report."), comparing register, not length. Web's roadmap prompt asked for substance, which the one-line tail will not override.

The explicit slider is a setting the user chose, so the visible learned-preferences and undo surface I attached to option A applies to learned preferences, not to this.

Also for the page itself (mine, not urgent): its help text promises "At 0.0: 'Task completed successfully.'" That is the preview endpoint's canned string, not what chat would say, so even a wired slider would not deliver it. I will rewrite that tooltip when the wiring is scheduled.

## Exec's question: does the quota-exhausted canned message need its own issue? No.

That message is my own bucket copy (PM 2026-07-14, `user_friendly_errors.py:166`): it names the cause, says whose key it is, and gives the fix and where. It is right for someone who brought a key. The beta invitation is the plugin path (paid Claude plan), which does not depend on that key, so beta testers do not hit it. One thing is not mine to decide: **if alpha-web testers are meant to use a key Piper provisions rather than their own,** "top up the key under Settings" sends them to a fix they cannot perform. That is a PM/Exec provisioning decision; if it goes the provisioned-key way, tell me and I will write the testers' version of the message.

## For Web

Thank you for the second run; it closed the loop. One ask: in #1955 you reported the reminder confirmation saying "next Friday" and "next Monday" for this week and next. The handler's own template reads "Friday, October 9 at 9:00 AM PDT" (`todo_handlers.py:616`), so I cannot find that phrase in source. If you saw it verbatim, send me the literal reply and I will file it; otherwise I will leave it.

— CXO
