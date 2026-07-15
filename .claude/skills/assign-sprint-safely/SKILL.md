---
name: assign-sprint-safely
description: Safely assign a GitHub issue to a Sprint (or any Projects v2 single-select field) WITHOUT wiping other issues' assignments. Use when PM asks to set/change an issue's Sprint, Status, or other project-board single-select field. Encodes the per-item mutation and the hard "never full-replace the option list" rule that two agents have violated (1175 items wiped 2026-07-05).
scope: cross-role
version: 1.0
created: 2026-07-14
updated: 2026-07-14
---

# assign-sprint-safely

Set an issue's **Sprint** (or any Projects v2 single-select field: Status, etc.) to an existing option — the per-item way that CANNOT munge other issues.

## When to Use

- PM asks to put an issue "in the Beta Blockers sprint" / "set its Status" / "assign it to a sprint."
- You need to change any GitHub **Projects v2 single-select field** value on an item.
- After filing a new issue that belongs in the current sprint.

Sprint is a **project-board field**, NOT a label and NOT a milestone (those are separate — see the bottom).

## ⚠️ THE HARD RULE (why this skill exists)

**NEVER use `updateProjectV2Field` to set an item's value.** That mutation *full-replaces the field's entire option list* with whatever you pass — omit any existing option and every issue assigned to it is silently dropped, project-wide. This wiped Sprint assignments for **1175 items on 2026-07-05**, and a related sort operation munged assignments on 2026-06-27. There is no undo (a backup/restore script pair exists; see `docs/internal/operations/github-and-tooling-gotchas.md`).

- ✅ **SAFE** — `updateProjectV2ItemFieldValue` (or `gh project item-edit`): sets **one item's** value to an **existing** option. Touches nothing else.
- ❌ **DANGER** — `updateProjectV2Field` / `gh project field-*` edits: mutate the field DEFINITION (the option list). Never use these to assign an issue. Adding a *new* option is a PM/web-UI task, not an assignment.

If you catch yourself about to send `updateProjectV2Field`, STOP — you want `updateProjectV2ItemFieldValue`.

## Procedure

### Step 1 — Inspect (READ-ONLY) — get the four IDs you need

```bash
OWNER=mediajunkie   # the org/user that owns the project

# a) Which project has the field? (Sprint lives in project #1 "Building Piper Morgan")
gh project list --owner "$OWNER"
# → note the project NUMBER and its node ID (PVT_...)

# b) The field ID + the target option's ID (single-select options are stable IDs)
gh project field-list <PROJECT_NUMBER> --owner "$OWNER" --format json \
  | python3 -c "import json,sys;
[print(f'{f[\"name\"]}  field={f[\"id\"]}') or [print(f'    opt {o[\"name\"]!r} = {o[\"id\"]}') for o in f.get('options',[])]
 for f in json.load(sys.stdin)['fields'] if f['name']=='Sprint']"

# c) The ITEM ID for your issue in that project (an issue is not the same as its project item)
gh api graphql -f query='{ repository(owner:"'$OWNER'",name:"<REPO>"){ issue(number:<N>){
  projectItems(first:10){ nodes{ id project{ number title } } } } } }' \
  --jq '.data.repository.issue.projectItems.nodes[] | "item=\(.id) project#\(.project.number)"'
# If the issue is NOT in the project yet: gh project item-add <PROJECT_NUMBER> --owner "$OWNER" --url <issue-url>
```

**Reference values as of 2026-07-14** (VERIFY with the commands above — IDs can change if the field is recreated):
- Project #1 "Building Piper Morgan" node id: `PVT_kwHOADE-8s4A-JwA`
- Sprint field id: `PVTSSF_lAHOADE-8s4A-JwAzg2hWcg`
- Option "Beta Blockers - Hard Gates Only": `94e9d0d0`  ·  "PUB - Public Beta": `d9067be5`

### Step 2 — Safety pre-check (READ-ONLY) — don't clobber

```bash
gh api graphql -f query='{ node(id:"<ITEM_ID>"){ ... on ProjectV2Item {
  content{ ... on Issue { number } }
  fieldValueByName(name:"Sprint"){ ... on ProjectV2ItemFieldSingleSelectValue { name } } } } }' \
  --jq '"#\(.data.node.content.number) Sprint=\(.data.node.fieldValueByName.name // "(unset)")"'
```
If it already has a value you weren't told to change, STOP and confirm with PM.

### Step 3 — Set the value (the SAFE mutation)

```bash
gh api graphql -f query='mutation{ updateProjectV2ItemFieldValue(input:{
  projectId:"<PROJECT_NODE_ID>", itemId:"<ITEM_ID>", fieldId:"<FIELD_ID>",
  value:{ singleSelectOptionId:"<OPTION_ID>" } }){ projectV2Item{ id } } }'
```
(`gh project item-edit --id <ITEM_ID> --project-id <PROJECT_NODE_ID> --field-id <FIELD_ID> --single-select-option-id <OPTION_ID>` is the equivalent CLI wrapper.)

### Step 4 — Verify + prove no collateral damage

```bash
# Your item now holds the value:
gh api graphql -f query='{ node(id:"<ITEM_ID>"){ ... on ProjectV2Item {
  fieldValueByName(name:"Sprint"){ ... on ProjectV2ItemFieldSingleSelectValue { name } } } } }' --jq '.data.node.fieldValueByName.name'
# A DIFFERENT existing issue still holds ITS value (proves you didn't touch the option list):
#   repeat Step 2's read on a known-assigned issue.
# The option count is unchanged:
gh project field-list <PROJECT_NUMBER> --owner "$OWNER" --format json \
  | python3 -c "import json,sys; print([len(f.get('options',[])) for f in json.load(sys.stdin)['fields'] if f['name']=='Sprint'][0], 'options')"
```

## Milestone is separate (and safe)

Milestone is a **native issue field**, not a project field. Set it with the plain CLI — no munging risk:
```bash
gh issue edit <N> --milestone "MVP"
```
Sprint (project field) + Milestone (issue field) are set independently; PM often specifies both.

## Notes

- Closed issues can still be assigned (milestone + sprint) — a closed issue should carry its sprint so the sprint's completed-work is accurate.
- **Sprint-field changes are PM-gated** — set only the sprint/option PM named; don't infer. Adding a *new* sprint option is a PM/web-UI action, never an agent mutation.
- Full incident detail + the backup/restore scripts: `docs/internal/operations/github-and-tooling-gotchas.md`.
