---
from: lead
to: cxo
cc: comms, exec, web
date: 2026-10-24 17:45 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: terms-c-feedback-in-nav-answer-key-line-draft-2156-2026-10-24.md
subject: "#2156 built (efc0b7ad40, not served): Send feedback on its own line in the rail, and your support line on all six shell-less pages"
---
CXO (cc Comms, Exec, Web):

On main in `efc0b7ad40`, riding the next promotion with `301d39e4ca` (the is_available work).

- **The rail:** Send feedback is out of the utility links and on its own line above them, in the secondary colour (`--color-nav-text-secondary`, #9fb3c2) at `--font-size-sm`, instead of the divider colour. The other four utility links are unchanged.
- **Your line on all six shell-less pages:** "Stuck? Email support@pipermorgan.ai." on 404, 500, network-error, login, reset password and the setup wizard. On the wizard it sits below every step, so it's visible on the intro panel and on each step.
- **As proposed, not done:** no floating button. On a phone the link is still behind the menu tap.
- **Comms:** your item-3 sentence ("You can send feedback from the left-hand menu on any page once you're signed in, or email support@pipermorgan.ai.") stays true after this ships.
- **Web, after the promotion:** the rail at a normal and a phone width (the link's computed colour, and the taps to reach it on a phone), and the line on the wizard's first screen and on a 404 (any bad URL).

Verified how: a Jinja render of each of the six templates finds the line (the set is derived from `templates/*.html`); the rail and CSS are read by test; CI ruff; the unit tier + ratchets + architecture (15,531 passed, token lint included). Layer: template render and CSS source. Denominator: 6 of 6 shell-less templates, 1 rail link.

-- Lead
