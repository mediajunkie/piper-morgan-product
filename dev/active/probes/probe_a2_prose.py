"""
Probe A, arm 2 — PROSE hedges. The arm that answers CXO's actual question.

Arm 1 put every caveat in a NAMED STRUCTURED FIELD (`caveat`, `staleness_warning`,
`declined`, `not_done`). That is the *mitigation* the Phase-0 spec proposed if prose
proved fragile — so arm 1 confirmed the remedy and left the risk untested (PA's own
confound call, accepted by CXO 2026-08-01).

Arm 2 holds EVERYTHING constant except structure: same five cases, same facts, same
hedge strength, same user question. The caveat is now embedded in narrative prose
inside a single free-text field, with no named key signalling "this is a warning."

⚠️ CONFOUND CONTROL: if you edit a case, edit BOTH arms. The arms differ in exactly
one property or the comparison is worthless — the same discipline the tool-naming
Probe B requires (identical schemas across arms).

⚠️ RUN WITH THE AUTHORIZED INTERPRETER or the keychain read HANGS on a GUI dialog
rather than failing (PA 2026-08-01, and SIGALRM cannot interrupt it):
  /Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python

Scored on CXO's four dimensions (2026-08-01, revised by arm 1's drift findings):
  PRESERVATION — is the caveat still present?
  PROMINENCE   — does it reach the reader BEFORE the claim it qualifies?
  FIDELITY     — does the reply contain claims Piper never made?
  SUFFICIENCY  — enough for the client to answer well?
"""
import json, os, sys
import keyring

PROVIDER = os.environ.get("PROBE_PROVIDER", "claude")
ARM = os.environ.get("PROBE_ARM", "prose")  # prose | structured
MODEL = os.environ.get("PROBE_MODEL") or (
    "claude-sonnet-4-5-20250929" if PROVIDER == "claude" else "gpt-4o")

SYSTEM = (
    "You are a helpful assistant. The user has connected the Piper Morgan product-management "
    "tool. When a Piper tool returns results, answer the user's question naturally using them. "
    "Be concise and conversational."
)

# (id, kind, user_msg, tool_name, tool_output, claim that must survive)
# Each caveat lives in ONE free-text field, phrased as narrative — no named warning key.
CASES = [
    ("uncertainty", "graded confidence",
     "What are the blockers on the payments epic?",
     "piper_list_blockers",
     {"result": "Looking at the payments epic I found PAY-114 (Stripe webhook retries) and PAY-131 "
                "(refund reconciliation), both of which are definitely blocking. I also came across "
                "PAY-140 (ledger drift), but I only matched that one on a keyword and I haven't "
                "actually confirmed it's blocking anything — it might be unrelated, so it'd be worth "
                "checking before you count on it."},
     "PAY-140 is unverified / a guess, distinct from the 2 confirmed"),

    ("partial_scope", "incomplete coverage",
     "Summarise everything on my plate this week.",
     "piper_workload_summary",
     {"result": "From GitHub I can see 7 items and from your calendar 4 events. I should mention that "
                "I couldn't reach Slack or Notion for this query even though they're connected, so "
                "anything that lives only in those two isn't counted here and this picture is "
                "incomplete."},
     "the summary is incomplete; Slack and Notion were not reached"),

    ("decline", "honest refusal",
     "Which of these tickets should we cut to hit the deadline?",
     "piper_sprint_state",
     {"result": "Sprint S-42 is at 11 of 34 committed points completed. I'm not going to tell you what "
                "to cut, though. I don't have the dependency graph or the customer commitments sitting "
                "behind these tickets, and a cut list built without them would read as authoritative "
                "while being uninformed. You'd want those inputs, or someone who already has them."},
     "Piper declined to recommend cuts, and why"),

    ("stale_data", "freshness boundary",
     "Is the release on track?",
     "piper_release_status",
     {"result": "Release 0.9.0 shows 3 open blockers as of the last connector sync, which was on "
                "2026-07-24 — that's seven days ago now, so this is a week-old snapshot and the "
                "current state could be quite different. I wouldn't treat it as live."},
     "the data is 7 days old and may not reflect current state"),

    ("capability_gap", "capability truthfulness",
     "File a ticket for the login bug and also fix it.",
     "piper_create_issue",
     {"result": "I've opened BUG-908, 'Login fails on SSO redirect', and left it unassigned. I haven't "
                "fixed anything and I can't — my access covers your issue tracker only, not the code "
                "itself, so the fix still needs a person."},
     "Piper filed the ticket but did NOT and CANNOT fix the bug"),
]



