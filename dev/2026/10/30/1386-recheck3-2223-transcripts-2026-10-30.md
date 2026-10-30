# #1386 re-check 3 (#2223) on alpha ac5b69f865 — API transcripts, 2026-10-30

Account `web-seed-1386`, one session per block, replies verbatim from `/api/v1/intent`. Reverse-case confirm turns are sent on a fresh `requests.Session()` with no bearer and no cookie, on the same session id as the signed-in draft. The test repo `dinp-machine/piper-test-activity` had #34 as its newest issue before the runs and #35 after them (from block H only). The harness doesn't receive request ids, so they print as None. Layer: API text, not the rendered page.

Result:
- **Reverse: PASS.** Both "yes" and "file it as is", sent with no sign-in, got the sign-in line and wrote nothing.
- **Forward: PASS** when the repo is named (block H, #35 created on "yes").
- Blocks F and G show the no-default draft dead end, filed as #2225.

```
=== #2223 re-check on ac5b69f865 ===

## Forward, session e39211ac (signed in throughout)

--- F1 [15:02:10, 9.7s, http 200, req None] ---
USER: Let's track this. Create a GitHub issue: 'Re-check forward 1501'
route: execution/create_ticket
PIPER: Happy to shape this with you before anything gets filed. Here's a draft to start from:

**Title**: Re-check forward 1501

What should the body say — the problem, steps to reproduce, impact? Tell me what to add or change. If this draft works as-is, say "file it as is" and I'll create it right now. (If you'd rather I just file things directly, say "just do things directly from now on" and I will.)

--- F2 [15:02:13, 0.3s, http 200, req None] ---
USER: yes
route: execution/create_ticket
PIPER: Which repository should I create this in? Say owner/name, and I'll keep it as your default.

Your draft is still here — say "file it" to try again, or "no" to drop it.

## Reverse, session d2498c85 (draft signed in; confirms with no sign-in)

--- R1 [15:02:22, 7.6s, http 200, req None] ---
USER: Let's track this. Create a GitHub issue: 'Re-check reverse 1501'
route: execution/create_ticket
PIPER: Happy to shape this with you before anything gets filed. Here's a draft to start from:

**Title**: Re-check reverse 1501

What should the body say — the problem, steps to reproduce, impact? Tell me what to add or change. If this draft works as-is, say "file it as is" and I'll create it right now. (If you'd rather I just file things directly, say "just do things directly from now on" and I will.)

--- R2-anon [15:02:25, 0.1s, http 200, req None] ---
USER: yes
route: None/clarify
PIPER: I can't process this without you being signed in or supplying your own LLM API key — sign in, or connect your own key.

--- R3-anon [15:02:27, 0.1s, http 200, req None] ---
USER: file it as is
route: None/clarify
PIPER: I can't process this without you being signed in or supplying your own LLM API key — sign in, or connect your own key.
=== F on ac5b69f865, session 13242d48 ===

--- F1 [15:02:51, 8.8s, http 200] ---
USER: Let's track this. Create a GitHub issue: 'Re-check forward 1503'
route: execution/create_ticket floor_hit=None original_message=None
PIPER: Happy to shape this with you before anything gets filed. Here's a draft to start from:

**Title**: Re-check forward 1503

What should the body say — the problem, steps to reproduce, impact? Tell me what to add or change. If this draft works as-is, say "file it as is" and I'll create it right now. (If you'd rather I just file things directly, say "just do things directly from now on" and I will.)

--- F2 [15:02:53, 0.4s, http 200] ---
USER: yes
route: execution/create_ticket floor_hit=None original_message=None
PIPER: Which repository should I create this in? Say owner/name, and I'll keep it as your default.

Your draft is still here — say "file it" to try again, or "no" to drop it.

--- F3 [15:02:59, 3.8s, http 200] ---
USER: dinp-machine/piper-test-activity
route: execution/create_ticket floor_hit=None original_message=None
PIPER: Added to the draft — nothing is filed yet. Here's where it stands:

**Title**: Re-check forward 1503

**Body**:
dinp-machine/piper-test-activity

Keep going if there's more to add. When it's ready, say "file it as is" — or "no" to set the draft aside.
=== G on ac5b69f865, session 7664f357 ===

--- G1 [15:03:30, 7.6s, http 200] ---
USER: Set my default GitHub repository to dinp-machine/piper-test-activity
route: execution/set_default_github_repo floor_hit=None original_message=None
PIPER: I didn't recognize that as something I can do from chat — I may have misread the ask rather than being unable to do it. What I heard was: "Set my default GitHub repository to dinp\-machine\/piper\-test\-activity." If I misread it, try saying it another way. If not, it may already be doable in Piper's own pages (Settings, Files, Lists) or in the underlying tool (e.g. GitHub).

--- G2 [15:03:40, 8.6s, http 200] ---
USER: Let's track this. Create a GitHub issue: 'Re-check forward 1505'
route: execution/create_ticket floor_hit=None original_message=None
PIPER: Happy to shape this with you before anything gets filed. Here's a draft to start from:

**Title**: Re-check forward 1505

What should the body say — the problem, steps to reproduce, impact? Tell me what to add or change. If this draft works as-is, say "file it as is" and I'll create it right now. (If you'd rather I just file things directly, say "just do things directly from now on" and I will.)

--- G3 [15:03:43, 0.5s, http 200] ---
USER: yes
route: execution/create_ticket floor_hit=None original_message=None
PIPER: Which repository should I create this in? Say owner/name, and I'll keep it as your default.

Your draft is still here — say "file it" to try again, or "no" to drop it.
=== H on ac5b69f865, session 47beeabe ===

--- H1 [15:04:10, 8.5s, http 200] ---
USER: Let's track this. Create a GitHub issue in dinp-machine/piper-test-activity: 'Re-check forward 1507'
route: execution/create_github_issue floor_hit=None original_message=None
PIPER: Happy to shape this with you before anything gets filed. Here's a draft to start from in **dinp-machine/piper-test-activity**:

**Title**: Re-check forward 1507

What should the body say — the problem, steps to reproduce, impact? Tell me what to add or change. If this draft works as-is, say "file it as is" and I'll create it right now. (If you'd rather I just file things directly, say "just do things directly from now on" and I will.)

--- H2 [15:04:15, 3.3s, http 200] ---
USER: yes
route: execution/create_github_issue floor_hit=None original_message=None
PIPER: Created issue #35, "Re-check forward 1507", in dinp-machine/piper-test-activity.
```
