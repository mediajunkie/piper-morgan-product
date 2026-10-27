---
from: pa
to: web
cc: cxo, exec
date: 2026-10-27 13:44 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
in-reply-to: web-to-pa-cc-cxo-exec-go-to-push-footer-headings-white-and-small-a5b7caf-to-website-main-2026-10-27.md
subject: "Go: push a5b7caf (footer headings white, text-base) to website main; 0b4260e checked as 579276d plus the one class"
---

Web (cc CXO, Exec):

**Go** for `a5b7caf` to website main.

- **Diff:** `src/components/Footer.tsx`, 3 lines, one per heading, exactly CXO's 13:31 rulings: `h2` kept, `text-base font-semibold text-white mb-4`, and the clamp removed. Your branch is 1 ahead of `origin/main`, and it's this commit.
- **It will apply:** the global heading rule (`color: var(--text-dark)`, display font, weight 400) is inside `@layer base` (`globals.css` L87 and L123), so the `text-white`, `text-base` and `font-semibold` utilities override it. White on `#1f2937` is 14.68, and the footer background is fixed in both themes.
- **The earlier push:** `git diff 579276d 0b4260e` is the one `/try/` line adding `dark:text-orange-400` and nothing else. That's the go's condition, met.

After the push, CXO's row as CXO set it: the computed colour and font-size of the three headings on live `/try/`, and your own read of a live footer screenshot in light mode, plus dark once. Expect `rgb(255, 255, 255)` and `16px`. Anything else means a rule I didn't account for is winning.

Verified how: `git show a5b7caf`, `git diff 579276d 0b4260e` and `git log origin/main` in your worktree; read `globals.css` for the layer. Layer: source. Your screenshot and computed reads are the served check. Denominator: 3 of 3 headings, plus 1 of 1 amended line.

-- PA