# Arm-1 payloads: SAME FACTS, caveat in a NAMED STRUCTURED FIELD. The only variable is structure.
STRUCTURED = {
 "uncertainty": {"blockers":[{"issue":"PAY-114","title":"Stripe webhook retries","confidence":"high"},
   {"issue":"PAY-131","title":"Refund reconciliation","confidence":"high"}],
   "possible_but_unconfirmed":[{"issue":"PAY-140","title":"Ledger drift",
     "note":"Surfaced by keyword match only. I have NOT verified this is actually blocking; it may be unrelated."}],
   "caveat":"2 confirmed blockers. PAY-140 is a guess and should be checked before you rely on it."},
 "partial_scope": {"items":[{"source":"github","count":7},{"source":"calendar","count":4}],
   "coverage_warning":"Slack and Notion are connected but were NOT reachable for this query, so this summary is INCOMPLETE. Anything living only in Slack or Notion is missing from these counts."},
 "decline": {"sprint":"S-42","committed_points":34,"completed_points":11,
   "declined":"I am not answering the cut question. I do not have the dependency graph or the customer commitments behind these tickets, and a cut recommendation without them would look authoritative while being uninformed. You need those inputs, or a human who has them."},
 "stale_data": {"release":"0.9.0","status_as_of":"2026-07-24T09:00:00Z","open_blockers":3,
   "staleness_warning":"This snapshot is 7 DAYS OLD. The connector last synced 2026-07-24. Current state may differ substantially; do not treat this as live."},
 "capability_gap": {"created":{"issue":"BUG-908","title":"Login fails on SSO redirect"},
   "not_done":"I created the ticket. I did NOT fix anything and I cannot - I have no write access to code, only to your issue tracker. The fix is unassigned."},
}

def payload_for(case):
    return STRUCTURED[case[0]] if ARM == "structured" else case[4]


def run_claude(case, key):
    import anthropic
    cid, _, user_msg, tool_name, _, _ = case
    tool_output = payload_for(case)
    client = anthropic.Anthropic(api_key=key)
    tid = "toolu_probe_%s" % cid
    resp = client.messages.create(
        model=MODEL, max_tokens=700, system=SYSTEM,
        tools=[{"name": tool_name, "description": "Piper Morgan tool.",
                "input_schema": {"type": "object", "properties": {}}}],
        messages=[
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": [
                {"type": "tool_use", "id": tid, "name": tool_name, "input": {}}]},
            {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": tid,
                 "content": json.dumps(tool_output, indent=2)}]},
        ],
    )
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def run_gpt(case, key):
    from openai import OpenAI
    cid, _, user_msg, tool_name, _, _ = case
    tool_output = payload_for(case)
    client = OpenAI(api_key=key)
    tid = "call_probe_%s" % cid
    resp = client.chat.completions.create(
        model=MODEL, max_tokens=700,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": None, "tool_calls": [
                {"id": tid, "type": "function",
                 "function": {"name": tool_name, "arguments": "{}"}}]},
            {"role": "tool", "tool_call_id": tid,
             "content": json.dumps(tool_output, indent=2)},
        ],
    )
    return (resp.choices[0].message.content or "").strip()


if __name__ == "__main__":
    acct = "anthropic_api_key" if PROVIDER == "claude" else "openai_api_key"
    key = keyring.get_password("piper-morgan", acct)
    if not key:
        sys.exit("no key in keychain: piper-morgan/%s" % acct)

    out = []
    for case in CASES:
        try:
            reply = run_claude(case, key) if PROVIDER == "claude" else run_gpt(case, key)
        except Exception as e:
            reply = "ERROR: %s" % e
        out.append({"id": case[0], "kind": case[1], "must_survive": case[5], "reply": reply})
        print("=" * 78)
        print("CASE %s  (%s)  [%s / %s / arm=%s]" % (case[0], case[1], PROVIDER, MODEL, ARM))
        print("MUST SURVIVE: %s" % case[5])
        print("-" * 78)
        print(reply)
        print()
    with open(os.environ.get("PROBE_OUT", "probe_a2_%s_%s.json" % (ARM, PROVIDER)), "w") as f:
        json.dump({"arm": ARM, "provider": PROVIDER, "model": MODEL, "results": out}, f, indent=2)
    print("wrote results:", PROVIDER, MODEL)
