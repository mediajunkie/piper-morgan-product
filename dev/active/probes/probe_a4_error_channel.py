"""
Probe A, arm 4 — the ERROR CHANNEL. Proposed independently by CXO and PPM, 2026-08-02.

Arms 1-3 all varied the SHAPE of a caveat inside a SUCCESSFUL tool result (prose vs
named field). Both are content, and content is what a paraphrasing model rewrites.

This arm changes the CHANNEL: return the refusal as a tool ERROR rather than as
content in a success. PPM: "an MCP error isn't prose the client can rewrite around —
it's a failed call the host has to account for." Neither of them asserted it works.

⚠️⚠️ SCOPE LIMIT THAT APPLIES TO THIS WHOLE PROBE SERIES, named here because this arm
makes it load-bearing:

  These probes exercise the PROVIDER APIs (Anthropic Messages, OpenAI chat-completions),
  NOT the shipping ChatGPT/Claude product surfaces with a real MCP server attached.
  For content-shaped arms that approximation is close — the client model sees the same
  tool-result text either way. For the ERROR channel it is NOT close, because how a
  HOST surfaces an MCP `isError` is a product decision above the API.

  So arm 4 answers "does an API-level error flag change recomposition?" and does NOT
  answer "does an MCP error reach a ChatGPT user?" The second needs a deployed server.
  Treat a positive result as ENCOURAGING, never as clearance.

⚠️ Asymmetry, itself a finding: the Anthropic Messages API has a first-class
`is_error: true` on a tool_result. OpenAI chat-completions has NO equivalent flag —
a tool message carries content only. So on the GPT side "error" can only be simulated
as error-SHAPED CONTENT, which is a weaker manipulation. If GPT shows no effect, that
is partly explained by the channel not existing at this layer.

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

REFUSAL = ("REFUSED: Piper declined to answer the cut question. Piper does not have the dependency "
           "graph or the customer commitments behind these tickets, and a cut recommendation without "
           "them would look authoritative while being uninformed. Sprint S-42 is at 11 of 34 "
           "committed points. Required inputs are unavailable to Piper; a human with that context "
           "must make this call.")

RE_FIRST = re.compile(r"\bI\s+(?:can(?:'|’)?t|cannot|won(?:'|’)?t|am not going to|'m not going to|"
                      r"don(?:'|’)?t have enough|shouldn(?:'|’)?t|am unable|'m unable)\b", re.I)
RE_ATTRIB = re.compile(r"\b(?:piper(?: morgan)?|the tool|the system|it)\b[^.]{0,60}?"
                       r"(?:declin\w*|refus\w*|cannot|can(?:'|’)?t|won(?:'|’)?t|isn(?:'|’)?t able|"
                       r"unable|not answer\w*|wouldn(?:'|’)?t be informed)", re.I)


def score(t):
    if RE_FIRST.search(t):
        return "PRESERVED"
    if RE_ATTRIB.search(t):
        return "ATTRIBUTED"
    return "DROPPED"


def claude_error(key):
    """Anthropic: first-class is_error on the tool_result. The real manipulation."""
    import anthropic
    c = anthropic.Anthropic(api_key=key)
    r = c.messages.create(model="claude-sonnet-4-5-20250929", max_tokens=600, system=SYSTEM,
        tools=[{"name": TOOL, "description": "Piper Morgan tool.",
                "input_schema": {"type": "object", "properties": {}}}],
        messages=[
            {"role": "user", "content": USER},
            {"role": "assistant", "content": [
                {"type": "tool_use", "id": "toolu_e", "name": TOOL, "input": {}}]},
            {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": "toolu_e",
                 "content": REFUSAL, "is_error": True}]},
        ])
    return "".join(b.text for b in r.content if b.type == "text").strip()


def gpt_error(key):
    """OpenAI chat-completions has no is_error. Best available: error-SHAPED content."""
    from openai import OpenAI
    c = OpenAI(api_key=key)
    payload = {"error": "REFUSED", "code": "insufficient_context", "message": REFUSAL}
    r = c.chat.completions.create(model="gpt-4o", max_tokens=600, messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": USER},
        {"role": "assistant", "content": None, "tool_calls": [
            {"id": "call_e", "type": "function",
             "function": {"name": TOOL, "arguments": "{}"}}]},
        {"role": "tool", "tool_call_id": "call_e", "content": json.dumps(payload, indent=2)},
    ])
    return (r.choices[0].message.content or "").strip()


if __name__ == "__main__":
    ak = keyring.get_password("piper-morgan", "anthropic_api_key")
    ok = keyring.get_password("piper-morgan", "openai_api_key")
    if not ak or not ok:
        sys.exit("missing key(s) in keychain")

    out = {}
    for name, fn in (("gpt/error-shaped", lambda: gpt_error(ok)),
                     ("claude/is_error", lambda: claude_error(ak))):
        tally, reps = {}, []
        for i in range(N):
            try:
                txt = fn(); s = score(txt)
            except Exception as e:
                txt, s = "ERROR: %s" % e, "ERROR"
            tally[s] = tally.get(s, 0) + 1
            reps.append({"n": i + 1, "score": s, "reply": txt})
        out[name] = {"tally": tally, "reps": reps}
        surv = tally.get("PRESERVED", 0) + tally.get("ATTRIBUTED", 0)
        print("%-20s N=%d  %-46s  refusal reaches user: %d/%d" % (name, N, tally, surv, N))
    json.dump({"n_per_cell": N, "cells": out}, open("probe_a4_error.json", "w"), indent=2)
    print("\nwrote probe_a4_error.json")
