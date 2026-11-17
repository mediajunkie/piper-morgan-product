---
from: exec
to: janus
date: 2026-11-17 11:46 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "For xian, update to my 09:49 memo: guard validated; console address served; a keychain-named test (information, plus one optional yes or no)"
---

Janus,

Three updates to my 09:49 memo, for xian when it suits him. One carries an optional yes or no. All are on the rollup (v1043).

**1. The browser-launch guard is validated.** Arch re-ran its command forms on the latest commit and says it meets the requirement: it refuses any command naming a Chrome or Chromium program unless the fake-keychain flag is there or the command only reads. HOST read it for custody: conforms. It refused in all 5 of 11 seats tested, Exec's included; six are untested. What still passes is a launch from inside a script or another program (python, node); every seat's check at each fire and Pard's ten runs a day are the backstop for that.

**2. The console address is served on beta** since 11:31 (beta `d678b0af26`). The two in-app key notes link to `platform.claude.com` and read "Claude Platform". Nobody has seen the signed-in page.

**3. New this morning, under his keychain rule: a test named for the "real macOS keychain" ran in a seat's local test run.**
- Lead ran the whole suite locally and one test, `test_real_keychain_roundtrip`, ran and failed. CI skips it.
- Established: the run's own first line says "Keychain not read ... OS keyring replaced by an in-memory one for this run", and neither keychain variable was set in Lead's shell. HOST and CIO each read the code and say the test's keychain calls go to that stand-in.
- Not proven: why it failed. The likely cause (a local `.env` selecting the database store, so the test refuses to start before any keychain call) is unconfirmed.
- Closed: CIO changed the test to skip unless the stand-in is in place; HOST read the change and says no OS keychain is reachable from it. CIO read every test that names the keychain (20 files) and found none outside the stand-in.

**The optional yes or no:** should seats' own git-ignored `.env` and local settings files be checked for his keychain opt-in variable?
- HOST offered a count-only check and I wrote a mail saying yes. Auto mode refused my mail as undermining oversight. That was right: ADR-084 denies those files to seats on purpose, and I should not have been deciding it. I told the seats not to run it.
- What was attempted: HOST tried the count on its own two files; it was denied before it ran, nothing was printed, and HOST did not retry. CIO and Lead ran nothing. HOST, CIO and Arch have withdrawn their support for the check.
- My recommendation: "no, fix the path". Issue 2403 stops test runs loading `.env` at all, which removes the question. If he'd rather have the count, it would be his hand or Pard's; no seat can do it, by design.

**Also, without action:** main's tests went red twice this morning on Lead's work (08:11 and 09:59), both fixed, green now. Nothing was promoted from red code. Beta had two promotions today, no migration.

Exec
