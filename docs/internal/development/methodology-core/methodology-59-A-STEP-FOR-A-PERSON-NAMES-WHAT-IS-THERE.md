---
type: methodology
title: A Step for a Person Names What Is There
valid_from: "2026-11-26"
last_updated: "2026-11-26"
---

# A Step for a Person Names What Is There

**Status**: Emerging. Set 2026-11-26 by CIO under self-approval.
**Summary**: When a step written for a person names a thing (a line in a file, a page, a window, a button), check that the thing is actually there before the person reads the step. A person who can't find it does the nearest plausible thing, and does it with full confidence.

**Status note**: Emerging. Three instances in one hour of one sitting, from two seats (CIO, Exec). One caused a credential exposure. Graduation conditions are below.
**Filed**: 2026-11-26 by CIO. **Origin**: the ADR-084 Step F.4 and Step G sitting, 11-26.
**Companions**: [[methodology-44]] (a clear is not a measurement; here, a written step is not a checked one) ·
[[methodology-55]] (a name is not a definition) · [[methodology-36]] (mechanisms over vigilance) ·
memory `feedback_no_flattened_commands_without_referents` (the agent-to-agent form of this)

## The rule

**Before a step goes to a person, open each thing it names in the state the person will meet it: the
file's actual lines, the page as the host serves it, the rule that governs the window. If you can't
open it, say in the step that you didn't, and what to do if it isn't there.**

An agent that meets a missing referent stops and asks (the memory above). A person following a card
mid-sitting usually doesn't. They take the closest match. So the check has to happen at the writing end.

## The instances (2026-11-26, one sitting)

1. **A browser the rules forbid (CIO's steps file).** Step F.4 said to connect "in the dedicated seat
   browser". Step D in the same file forbids any real-provider Connect in it. Exec caught the
   contradiction before the sitting began. The F.4 line was older than Step D's rule and was never
   re-read against it.
2. **A line the file doesn't have (Exec's card).** xian was told the seat account's email was in its
   credential file. That file holds `username:` and `password:` only. He took the closest line and
   typed the password into a `--user-email` argument. The script refused it, but the value reached a
   chat transcript, his shell history and a short-lived process argv on the beta machine. Remedy:
   rotation, HOST's call.
3. **A page the host doesn't serve (Exec's first remedy).** The rotation advice said to change the
   password "on beta's account page". `templates/account.html` reads "Change password functionality
   coming soon". Exec corrected it within a minute, before anyone acted on it.

Exec noted the cost of instance 2 was "partly mine". In all three, the step was written from memory
of the artifact, not from the artifact.

## What is not this

The same sitting had two other misses. The authorize page wasn't read before Authorize was pressed,
and the window wasn't a private one. In both cases the thing named was there. The check simply
came as prose ahead of the action and didn't stop it. That is a separate candidate, held for the
12-29 audit: give a person's step its own stop line ("screenshot the page, then press").

## Graduation

Proven when the check becomes part of how cards are written: Exec's card template or the steps-file
form carries a line such as "Opened: <each named thing, how>", and a further sitting runs with no
missing-referent miss. Removed if two months pass with no further instance.
