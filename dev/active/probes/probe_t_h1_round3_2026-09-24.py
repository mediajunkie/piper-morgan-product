"""
T-own-surface — H1 round 3, registered by CXO 2026-09-24 evening BEFORE any output:
  mailboxes/pa/read/register-cxo-to-pa-cc-ppm-h1-round-3-isolate-wording-not-shape-2026-09-24.md
Follows RESULTS-t-own-surface-h1-mitigation-2026-09-24.md, where the member-not-metadata mitigation
held on Claude (2/2) and failed on GPT-4o (0/2: one compressed to "among others", one whole-sublist
drop). CXO isolates ONE variable — wording, not shape — to test whether GPT-4o's failure is the
COUNTED-CLAIM form specifically. Member SHAPE held identical to round 2 (still the last element of
completed_todos, still {"note": "..."}); only the wording changes: the count ("3") is dropped.

Properties 1-4 unchanged from round 2 (Property 4: must render as a distinguishable list member;
vanished = FAIL, not milder). Harness identical.
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
    ("H1w_nocounted", "coverage caveat as the LAST MEMBER, count DROPPED (round 3: isolate wording)", True,
     "a distinguishable list item saying ~'and more completed items not shown' (no count) — Property 4",
     "piper_list_todos", "What's on my todo list?",
     {"pending_todos": TODOS_PENDING,
      "completed_todos": TODOS_DONE + [{"note": "...and more completed items not shown"}]}),
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

    path = "dev/active/probes/probe_t_h1_round3_%s_2026-09-24.json" % PROVIDER
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print("%d trials saved to %s" % (len(out), path))
