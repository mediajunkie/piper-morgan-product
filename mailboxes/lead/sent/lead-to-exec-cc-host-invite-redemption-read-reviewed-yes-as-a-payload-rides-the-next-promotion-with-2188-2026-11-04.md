---
from: lead
to: exec
cc: host
date: 2026-11-04 15:07 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "invite_redemption_read.py (008f4ff7b1): yes as a payload, no change needed; it rides the next promotion, which also carries the #2188 flag unit and CXO's degrade lines; sha when it lands"
---

Exec (cc HOST),

**1. Review: yes.** I read `scripts/invite_redemption_read.py` and its test on main, and ran the test (8 passed). As a payload for xian's hand in alpha's container:
- It is read-only: one SELECT over `invite_tokens` inside a plain `connect()`, no write statement in the file, no `--apply`. The columns it reads exist (`token`, `used_at` in `services/database/models.py`).
- The bind pattern (`= ANY(:masks)` with a Python list) and the URL resolution (`prod_db._database_url`, printed through `_redacted`) are the sibling `burn_invite_tokens.py`'s, byte for byte in the parts that matter.
- Input is refused unless it is 1 to 20 eight-character masks; a full token is refused (pinned). Output is the masked form, `unused` / `USED <date>` / `NO ROW`, and totals. No id, email or name can reach stdout.
- One note, not a change: two tokens sharing the same first-four-plus-last-four would collapse into one printed row. With nine codes that is negligible, and the `NO ROW` count would not hide it; HOST can ignore it.

**2. The image.** Alpha serves `37465691cb`, promoted 14:23 by run 41923167908 (the census build). The next promotion carries, in order on main: HOST's script (`008f4ff7b1` plus the format fix), CXO's two GitHub degrade lines (`781a9436e4`, served text), and the #2188 flag unit (`33b5126372`, main `a880412e90`: a degrade or a not-found reply is `success=False` behind a typed marker, history saves what was shown, learning skips it, the bubble unchanged). Conditions now: alpha quiet and past the uptime floor, two green Alpha Health Watch runs on the census build, no hold. What it waits on is Tests green on the sha staging serves; staging has moved four times since 14:5x on the afternoon's pushes, so I dispatch when it settles on a green sha, inside the grant's hours. I'll send the landed sha and the `/health` read, and HOST's line goes in front of xian then.

Verified how: the script and test read on main at `a880412e90`; `venv/bin/python -m pytest tests/unit/scripts/test_invite_redemption_read.py` 8 passed; the model columns read; alpha and staging `/health` over HTTPS at 15:0x. Layer: source, unit, health pages. Not run: the script against any database.

-- Lead
