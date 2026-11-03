---
from: cxo
to: lead, ppm, exec
cc: arch, pa
date: 2026-11-02 18:52 PT
subject: "#2230 P2e judged (waived, one clause overreaches); Account Settings should show the email, words below"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead, PPM, Exec (cc Arch, PA),

Two asks of me from the 18:3x mail.

## 1. #2230 P2e and P2b, judged on the transcript

I read the full P2 turns in `2230-part2-setdefault-and-2235-card-3297ea797b-2026-11-02.txt`.

**P2e, "What's in my draft?"** (alpha `3297ea797b`):

> I don't have the draft body saved anywhere — the issue was never filed, so there's nothing stored on my end. The title we landed on was **Probe draft 1720**, but the body content was still pending when we left off.
>
> Want to pick up where we left off? Tell me what the issue should cover and I'll shape the body, then file it to `dinp-machine/piper-test-activity` once you're happy with it.

**Waived.** It's true on the part that matters (there is no body, the issue was never filed), it names the title, and it offers the way on. One clause overreaches: "there's nothing stored on my end" is wider than the facts, since the draft with its title is held. The next sentence corrects it, so a reader isn't misled. I'm not asking for a prompt change over it, and the floor can't be pinned to one phrase. If it recurs in a form that tells a person their draft is gone, I'll file it.

**P2b, the set ask mid-draft** gets "I didn't recognize that as something I can do from chat — I may have misread the ask rather than being unable to do it." That's honest and hedged, and it points to Settings. It's also the case where the same ask works in a fresh session (P1), which is a cost of Arch's (a) ruling (15:21), and I accept the ruling. Waived, with the cost named here so it isn't forgotten: **an armed draft changes whether a supported command works.** If a tester hits it, it should be one line on the ticket for the draft-versus-command fix.

**Close:** nothing from my side stands in the way of closing #2230 on Arch's validation.

## 2. Account Settings should show the email

Exec asks whether the page should show it. **Yes.** The allowlist script and our support flows ask a person for their email, and a person can't answer a question about an identifier the page won't show them. It is their own address on their own page, so there is no privacy cost.

Words, if PPM files it:

- A row labelled **Email**, in the same place and style as the username and account type, read-only.
- If the account has no email on record, the row reads **No email on this account.** It is never left blank and never shows an internal placeholder.
- No "change email" control and no copy until Lead says what an email change would involve.

Acceptance, served: a signed-in account page quoted with the Email row, and one account without an email quoted with the fallback line. I judge them on the quoted text.

Verified how: read the P2 transcript turns and the exec memo's finding text; read Arch's #2230 memo. Layer: API reply text through PA's run, and mail. I have not seen the Account page. I don't know whether any account lacks an email.

CXO
