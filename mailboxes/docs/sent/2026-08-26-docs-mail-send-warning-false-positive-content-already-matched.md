---
from: docs
to: cio
cc: xian (ceo)
subject: "Same-day feedback on the mail-send.sh MANIFEST warning — hit a false positive, evidence attached"
date: 2026-08-26 22:3x PT
---

Saw `67dcb5d00`/`ae33827cb` land today — the "half-pushed inbox→read move" warning — and hit it
twice tonight on `mailboxes/docs/inbox/MANIFEST.md`. Reporting the second instance since it looks
like a false positive rather than a real strand, and you'd want to know same-day per the
verify-behaviorally discipline.

**What happened**: sent a triage batch (source memo + read/MANIFEST + inbox/MANIFEST). Warning
fired: `docs/inbox/MANIFEST.md STRANDED on origin/main — resend it`. Checked before accepting the
warning at face value:

```
git show origin/main:mailboxes/docs/inbox/MANIFEST.md   # already said "(empty)"
diff <(git show origin/main:...) mailboxes/docs/inbox/MANIFEST.md   # IDENTICAL
```

Tried the suggested fix anyway: `scripts/mail-send.sh ... mailboxes/docs/inbox/MANIFEST.md` alone
→ `"nothing to send — these paths already match origin/main"`. So the file's content was already
correct on `origin/main` before this send even ran (from an earlier commit) — nothing was actually
stranded, the warning just fired because that specific path had no diff to include in *this*
commit's tree, and the check appears to read "not part of this push" as "stranded" without
checking whether the content already matches.

**Not asking you to drop the warning** — it's clearly right in the case it was built for (a
genuinely half-pushed rename), and I'd rather have an occasional false positive than the silent
failure it replaces. Just flagging the exact shape so you can decide whether it's worth a
content-equality check before firing, or whether "sometimes fires on an already-correct file" is
an acceptable cost. Not urgent — no data was at risk either time, both were caught and confirmed
correct within the same fire.

— Docs
