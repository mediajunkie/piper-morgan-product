"""
BYOC tool-catalog naming test — TARGETED FOLLOW-UP on the one unresolved case.

Design/prior results: dev/active/probes/RESULTS-naming-test-control-2026-09-22.md, "Recommendation"
section. list_projects vs attention_query was the one failure that persisted even under a good
independent object-shaped description (utterance: "Remind me what I've got going on right now").
This run varies the utterance for just that pair (3 new phrasings, ranging clear-list to
clear-attention to still-ambiguous) to see whether the earlier failure was a real naming effect or
one hard phrasing.

Reuses the CONTROL pass's catalogs (independently-authored object descriptions, unchanged
situation descriptions) for a clean comparison against both prior runs. Full 12-tool catalog
present each call, as in both prior passes -- only new utterances, scored against the intended
target for each.

PM-approved 2026-09-23 ("Please proceed!").
RUN WITH THE AUTHORIZED INTERPRETER: /Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python
"""
import json, os, sys

MODEL = os.environ.get("PROBE_MODEL", "claude-sonnet-5")

SYSTEM = (
    "You are a helpful product-management assistant with access to tools. When the "
    "user's message clearly matches one of your available tools, call that tool. "
    "Do not ask clarifying questions if a tool is a clear match."
)

# Full 12-op catalog, SAME as the control pass (independent-author object descriptions).
OPERATIONS = [
    ("create_issue", "create_issue", "Creates a new tracked issue or ticket in the system when a "
     "piece of work, bug, or request needs to be captured for the first time and does not yet "
     "exist as a tracked item.",
     "track_a_new_piece_of_work", "Use when the user has an idea, bug, or task they want tracked going forward."),
    ("close_issue", "close_issue", "Marks an existing tracked issue as complete/resolved when its "
     "work is finished, without altering any of its other fields.",
     "mark_this_done", "Use when the user indicates something they were tracking is finished."),
    ("update_issue", "update_issue", "Modifies one or more fields (title, description, status, "
     "assignee, etc.) on an existing tracked issue when the issue itself remains open and only its "
     "details or state need to change, as opposed to marking it fully complete.",
     "update_something_im_tracking", "Use when the user wants to change details on something already being tracked."),
    ("delete_todo", "delete_todo", "Permanently removes a todo item from the system, for use only "
     "when a todo was created in error or is no longer wanted at all, rather than being completed "
     "or converted into a tracked issue.",
     "remove_something_from_my_list", "Use when the user wants an item taken off their to-do list."),
    ("attention_query", "attention_query", "Retrieves the set of items currently requiring the "
     "user's action, such as those that are blocked, overdue, or explicitly flagged, for a "
     "real-time \"what needs me right now\" view rather than a historical or metrics view.",
     "whats_needing_my_attention", "Use when the user wants to know what's blocked, overdue, or needs a decision right now."),
    ("changes_query", "changes_query", "Retrieves what has changed across the user's items since "
     "their last check, for catching up on activity and updates rather than surfacing items that "
     "need action.",
     "whats_changed_since_i_looked", "Use when the user wants a catch-up on what's happened since they were last checked in."),
    ("productivity_query", "productivity_query", "Retrieves aggregate productivity or velocity "
     "metrics for the team over a specified recent period, for reporting on team-level throughput "
     "trends rather than individual item status.",
     "hows_the_team_doing_this_week", "Use when the user wants a read on team pace/output over a recent period."),
    ("list_projects", "list_projects", "Retrieves the list of projects the user currently has, for "
     "orientation or navigation when the user needs to see what projects exist rather than details "
     "of any single item within one.",
     "show_me_what_im_working_on", "Use when the user wants an overview of their active projects."),
    ("strategic_planning", "strategic_planning", "Generates or updates a strategic plan or roadmap "
     "for a given initiative, for higher-level, multi-step planning work rather than for creating "
     "or editing a single issue or todo.",
     "help_me_plan_this_out", "Use when the user has a fuzzy initiative and wants help turning it into a real plan."),
    ("learn_pattern", "learn_pattern", "Records a preference or behavioral pattern the user has "
     "demonstrated so it can be applied automatically in future interactions, for capturing durable "
     "user-specific conventions rather than performing a one-off action.",
     "remember_how_i_like_this_done", "Use when the user is teaching Piper a preference or habit to reuse later."),
    ("summarize_document", "summarize_document", "Produces a summary of the contents of a document "
     "the user has shared or uploaded, for condensing existing document content rather than "
     "generating new planning or tracking artifacts.",
     "give_me_the_gist", "Use when the user wants a quick summary of a document they've shared."),
    ("meeting", "meeting", "Schedules a new meeting or finds available time for one among relevant "
     "participants, for calendar/scheduling requests rather than any issue-, todo-, or "
     "document-related operation.",
     "find_time_to_meet", "Use when the user wants to schedule or find a meeting time."),
]

# NEW utterances for this follow-up: (utterance, expected_op_id, note)
FOLLOWUP_UTTERANCES = [
    ("What projects do I currently have?", "list_projects", "clear list-projects phrasing"),
    ("What needs my attention today?", "attention_query", "clear attention-query phrasing"),
    ("What am I currently working on?", "list_projects", "still-ambiguous phrasing, closest to the original failure"),
]


def build_tools(condition):
    tools = []
    for op_id, obj_name, obj_desc, sit_name, sit_desc in OPERATIONS:
        name, desc = (obj_name, obj_desc) if condition == "object" else (sit_name, sit_desc)
        tools.append({"name": name, "description": desc, "input_schema": {"type": "object", "properties": {}}})
    return tools


def op_name(op_id, condition):
    for oid, obj_name, _, sit_name, _ in OPERATIONS:
        if oid == op_id:
            return obj_name if condition == "object" else sit_name
    raise ValueError(op_id)


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
        for utterance, expected_op_id, note in FOLLOWUP_UTTERANCES:
            expected = op_name(expected_op_id, condition)
            try:
                tool_calls, text = run_claude(tools_for_condition, utterance, key)
            except Exception as e:
                tool_calls, text = [], "ERROR: %s" % e
            correct = (len(tool_calls) == 1 and tool_calls[0] == expected)
            out.append({
                "condition": condition, "utterance": utterance, "note": note,
                "expected": expected, "tool_calls": tool_calls, "correct": correct,
                "text_if_no_call": text if not tool_calls else "",
            })
            print("=" * 78)
            print("[%s] %-45s expected=%s got=%s  %s" % (
                condition, utterance, expected, tool_calls,
                "CORRECT" if correct else "WRONG"))

    with open("dev/active/probes/probe_naming_test_followup_results_2026-09-23.json", "w") as f:
        json.dump(out, f, indent=2)

    n_correct = sum(1 for r in out if r["correct"])
    print("\n%d / %d correct overall" % (n_correct, len(out)))
    for condition in ("object", "situation"):
        rows = [r for r in out if r["condition"] == condition]
        c = sum(1 for r in rows if r["correct"])
        print("  %s: %d / %d" % (condition, c, len(rows)))
