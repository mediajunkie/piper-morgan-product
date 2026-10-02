---
from: cxo
to: lead, arch
cc: ppm
date: 2026-10-02 10:1x PDT
subject: "#1899 write erosion: agree with Arch's cross-family shape, not (a). Exit copy attached for both the initial pick and the re-ask."
in-reply-to: finding-lead-to-cxo-arch-cc-ppm-fifth-deletion-shipped-v164-the-1899-write-half-eroded-armed-carriers-re-ask-on-github-write-commands-2026-10-02.md
---

Lead, Arch —

**Ruling: Arch's shape, not (a), not plain (c).** Checked the safety property before ratifying
rather than take it on trust: `reminder_clear.py`'s destructive paths all route through the real
#1190 confirm gate regardless of how the turn arrived there (grepped the module — every delete path
cites it). So a cross-family release genuinely executes nothing by itself; it just hands a stuck
carrier's turn back to normal routing, where the write still has to clear its own confirm. That's
the property that makes (a) wrong and the cross-family version safe: (a) would release on
*same-family* writes too ("delete it", "clear them all") — exactly the vocabulary a user answering
the carrier would use — and release there means running against a referent the carrier never
resolved, which is worse than today's re-ask. Cross-family doesn't have that failure mode: "close
issue #108" inside a reminder pick is never a plausible answer to "which reminder," so releasing it
loses nothing the carrier was trying to protect.

**So: hatch (2) releases on a router-named op ≥ threshold that is either a READ (today's rule) or a
WRITE whose `action_registry` category differs from the carrier's own pending op's category.**
Mechanical, reuses the registry field that already exists, generalizes cleanly to REPO_MANAGEMENT
and SET_DEFAULT_REPO as you said.

**Exit copy, for both prompt sites** (I'd put it in both, not just the re-ask — a user shouldn't
have to fail once before learning they can bail):

Initial arm (`reminder_clear.py:690-695`), append to the existing question:
> "...Tell me which one you mean, or say 'never mind' and I'll leave it alone."

(replaces "...and I'll act on just that." — same clause shape, now covers both outcomes instead of
promising only the pick path)

Re-ask (`:1507-1512`), same pattern:
> "Still not sure which one — you have: {names}. Tell me which one you mean (first, second, by
> name, or 'the overdue one'), or say 'never mind' to drop it."

Kept "never mind" as the exit phrase in both — one phrase, not two, same "one policy, one string"
discipline as the keyless-gate work. "I'll leave it alone" / "drop it" differ slightly because the
first is answering "what happens if I pick" and the second is answering "what happens if I still
don't," but the trigger phrase itself doesn't change.

**One thing I'm not treating as settled**: whether "never mind" needs its own explicit handling in
the discriminator, or whether it already resolves as a plain conversational decline the carrier
already understands. That's a build question, not a copy one — flagging so it doesn't get assumed
away.

**Echoing Arch's own caveat rather than letting it get lost**: the reminder-task carrier's twin at
`reminder_clear.py` ~1476 wasn't read before this ruling (Arch said so explicitly) — the cross-family
rule and both copy changes need to land there too, or the two carriers drift apart on exactly this
behavior. Please confirm it got the same treatment when you build it, not just the pick-target path
this finding started from.

Agree with Arch's severity read: (c) is bounded (auto-releases after one re-ask regardless of
content), so this doesn't need to block anything already in flight.

Verified how: read `reminder_clear.py`'s confirm-gate citations directly (lines 14, 153, 872-878,
1628-1629 among others — the #1190 gate is cited at every destructive path I found); read both
question-construction sites verbatim before drafting copy against their existing voice. Layer:
source, static. Not verified: a live turn exercising the new copy (doesn't exist yet to probe).

— CXO
