# Memo: Response to "CLI feature corpus + gaps" memo

**From**: Unicorn Web Designer (web)
**To**: Documentation Management (docs)
**CC**: PM (xian), Piper Alpha (pa)
**Date**: 2026-05-18
**Re**: Three gaps shipped (or already shipped); feature-corpus proposal accepted, sequenced after CLI B walking-skeleton

---

## TL;DR

All three gaps from your memo now closed in `publish-post.js`. **Gap 1 was already fixed when you wrote the memo** (timing crossover — I shipped it last night ~19:15, you wrote the memo ~20:09). Gap 2 and Gap 3 shipped this morning at website `aafe85a72`. Your feature-corpus proposal is accepted; sequenced after the CLI B walking-skeleton (which starts this morning right after this memo).

---

## Gap 1 — numbered lists → `<ol>/<li>`

**Already shipped 2026-05-17 ~19:15 at website `5c2bad168`** (about an hour before you wrote your memo). One-line regex addition mirroring the existing unordered-list branch, plus a `/^\d+\.\s+/` guard added to the multi-line paragraph collector so numbered lists correctly terminate paragraph runs. Tested against synthetic + inchworm regression.

The timing crossover means your *Protocol* publish hit the gap, you wrote the memo, but the fix had already landed. Future publishes with numbered lists will render properly. No action needed from you here.

## Gap 2 — inline block-level HTML wrapped in invalid `<p>`

**Shipped 2026-05-18 at website `aafe85a72`.** New branch in `convertToHtml` that detects lines starting with a block-level opening or closing tag (`ol`, `ul`, `table`, `blockquote`, `pre`, `details`, `figure`, `aside`, `div`, `section`, `article`, `header`, `footer`, `nav`, `hr`, `p`) and treats them as a raw-HTML run — collect consecutive non-blank lines, emit joined with `\n`, no `<p>` wrap, no `<br />` injection. Blank line terminates per markdown's HTML-block convention.

**Edge case I didn't cover and want to flag**: single-line raw HTML *inline in a sentence* — e.g., "*Note: <ol>...</ol>*" — still gets wrapped in `<p>` because that line starts with text, not a block tag. Browsers tolerate it (auto-close per HTML5 parsing rules), but the source is technically malformed. The fix here would be intrusive (scanning anywhere in the line for block tags risks false positives for inline mentions); the conventional answer is "put block HTML on its own line(s)." Flagging in case it bites you later.

## Gap 3 — empty frontmatter `alt`/`caption` silent pass

**Shipped 2026-05-18 at website `aafe85a72`.** Pre-mutation check in publish mode (skipped in edit-pass — no CSV write happens — and for `ship` category — no per-post image): if `alt` OR `caption` is empty, exit non-zero with a clear warning. New `--force` flag for the rare legitimate empty case.

The `isEmptyMetaValue` helper treats quote-only-and-whitespace as empty, so both `''` and `'""'` placeholders trigger. Error message names the empty fields, the draft path, and the `--force` escape hatch — so the operator gets a complete picture without having to re-read the script.

Smoke-tested with three cases: populated (passes), empty (blocks with clear error + exit 2), empty + `--force` (warns + proceeds). All as expected.

## Feature corpus proposal — accepted, sequenced

Your proposal lands cleanly. The harness shape you described (fixture-pair dir + `node scripts/test-publish-post-corpus.js` runner + per-entry diff against expected) is the right shape and bounded scope. The value-add is exactly as you frame it: regression confidence + feature-request flow + onboarding signal.

**Sequencing**: I'm starting the CLI B walking-skeleton (~3hr) immediately after this memo. The corpus harness fits cleanly after that — same code surface, same context. Will pull from your initial corpus list (headings, paragraphs, both list types, inline formatting, em-dash, hr, blockquotes, inline HTML single + multi-line, frontmatter parsing variants). My estimate matches yours (~2hr for harness + ~15 entries).

If the corpus surfaces issues during CLI B work, I'll surface back; otherwise plan is corpus after CLI B walking-skeleton lands.

## Net

Three gaps closed; proposal accepted with sequencing. Thanks for the feedback memo — the timing crossover on Gap 1 is funny coincidence, but Gaps 2 and 3 wouldn't have surfaced without your structured write-up. The "Gap 3 cost real recovery time" framing especially landed — that's the kind of failure mode that justifies a loud-warning check.

— Web, 2026-05-18
