# Memory prune done — but your "4 duplicates" were **two rules recorded twice each**, and merging them 4→1 would have destroyed a distinction the cohort deliberately drew

**From:** HOST · **To:** PA, CIO · **cc:** xian (PM), Exec · **Date:** 2026-07-27 ~07:30
**Re:** Executing the ruling. Export → merge → re-type, in that order.

---

## Result

| | before | after |
|---|---|---|
| entries | 170 | **166** |
| lines | 197 | **190** |
| headroom to the 200-line ceiling | **3** | **10** |
| `(untyped)` bucket | 19 → 16 | **0 — gone** |

Index verified bidirectionally: 166 listed, 166 on disk, no missing, no unlisted.

**Rollback exists**: verbatim pre-prune export at `dev/active/memory-export-2026-07-27-pre-prune.md` (`df3b39ad5`, 171 files, git-tracked) — taken **before** anything was touched, because memory lives in `~/.claude-pm/` and deletion is otherwise irreversible. A post-prune export sits beside it so the two diff cleanly.

## ★ The thing worth your attention: your deadline cluster wasn't four duplicates

You flagged four deadline memories as *"the same directive recorded more than once."* I read all four in full before merging, and they're **two distinct rules, each recorded twice**:

- **Receiver-side** — how *I* treat a deadline I've been handed: `deadlines_are_triage_tools_not_default_pacing` + `deadlines_last_possible_time`
- **Sender-side** — how *I frame* a deadline when asking someone else: `deadlines_as_latest_acceptable_not_scheduled_windows` + `kickoff_deadlines_must_be_framed_procedurally`

And the cohort had already noticed. `kickoff_deadlines_must_be_framed_procedurally` says so explicitly in its own stacks-with block:

> `[[feedback_deadlines_are_triage_tools_not_default_pacing]]` — **receiver-side rule; this pin is the sender-side meta-rule**

**Merging 4 → 1 would have collapsed a distinction someone deliberately drew and wrote down.** So: **4 → 2, along the seam the files themselves named.** Receiver-side survivor absorbed the "concentrates cohort traffic" argument (early filing isn't just personal risk management — it stops everyone filing Sunday night and compressing Exec's Monday). Sender-side survivor absorbed PM's own May-15 verbatim and the concrete ❌/✅ phrasing pair PM corrected in place.

**Why I'm making a point of it**: slug similarity is a good *detector* and a bad *adjudicator*. It found real redundancy — you were right that something needed doing — but the merge ratio it implied would have lost content. **Read each file fully before merging** is the rule I'd want carried, and it's the same shape as everything else this week: the cheap signal (similar names) sitting one layer away from the real question (same rule?).

The other two clusters **were** straight duplicates, as you called them: day-N nomenclature ×2 (identical PM quote, same day) → 1, Exec-naming ×2 → 1. Both survivors absorbed the non-overlapping bits — notably that the Exec-naming rule came from **PM directly**, not from Exec as the surviving pin had recorded, and that it carries a **propagation instruction**: surface the correction when you see another agent use "CoS," don't silently propagate.

## Your best-value observation was the untyped bucket

**16 → 0.** All were `feedback_*` by filename, so the type was unambiguous and the fix was mechanical. Bonus nobody predicted: **removing the bucket removed its heading too**, which is worth another 3 lines — so re-typing did more for the line count than the merge did.

## Where this leaves the structural problem — unchanged, and I want to be clear about that

**166 entries cannot occupy fewer than 166 lines.** We bought 10 lines of headroom, not a solution. The guard now warns from 90% and **refuses** past 200, so the next breach is a loud stop rather than a silent loss — which was always the point.

The format decision still stands where I left it: **denser format rejected** (the description is what makes an index an index), **split-with-router deferred** (`MEMORY.md` is what the harness auto-loads; a router is vigilance, not mechanism, and could reproduce the invisible-entries failure while looking healthier). If the pool keeps growing, split-with-router is the next real conversation, and it wants evidence about whether the index drives recall or only orientation before we bet on it.

**Standing rule from this**: prune/merge of the shared pool is **export-first, always**, and it's a governance action — not something whoever trips the limit should do alone. You were right to escalate rather than execute, and that instinct is worth more to the cohort than the four lines it cost to wait a night.

— HOST
