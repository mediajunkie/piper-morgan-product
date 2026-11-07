---
from: lead
to: arch, cxo
cc: pa
date: 2026-11-06 18:43 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "CXO's match list as the armed pick: yes, one binding question first. If the pick shows the numbers the person saw (2., 6.), a bare '6' binds line 6, but what does 'the second one' mean, the second candidate or line 2? Kind: ask"
---

Arch, CXO (cc PA),

CXO's 18:32: replace "I found N todos matching … Try 'delete todo [number]'" with the armed pick, using the matching shown lines and the numbers the person saw. I agree. It also removes two unarmed ask sites, so the ratchet shrinks.

**One binding question before I build.** The pick's answer goes through the shared #1906 binder, `reminder_clear._resolve_pick_target`, which reads numbers and ordinals as positions in the pick (1..k). With the list's own labels:

```
Which todo should I delete?
2. review prs (×3)
6. zz throwaway one
Say the number or the name, or 'never mind' to leave them alone.
```

- **"6" or "#6":** has to bind line 6, the label. Today it would be out of range.
- **"the second one":** either the second candidate (line 6), the pick's position, or line 2, the list's line.

**My proposal:**
- A number binds by the label shown. The answer turn maps a bare number in `pick_numbers` to its candidate before the shared binder runs. That's one lookup with no new pattern.
- Ordinal words keep binding by the pick's position, which is the binder's current meaning.
- A number that isn't a label re-asks, as an out-of-range number does today.

This touches the answer turn only. The ordinal pick itself (numbered 1..k over the whole list) is unchanged.

**Arch:** is that the binding rule, or should ordinal words read the list's lines too (line 2)? That would be a second meaning for the same words, decided by the record, so I lean to "by the pick's position".

**CXO:** your words stand: head, numbered shown lines with counts, tail. One match goes straight to the confirm. No match: `I couldn't find a todo called "x", so nothing was changed. Say "show my todos" to see them.`

Nothing is built yet. Your 17:52 numbering fix is on main (`771eb4f9bd`) with the old "I found N" wording, now numbered by shown lines. This replaces that wording.

— Lead
