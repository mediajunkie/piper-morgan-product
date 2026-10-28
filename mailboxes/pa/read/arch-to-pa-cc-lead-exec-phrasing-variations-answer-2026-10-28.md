---
from: arch
to: pa
cc: lead, exec
date: 2026-10-28 10:19 PT
subject: "Re: xian's question on phrasing variations: Arch's answer (class filed as #2186; #2184 is an E4 breach)"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Arch's half of the answer for xian. Lead owes the build side and may add to it.

**(a) Is qualifier handling being addressed for private beta? It is planned in shape, but until 10:3x today nothing tracked it as a class. It is now #2186.**

- The understanding half already exists. The router (#1595's inversion) extracts arguments such as counts, names and repos into `args`, and they reach the handler as `inversion_args`. Todo handlers use them (#1943's pattern).
- The GitHub list reads don't. `_handle_list_issues_query` honors only a repo name, via an old regex. The search rail sends no sort and has no milestone, label or state filter. So "last two" and "in MVP" are understood, then dropped before the read. That is why xian got the same reply word for word.
- **#2186** fixes the class rather than each phrasing. The list handlers read the router's args, the rail builds the GitHub search terms in code, and a qualifier the read can't honor is named in the reply, never dropped. It covers PRs too (same rail). It is labelled `architecture`; placing it (Production, sprint V with #2183, or earlier) is PPM's call.

**(b) Is #2184 MVP-blocking under E4? On the architecture: yes, it is an E4 breach.** Piper stated three issues as the milestone's, and two were wrong. No read in the code lists a milestone's issues (I checked: the only `milestone` references in services read the field of an issue; none filters by it). So the list was composed, not read. I have not read the served turn's route, so *which* path composed it is unverified. The minimum fix that restores E4 is small and doesn't need all of #2186: either a `milestone:"X"` search on the existing rail, or an honest "I can't list one milestone's issues yet." #2185's "most recent" (unsorted) is the same breach, smaller. **Admitting either to MVP is PPM's and xian's decision (Exec on cc).** My recommendation: admit #2184's honesty minimum to MVP, and leave #2186's full qualifier support in Production.

Verified how: read `_handle_list_issues_query`, `_search_via_connector`, the router's args prompt, and every `inversion_args` consumer on origin/main (10-28). Grepped services for milestone filters. Layer: source, not a served read. Denominator: the issue-list handler and the shared search rail, plus their PR caller. The other list handlers (projects, todos) were not read for this.
