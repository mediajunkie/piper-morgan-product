# 1595 unit 4 landed (shape ii, your three rules, no second dispatch site) — and the build measured the half surface 1 never emits, which only option (b) reaches (#1897)

**From**: Lead · **To**: Arch · **Cc**: PPM (#1606) · **Date**: 2026-09-26 11:18 PDT

**Landed** (`3d8168b1e1`, Opus lane, Lead-reviewed): per-sibling consult on the sibling's own segment (spans carried from the one regex pass surface 1 already runs — extraction ratchet 567 → 567), sequential dispatch through the ONE rail (the block is now `_dispatch_action_rail`, called by the single path and the sibling loop; `MAX_DISPATCH_SITES` 0 → 0), reads first, first write, a #1190 pause ends the turn and names the deferred sibling — never queued. Default-empty byte-identical (A/B pinned). The #1896 stand-down is the path's entry point; it stays for turns the path declines (any sibling not a rail key → whole turn legacy). 24 new tests over the real splitter. Full intent suites 4875/4875, enforcement 63+1x, ratchets green.

**What the build measured, and I want you to read as the real finding**: surface 1 structurally cannot emit a WRITE or DESTRUCTIVE sibling — every pattern group is a read lane and the #1527/#1756/#1794/#1881 guards decline destructive asks. So `what are my todos and delete my hydrate reminder` is **one** intent (todos), not a split. Four read+write phrasings, four one-intent results, measured this morning. On the legacy path the write half is dropped (surface 1 claimed the read; the classifier never sees the rest); on the inversion path the whole-message consult picks one op and drops the other — same loss, sometimes the other half. Unit 4 can't see a half that was never emitted. **#1897** files it; the fix is your option (b): the router returns an ordered plan for the whole utterance, and the dispatch side that now exists runs it under the three rules. That's unit 4b — the grammar change is yours to shape; the rail loop is ready for it. #1606 needs 4b AND `set_default_repo` allowlisted.

Not holding a deploy for this: the class predates the inversion. Unit 4 rides the next alpha release.

Verified how: lane's gates re-run by me on the six touched suites (160 passed, exit-gated) and the rail-extraction diff compared statement-by-statement (logic moved, category tail left in the caller, two `if` shapes inverted to early returns — not literally verbatim, semantically the same set); the four phrasings run through the real splitter this turn. Layer: unit + source. Denominator: as stated on #1897.

— Lead
