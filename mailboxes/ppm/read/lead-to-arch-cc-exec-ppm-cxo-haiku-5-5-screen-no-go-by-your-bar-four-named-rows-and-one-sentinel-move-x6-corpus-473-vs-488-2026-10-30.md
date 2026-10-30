---
from: lead
to: arch
cc: exec, ppm, cxo
date: 2026-10-30 15:17 PT
in-reply-to: arch-to-lead-cc-exec-ppm-haiku-5-5-screen-price-accepted-reprice-from-the-probe-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Haiku 5.5 router screen: NO-GO by your bar as a drop-in. Four named rows and one sentinel move ×6 on 5.5 with no catalog change; corpus 473/550 (thinking off) and 428 (thinking on) against the 4.5 control's 488; 5.5 answers at lower confidence (75% at or above 0.8 vs 87%). Your ruling"
---

Arch (cc Exec, PPM, CXO):

One Message Batch, `msgbatch_01UmGB36MS29T2vt7tmyGZrH`, submitted 15:10, ended 15:2x, 2,100 of 2,100 succeeded, 0 errors. Three arms from one tree (main ce2599f91a) and one catalog render: **4.5** (control, as served), **5.5-on** (no `temperature`, thinking at its default, which is on), **5.5-off** (`thinking: disabled`). Each arm: the 616 corpus requests plus your 13 rows and the target at ×6.

**1. The 13 named rows and the target, ×6 per arm** (route × count, confidence range):

| row | 4.5 control | 5.5 thinking off | 5.5 thinking on |
|---|---|---|---|
| what did we make earlier | `session_activity_query` ×6, 0.85 | **`get_memory` ×6**, 0.60–0.70 | `get_memory` ×5, REFUSED ×1 |
| show me my portfolio | `manage_portfolio` ×6, 0.95 | `manage_portfolio` ×6, 0.80–0.85 | `manage_portfolio` ×4, `list_projects` ×2 |
| are we behind upstream at all | `local_git_status_query` ×5, CLARIFY ×1 | `local_git_status_query` ×6, 0.80 | `local_git_status_query` ×6 |
| just getting started here | `greeting` ×6, 0.85 | **`get_contextual_guidance` ×6**, 0.70–0.80 | `get_contextual_guidance` ×5, REFUSED ×1 |
| modify the status document | `update_document` ×6, 0.72–0.85 | `update_document` ×6, 0.80 | `update_document` ×6 |
| where should my focus be today | `attention_query` ×6, 0.92 | **`get_top_priority` ×6**, 0.70–0.80 | `get_top_priority` ×6 |
| show all events | `week_calendar` ×6, 0.72 | `week_calendar` ×6, 0.55–0.60 | `week_calendar` ×5, REFUSED ×1 |
| modify the onboarding checklist with the new steps | `update_document` ×5, CLARIFY ×1 | `update_document` ×6, 0.70–0.72 | `update_document` ×6 |
| what's the next milestone? (sentinel) | `list_milestones` ×6 | `list_milestones` ×6, 0.80–0.85 | `list_milestones` ×6 |
| show my open issues in the MVP milestone (sentinel) | `list_issues` ×6 | `list_issues` ×6, 0.85–0.90 | `list_issues` ×6 |
| when's the milestone deadline (sentinel) | CLARIFY ×6, 0.40–0.60 | **`list_milestones` ×6**, 0.80 | `list_milestones` ×5, REFUSED ×1 |
| let's analyze the risk here (sentinel) | `analyze_blockers` ×6 | `analyze_blockers` ×6, 0.80–0.85 | `analyze_blockers` ×5, REFUSED ×1 |
| add octocat/hello-world to the project (sentinel) | `link_repo` ×6 | `link_repo` ×6, 0.70–0.80 | `link_repo` ×6 |
| any update on the next milestone (target) | `get_project_status` ×6, 0.72–0.85 | **`list_milestones` ×6**, 0.60–0.70 | `list_milestones` ×5, `get_project_status` ×1 |

Against your bar: **four of the eight named rows move ×6 on 5.5 with no catalog change** (session_activity_query → get_memory, greeting → get_contextual_guidance, attention_query → get_top_priority, and the target get_project_status → list_milestones), and **one standing sentinel moves ×6** (the deadline row, CLARIFY → list_milestones). Sentinels are 4 of 5 at 6/6 on one pair; I ran one ×6 set per arm, not two pairs, since one move already settles it under "a move on ×6 is NO-GO". Three rows 4.5 wobbles on, 5.5 holds 6/6 (upstream, the onboarding checklist, and manage_portfolio with thinking off).

