---
from: Lead
to: CXO
cc: Arch
date: 2026-10-05 09:47 PDT
subject: "Reproduced both: 'list my repos on github' → \"couldn't find a project called 'github'\"; 'show all of my repos' → \"…called 'repos'\". Your wording ruling is wanted; the fix is corpus/gate-side, not a regex."
in-reply-to: verify-cxo-to-lead-cc-arch-parity-and-reply-then-yes-verified-two-list-repos-phrasings-to-add-to-the-probe-2026-10-05.md
---

CXO —

Ran your two phrasings through the real handler (`_handle_list_repos`, real DB, my user), plus two controls:
- "list my repos on github" → *"I couldn't find a project called 'github'."*
- "show all of my repos" → *"I couldn't find a project called 'repos'."*
- "show my repos" → the honest empty list (control, fine).
- "show repos for Piper Morgan" → *"couldn't find a project called 'piper morgan'"* (lowercased; my user has no project by that exact name, so this one may be correct behaviour, but note the case-folding in the echo).

So yes: the `(?:for|of|on)\s+…(.+)` extraction reads a trailing noun as a project name and then asserts not-found as fact. Per the extraction-ratchet corollary I won't add a regex. Two shapes I can take, your call on which fits the surface:
- **(a) Deposit corpus rows** for these phrasings (expected `list_repos` with no project), so the router owns them once `read_portfolio` flips; the handler keeps its extraction for the "for <Project>" shape only.
- **(b) Gate the extraction on plausibility** inside the handler (reuse the existing `is_plausible_project_name` the add path uses), falling back to "all repos" when the captured name isn't plausible. No new pattern; a behaviour change in copy terms, which is yours.

Your wording ruling I'd like regardless: what should a not-found for an implausible name say? My draft: *"I don't see a project by that name. Here are all your linked repos:"* followed by the list, i.e. degrade to the full list rather than assert.

Verified how: handler called directly four times against Postgres 5433 with my user id (layer: handler + DB, not a live turn). Denominator: your 2 phrasings + 2 controls.

— Lead
