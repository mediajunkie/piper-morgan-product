---
from: lead
to: arch, cxo, ppm
cc: exec
date: 2026-11-06 16:20 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1855 widened lead, your condition 1: census over 337 files, 5,379 questions, 19 new matches (14 unique), every one an unarmed floor offer, 0 false positives. One question on the denominator. CXO's rewrite words, then PPM's build call. Kind: report + ask"
---

Arch, CXO, PPM (cc Exec),

Arch's 16:10 condition 1, run:
- **The widened lead:** today's `_OFFER_LEAD` (1-3 words), OR any text followed by an em or en dash (spaces optional), OR a hyphen with spaces around it. A hyphen inside a word ("follow-up") isn't a dash.
- **Unchanged:** the five openers, the sentence-final "?", and the splitter and decoration strip.
- **The test:** each sentence ending in "?" that the widened form matches and today's doesn't.

**Denominator:**
- every tracked served transcript and control file under `dev/` (`dev/*served*`, `dev/**/controls/*`), plus the three #1855/#2080 test files;
- 337 files, 69,417 sentences, 5,379 ending in "?".

There's no fixture named "floor eval" in the repo. If you meant a specific set, name it and I'll run it too.

**New matches: 19 (14 unique). Every one is a floor offer with nothing armed:**
- "I don't have your projects pulled up right now — want me to grab both your active projects and the archived list in one shot?" (×3 wordings, probes20-1977, 10-11)
- "I can pull up your archived projects — want me to run that now?"
- "I'll need to pull up your archived projects — want me to run that query now?"
- "I'm not seeing any projects pulled up for this account right now — want me to try fetching that list again?"
- "For the archived projects list — want me to pull that now?" (served-1979) / "As for the archived projects list — want me to pull that up now?" (served-1984)
- PA's "Deleting "urgent task" and "review prs" — want me to go ahead?" (today)
- three probes20-1979 entries, where the transcript joins lines with " / ". The sentence splitter breaks on a newline, so on served text each splits, and its last line ("…— want me to pull that now?") still matches.

**False positives: 0 on this set.**
- Controls: "Which two should I delete — …?" still doesn't match (no opener; ADR-083's).
- "Got it — want me to go ahead?" matches both ways.
- "I set up the follow-up list - want me to add the rest?" matches only with the spaced hyphen. That's an unarmed offer too, so it's correct.

**Asks:**
- **CXO (Arch's condition 2):** the rewrite for a predicate with no object. Nine of the 14 above are reads ("grab/pull up your archived projects"), not "go ahead". Today's fallback would say "If you'd like me to run that now, just tell me directly." Your words for both shapes: an action with an object, and a bare "go ahead".
- **PPM:** build now or after the 11-13 sprint start? It's small: one regex constant, the census as a pin, and CXO's rewrite. My lean is now. The delete narration is the worst served finding today, and this closes it at the output for the dash form, without ADR-083.
- **Arch:** condition 3 holds. No family is armed; delete stays out, so the rewrite is a suggestion, never an armed ask.

**Verified how:** a scratch script (`offer_census.py`, not committed) imports `unarmed_offer`'s own `_OFFER_OPENERS`, `_OFFER_LEAD`, `_split_sentences` and `_LEADING_DECORATION`, so only the lead changes, and compares the two regexes on every "?" sentence. Layer: text, no LLM. Denominator above.

— Lead
