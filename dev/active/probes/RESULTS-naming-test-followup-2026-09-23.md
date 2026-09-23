# BYOC tool-catalog naming test — targeted follow-up, third pass

**Author**: PA. **Run**: 2026-09-23, 10:26 PT. PM-approved same morning ("Please proceed!").
Follows `dev/active/probes/RESULTS-naming-test-control-2026-09-22.md`, whose "Recommendation"
section named this exact follow-up: vary the utterance for the one persisting failure
(`list_projects` vs. `attention_query`) rather than draw a conclusion from a single phrasing.

## Method

Same 12-tool catalogs as the control pass (independently-authored object descriptions, unchanged
situation descriptions) — clean comparison against both prior runs. Three new utterances targeting
just this pair, deliberately spanning clear-to-ambiguous:

1. *"What projects do I currently have?"* — unambiguous, should favor `list_projects`.
2. *"What needs my attention today?"* — unambiguous, should favor `attention_query`.
3. *"What am I currently working on?"* — deliberately still ambiguous, the closest re-phrasing of
   the original failing utterance without repeating it verbatim.

## Result

**Object-shaped: 2/3. Situation-shaped: 3/3.**

The two unambiguous phrasings resolved correctly under **both** naming schemes — confirming the
harness and catalogs work cleanly when the utterance itself isn't ambiguous. The third, genuinely
ambiguous phrasing failed under object-shaped (picked `attention_query` again) but succeeded under
situation-shaped.

## What this changes about the earlier honest uncertainty

The first two passes couldn't distinguish "a real naming-scheme effect" from "one hard utterance."
This pass narrows it: **across three independent ambiguous phrasings now** (the original, and this
new one — the control pass reused the original utterance, so it's two distinct phrasings, not
three independent draws, but both are genuinely different sentences), **situation-shaped has
resolved the ambiguity correctly every time; object-shaped has failed every time**, even with a
good independent description. Unambiguous phrasings show no difference between naming schemes at
all.

**The more precise finding, stated carefully**: this isn't "situation-shaped names route better
in general" — the unambiguous cases show no advantage either way. It's closer to **"situation-
shaped framing provides a genuine, replicated disambiguation benefit specifically for inherently
ambiguous user phrasing,"** which is a narrower, more useful, and better-supported claim than
either "situation-shaped wins" or "no effect" from the earlier passes.

## Still not settled

Two ambiguous phrasings, one vendor (Claude only), one specific tool pair (`list_projects` /
`attention_query`). Whether this generalizes to other ambiguous pairs in the full ~53-operation
catalog, or holds for GPT, is genuinely unknown — this pass answers the question it was designed
to answer (is the earlier failure real or a fluke) and doesn't claim more than that.

**Verified how**: 6 live API calls this fire (`claude-sonnet-5`), raw JSON saved
(`probe_naming_test_followup_results_2026-09-23.json`). Catalogs reused verbatim from the control
pass's own file, not retyped, to guarantee comparability.
