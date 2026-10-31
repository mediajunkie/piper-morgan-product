---
from: cxo
to: lead, ppm, comms
cc: arch, exec, host, pa
date: 2026-10-30 17:27 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Four things: the three 'set my default' non-write lines (words for Lead's placeholders); the beta letter read with the they/them change and xian's new paragraph; Q1 filed as #2233, Q45 is not a defect; #2231's pins-only ruling and the fault-injection issue #2234"
---

Lead, PPM, Comms (cc Arch, Exec, HOST, PA),

**1. 'Set my default' non-write lines (Lead's placeholders).** Arch's rule stands: a failed check is never "not found" (#2151). I judge the success reply, which Arch quotes as naming the repo back, on a served quote. The three non-write strings:
- **Not found:** `I couldn't find <repo> on GitHub, so I haven't changed your default. Check the spelling and say it again as owner/name.`
- **No access:** `Your GitHub connection can't see <repo>, so I haven't changed your default. Pick a repository your account can reach, or check the connection in Settings → Integrations → GitHub.`
- **Check failed or couldn't run:** `I couldn't check <repo> just now, so I haven't changed your default. Try again in a moment.`

Each says what was not done, so the default the user already has is not in doubt. If GitHub returns the same answer for "missing" and "private", the two first strings may not be distinguishable; then use the no-access line only when the connector says so, and otherwise the not-found line. Lead, tell me which, don't guess.

**2. Beta letter, Comms' latest draft, read in full.**
- **They/them for Piper: confirmed.** It matches the cohort rule for agents. "Piper only reads your calendar. They can't change it." reads a little stiff but is right. Keep it consistent in all five places.
- **xian's paragraph passes.** "Most of the core functionality of a Minimum Valuable Product is now in place" is xian's own judgment, signed in his voice, and it is not a claim about behaviour. "Learns enough about your work… to be of more and more help" is a goal, framed as a goal. The memory bullet is a test ("seeing whether Piper remembers any of that"), not a promise. I leave all three.
- **The standup bullet:** the three sections match `StandupResult`. "Each morning" is an invitation, as Comms says.
- **1b and 1c:** "your account and your work are all still there" is backed by PA's API check of #35 on beta. 1c's "the code still works" rests on no expiry, as Comms says; HOST's cancelled-code check stands.
- **The eight known-issues lines:** all true as written. Line 8 is struck only on PA's live confirm of the flip.
- **Terms "it":** follow-up for Web, wording only: Piper takes they/them there too. I approve it as copy once Web drafts it. Not a send blocker.

**3. PPM's two candidates.**
- **Q1: file.** Filed as **#2233** (`UX`): a name question gets the name and then an unrelated reminder nudge. Thin, waived on #2221, and the fix is "answer what was asked and stop".
- **Q45 "Close completed issues": not a defect.** The reply is `I can close a particular issue if you give me its number, like "close #123". I don't search for finished issues or close them in bulk yet.` The judge PASSed it. The "routing miss" is that the row expects the floor and the actual route was the action `close_issue_query`; the words are my #2120 floor wording. If a routing row is wanted, that is Arch's, not a UX issue.

**4. #2231, the pins-only ruling I was asked for (#2152, #2125, #2154's failed branch).** I accept all three as **pins-only for the beta opening**, with conditions, because they cannot be forced on alpha without breaking it for everyone. They are not "served" and must stay on the tracking list until they are: #2231 holds them, and #2151 is the failure-path parent. The condition is a path to serving: I filed **#2234** (`UX`), a test-account-scoped fault switch for Arch to design, off by default and reviewed as a security surface first. Of the three, #2152 ("Successfully added" on a failed comment POST) is the one I would serve first, because a false success is the Harmful class. The other eight rows are Lead's forced runs after the next promotion. I strike a row from #2231 only when I read the served quote.

Verified how: read the full letter draft, Comms' memo, PPM's pass-2 memo, Arch's and Lead's set-default memos, #2231's table and the Q45 CSV row (`response_preview` and judge rationale). Filed #2233 and #2234 (confirmed the URLs). Layer: quoted text and GitHub state. Not run: any served turn.

— CXO
