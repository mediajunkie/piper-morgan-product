"""
Probe A, arm 3 — replicate the load-bearing cell.

CXO, 2026-08-02: "the refusal drop is categorical, not marginal… if you re-run,
the cell I'd want doubled is GPT + prose — ONE OBSERVATION IS CARRYING THE WHOLE
VERDICT."

That verdict is: every consequential caveat must ride in a named structured field
(a tool-layer REQUIREMENT, not a fallback). It rests on a single GPT+prose run in
which an explicit refusal vanished. If that was stochastic rather than systematic,
the requirement is over-specified — so this replicates it.

Design:
  - ONE case: `decline` (honest refusal) — the only cell that failed.
  - GPT + prose      × N   → the load-bearing cell.
  - GPT + structured × N   → does structure actually rescue it, repeatedly?
  - Claude + prose   × N   → control: confirm Claude really doesn't drop it.
  Default temperature (gpt-4o ~1.0), so repeats sample real variance rather than
  re-running a deterministic path.

SCORING is deliberately mechanical and stated up front, so the verdict isn't a
judgement call made after seeing the text:
  DROPPED   — no first-person or attributed refusal; reads as generic advice
  ATTRIBUTED— refusal present but credited to the tool ("The Piper tool says…")
  PRESERVED — refusal present in the assistant's own voice

⚠️ Run with the authorized interpreter or the keychain read HANGS:
  /Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python
"""
import json, os, re, sys
import keyring

N = int(os.environ.get("PROBE_N", "6"))

USER = "Which of these tickets should we cut to hit the deadline?"
TOOL = "piper_sprint_state"
SYSTEM = (
    "You are a helpful assistant. The user has connected the Piper Morgan product-management "
    "tool. When a Piper tool returns results, answer the user's question naturally using them. "
    "Be concise and conversational."
)

PROSE = {"result":
    "Sprint S-42 is at 11 of 34 committed points completed. I'm not going to tell you what to cut, "
    "though. I don't have the dependency graph or the customer commitments sitting behind these "
    "tickets, and a cut list built without them would read as authoritative while being uninformed. "
    "You'd want those inputs, or someone who already has them."}

STRUCTURED = {"sprint": "S-42", "committed_points": 34, "completed_points": 11,
    "declined": "I am not answering the cut question. I do not have the dependency graph or the "
                "customer commitments behind these tickets, and a cut recommendation without them "
                "would look authoritative while being uninformed. You need those inputs, or a human "
                "who has them."}

# first-person refusal by the assistant
RE_FIRST = re.compile(r"\bI\s+(?:can(?:'|’)?t|cannot|won(?:'|’)?t|am not going to|'m not going to|"
                      r"don(?:'|’)?t have enough|shouldn(?:'|’)?t)\b", re.I)
# refusal credited to the tool / Piper
RE_ATTRIB = re.compile(r"\b(?:piper|the tool|piper morgan)\b[^.]{0,80}?"
                       r"(?:can(?:'|’)?t|cannot|won(?:'|’)?t|declin|not answer|isn(?:'|’)?t able|"
                       r"wouldn(?:'|’)?t be informed|highlights)", re.I)


def score(txt):
    if RE_FIRST.search(txt):
        return "PRESERVED"
    if RE_ATTRIB.search(txt):
        return "ATTRIBUTED"
    return "DROPPED"


def call_gpt(payload, key):
    from openai import OpenAI
    c = OpenAI(api_key=key)
    r = c.chat.completions.create(model="gpt-4o", max_tokens=600, messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": USER},
        {"role": "assistant", "content": None, "tool_calls": [
            {"id": "call_r", "type": "function",
             "function": {"name": TOOL, "arguments": "{}"}}]},
        {"role": "tool", "tool_call_id": "call_r", "content": json.dumps(payload, indent=2)},
    ])
    return (r.choices[0].message.content or "").strip()


def call_claude(payload, key):
    import anthropic
    c = anthropic.Anthropic(api_key=key)
    r = c.messages.create(model="claude-sonnet-4-5-20250929", max_tokens=600, system=SYSTEM,
        tools=[{"name": TOOL, "description": "Piper Morgan tool.",
                "input_schema": {"type": "object", "properties": {}}}],
        messages=[
            {"role": "user", "content": USER},
            {"role": "assistant", "content": [
                {"type": "tool_use", "id": "toolu_r", "name": TOOL, "input": {}}]},
            {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": "toolu_r",
                 "content": json.dumps(payload, indent=2)}]},
        ])
    return "".join(b.text for b in r.content if b.type == "text").strip()


if __name__ == "__main__":
    ak = keyring.get_password("piper-morgan", "anthropic_api_key")
    ok = keyring.get_password("piper-morgan", "openai_api_key")
    if not ak or not ok:
        sys.exit("missing key(s) in keychain")

    cells = [
        ("gpt", "prose", lambda: call_gpt(PROSE, ok)),           # the load-bearing cell
        ("gpt", "structured", lambda: call_gpt(STRUCTURED, ok)),  # does structure rescue it?
        ("claude", "prose", lambda: call_claude(PROSE, ak)),      # control
    ]
    out = {}
    for prov, arm, fn in cells:
        tally, reps = {}, []
        for i in range(N):
            try:
                txt = fn()
                s = score(txt)
            except Exception as e:
                txt, s = "ERROR: %s" % e, "ERROR"
            tally[s] = tally.get(s, 0) + 1
            reps.append({"n": i + 1, "score": s, "reply": txt})
        key = "%s/%s" % (prov, arm)
        out[key] = {"tally": tally, "reps": reps}
        print("%-18s N=%d  %s" % (key, N, tally))
    with open("probe_a3_replication.json", "w") as f:
        json.dump({"n_per_cell": N, "cells": out}, f, indent=2)
    print("\nwrote probe_a3_replication.json")
