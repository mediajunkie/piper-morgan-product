---
last_updated: 2026-08-31
currency_claim: rewritten at every substantive fire (3x/day cadence)
max_age_days: 1
---

# CIO carry-forward — rewritten 2026-08-31 (16:37 WORK; frontmatter above is the checkable claim)

**Cron**: `a9ed03f9` · `7 10,16,22` LEAN · armed 2026-08-30 22:37 · **auto-expires ~2026-09-06
22:37**.
**Three silent cron deaths**: session exit · 7-day expiry · context compaction.
**Worktree**: Model A, `claude/cio-cycle`, upstream `origin/main`.

---

## ✅ NEW — the standing-items dating mechanism, real adoption + two real bugs fixed same-day

Direct PM engagement this morning (root-caused the recurring silent-deferral problem, built
`aging-standing-items.sh` via git archaeology not self-report, ran a cohort-wide audit via 3
subagents, delivered 8 per-role memos) generated real, immediate use this afternoon — not a
one-way broadcast:

- **CXO found a real false-positive class** (structural `Blocked on` column, invisible to
  phrase-matching) — fixed: any column named with "blocked" now blocks the row regardless of
  wording.
- **Web found a sharper bug**: my own broadcast said "date it like a diary entry," Web complied
  literally in inline prose, and the checker had zero path to read that shape — only table
  columns. Fixed: added a bold-inline-label form (`**Filed**:` under a heading) as a first-class
  recognized shape, corrected CLAUDE.md's own wording to name both forms precisely.
- **Caught my own bug while fixing the above**: shipped with `mapfile` (bash 4+), macOS ships
  bash 3.2. Caught by running it for real, not just syntax-checking. Fixed with a portable
  read-loop.
- Verified both fixes against real state AND dedicated fixtures (30/30 tests). Commits
  `2ab36bc3b` (checker), `d7d6c5e17` (CLAUDE.md).
- **Resolved the PA/Janus "possible overlap" honestly**: checked Janus's actual scope (Design in
  Product, not Piper Open/OpenLaws) before letting it consume a three-way — they're genuinely
  unrelated, told PA directly.
- **ppm retired their tracker independently, same-fire**, before my audit even reached them —
  same conclusion, arrived at separately.

**Coverage as of today**: 5 of 10 auditable trackers readable (cio, pa, docs, web, cxo); ppm/host
retired (legitimate); arch/comms/lead haven't adopted a dateable format yet.

## Open, non-blocking

- **Corpus-disposition pass (methodology-core)** — starts ~09-01 (tomorrow). Read `synthesis.md` +
  `findings/citation-census-summary.md` first; apply the B3 caution (citation-count triages, never
  disposes) from the first tier.
- **Chess-board day-close commit wiring** — second half of PM's cadence ruling. Not built. Whose
  duty-cycle step should own it — worth a quick PM check before assuming.
- **Non-interactive rate-limit setting** (raised 08-29 AM) — no PM reply yet.
- **`.mcp.json` chrome-devtools symlink** — still pending Pard's host-level half.
- **"Alarm-last-line" methodology candidate** — one instance (Lead, 08-26); watching for a second.

## Owed (re-read through the delegation lens before picking up)

- **`docs` inbox** — the cohort's one real mail backlog, not CIO's to fix.
- **Methodology candidate, not filed** (needs a 2nd instance): a completeness check keyed on the
  field that is never absent can never report incompleteness (Comms, 08-10).
- **Standing-items 7a-7e**: 7a raised to PM 08-31 (folded into 09-01 corpus-disposition context);
  7d filed as issue #1710; 7e already done; 7b/7c genuinely low-priority, waiting on others.

## Watch

- **arch/comms/lead** — haven't adopted a dateable format yet; not urgent, just genuinely
  incomplete coverage, stated honestly rather than chased.
- **Comms' BYOC marketplace narrative** — resurfaced to PM directly today (23 days since 3 angles
  + a steer, zero response); not mine to action, just tracking it resolved cleanly.
- **09-01 corpus-disposition pass** — the next real trigger on the calendar.
- **PM's response on the non-interactive rate-limit question and the day-close-commit ownership
  question** — neither blocking.

## ⭐ Operating-mode note, carried and reinforced today

"Shipped fast enough that real use corrected it same day" held twice more today, from two
different roles, on the same tool, within hours of shipping — the pattern is now well-established,
not a one-off. Both times the report named the exact fix rather than just the symptom (CXO: check
the column, not the phrase; Web: the mechanism has no path for this shape at all), which made both
fixes fast and confident rather than exploratory.

## Standing corrections to myself

- **A gap discovered at the next fire gets a retroactive close with the real cause, corroborated
  against other roles' independent accounts.** (08-28.)
- **When someone offers you their own relocated fix, match their discipline about WHEN to touch
  shared infrastructure — and then actually use the named trigger when it arrives.** (08-28 → 08-30.)
- **A new tool's first real output is a claim about the tool as much as about what it measured —
  don't report it as a finding about someone else until you've checked the tool is trustworthy.**
  (08-29 PM.)
- **Independent re-verification before landing catches implementation bugs, not design-assumption
  bugs.** (08-29 PM.)
- **"No rush" with no named trigger is the deferral antipattern — when a real trigger is named,
  use it at the trigger.** (08-30 AM.)
- **When you change your own stated plan mid-fire, send the correction the moment the plan
  changes — not whenever someone else's reply surfaces the gap.** (08-30 PM.)
- **When a caution is offered ahead of a task rather than discovered during it, bank it explicitly
  and apply it from the first instance.** (08-31 AM.)
- **Before flagging a possible overlap between two threads, check the actual scope of both — a
  plausible-sounding duplicate is still a guess until verified, and an unchecked flag can consume
  other people's attention on a non-issue.** (08-31 PM: the PA/Janus non-overlap.)
- **Test syntax-checking a script is not the same as running it — a portability bug (bash 4-only
  builtin on a bash-3.2 host) only surfaces by actually executing the thing.** (08-31 PM: `mapfile`.)
