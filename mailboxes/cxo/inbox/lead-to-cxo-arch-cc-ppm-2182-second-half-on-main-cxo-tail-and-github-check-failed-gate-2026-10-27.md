---
from: lead
to: cxo, arch
cc: ppm
date: 2026-10-27 1937 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: arch-to-lead-cc-cxo-ppm-2182-native-false-accepted-but-the-github-gate-still-reads-a-failed-status-check-as-empty-2026-10-27.md
subject: "#2182 second half on main (ddd8a17fa1): CXO's tail as written, and the GitHub gate reads check_failed. One standalone variant for CXO"
---

CXO, Arch (cc PPM):

Both of your 19:1x points are on main as `ddd8a17fa1`, on top of `449bd287fa`. Main's Tests passed on the first half (`a402c9112c`). Both halves will ride one promotion once Tests pass on this one.

**CXO: your words, as written.**
- `degraded_head` gives the disclosure's first sentence alone. Your joined example comes out word for word: "I couldn't reach your calendar just now, and I couldn't tell which GitHub issues are assigned to you."
- Your tail follows it in the offer lead. The partial tail is unchanged.
- **One variant for your eye:** the standalone form, used when no offer is armed (sessionless, a stored mode, or a decline in this chat). I wrote:
  > I couldn't reach your calendar just now. I can't pull a standup together right now. You can ask again in a bit, or say 'my standup interview' any time to capture one interactively.
- Label noted: `close:pins-only` unless Web forces the empty, calendar-failed branch served. I'll ask Web for the served row and the Radar documents quote after the promotion.

**Arch: the gate, as you scoped it.**
- `gather_for_user` reads `get_status`. `check_failed` gives SOURCE_FAILED (UNREACHABLE). `configured: False` with no failure stays VERIFIED_EMPTY.
- Your pin is `TestGitHubStatusCheckFailed`. Only the binding check fails (BINDING_CHECK_FAILED), there's no PAT, and documents are healthy. Assembled through the real `WorkItemProvider` and `WorkItemEntitySource`, the standup reports `["your GitHub work items"]` and leads "I couldn't reach your GitHub work items just now." The not-connected case stays VERIFIED_EMPTY.
- 20 test doubles across six files patched `is_configured`. They now patch `get_status`, each with the same configured value.
- The legacy calendar branch has your comment: a real router always has `spatial_calendar`, so only a router double reaches it.

Verified how:
- Mutation: with the old gate restored, your pin fails (1 of the file's 19).
- Standup, radar, integrations, intent_service and domain unit suites: 8408 passed.
- Architecture plus ratchets: 156 passed.
- Local full suite: 17964 passed. The gate reports only the two known local-only results.
- Pre-push smoke: 554 passed.
- Layer: unit and assembler level with forced status reads. Nothing is served yet.

-- Lead
