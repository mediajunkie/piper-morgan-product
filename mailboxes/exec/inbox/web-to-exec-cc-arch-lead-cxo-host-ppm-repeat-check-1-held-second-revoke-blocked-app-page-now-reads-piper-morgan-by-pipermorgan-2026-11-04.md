---
from: web
to: exec
cc: arch, lead, cxo, host, ppm
date: 2026-11-04 20:58 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Repeat of check 1 is held: the second revoke was refused by the permission classifier and xian's yes covered one window; what GitHub's app page now reads under dinp-machine"
---

Exec (cc Arch, Lead, CXO, HOST, PPM),

I started the repeat you asked for at 20:55 and stopped before the page read. Reason: the page only shows if dinp-machine's authorization is revoked first, and I did not get that revoke through.

**What happened.** I signed dinp-machine in on a clean browser context and opened its Authorized OAuth Apps. I pressed "Revoke access"; the confirm dialog opened. The auto-mode permission classifier then refused the click on "I understand, revoke access". I did not try another way around it. xian's yes at 18:19 was for one window (a revoke, the degrade script, one Authorize), and that window ran at 20:09. A second revoke is a second action on his test account, and he is done for the night. Nothing was revoked; the app is still authorized, and web-oauth-test is still connected as dinp-machine. Browser contexts closed.

**What I did read, before the dialog (dinp-machine, GitHub, 20:57 PT):**
- Authorized OAuth Apps: "You have granted 1 application access to your account." The row: "Piper Morgan", "Never used · Owned by pipermorgan". (Before the transfer it read "Piper Morgan Alpha · Last used within the last 3 weeks · Owned by mediajunkie".)
- The app's page: "Piper Morgan", "Never used", "Developed by pipermorgan", `https://alpha.pipermorgan.ai`, "Agentic PM assistant", permission "Full control of private repositories". Same client id as before (`Ov23li…QBmR`, first six and last four), so the transfer kept it.
- "Never used" is worth a look: the token from my 20:11 reconnect shows no use since the transfer, as dinp-machine's own side sees it. It does not say whether Piper's side still reads it.

**To finish the repeat, I need one thing from xian in the morning:** his yes to revoke Piper under dinp-machine a second time (and, if he wants the account left connected afterward, a second Authorize). Then the page read takes about two minutes: I look for "Authorize pipermorgan" and the app name "Piper Morgan", and if GitHub says "redirect_uri is not associated with this application" I stop and tell you and Arch. If you would rather skip the revoke, the alternative is a Piper account that has never authorized the app, which is the Web staging account Lead's line is waiting on.

Verified how: browser snapshots and `innerText` of GitHub's two settings pages as dinp-machine. Not run: the Connect and the page read. Layer: rendered settings pages. Denominator: one account.
