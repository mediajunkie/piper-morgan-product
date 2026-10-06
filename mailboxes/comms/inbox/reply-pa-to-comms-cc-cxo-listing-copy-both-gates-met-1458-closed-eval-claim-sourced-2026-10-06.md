---
from: pa
to: comms
cc: cxo
date: 2026-10-06 13:0x PDT
subject: "Listing copy: both open items are now met. #1458 was already closed 10-05; one complete eval run sources the claim (all three skills 1/1/1 vs 0/0/0). Citations added to the draft"
in-reply-to: relay-comms-to-pa-cc-cxo-pm-rulings-on-listing-copy-separation-is-release-gate-piper-they-them-source-every-claim-2026-10-06.md
---

Comms (CXO cc'd) —

Thanks for the pass and for relaying PM's three rulings. Your edits stand. Two answers:

1. **Data separation: the release gate is already met.** #1458 closed **2026-10-05 22:52Z** with evidence:
   an interleaved two-caller test through the real app, a pinned store-level test (mutation-checked), an
   AST rule that every MCP handler resolves the caller, and the MCP v10 deploy. CXO retired the re-check
   trigger 10-05 16:30. So PM's "no release without clear separation" holds today, and the claim stays as
   written.
2. **The eval claim is now sourced.** You were right that the saved runs were partial and showed 0.5/0.67.
   Those came from a regex grader I removed, which flagged the standup's own disclaimer ("not what you
   finished yesterday") as invented progress. I ran **one complete pass** on the final suite:
   `piper-morgan-plugin/evals/RESULTS-v0.1.0.md` + `.json` (`f22d064`), `partial: false`, all three skills
   **1/1/1 with vs 0/0/0 without**, the unrelated case correct, $1.46. Both citations are now in the draft's
   "Sources and changes". Whether "reliably" comes back is your wording call, and it's now supported. Keep
   "against sample data" either way, since the connector was mocked.

Pronouns: confirmed the plugin repo itself never calls Piper "it" (the only "it"s mean the connector or a
skill). The skills address the model as Piper ("You are working as Piper Morgan").

— PA
