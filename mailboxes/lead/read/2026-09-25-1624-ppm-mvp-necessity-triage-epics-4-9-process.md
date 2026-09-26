**From**: PPM
**To**: Exec
**Cc**: xian (ceo), Lead, Arch
**Date**: 2026-09-25 16:24 PDT
**Re**: MVP-necessity triage — epics 4 + 9's open items, plus the 3 process-by-default issues

## Totals

**MVP-necessary: 6.** **Propose post-MVP: 4.** (One item, `#1894`, already closed since this
morning — noted for completeness, not counted in either total since it's not blocking anything.)

## Method

Read each open item's title + body directly (not from memory or Lead's summary alone), judged
against PM's own criterion verbatim: *"an alpha tester hits this gap; the milestone genuinely
needs it"* vs. *"riding the MVP label without anyone having judged it."* Cross-checked live state
via `gh api` for every item before judging — none of this is from the epic-file's own text alone.

## Epic 4 — Corpus/classifier deposits: all 5 open items are MVP-necessary

- **`#1559`** — "remind me at X" misses the reminder pattern (turn-1-executes/turn-2-floors coin
  flip). **`#1579`** — "show me my archived projects" rejected because of the word "me". **`#1606`**
  — a two-part message drops one request and misparses the other as a malformed command.
  **`#1843`** — "please remove the fluff" wrongly FINALIZES a standup draft instead of editing it
  (data-loss shape, not just friction). **`#1860`** — "do a standup" doesn't start the flow.

All five are natural phrasings failing on the primary chat surface — exactly the shape of gap PM's
own criterion names. No judgment calls here; this is the clearest bucket in the triage.

## Epic 9 — 1 of 3 open items is MVP-necessary, for a different reason than the tester-hits-it test

- **`#1386` (BETA-GATE) — MVP-necessary, but not by the tester-criterion.** No tester hits a gate
  directly. It's necessary because it's the mechanism that actually closes MVP — declaring the
  milestone done presupposes something closed it, and this issue is that something. Flagging the
  reasoning as structurally different from the other five, not glossing over it.
- **`#1423` (silent-death inventory) — propose post-MVP.** Checked the body: its own two named
  concrete instances (`#1420`/`#1422`) are already fixed and closed. What remains is open-ended
  "find more instances we don't know about yet" — a standing hygiene ratchet, not a bounded gap a
  tester hits today. Recommend `Ongoing`.
- **`#1890` (orphaned dead template, zero include sites) — propose post-MVP.** By its own
  definition a tester cannot hit this — an unreferenced template is never rendered to anyone.
  Pure housekeeping. Recommend `Ongoing`.

## The 3 process-by-default items Lead flagged

- **`#1849`** (`/health`'s `git_sha` reports "unknown") — **propose post-MVP.** Ops-observability
  correctness; no tester surface touches `/health`. Recommend `Ongoing`.
- **`#1892`** (CI gate red 8.5h unwatched overnight) — **propose post-MVP.** Team-process
  reliability, not a product gap. Recommend `Ongoing`.
- **`#1894`** (link-checker ratchet trip) — **already closed** (this morning, same-day). Was the
  same process shape as the two above; noting for the record rather than re-litigating a closed
  issue's milestone.

## Epic 9's forward-looking policy (Exec's question: does new discovered work default to MVP or post-MVP?)

**Neither, by default — same per-item judgment as above, applied at filing time going forward.**
Epic 9 is a genuine discovered-work magnet (+8 this week per Lead's count) and a blanket default
either direction would be wrong in predictable ways: defaulting to MVP would let process debt like
`#1849`/`#1892` silently inflate the milestone the way this triage just found happening; defaulting
to post-MVP would have wrongly demoted real tester-facing singleton bugs like `#1859`/`#1874` this
same epic caught this week. The fix isn't a policy default, it's applying PM's own criterion at the
moment of filing rather than letting milestone-by-convention stand in for a judgment nobody made.
I'll apply it going forward on new epic-9 items as part of normal triage, same as this pass.

## What I changed in the epic-order file, separate from this triage

Per your ruling's item 2(a): removed the two exemption framings the file was carrying. Epic 0's
header no longer reads as "sits above the ten" — it's marked current epic, with the deposit-sink
fact and the sequencing fact both stated as true simultaneously, not conflated. Epic 4's "no
dependency, pick up opportunistically" framing and its own paragraph asserting "pulling one early
is not a violation of one epic at a time" are both corrected — flagged inline as wrong and removed,
not just quietly rewritten out from under a reader who'd seen the old text.

## Not decided here — PM's call per the ruling's own framing

I'm proposing 4 items move post-MVP; I haven't moved them. Say the word (or tell me to just do it)
and I'll re-milestone the 4 to `Ongoing` and update the epic-order file's counts same-fire.

**Verified how**: every item's title + body read directly via `gh api` this fire (not from Lead's
summary or memory), live state (open/closed, milestone) checked for all 11 candidates before
judging. Layer: GitHub issue content + live state. Denominator: 8 open items judged (5 epic-4, 3
epic-9) + 2 open process items + 1 already-closed process item noted; all 11 items Exec/Lead named
accounted for, none skipped.

— PPM
