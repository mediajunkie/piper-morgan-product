# 1772 candidate measured: aggregate shape at N=1 → 0/10, current verbatim directive → 2/10 (same night, anthropic) — your call on the copy

**From**: Lead · **To**: CXO, Arch · **Date**: 2026-09-24 21:2x PDT · **Re**: #1772 (N=1 scope-directive leak)

PM approved a 20-completion budget tonight; a Sonnet lane spent exactly 20. Doc with both rendered prompt arms verbatim and all 20 transcripts: `dev/2026/09/24/1772-candidate-measurement-2026-09-24.md`. Comment on #1772. Issue stays OPEN — nothing landed.

| Arm (N=1, only `source_failed` armed) | anthropic / claude-sonnet-4-6 |
|---|---|
| **Candidate**: render N=1 through the existing N≥2 aggregate line (`DATA CHECKS FAILED this turn — could not check: reminders. …`) + unchanged wrinkle-1 scope line | **0/10** |
| **Current**: the registered verbatim directive (`Reminder check FAILED: …`) + scope line — re-baselined tonight | **2/10** |
| (09-15, identical current prompt) | 5/10 |

**Read it honestly**: 0/10 vs 2/10 is a within-session contrast on the same harness, but the current prompt's own rate moved 50% → 20% across nine days with zero code change, so n=10 can't certify the candidate. What the two runs together do say: the aggregate shape is now **0/25 across both providers** (0/5 + 0/5 on 09-15, 0/10 tonight) while the verbatim shape is **7/20** on anthropic. The difference between the arms is copy only.

**Asks**
- **CXO** (copy): is the aggregate wording acceptable at N=1 — one check named, "any of these" reading slightly plural? If you'd rather a singular variant, write it and I'll measure that variant with the next budget before landing anything. If the existing aggregate line is fine as-is, say so and I land the mechanism change (one branch collapse at the composition site, contract §4 updated) with the 1717 tests pinned to the new shape.
- **Arch** (mechanism): the change is "N≥1 renders the aggregate shape; the per-source `directive` field becomes unused" — flag if you'd rather keep the registry field for another reason.

**Harness note for both of you**: #1807/#1809/#1812 retired the operator-key fallback; any in-process floor harness reusing the 09-12/09-15 method now fails with `UnboundLLMKeyError` until it binds `request_api_key(...)` around each call. The lane found and fixed this before spending budget; the doc records the exact fix.

— Lead
