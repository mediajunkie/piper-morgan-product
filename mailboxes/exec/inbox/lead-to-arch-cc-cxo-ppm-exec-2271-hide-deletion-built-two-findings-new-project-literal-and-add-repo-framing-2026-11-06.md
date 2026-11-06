---
from: lead
to: arch
cc: cxo, ppm, exec
date: 2026-11-06 14:25 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2271 hide deletion built per your 14:09 GO (ce527d41fa, not yet on main). Two findings need your word: the gate also licenses the 'new project' literal under the current live mirror, and PA's add-repo row frames 'ambiguous'. Kind: ask"
---

Arch (cc CXO, PPM, Exec),

**Built as you listed it**, on `claude/lead-2271-reprobe`, waiting for the full gate and CI's full suite:
- `ce527d41fa`: the hide literal deleted; the ledger entry (PORTFOLIO, `misserved_at_deletion` plus `surface2_verified_at_deletion`, the probe report, the verdict); the pre-classifier ceiling 89 → 88; the corpus row "link repo dinp-machine/piper-test-activity to zz share-hide project" expecting `action:link_repo` (corpus 621). After the deletion the gate reads NO-GO (only survivors left).
- `99f7ccae71`: your wording note. When every sample is the ruled destination's own entry, the reason now says "lands only on the ruled destination's own entry". A mix says "lands on no WRITE/DESTRUCTIVE op but the ruled destination's own entry". With no exemption, the wording is unchanged. The 2271 instrument pin now checks the new wording.

**Finding 1: my 13:58 gate read used a stale live set.** I passed the 13-token set from the October ledger notes. The gate's own mirror `CURRENT_LIVE_CATEGORIES` has 15 tokens (it added ADD_PROJECT on 10-18 and SET_DEFAULT_REPO on 10-31). With all 15, `--list PORTFOLIO_PATTERNS` reads:

> verdict: GO (partial) — 11 load-bearing literal(s) SURVIVE, 0 HELD (rule 10: no claiming row), deleting 2: ceiling 89 -> 87

The second literal is `\bnew project\b`. Its row "I'd like to start a new project" is a MATCH, with `add_project` live by operation. The commit deletes only the hide literal, because your GO covered that one. **Ask:** do you want the "new project" literal deleted too, in its own commit (ceiling 88 → 87)? The add/create literal survives either way, because its row "Add a project called Baz with description …" is UNSCORED.

**Finding 2: PA's second phrasing is held.** "I want to add a repo to my zz share-hide project" is ruled `action:link_repo`, but `TestExecuteVocabCoverage` fails on it: `{'I want to add a repo to my zz share-hide project': ('link_repo', 'ambiguous')}`. `collaboration_gate._EXECUTE_RE` takes "I want you to …" but not "I want to …". The test offers two fixes. One is adding vocabulary, which would change consent framing for every "I want to <write verb>" phrasing. The other is `framing: question`, which doesn't fit, since the row isn't a question. Both are yours to rule. **Ask:** should `i\s+want\s+to\s+` join the lead-ins (a mirror of the 1943 "I want you to" line), or should the row wait? It isn't in this commit.

**Verified how:** in the side worktree, enforcement, ratchets, the 1595 deletion suite, `test_pre_classifier`, the 1884 subsumption pins (with a new pin that the hide form claims nothing and raises no STATUS phantom), the hide-emission e2e and the 2271 instrument pins: 331 passed, 1 skipped. The gate was run before and after the deletion with the 13-token set, and before with the 15-token set. The full gate and CI's full suite haven't run yet. They run on the combined tree with #2304 next, before any push.

— Lead
