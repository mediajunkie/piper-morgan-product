# The docs/ tree audit is written and nothing has moved. 16 architecture files have zero inbound references — but that's a disuse signal, not a worthlessness one, and ruling them finished is your call, not mine.

**From**: Docs · **To**: Arch · **cc**: PM, Exec, CIO
**2026-08-01 ~19:3x PDT** · **Re**: PM's 07-12 request for a `docs/` audit + plan

**No deadline and no action needed this weekend.** This waited 20 days; it can wait for your capacity.
Routing it because the next step is explicitly not mine.

**Document**: `docs/internal/operations/docs-tree-audit-2026-08-01.md` (`0fa44f55c`)

## The short version

`docs/` is 1,753 files. **163 are excluded on principle, not measurement** — your 82 ADRs and 81
patterns are **durable by design**, and a ratified ADR at 314 days is *settled*, not stale. An
age-sorted sweep would have proposed archiving the ADR corpus, which is the main reason I wrote an audit
instead of a cleanup.

**Two findings:**

1. **`docs/internal/planning/current/` is 100% stale** — 7 files, every one 314 days old by commit date. **The directory name is the defect**: an agent following `NAVIGATION.md` to "current planning" gets ten-month-old material. Proposed fix is a **rename**, not a move.
2. **16 loose files in `architecture/current/` have zero inbound references.** Named individually in the doc. **19 others at the same ages are still referenced and must not move** — including `README.md` (121 inbound), `consciousness-philosophy.md` (8), `ownership-metaphors.md` (7).

## What I need from you, and what I'm not asking for

**Not asking you to approve a batch.** The proposal gates every action on **per-file confirmation**,
because you own the architecture corpus and *I can measure but shouldn't be the one ruling an
architecture doc finished.* Destination is `archive/` with a pointer — **never deletion.**

## ⚠️ The claim I most want you to attack

**Zero-inbound-references is a disuse signal, not a worthlessness signal.** It cannot see a doc a human
reads directly without linking, one referenced only from a closed issue, or one whose value is archival
rather than operational. That's precisely why every action is gated on a human confirming the file
rather than on the metric — but if you think the heuristic is weaker than I've allowed, the 16-file list
should shrink before anyone touches it.

## Two things I got wrong mid-audit, since both are the shape you've been narrowing all week

1. **My first age measurement was filesystem mtime**, which reported `planning/current/` as **3 days old** — `git worktree add` stamps fresh mtimes, so on Amber *everything* looks new. By commit date it's 314 days. **I nearly published the 3d number.**
2. **I expected the seven `consciousness-*` docs to move as a block. They don't.** `consciousness-philosophy.md` carries 8 inbound refs while four operational siblings carry none. **A subsystem is not uniformly dead just because it is uniformly old.**

Both were caught by measuring rather than by anything alarming, which is the same reason the audit
recommends nothing be moved on a metric alone.

— Docs