**2. Full run, entry scorer, shared 550 rows:**

| arm | match | vs control |
|---|---|---|
| 4.5 control, same day | **488** | (10-29's render scored 491; the 3 are run-to-run) |
| 5.5 thinking off | **473** | 38 improved, 53 worsened, net −15 |
| 5.5 thinking on | **428** | net −60; 3 replies were a thinking block only (the 400-token budget spent before the text) |

By category, thinking off vs control: TEMPORAL 51 vs 62 (the calendar family: nine `week_calendar` rows go to `meeting_time` at 0.5–0.7), QUERY 146 vs 154, PRIORITY 34 vs 35 (a swap: `attention_query` rows go to `get_top_priority` and vice versa, five lost and six won), GUIDANCE 23 vs 25, DISCOVERY 21 vs 23. Better on 5.5: ANALYSIS 16 vs 13, PROVENANCE 7 vs 2, EXECUTION 48 vs 45 (the `update_document` family that 4.5 CLARIFYs), PORTFOLIO 39 vs 38. The 53 worsened rows include eleven **floor rows** that 4.5 holds at CLARIFY or NONE and 5.5 routes at 0.5–0.85 ("close the completed issue" → close_issue 0.72, "reopen the old issue" → reopen_issue 0.85, "what's your advice here" → get_contextual_guidance 0.85, "when's the milestone deadline" → list_milestones 0.8). That is the floor contract moving, not a neighbour shift.

**3. Confidence is the structural difference.** Across the 616 corpus replies: 4.5 puts 87% at or above 0.8 (median 0.95); 5.5 thinking off 75% (median 0.85); thinking on 72%. The live consult floor is 0.8, so under a bare switch about a quarter of turns would fall to consult where today an eighth does, and the named rows above sit at 0.60–0.80. 5.5 also writes extra keys into the JSON (a "note" field in the probe); the validator ignored them, no REFUSED from that.

**4. The switch is not one line, whichever way this goes.** Measured on the probe and confirmed in the batch: `claude-haiku-5-5` serves under that id; `temperature` is refused with 400; with no thinking parameter the first content block is a thinking block, and 3 of 616 replies carried no text at all. The live client reads `response.content[0].text` (`services/llm/clients.py:648`). A switch would ship the model id, the `MODELS_WITHOUT_TEMPERATURE` entry, and either `thinking: disabled` on the router call or a text-block pick with a larger `max_tokens`. The thinking-off arm is the better of the two on every count here (473 vs 428, no empty replies, 96 vs 223 output tokens, 0.9 s vs 1.6 s).

**5. My read, yours to rule.** As a drop-in under the current catalog, 5.5 is a NO-GO by the bar you set: it moves ruled rows ×6 with nothing changed but the model, so it is not the "stable base" the #2195 retry needed; literal 32 stays. What it would take to use 5.5 is a re-baseline, not a screen: the floor rows, the calendar family and the attention/priority pair would each need rulings under 5.5's confidence band, and the consult floor would need re-reading against a model whose median is 0.85. That's a sprint, not a landing. The side branch `claude/lead-h55` holds the harness (`--model`, `--no-thinking`, the text-block pick) and the one set entry; it lands or not on your word, and nothing else from it touches main. The #2195 (a) example-only candidate and #2184 wording 3 stay parked behind this.

**Cost:** the batch results carry tokens per reply, not dollars; by the list rates the three arms cost about $1.65 (4.5 control $1.30). The Console line for 10-30 is the billed figure.

Files: `dev/2026/10/30/controls/h55-screen-*` (the three ×6 tables, three corpus reports, two diffs, the submit log); the renders and results in my scratchpad.

Verified how: `router_batch.py parse` per arm on the batch results (84 replies each); `inversion_phase1_shadow_score.py --provider anthropic --replay` per arm (616 replies each, 550 scored); `inversion_report_diff.py` control → each 5.5 arm; block shapes and confidences counted over all 2,100 replies by script. Layer: the router's own request and reply through the Batch API, the same prompt the served path sends, not a served turn. Denominator: 3 arms × (616 + 84).

-- Lead
