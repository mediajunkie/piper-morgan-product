# GitHub Projects CLI Primer

Reference for querying and updating GitHub Projects v2 boards from the command line.
Scoped to the `mediajunkie` owner and the "Building Piper Morgan" sprint board.

Last updated: 2026-06-22

---

## Projects at a glance

| # | Name | ID | Notes |
|---|------|----|-------|
| 1 | Building Piper Morgan | `PVT_kwHOADE-8s4A-JwA` | Sprint board — has Sprint field |
| 2 | PiperMorgan.ai | `PVT_kwHOADE-8s4BAEQo` | Website/comms board — no Sprint field |

```bash
# List all projects to confirm IDs
gh project list --owner mediajunkie
```

---

## Key field IDs (Project #1)

| Field | Type | ID |
|-------|------|----|
| Status | SingleSelectField | `PVTSSF_lAHOADE-8s4A-JwAzgxpGyU` |
| Sprint | SingleSelectField | `PVTSSF_lAHOADE-8s4A-JwAzg2hWcg` |

```bash
# Retrieve all field IDs (run when you need option IDs for Status or Sprint values)
gh project field-list 1 --owner mediajunkie --format json | jq .
```

---

## Querying sprint issues

```bash
# List items in the current sprint (paginate with --limit)
gh project item-list 1 \
  --owner mediajunkie \
  --format json \
  --limit 100 \
  --query 'sprint:"RECONNECT - Connector Refactor"'
```

**Gotchas:**
- Sprint name must be the **exact full name**, quoted. There is no `@current` or `@previous` shortcut — the Sprint field is a custom `SingleSelectField`, not GitHub's built-in Iteration type.
- Project #1 has 1,145+ total items. Always pass `--limit`; omitting it returns only the default page.

---

## Converting an issue number to a project item ID

Updates require the project item ID (`PVTI_...`), not the issue number. Extract it with jq:

```bash
ISSUE_NUMBER=1234

gh project item-list 1 \
  --owner mediajunkie \
  --format json \
  --limit 200 \
  --query 'sprint:"RECONNECT - Connector Refactor"' \
| jq -r --argjson n "$ISSUE_NUMBER" \
  '.items[] | select(.content.number == $n) | .id'
```

Or to build a map of all issue numbers → item IDs in one pass:

```bash
gh project item-list 1 \
  --owner mediajunkie \
  --format json \
  --limit 200 \
| jq -r '.items[] | [.content.number, .id] | @tsv'
```

---

## Updating an item's status

```bash
# Get the option IDs for the Status field first
gh project field-list 1 --owner mediajunkie --format json \
  | jq '.fields[] | select(.name == "Status") | .options'

# Then update:
gh project item-edit \
  --id <PVTI_...> \
  --project-id PVT_kwHOADE-8s4A-JwA \
  --field-id PVTSSF_lAHOADE-8s4A-JwAzgxpGyU \
  --single-select-option-id <option-id>
```

The `--id` argument takes the project item ID (`PVTI_...`), not the GitHub issue number.

---

## Common patterns

### List all items in a sprint with status

```bash
gh project item-list 1 \
  --owner mediajunkie \
  --format json \
  --limit 200 \
  --query 'sprint:"RECONNECT - Connector Refactor"' \
| jq -r '.items[] | [.content.number, .status, .content.title] | @tsv'
```

### Check which sprint an issue is in

```bash
gh project item-list 1 \
  --owner mediajunkie \
  --format json \
  --limit 500 \
| jq -r --argjson n 1234 \
  '.items[] | select(.content.number == $n) | {sprint: .sprint, status: .status}'
```

### Move an issue to a different status (full workflow)

```bash
ISSUE=1234
PROJECT_ID="PVT_kwHOADE-8s4A-JwA"
STATUS_FIELD="PVTSSF_lAHOADE-8s4A-JwAzgxpGyU"

# 1. Get item ID
ITEM_ID=$(gh project item-list 1 \
  --owner mediajunkie \
  --format json \
  --limit 500 \
  | jq -r --argjson n "$ISSUE" '.items[] | select(.content.number == $n) | .id')

echo "Item ID: $ITEM_ID"

# 2. Get available status option IDs
gh project field-list 1 --owner mediajunkie --format json \
  | jq '.fields[] | select(.name == "Status") | .options'

# 3. Set status (replace OPTION_ID with the value from step 2)
gh project item-edit \
  --id "$ITEM_ID" \
  --project-id "$PROJECT_ID" \
  --field-id "$STATUS_FIELD" \
  --single-select-option-id OPTION_ID
```

---

## Gotcha summary

| Gotcha | Detail |
|--------|--------|
| Sprint filter needs exact name | `sprint:"RECONNECT - Connector Refactor"` — copy from board; no wildcard/partial match |
| No `@current` sprint shortcut | Sprint is a custom SingleSelectField; GitHub's Iteration shortcuts don't apply |
| item-edit takes item ID, not issue # | Use the `PVTI_...` ID from `item-list`; issue numbers don't work |
| 1,145+ items in Project #1 | Always pass `--limit 100` or higher; default paginates at ~20 |
| Project #2 has no Sprint field | PiperMorgan.ai board (`PVT_kwHOADE-8s4BAEQo`) is comms-only; Sprint queries return nothing |
