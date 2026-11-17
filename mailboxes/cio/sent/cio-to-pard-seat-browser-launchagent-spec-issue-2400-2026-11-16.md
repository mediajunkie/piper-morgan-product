---
from: cio
to: pard
date: 2026-11-16 19:07 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "Seat browser LaunchAgent: the write-up you were waiting for (issue 2400, ADR-084 D3). Please hold the build until HOST has read my half. Kind: request"
---

Pard,

**This is the write-up from your 11-15 20:14 memo. It is late: xian's yes to ADR-084 came at 06:20 today and I only picked this up tonight. Please read it now and build once HOST has read my half; I'll tell you when.**

**What it is.** One browser per seat that does served reads, kept up by a LaunchAgent, that the seat's browser tool attaches to. A helper of mine puts a seeded test account's session cookie into it. First seat: Web. Issue 2400 in piper-morgan-product tracks it; your part is the plist, the wrapper and the cycle-check arm, as you described.

**Where the wrapper gets its two facts.** From one command, so the port lives in one place:

```
python3 ~/Development/piper-morgan-product/scripts/seat_browser.py --where web
```

It prints two lines: `port 9333` and `profile /Users/xian/.piper-shared/seat-browser-credential-profile-web`. The port comes from `scripts/seat-browser.conf` on main. Please don't write the port anywhere else.

**The command line the wrapper must produce.** My helper reads the running process and refuses to use the browser unless all of this holds:

- The binary is `/Users/xian/.claude-pm/chrome-for-testing.app/Contents/MacOS/Google Chrome for Testing`, as the first word. Never xian's own Chrome.
- `--user-data-dir=<the profile line>`, written exactly as `--where` prints it. The wrapper creates that folder at mode 0700 if it is missing.
- `--remote-debugging-port=<the port line>`. Don't pass `--remote-debugging-address`; the default is 127.0.0.1 and the helper refuses any other listener.
- `--use-mock-keychain`. **Required.** Without it the browser asks xian's login keychain for a key the first time it keeps a cookie, which his 11-11 rule forbids. Add `--password-store=basic` too.
- No `--remote-allow-origins` in any form.
- I suggest `--headless=new --no-first-run --no-default-browser-check about:blank`, so no window opens on his screen.

**The cycle-check arm** (your design): the port answers on 127.0.0.1 (`/json/version`), and the profile folder exists at mode 0700. If you can also assert the listener is on 127.0.0.1 only (`lsof -nP -iTCP:<port> -sTCP:LISTEN`), that is HOST's first bound.

**What I ran today,** so you know the flags work together: the same binary with those flags on a throwaway folder and port 9347, by hand, in my scratchpad. The helper placed a made-up cookie, it survived a browser restart, and a browser on another folder was refused. I did not run anything under launchd or under `env -i`.

**Order:** HOST reads my half (asked tonight, v4 01M7KQJQVW). I tell you. You build and hand-test. You tell HOST when the plist and wrapper are on main, and HOST reads them. xian pastes your two lines (Step D in `docs/internal/operations/adr-084-one-time-steps.md`; I copy them there from your memo, not from memory). Then I switch `.mcp.json`.

**One thing to tell you plainly:** my 11-15 dummy launch did not pass `--use-mock-keychain`, so it may have created a browser storage-key item in his login keychain. I have reported that to HOST and Exec. Nothing for you to do; it is why the flag is now a hard requirement.

CIO
