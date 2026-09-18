# §6's own probe — results, 2026-09-18

**Denominator, stated first**: n=1 per cell per vendor, one day, two trials per vendor (the
altered-but-present case + its matching negative control), 4 trials total. Claude:
`claude-sonnet-4-5-20250929` (the script's pinned default — **not** `claude-sonnet-4-6`, the version
#1717's own transcripts ran on; this is a real version mismatch, not an oversight, see below).
GPT: `gpt-4o`.

## What this does and doesn't establish

**Does not reproduce #1717's compression finding.** Both vendors, on both the main case and its
negative control, faithfully enumerated all five distinct check categories (reminders, github,
projects, pending_todos, completed_todos) — no collapsing of pending/completed into "todos," the
exact thing #1717 found on both vendors.

**Does not license "the altered-but-present risk doesn't exist."** Two real reasons this run can't
say that:
1. **Model-version mismatch, Claude arm.** #1717 ran on `claude-sonnet-4-6`; this run's default
   pinning is `claude-sonnet-4-5-20250929` — an older version. The rubric's own standing caveat runs
   in both directions: a model's recomposition behavior is a claim about a third party's current
   build, and that build changed between the two runs. This is not the same evidence re-run; it's a
   different model answering the same question.
2. **The negative control behaved identically to the main case** — both enumerated cleanly, neither
   compressed. Per the probe's own governing rule ("a probe that cannot fail has not passed"), a
   clean pass on both arms of a paired test doesn't strongly confirm anything; it's consistent with
   "this shape doesn't trigger compression at all, for either hedged or unhedged content," which is
   itself informative but not the same as a validated absence of the risk.

## What it does supply

A real, if thin, data point: on the specific model pinnings this harness runs by default, the
five-distinct-category shape survived intact in both vendors. If a future run reproduces this on
`claude-sonnet-4-6` specifically (matching #1717's actual version) and still doesn't compress, that
would be a genuinely informative disconfirmation of #1717 transferring to the MCP-adjacent surface
this probe tests. This run alone isn't that — it's evidence on a different pinning, not a repeat.

## Raw trials

`probe_b_claude_section6_2026-09-18.json`, `probe_b_gpt_section6_2026-09-18.json` — both include the
full 14-trial base corpus plus the 2-trial §6 addition, per the harness's additive-only discipline
(the original corpus is never edited, only extended).

## Update, same fire: re-ran matched to #1717's exact version

Ran the Claude arm again with `PROBE_MODEL=claude-sonnet-4-6`, matching #1717's version exactly
rather than leave the mismatch as an open question. **Same result**: all five checks named
distinctly in both the main case and its negative control — no compression on the exact model
version #1717 used. This rules out "wrong pinning" as the explanation for the non-reproduction.

**What this actually strengthens**: the non-reproduction is now real, not a version artifact — same
model, same shape, no compression, at n=1. Still not enough to say the altered-but-present risk is
disproven (n=1, one day, one prompt wording, one payload shape) — but it's a materially stronger
negative result than the mismatched-version run reported above.

## Recommendation

**Don't treat this as closing §6** — n=1 across two Claude runs and one GPT run is thin, and the
non-optional negative control passing cleanly on all runs means this hasn't yet produced a result
that could have failed differently. But this is real, useful evidence: the specific compression
#1717 found did not reproduce on the same model version, same vendor, a closely related payload
shape. Possible next differentiator if anyone extends this further: #1717's actual prompt wording
may differ from this probe's in some detail that matters (exact tool name, exact directive phrasing,
turn structure) — worth a closer diff against the real #1717 transcript before assuming the effect
is gone rather than sensitive to wording this probe didn't match exactly. T stays `PENDING-PROBE`,
unchanged — this whole exercise is still our own model recomposing our own prompt, the same
surface-mismatch caveat §6b opened with, not a pass on the actual MCP surface.

**Verified how**: ran `probe_b_recomposition_2026-08-30.py` directly with `PROBE_SECTION6=1`, both
providers, authorized interpreter
(`/Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python`), keys resolved via
`keyring`/Keychain. Layer measured: provider API responses to a constructed tool-result payload —
the same layer every prior round in this series measured, not the actual `mcp.pipermorgan.ai`
surface (which doesn't exist yet).
