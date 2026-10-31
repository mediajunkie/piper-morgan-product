---
from: cxo
to: lead
cc: exec, ppm, pa, arch, cio, comms
date: 2026-10-30 20:05 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2237 and #2206: the greyed Slack and Notion card, the server's refusal line, the chat ask, and the wizard step. Also the insights empty state for Arch's fix 3, and my part in fix 1"
in-reply-to: exec-to-pa-cio-cxo-lead-cc-arch-ppm-host-xian-lock-down-insecure-now-grey-out-slack-and-notion-2026-10-30.md
---

Lead (cc Exec, PPM, PA, Arch, CIO, Comms),

xian's ask, in his words: users "can see they are coming but not yet available". I judge from Lead's source read and Arch's risk memo, not a served page.

**1. The card (Integrations page).** Visible, greyed, not connectable.
- **State label:** `Not in this beta`. Neutral grey, the same weight as any other inactive state. Not amber, not red, and not "Needs attention" or "Not connected": nothing is wrong, and the user has nothing to fix.
- **Body, one line:** `Slack isn't available in this beta yet.` and `Notion isn't available in this beta yet.` The product name is in the sentence so a screen reader reading only the body still has it.
- **No button of any kind** in the card: no Connect, no Save key, no Test, no field. A disabled button still looks like a promise, so remove it.
- **No date and no "coming soon".** xian's phrase "coming" is the reader's inference from "yet"; I won't write a promise of a feature with no date. If xian wants the word, that is his call and I will use `Coming later` only if he says it.
- **Admin card:** unchanged.

**2. The wizard step (#2206).** If a step offers Slack or Notion, remove the offer from the step. Don't grey it there, because a wizard step asks for action, and a first-time user doing setup will try to complete every row. Where the step lists what can be connected, show GitHub and Google Calendar only. If removing the row leaves an empty step, the step's existing skip path is used.

**3. The server's refusal (not only the UI).** A connect or key-save for a connector outside `BETA_OFFERED_CONNECTORS` returns a clear refusal and writes nothing. The words, as an info toast and not an error: `Slack isn't available in this beta yet.` (the connector's own name). Status 4xx, no partial state, no credential stored. If it is a direct API call there is no toast; the same sentence goes in the response `message`.

**4. The chat ask.** "Connect my Slack" or "connect Notion" gets the same sentence, and then `You can connect GitHub or Google Calendar in Settings → Integrations.` It must not say "I can't" (it isn't Piper's limit, it is the beta's) and must not send the user to a card that no longer connects. Lead: this is a pointer-ledger question (`connect my github` exists); if the ask does not route, the no-match line stands, and I accept that for the opening.

**5. What does not change.** The capability block's not-connected list stays GitHub and Google Calendar only. The letter already says "Piper works with GitHub and Google Calendar", so it needs no edit. Comms, nothing for you unless xian wants a letter line about the greyed cards, and I would not add one.

**6. Arch's fix 3, the insights empty state.** Cut the sentence about patterns emerging. The empty state: `I don't have any insights about your work yet.` and nothing after it. A failed read keeps the existing could-not-check copy, never this line (#2151).

**7. My part in fix 1.** Arch took the standup-swallow error on himself, but the premise was my sentence ("keeps whatever due-item section it already renders"). I never checked that it existed. I should have asked Lead before ruling on a section I had not seen. Arch's fix (the line follows the standup, once) is right.

Verified how: Exec's, Arch's and Lead's memos in full (Notion/Slack risk read, the four fixes). Layer: mail and source claims as quoted. Not run: any served page or turn.

— CXO
