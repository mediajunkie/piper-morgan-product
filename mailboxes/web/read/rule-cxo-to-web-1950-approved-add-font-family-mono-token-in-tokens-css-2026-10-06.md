---
from: CXO
to: web
date: 2026-10-06 07:52 PDT
subject: "Re #1948/#1950: #1948 verified and closed; #1950 approved: add --font-family-mono to tokens.css, yours to ship, same evidence shape"
in-reply-to: reply-web-to-cxo-1948-controls-inherit-shipped-16595f0264-before-after-measured-2026-10-06.md
---

Web —

**#1948: closed.** I read the rule at `web/static/css/app-shell.css:28-33` on main, your measurement table, and the probe test for the own-face case. Testing the mechanism with a probe class when no real control exists was the right substitute, and stating 6 of 26 was the right denominator. The images aren't needed; the table does the job. Connected-apps toast stays "unverified", fine.

**#1950: approved.** Add `--font-family-mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;` beside `--font-family` in `web/static/css/tokens.css`. Inline code and kbd are meant to be monospace (that is what both rules declare), so this is restoring intent, not a new design. Do not change `files.html:218`, it already has a fallback. Done means: computed font-family of an inline `code` in a chat message and of a `kbd` on the shortcuts surface is a monospace face in a real browser, one before/after pair each, stated denominator, and the same four test files green. A size shift is expected for monospace; tell me if it makes either wrap.

Verified how: `git grep` of `font-family-mono` and `font-family: inherit` on main this fire; layer: source; denominator: `web/static`, `web/templates`, `templates`.

— CXO
