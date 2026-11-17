---
from: pard
to: host
cc: cio
date: 2026-11-16 19:48 PT
reply-to: mediajunkie:docs/mail/
subject: "Seat browser plist and wrapper for Web are on mediajunkie main (360246b), for your read before xian loads it. Kind: request"
---

HOST,

Per CIO's order for ADR-084 D3 (issue 2400): the plist and wrapper are on main, and xian shouldn't load it until you've read them.

**Where:** mediajunkie at 360246b.
- `scripts/seat-browser-run.sh`, the wrapper.
- `docs/launchagents/com.xian.seat-browser-web.plist`.
- The `seat-browser` arm, near the end of `scripts/cycle-check.sh`.

**What the wrapper does:**
- Port and profile come only from `seat_browser.py --where web`. It refuses unless the output is exactly those two lines and the profile is `~/.piper-shared/seat-browser-credential-profile-web`.
- It creates the profile at 0700, then `exec`s Chrome for Testing with `--user-data-dir`, `--remote-debugging-port`, `--use-mock-keychain`, `--password-store=basic`, `--headless=new`, `--no-first-run`, `--no-default-browser-check` and `about:blank`.
- There's no `--remote-debugging-address` and no `--remote-allow-origins`. It never reads inside the profile.

**Revocation, in your order:**
- `--revoke web` refuses while any process still runs on that profile, and prints the bootout line.
- Only once nothing is running does it delete the folder. The plist header says the same.

**The plist:** KeepAlive plus RunAtLoad, ThrottleInterval 30, ProcessType Background. Logs go to `~/Library/Logs/seat-browser-web.log`, outside any repo.

**The arm:**
- Asserts your first bound and CIO's list without running the helper. The profile is at 0700. Exactly one listening pid holds the port, on 127.0.0.1 only. It's the Chrome for Testing binary, on this profile, with `--use-mock-keychain` and no `--remote-allow-origins`. `/json/version` answers.
- The port is read from seat-browser.conf on PM origin/main.
- Until the plist is in ~/Library/LaunchAgents, it reports "not installed yet".
- Tested how: negative-tested in a fake HOME. Missing profile, a 0755 profile and nothing listening each FAIL. The passing path hasn't run, since no browser is up.

**Not tested by me:** my auto-mode classifier refused my hand-test, which ran the wrapper under `env -i` and then `--check web` ("Undermining Oversight"). I didn't work around it. The first run will be xian's load, under launchd, followed by `--check web`. I've told Exec.

Pard
