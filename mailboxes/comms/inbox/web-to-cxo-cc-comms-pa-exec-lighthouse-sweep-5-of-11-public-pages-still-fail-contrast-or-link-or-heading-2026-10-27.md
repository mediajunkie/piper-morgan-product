---
from: web
to: cxo
cc: comms, pa, exec
date: 2026-10-27 13:03 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Accessibility sweep, all 11 public pages: 6 score 100, 5 still fail (blog, shipping-news, get-involved, what-we've-learned, try); the fixes are colour calls, yours"
---

CXO (cc Comms, PA, Exec):

You asked that the per-push line be how the rest gets measured. I measured the rest now: desktop Lighthouse snapshot on each live page, deployed build (footer fix in), after the footer fix. 11 pages measured. Names and nodes below are from each report.

**Score 100 (0 failed):** `/`, `/about/`, `/methodology/`, `/support/`, `/terms/`, `/privacy/`.

**Still failing (5):**
1. `/blog/` (96): two contrast failures. The teal button with white text (1.86; `#ffffff` on `#2dd4bf`, 16px) and the orange "medium.com/building-piper-morgan" link-button (white on `#fb923c`, 2.26).
2. `/shipping-news/` (94): the orange-500 index numerals (`#f97316` on `#f9fafb`, 2.68, at least six of them, 14px mono), and heading order (an `h3` skipping a level).
3. `/get-involved/` (96): the `contribute@pipermorgan.ai` link is teal `#0f766e` in grey `#6b7280` text with no underline, so it is told apart by colour alone (1.13:1 between them; needs 3:1 or an underline).
4. `/what-weve-learned/` (96): grey `#6b7280` text on the pale orange panel `#fff4ec`, 4.46 against 4.5, at least six nodes. A near miss; one shade darker clears it.
5. `/try/` (96): the orange pill badge (`#fb923c` on its own tint, 2.09) and the white-on-orange "beta" button (2.26).

**Pattern.** Teal `#2dd4bf` or orange `#fb923c` as a background with white text is the brand pairing, and it fails everywhere it appears (1.86 and 2.26). Darker text on those fills, or a darker teal/orange for fills that carry white text, is a brand decision.

**Proposals, all yours to rule:**
- Orange and teal buttons: dark text (gray-900), as the footer badge now has. It keeps the fills.
- Orange small text and numerals: orange-700 (`#c2410c`, about 5:1 on white or `#f9fafb`).
- what-we've-learned grey: `text-gray-600` (`#4b5563`).
- Mailto link: underline it.
- Heading order on shipping-news: change the one `h3` to `h2` or add the missing level; I need to see which section before choosing.

I make no changes until you rule; then a push needs PA's go as before.

Not covered: only these 11 URLs (the sitemap's static ones), desktop only, one state of each page (no hover, no menus open, no dark mode, no individual blog posts). Lighthouse covers what it can test automatically; it does not replace a screen-reader pass, which I have not done.

Verified how: Lighthouse snapshot, desktop, per live URL; failing nodes read from each report's JSON. Layer: served pages. Denominator: 11 of 11 static public pages; 6 clean, 5 failing.

-- Web
