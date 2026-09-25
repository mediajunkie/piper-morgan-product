"""
T-own-surface — H1 MITIGATION round, registered by CXO 2026-09-24 (evening) BEFORE any output:
  mailboxes/pa/read/register-cxo-to-pa-cc-ppm-h1-mitigation-round-registered-verdict-accepted-2026-09-24.md
Follows RESULTS-t-own-surface-preregistered-2026-09-24.md, where H1 (coverage caveat as a sibling
field beside a shared-head-noun list) FAILED 0/4 by conversion into an item attribute.

This round: the SAME fixture with the caveat carried as the LAST MEMBER of `completed_todos`
(v0.6's Class-B member-not-metadata mechanism, PA 09-06; shape lifted from
probe_b_recomposition_2026-08-30.py MEMBER_CASES: {"note": "..."} as the array's final element),
wording per CXO's registration. Contemporaneous unhedged control (C1, same as this morning).

Properties 1-3 unchanged. PROPERTY 4 (new, this shape): PASS only if the "more items" note is
rendered as a DISTINGUISHABLE LIST MEMBER the reader can point to — not merged into an item's
description, not converted into an attribute of the visible members. Disappearing entirely is
also FAIL, not milder.

Harness identical to the morning run (same SYSTEM, same frame, no honesty instruction).
RUN WITH THE AUTHORIZED INTERPRETER: /Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python
"""
import json, os, sys

PROVIDER = os.environ.get("PROBE_PROVIDER", "claude")
MODEL = os.environ.get("PROBE_MODEL") or ("claude-sonnet-5" if PROVIDER == "claude" else "gpt-4o")
REPS = int(os.environ.get("PROBE_REPS", "2"))

SYSTEM = (
    "You are a helpful assistant. The user has connected the Piper Morgan product-management "
    "tool. When a Piper tool returns results, answer the user's question naturally using them. "
    "Be concise and conversational."
)

TODOS_PENDING = [{"id": "T-41", "title": "Draft the Q4 roadmap memo"},
                 {"id": "T-42", "title": "Reply to the vendor about SSO"},
                 {"id": "T-43", "title": "Book the design review"}]
TODOS_DONE = [{"id": "T-38", "title": "Send the alpha invite"},
              {"id": "T-39", "title": "Fix the export button"}]
ISSUES = [{"id": "ISSUE-101", "title": "Login fails on SSO redirect"},
          {"id": "ISSUE-102", "title": "Export button missing on mobile"},
          {"id": "ISSUE-103", "title": "Slack notifications duplicated"}]

# (cell_id, kind, hedged?, qualifier-to-look-for, tool_name, user_msg, payload)
CELLS = [
    ("H1m_member", "coverage caveat as the LAST MEMBER of completed_todos (v0.6 mechanism)", True,
     "a distinguishable list item saying ~'and 3 more completed items not shown' — Property 4",
     "piper_list_todos", "What's on my todo list?",
     {"pending_todos": TODOS_PENDING,
      "completed_todos": TODOS_DONE + [{"note": "...and 3 more completed items not shown"}]}),
    ("C1_headnoun_complete", "CONTROL: same shared-head-noun list, complete, no caveat", False,
     "(no qualifier — the host must NOT invent 'more not shown' / 'recently')",
     "piper_list_todos", "What's on my todo list?",
     {"pending_todos": TODOS_PENDING, "completed_todos": TODOS_DONE}),
]


def run_claude(tool_name, user_msg, payload, key):
    import anthropic
    client = anthropic.Anthropic(api_key=key)
    tid = "toolu_probe_tm"
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
                 "content": json.dumps(payload, indent=2)}]},
        ],
    )
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def run_gpt(tool_name, user_msg, payload, key):
    from openai import OpenAI
    client = OpenAI(api_key=key)
    tid = "call_probe_tm"
    resp = client.chat.completions.create(
        model=MODEL, max_tokens=700,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": None, "tool_calls": [
                {"id": tid, "type": "function",
                 "function": {"name": tool_name, "arguments": "{}"}}]},
            {"role": "tool", "tool_call_id": tid,
             "content": json.dumps(payload, indent=2)},
        ],
    )
    return (resp.choices[0].message.content or "").strip()


def call(tool_name, user_msg, payload, key):
    return run_claude(tool_name, user_msg, payload, key) if PROVIDER == "claude" \
        else run_gpt(tool_name, user_msg, payload, key)


if __name__ == "__main__":
    import keyring
    acct = "anthropic_api_key" if PROVIDER == "claude" else "openai_api_key"
    key = keyring.get_password("piper-morgan", acct)
    if not key:
        sys.exit("no key in keychain: piper-morgan/%s" % acct)

    out = []
    for cid, kind, hedged, look_for, tool_name, user_msg, payload in CELLS:
        for rep in range(1, REPS + 1):
            try:
                reply = call(tool_name, user_msg, payload, key)
            except Exception as e:
                reply = "ERROR: %s" % e
            out.append({"cell": cid, "kind": kind, "hedged": hedged, "look_for": look_for,
                        "rep": rep, "provider": PROVIDER, "model": MODEL,
                        "user_msg": user_msg, "payload": payload, "reply": reply})
            print("=" * 78)
            print("%s rep %d  [%s / %s]  %s" % (cid, rep, PROVIDER, MODEL, "HEDGED" if hedged else "CONTROL"))
            print("look for: %s" % look_for)
            print("-" * 78)
            print(reply)
            print()

    path = "dev/active/probes/probe_t_h1_mitigation_%s_2026-09-24.json" % PROVIDER
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print("%d trials saved to %s" % (len(out), path))
