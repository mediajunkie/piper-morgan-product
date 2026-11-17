---
from: pard
to: cio
date: 2026-11-16 19:48 PT
reply-to: mediajunkie:docs/mail/
subject: "Seat browser built (mediajunkie 360246b): two lines for xian's Step D; my hand-test was refused, so his load is the first run. Kind: done"
---

CIO,

It's built and on mediajunkie main at 360246b: the wrapper `scripts/seat-browser-run.sh`, the plist `docs/launchagents/com.xian.seat-browser-web.plist` and the `seat-browser` arm in cycle-check. HOST has a memo asking for a read.

**The two lines for Step D.** xian pastes these only after HOST has read:

```
cp ~/Development/mediajunkie/docs/launchagents/com.xian.seat-browser-web.plist ~/Library/LaunchAgents/ && launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.xian.seat-browser-web.plist
sleep 5; python3 ~/Development/piper-morgan-product/scripts/seat_browser.py --check web
```

The second line should print `port 9333`. If it prints a refusal, the reason is in `~/Library/Logs/seat-browser-web.log`.

**Rollback (stop, then delete, HOST's order):**

```
launchctl bootout gui/$(id -u)/com.xian.seat-browser-web && ~/Development/mediajunkie/scripts/seat-browser-run.sh --revoke web
```

**Hand-test:** the classifier refused it ("Undermining Oversight"). That run was the wrapper under `env -i`, then `--check web`. I didn't retry. So line 2 after xian's load is the first real run, and it's a better test anyway because it runs under launchd. I've told Exec with the reason and the D6 line.

**After the load:** I add the manifest row to docs/schedules.md (the drift detector flags an unmanifested agent), and the arm moves from "not installed yet" to the full assertion.

**For `.mcp.json`:** the arm doesn't run `seat_browser.py`. It asserts the same properties itself, so nothing in my cycle sends to the browser.

Pard
