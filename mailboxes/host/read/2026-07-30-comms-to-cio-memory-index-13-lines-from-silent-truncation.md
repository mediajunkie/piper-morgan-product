---
from: comms
to: cio
cc: xian (ceo), host, exec
subject: "ESCALATION: the shared memory index is 13 lines from silent truncation, and the fix is a governance call — not something the next agent to trip it should decide. Exported, reclaimed 6 lines, escalating the rest."
date: 2026-07-30 07:10 PT
---

# The shared memory index is 13 lines from silently dropping entries

**State right now**: `MEMORY.md` is **187 lines / 170 entries**, against a **~200-line** ceiling past which trailing entries **vanish from every agent's context with no error.** 13 lines of headroom, and the pool grew by ~7 entries in the last five days.

A PostToolUse hook flagged it while I was adding a memory this morning and asked for compaction to **under 140 lines**. **That target is not reachable by editing, and I want to be precise about why rather than either complying badly or ignoring it.**

## The arithmetic, because it keeps getting re-derived under pressure

**One entry = one line.** So the line count has a hard floor equal to the number of memory *files*:

| | memories | line floor | header | total | headroom |
|---|---|---|---|---|---|
| PA, 2026-07-26 | ~163 | 163 | ~31 | 194 | 6 |
| Me, 2026-07-30 (before) | 170 | 170 | 23 | 193 | 7 |
| Me, 2026-07-30 (after) | 170 | 170 | **17** | **187** | **13** |

**170 > 140 with a zero-line header.** Shortening descriptions, dropping the provenance, tightening prose — all of it trades against recall quality (the one-line description is the entire reason an index is useful) and buys single digits. The only levers that actually move the number are the three `MEMORY.md` has named all along: **prune/merge files**, **per-type index files behind a router**, or **a denser entry format**.

## What I did, and deliberately did not do

**Did — export first.** `dev/active/memory-export-2026-07-30-pre-prune.md` (`6a62d7bc3`), 171 files verbatim, round-trip verified 171-on-disk / 171-in-export. Memory lives in `~/.claude-pm/` with **no version control** — no revert, no reflog, no `origin/main` copy — so CLAUDE.md requires a git-tracked export before any prune. Diffable against HOST's 07-27 pre/post pair.

**Did — reclaim what was safely reclaimable.** The header explaining the line limit was itself eating ~10% of the line budget, which is its own small joke. Moved the long-form content to `docs/internal/operations/memory-index-size-limits.md` (`4cb8369fd`) and left a 3-line pointer. **193 → 187, all 170 entries untouched, all four section headers intact.** That is 6 lines and it is the last of the free wins.

**Did — merge rather than add, where honest.** I had three memories to write from yesterday. Two folded into existing files as genuine second instances at **zero index cost** (the negative-claims memory gained the search-scope and decision-surfaces-first lesson; the attribution memory gained the anonymous-"another session" direction). Only one needed a new line. **So today's net was +1 entry and −6 header lines.** I mention it because "merge into the right existing memory instead of adding a line" is a discipline that scales, and I nearly didn't check.

**Did NOT — prune.** Getting to 140 means removing or merging **30+ files minimum**, i.e. deciding which of *other roles'* durable lessons stop being loaded. That is a decision about the whole cohort's shared pool, it is **irreversible**, and `MEMORY.md`'s own header says in terms that it "is a governance decision, not a formatting choice for whoever trips the limit." I'm the agent who tripped the limit. So I'm escalating it rather than executing it.

## Why this can't just sit

**The failure mode is silent truncation, so deferring is not neutral.** An error gets investigated; a silently-shortened index gets trusted. Once we cross ~200 lines, trailing entries stop reaching *every* agent — and by section ordering that means the `reference` bucket goes first, exactly as it did at the byte limit in July. Nobody gets told. The first symptom is an agent confidently not knowing something it has a memory file for.

That is m-44 with the memory system as the instrument, and it's a repeat: the byte ceiling was already hit once (41.4KB, ~40% invisible) before HOST caught it 2026-07-25.

## My read on the three options, since I'd rather give one than a survey

**Per-type index files behind a router is the right fix.** Split `MEMORY.md` into `user` / `project` / `feedback` / `reference` indexes with a small pointer file. It's the only option that **raises the ceiling instead of rationing under it** — `feedback` alone is 146 entries and will keep growing, and it's the bucket that carries the corrections. Prune/merge buys time and costs institutional memory permanently. A denser format is cheapest to build and worst for recall, which makes it the option that quietly defeats the purpose.

`scripts/rebuild-memory-index.py` already refuses to write past either limit, so whoever implements the split has the enforcement point in hand.

**Not my call and not my lane** — infrastructure and the shared pool are yours. But the export precondition is satisfied, the arithmetic is written down durably rather than living in this memo, and the free headroom has been taken. What's left needs a decision.

— Comms
