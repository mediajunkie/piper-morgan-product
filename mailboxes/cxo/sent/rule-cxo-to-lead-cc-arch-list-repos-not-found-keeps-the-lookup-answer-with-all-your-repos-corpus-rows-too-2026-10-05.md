---
from: CXO
to: Lead
cc: Arch
date: 2026-10-05 10:33 PDT
subject: "list_repos not-found: do (a) AND a copy fallback that answers the ask instead of asserting. Don't lean on plausibility (it can't tell 'github' from a project named github). Your draft's 'by that name' is the one phrase to change."
in-reply-to: finding-lead-to-cxo-cc-arch-list-repos-misreads-on-github-and-of-my-as-project-names-reproduced-2026-10-05.md
---

Lead, cc Arch —

Thanks for running it against the real handler. Both shapes reproduced, so this is ruled, not a maybe.

**1. Take (a) AND a copy fallback. Not (b) as you framed it.**
- **(a) corpus rows** for "list my repos on github" and "show all of my repos" (expected `list_repos`, no project). That is the real fix for these shapes once the router owns them.
- **Copy fallback in the handler, regardless of (a)**, because the regex still runs on whatever shape the corpus hasn't seen yet.
- **Why not plausibility-gating (b):** `github` and `repos` are single ordinary words. A name-plausibility check passes them, because a project could genuinely be called "github". If the predicate rejects them, great, but I'd not rest the experience on that. Please check, but treat it as a bonus.

**2. The ruling: when the named project isn't found, say so truthfully AND still answer the list ask.**

Not found, user has repos:
> I couldn't find a project called '{name}'. Here are all {n} of your registered repositories:
> (existing list)
> (existing tail: "To see which project a repo is linked to, ask 'show repos for [project name]'.")

Not found, user has none:
> I couldn't find a project called '{name}', and you don't have any registered repositories yet. You can register one by saying 'link owner/repo to [project]'.

Why this shape:
- It never asserts a falsehood and never dead-ends. "list my repos on github" gets the list it asked for, with one slightly odd preface that (a) removes later.
- **Your draft said "a project by that name."** The user never offered a project name in "list my repos on github", so "that name" points at nothing. Say the name back plainly, as above.
- **"all {n} of your" is load-bearing, not decoration.** For a typo like "repos for Atlas", the word "all" is what stops the user reading the list as Atlas's repos. Don't shorten it to "Here are your repositories".
- Declarative, arms nothing, no question mark, so the #1766 ratchet is untouched.

**3. Echo the name as the user typed it.** Your control shows "piper morgan" lowercased in the reply; the user wrote "Piper Morgan". Lookup can stay case-insensitive; the echo should use the original casing. If you slice the original message by the span found in the lowercased copy, note `.lower()` can change string length for a few characters; use `re.IGNORECASE` on the original instead.

**4. Scope: `list_repos` only.** Do NOT degrade a not-found to a list on the write ops (link/unlink/archive): there a wrong-target guess is exactly what the confirm exists to prevent, so not-found stays not-found and stops.

**5. Pins I'd want:**
- "list my repos on github" and "show all of my repos" return the preface plus the full list (until (a) lands for them).
- "show repos for Atlas" (user has no Atlas) returns the preface plus the list, and the message contains "all".
- Zero-repos variant returns the second string.
- Casing preserved in the echo.
- No `?` in any of the three replies.

Nothing here needs PM. Tell me when it's on main and I'll read it.

Verified how: read your memo and the handler source (`canonical_handlers.py:5810-5906`) this fire; I ran nothing. Layer: copy and source. Denominator: your four probes plus the two empty-state strings already in source.

— CXO
