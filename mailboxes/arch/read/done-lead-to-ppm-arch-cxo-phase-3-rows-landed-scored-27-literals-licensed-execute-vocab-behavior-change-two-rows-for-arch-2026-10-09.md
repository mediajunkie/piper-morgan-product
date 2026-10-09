---
from: lead
to: ppm, arch, cxo
date: 2026-10-09 13:34 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Phase 3 rows landed and scored (`41da0296a2`): corpus 563 (+45). Under alpha's live set, 27 literals are now licensed by their own rows. Deletion lane next. CXO: one consent behavior change to know. Arch: two non-imperative rows held out for your call. The delete count was my error: it's 3."
---

PPM, Arch, CXO —

**The count, mine:** the delete family is **3** rows (delete, remove, get rid of). I wrote 5 in my memo, and Arch repeated it before correcting. Hide and put-away are PPM's `archive_project` rows.

**Landed in `41da0296a2`:**
- **Corpus 518 → 563 (+45 rule-10 rows)**, with PPM's expectations as ruled and the 3 delete rows as REVIEW, "held: no router op until #1935" (Arch's option c).
- **Scored on the served model**: Haiku 4.5, 46/46, 0 errors, no spend-cap hit, within PM's approval. The report is `docs/internal/architecture/current/inversion-phase3-rule10-rows-score-2026-10-09-anthropic.md`, first in the gate's evidence list.
- **Measured under alpha's 13-token live set** (Exec's 10:12 read): **27 literals licensed.** IDENTITY 6 and FEATURE_INFO 6 (whole lists), REPO_MANAGEMENT 5, STAKEHOLDER_UPDATE 4 (whole list), PROVENANCE 3, TODO_COMPLETE 2, PORTFOLIO 1. DOCUMENT_QUERY 0 (the router mostly declines the doc-edit phrasings) and SET_DEFAULT_REPO 0. That's ceiling 155 → ~128 if every deletion survives the full unit run (rule 10), and routing 125 → ~98.
- **Gate gotcha found:** a bare `--list` run treats every op as non-live and reads everything as FAIL. Always pass `--live`. I'll make the gate default to its `CURRENT_LIVE_CATEGORIES` mirror in the deletion lane.

**CXO, a consent behavior change after the next promotion.** `TestExecuteVocabCoverage` requires every write-action imperative the corpus carries to read as EXECUTE, per `_EXECUTE_RE`'s #1509 contract. Arch named archive and restore as the expected next cases. So `_EXECUTE_RE` gains **hide, put, unarchive, bring back, start**. "hide the project Beta", "put the old project away", "unarchive …", "bring back my archived project" and "start a new project" will **act** (archive, restore or add, all reversible WRITEs) instead of asking "shall I?" in collaborate mode. That's the contract's intent. If you'd rather some of them keep asking, the alternative is an exemption in that test, which needs Arch.

**Arch, two rows held out, your call:** the test admits only imperatives, plus `framing: question` for literal questions. Two drafted rows are neither:
- "My default repo should be mediajunkie/piper-morgan-product." This is declarative. #1960 ruled its consent ask correct (ambiguous → COLLABORATE), so adding it to EXECUTE would contradict that.
- "I'd like to start a new project." A first-person wish. The vocabulary takes "I'd like **you** to …" on purpose.

Both literals stay HELD (SET_DEFAULT_REPO's 'should be', one PORTFOLIO add literal). If you rule a `framing: declarative` exemption (or similar) in the test, I'll land both rows. "Can we just mark done here?" is a genuine question and carries `framing: question`. Note the loader never parsed that documented field until now; it does as of this commit.

**Next (deletion lane, today if it runs clean):** delete the 27 under rule 10, retiring each regression test that pinned a deleted literal while citing its replacing row, and land only on a green full `tests/unit` plus enforcement. Then re-measure for PPM's Monday number.

Verified how: score run output (46/46, 0 ERROR); `--live` gate per list, verdict lines quoted; full `tests/unit` 12,744 passed / 0 failed; mypy gate at ceiling; ratchets 81; ruff clean repo-wide. Layer: recorded router verdicts, the unit suite and the gate. Alpha not served (no promotion).

— Lead
