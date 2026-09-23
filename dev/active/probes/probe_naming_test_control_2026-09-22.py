"""
BYOC tool-catalog naming test — INDEPENDENT-AUTHOR CONTROL, second pass.

Design: dev/active/byoc-tool-catalog-naming-test-design-2026-09-22.md
First pass: dev/active/probes/RESULTS-naming-test-first-pass-2026-09-22.md found situation-shaped
12/12 vs object-shaped 10/12, but flagged a real confound: PA wrote both catalogs in one sitting,
and the situation-shaped descriptions naturally came out more disambiguating.

THIS RUN controls for that: the object-shaped DESCRIPTIONS below were written by a fresh,
isolated agent with NO knowledge of this test, the situation-shaped alternatives, or that the
descriptions would be compared to anything -- it was only told "write a good API-reference
description for each operation." Names are unchanged (still create_issue, close_issue, etc.).
Situation-shaped catalog and the 12 utterances are UNCHANGED from the first pass, for a clean
comparison.

Authorized to run without further spend approval per PM's 2026-09-22 directive ("do not
self-throttle or postpone work over usage right now... drain your queues normally") -- the first
pass's cost-narrowing was explicitly about that caution, now lifted for the current window.

RUN WITH THE AUTHORIZED INTERPRETER: /Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python
"""
import json, os, sys

MODEL = os.environ.get("PROBE_MODEL", "claude-sonnet-5")

SYSTEM = (
    "You are a helpful product-management assistant with access to tools. When the "
    "user's message clearly matches one of your available tools, call that tool. "
    "Do not ask clarifying questions if a tool is a clear match."
)

# (op_id, object_name, INDEPENDENTLY-AUTHORED object_description, situation_name, situation_description, utterance)
# Object descriptions from a fresh isolated agent call, 2026-09-22 -- see the design/results docs
# for the exact prompt used. Situation side + utterances unchanged from the first pass.
OPERATIONS = [
    ("create_issue",
     "create_issue", "Creates a new tracked issue or ticket in the system when a piece of work, "
     "bug, or request needs to be captured for the first time and does not yet exist as a tracked item.",
     "track_a_new_piece_of_work", "Use when the user has an idea, bug, or task they want tracked going forward.",
     "There's a bug where the export button doesn't work on mobile, can you track that?"),

    ("close_issue",
     "close_issue", "Marks an existing tracked issue as complete/resolved when its work is finished, "
     "without altering any of its other fields.",
     "mark_this_done", "Use when the user indicates something they were tracking is finished.",
     "The onboarding bug is fixed now, go ahead and wrap that one up."),

    ("update_issue",
     "update_issue", "Modifies one or more fields (title, description, status, assignee, etc.) on an "
     "existing tracked issue when the issue itself remains open and only its details or state need to "
     "change, as opposed to marking it fully complete.",
     "update_something_im_tracking", "Use when the user wants to change details on something already being tracked.",
     "Can you change the priority on the login bug to urgent?"),

    ("delete_todo",
     "delete_todo", "Permanently removes a todo item from the system, for use only when a todo was "
     "created in error or is no longer wanted at all, rather than being completed or converted into "
     "a tracked issue.",
     "remove_something_from_my_list", "Use when the user wants an item taken off their to-do list.",
     "Actually I don't need to follow up on that reminder anymore, take it off my list."),

    ("attention_query",
     "attention_query", "Retrieves the set of items currently requiring the user's action, such as "
     "those that are blocked, overdue, or explicitly flagged, for a real-time \"what needs me right "
     "now\" view rather than a historical or metrics view.",
     "whats_needing_my_attention", "Use when the user wants to know what's blocked, overdue, or needs a decision right now.",
     "What's on fire right now that I should look at?"),

    ("changes_query",
     "changes_query", "Retrieves what has changed across the user's items since their last check, "
     "for catching up on activity and updates rather than surfacing items that need action.",
     "whats_changed_since_i_looked", "Use when the user wants a catch-up on what's happened since they were last checked in.",
     "I've been out for two days, what did I miss?"),

    ("productivity_query",
     "productivity_query", "Retrieves aggregate productivity or velocity metrics for the team over a "
     "specified recent period, for reporting on team-level throughput trends rather than individual "
     "item status.",
     "hows_the_team_doing_this_week", "Use when the user wants a read on team pace/output over a recent period.",
     "How's the team pacing this sprint?"),

    ("list_projects",
     "list_projects", "Retrieves the list of projects the user currently has, for orientation or "
     "navigation when the user needs to see what projects exist rather than details of any single "
     "item within one.",
     "show_me_what_im_working_on", "Use when the user wants an overview of their active projects.",
     "Remind me what I've got going on right now."),

    ("strategic_planning",
     "strategic_planning", "Generates or updates a strategic plan or roadmap for a given initiative, "
     "for higher-level, multi-step planning work rather than for creating or editing a single issue "
     "or todo.",
     "help_me_plan_this_out", "Use when the user has a fuzzy initiative and wants help turning it into a real plan.",
     "I have a rough idea for a new feature area but no real plan yet -- help me shape it."),

    ("learn_pattern",
     "learn_pattern", "Records a preference or behavioral pattern the user has demonstrated so it can "
     "be applied automatically in future interactions, for capturing durable user-specific conventions "
     "rather than performing a one-off action.",
     "remember_how_i_like_this_done", "Use when the user is teaching Piper a preference or habit to reuse later.",
     "From now on, always ask me before closing anything without a test."),

    ("summarize_document",
     "summarize_document", "Produces a summary of the contents of a document the user has shared or "
     "uploaded, for condensing existing document content rather than generating new planning or "
     "tracking artifacts.",
     "give_me_the_gist", "Use when the user wants a quick summary of a document they've shared.",
     "Can you give me the highlights of this spec I just uploaded?"),

    ("meeting",
     "meeting", "Schedules a new meeting or finds available time for one among relevant participants, "
     "for calendar/scheduling requests rather than any issue-, todo-, or document-related operation.",
     "find_time_to_meet", "Use when the user wants to schedule or find a meeting time.",
     "Find 30 minutes with the design team this week."),
]


def build_tools(condition):
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

    with open("dev/active/probes/probe_naming_test_control_results_2026-09-22.json", "w") as f:
        json.dump(out, f, indent=2)

    n_correct = sum(1 for r in out if r["correct"])
    print("\n%d / %d correct overall" % (n_correct, len(out)))
    for condition in ("object", "situation"):
        rows = [r for r in out if r["condition"] == condition]
        c = sum(1 for r in rows if r["correct"])
        print("  %s: %d / %d" % (condition, c, len(rows)))
