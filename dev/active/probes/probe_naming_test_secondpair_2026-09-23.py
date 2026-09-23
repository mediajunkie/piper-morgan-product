"""
BYOC tool-catalog naming test — SECOND AMBIGUOUS PAIR, generalization check.

Prior passes (control + followup) established a real, replicated disambiguation benefit for
situation-shaped naming, but only on ONE pair (list_projects / attention_query) drawn from the
Read/query category. RESULTS-naming-test-followup-2026-09-23.md's "Still not settled" section
names the open question directly: does this generalize to a DIFFERENT ambiguous pair, not just a
different phrasing of the same one?

This pass adds a genuinely distinct pair from a different category (CRUD writes, not queries):
create_reminder vs. create_todo. Verified against the real handler
(services/intent_service/todo_handlers.py:536-544, handle_create_reminder docstring, #903): a
reminder is "a time-annotated todo" -- the real distinction is presence/absence of a time cue, not
a synonym pair. This is a different KIND of ambiguity than list_projects/attention_query (which
was about intent-purpose -- orientation vs. action-needed -- not time-presence), so a replication
here would be broader evidence than a third phrasing of the same pair.

Extends the CONTROL pass's 12-op catalog (independently-authored object descriptions, unchanged
situation descriptions) with these 2 new ops, both authored fresh in the same voice/style as the
existing 12 -- not derived from the internal code docstrings, to avoid the same-author confound
pass 1 was flagged for.

PM instructed "continue working on byoc" 2026-09-23; this is PA-owned, no-build-dependency Phase A
work per the readiness checklist, and directly answers the "still not settled" question named in
PA's own prior results doc rather than re-testing the same pair a fourth time.

RUN WITH THE AUTHORIZED INTERPRETER: /Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python
"""
import json, os, sys

MODEL = os.environ.get("PROBE_MODEL", "claude-sonnet-5")

SYSTEM = (
    "You are a helpful product-management assistant with access to tools. When the "
    "user's message clearly matches one of your available tools, call that tool. "
    "Do not ask clarifying questions if a tool is a clear match."
)

# The control pass's 12 operations, verbatim (op_id, obj_name, obj_desc, sit_name, sit_desc).
BASE_OPERATIONS = [
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

# NEW pair, freshly authored, same voice as BASE_OPERATIONS -- not derived from code docstrings.
NEW_PAIR = [
    ("create_reminder", "create_reminder",
     "Creates a time-anchored reminder that will notify the user at or near a specified time, for "
     "use when the request includes an explicit or implied timing cue, as opposed to an "
     "open-ended task with no target time attached.",
     "remind_me_at_a_time",
     "Use when the user wants to be nudged at or around a particular time -- their phrasing "
     "includes or implies a \"when.\""),
    ("create_todo", "create_todo",
     "Creates an open-ended todo item with no attached notification time, for use when the user "
     "wants something tracked to do later without a specific time attached, as opposed to a "
     "reminder tied to a particular time.",
     "add_to_my_list",
     "Use when the user wants something tracked to do later, with no particular time attached."),
]

OPERATIONS = BASE_OPERATIONS + NEW_PAIR

# (utterance, expected_op_id, note)
UTTERANCES = [
    ("Remind me to call the vendor tomorrow at 3pm.", "create_reminder", "clear reminder phrasing, explicit time"),
    ("Add 'review the Q3 budget' to my list.", "create_todo", "clear todo phrasing, no time"),
    ("I need to follow up with the vendor sometime tomorrow.", "create_reminder",
     "genuinely ambiguous -- soft time cue ('sometime tomorrow') inside a general-need phrasing, "
     "not an explicit reminder request; scored against create_reminder because a soft-but-present "
     "time cue is what handle_create_reminder's real trigger condition is (time-annotation "
     "presence), but a reasonable system could file this as a todo instead -- that's the point"),
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
        for utterance, expected_op_id, note in UTTERANCES:
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
            print("[%s] %-55s expected=%s got=%s  %s" % (
                condition, utterance, expected, tool_calls,
                "CORRECT" if correct else "WRONG"))

    with open("dev/active/probes/probe_naming_test_secondpair_results_2026-09-23.json", "w") as f:
        json.dump(out, f, indent=2)

    n_correct = sum(1 for r in out if r["correct"])
    print("\n%d / %d correct overall" % (n_correct, len(out)))
    for condition in ("object", "situation"):
        rows = [r for r in out if r["condition"] == condition]
        c = sum(1 for r in rows if r["correct"])
        print("  %s: %d / %d" % (condition, c, len(rows)))
