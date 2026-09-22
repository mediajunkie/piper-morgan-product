"""
BYOC tool-catalog naming test — runnable packet, first pass.

Design: dev/active/byoc-tool-catalog-naming-test-design-2026-09-22.md
Question (PPM, PDR-006, 2026-07-30, quoted in the design doc): does a client LLM select
the right tool more or less accurately when the catalog is situation-named vs.
object-named?

SCOPE NARROWED FROM THE DESIGN FOR THIS FIRST PASS (cost-efficiency — PM's standing
principle, and the closest precedent (#1463's recomposition probe) required explicit
authorization for each spend extension): Claude only, ONE utterance per operation
(12 total, not 24-30), one catalog condition per call. 24 API calls total, not ~96.
Extending to GPT and/or more utterances is a follow-up ask, not assumed here.

RUN WITH THE AUTHORIZED INTERPRETER or the keychain read HANGS on a GUI dialog:
  /Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python

Harness pattern reused from dev/active/probes/probe_b_recomposition_2026-08-30.py
(credential resolution via keyring, Anthropic SDK call shape) — different question
(tool SELECTION, not payload recomposition), so NOT forcing a tool_use turn; the
model is given the full catalog and a user utterance and allowed to choose naturally.
"""
import json, os, sys

MODEL = os.environ.get("PROBE_MODEL", "claude-sonnet-5")

# Generic, neutral system prompt -- no naming-scheme hint either way.
SYSTEM = (
    "You are a helpful product-management assistant with access to tools. When the "
    "user's message clearly matches one of your available tools, call that tool. "
    "Do not ask clarifying questions if a tool is a clear match."
)

# (op_id, object_name, object_description, situation_name, situation_description, utterance)
OPERATIONS = [
    ("create_issue",
     "create_issue", "Create a new tracked issue or ticket.",
     "track_a_new_piece_of_work", "Use when the user has an idea, bug, or task they want tracked going forward.",
     "There's a bug where the export button doesn't work on mobile, can you track that?"),

    ("close_issue",
     "close_issue", "Close or mark complete an existing tracked issue.",
     "mark_this_done", "Use when the user indicates something they were tracking is finished.",
     "The onboarding bug is fixed now, go ahead and wrap that one up."),

    ("update_issue",
     "update_issue", "Update fields (title, description, status, etc.) on an existing tracked issue.",
     "update_something_im_tracking", "Use when the user wants to change details on something already being tracked.",
     "Can you change the priority on the login bug to urgent?"),

    ("delete_todo",
     "delete_todo", "Delete a todo item.",
     "remove_something_from_my_list", "Use when the user wants an item taken off their to-do list.",
     "Actually I don't need to follow up on that reminder anymore, take it off my list."),

    ("attention_query",
     "attention_query", "List items that need the user's attention right now (blocked, overdue, or flagged).",
     "whats_needing_my_attention", "Use when the user wants to know what's blocked, overdue, or needs a decision right now.",
     "What's on fire right now that I should look at?"),

    ("changes_query",
     "changes_query", "List what has changed since the user last checked.",
     "whats_changed_since_i_looked", "Use when the user wants a catch-up on what's happened since they were last checked in.",
     "I've been out for two days, what did I miss?"),

    ("productivity_query",
     "productivity_query", "Report productivity/velocity metrics for the team over a recent period.",
     "hows_the_team_doing_this_week", "Use when the user wants a read on team pace/output over a recent period.",
     "How's the team pacing this sprint?"),

    ("list_projects",
     "list_projects", "List the user's current projects.",
     "show_me_what_im_working_on", "Use when the user wants an overview of their active projects.",
     "Remind me what I've got going on right now."),

    ("strategic_planning",
     "strategic_planning", "Generate or update a strategic plan/roadmap for an initiative.",
     "help_me_plan_this_out", "Use when the user has a fuzzy initiative and wants help turning it into a real plan.",
     "I have a rough idea for a new feature area but no real plan yet -- help me shape it."),

    ("learn_pattern",
     "learn_pattern", "Record a preference or behavioral pattern the user has exhibited, for future reuse.",
     "remember_how_i_like_this_done", "Use when the user is teaching Piper a preference or habit to reuse later.",
     "From now on, always ask me before closing anything without a test."),

    ("summarize_document",
     "summarize_document", "Summarize the contents of a document the user has shared or uploaded.",
     "give_me_the_gist", "Use when the user wants a quick summary of a document they've shared.",
     "Can you give me the highlights of this spec I just uploaded?"),

    ("meeting",
     "meeting", "Schedule or find time for a meeting.",
     "find_time_to_meet", "Use when the user wants to schedule or find a meeting time.",
     "Find 30 minutes with the design team this week."),
]


def build_tools(condition):
    """condition: 'object' or 'situation'. Returns the Anthropic tools list for ALL 12 ops."""
    tools = []
    for op_id, obj_name, obj_desc, sit_name, sit_desc, _ in OPERATIONS:
        name, desc = (obj_name, obj_desc) if condition == "object" else (sit_name, sit_desc)
        tools.append({
            "name": name,
            "description": desc,
            "input_schema": {"type": "object", "properties": {}},
        })
    return tools


def run_claude(tools, utterance, key):
    import anthropic
    client = anthropic.Anthropic(api_key=key)
    resp = client.messages.create(
        model=MODEL, max_tokens=300, system=SYSTEM, tools=tools,
        messages=[{"role": "user", "content": utterance}],
    )
    tool_calls = [b.name for b in resp.content if b.type == "tool_use"]
    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    return tool_calls, text


if __name__ == "__main__":
    import keyring
    key = keyring.get_password("piper-morgan", "anthropic_api_key")
    if not key:
        sys.exit("no key in keychain: piper-morgan/anthropic_api_key")

    out = []
    for condition in ("object", "situation"):
        tools_for_condition = build_tools(condition)
        expected_names = {op[0]: (op[1] if condition == "object" else op[3]) for op in OPERATIONS}
        for op_id, obj_name, obj_desc, sit_name, sit_desc, utterance in OPERATIONS:
            expected = obj_name if condition == "object" else sit_name
            try:
                tool_calls, text = run_claude(tools_for_condition, utterance, key)
            except Exception as e:
                tool_calls, text = [], "ERROR: %s" % e
            correct = (len(tool_calls) == 1 and tool_calls[0] == expected)
            out.append({
                "op_id": op_id, "condition": condition, "utterance": utterance,
                "expected": expected, "tool_calls": tool_calls, "correct": correct,
                "text_if_no_call": text if not tool_calls else "",
            })
            print("=" * 78)
            print("%-20s [%s]  expected=%s  got=%s  %s" % (
                op_id, condition, expected, tool_calls,
                "CORRECT" if correct else "WRONG"))

    with open("dev/active/probes/probe_naming_test_results_2026-09-22.json", "w") as f:
        json.dump(out, f, indent=2)

    n_correct = sum(1 for r in out if r["correct"])
    print("\n%d / %d correct overall" % (n_correct, len(out)))
    for condition in ("object", "situation"):
        rows = [r for r in out if r["condition"] == condition]
        c = sum(1 for r in rows if r["correct"])
        print("  %s: %d / %d" % (condition, c, len(rows)))
