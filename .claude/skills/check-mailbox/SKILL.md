---
name: check-mailbox
description: Check your agent mailbox for messages at session start. Use at the beginning of every session to review communications from other agents or advisors and note any action items.
scope: cross-role
version: 1.0
created: 2026-01-21
---

# check-mailbox

Check your agent mailbox for messages at session start and process any pending communications.

## When to Use

Use this skill:
- At the **start of every session** (before beginning assigned work)
- When PM mentions you have messages
- When resuming after a break
- After another agent references sending you something

## Procedure

### Step 1: Check Your Inbox

```bash
ls mailboxes/{your-role-slug}/inbox/
```

**Role slugs**: `arch`, `cio`, `lead`, `comms`, `ppm`, `cxo`, `host`, `docs`, `exec`, `spec`

**If empty**: Note "Mailbox empty" in session log and proceed with assigned work.

**If messages exist**: Continue to Step 2.

### Step 2: Read Each Message

For each file in inbox:
1. Read the full message
2. Note the headers:
   - `From`: Who sent it
   - `Response-Requested`: yes/no
   - `Priority`: high/medium/low
3. Understand what's being asked or communicated

### Step 3: Process and Move

After reading each message:

```bash
mv mailboxes/{your-slug}/inbox/{filename} mailboxes/{your-slug}/read/
```

**Why move?** Messages in `inbox/` = unread. Moving to `read/` prevents re-reading next session.

**The `mv` alone is not durable.** It changes only your worktree. To land the move on `origin/main`, send it through `scripts/mail-send.sh` in one call, passing BOTH sides of the move (the `inbox/` path and the `read/` path) plus any outbound memo paths: `scripts/mail-send.sh "mail({role}): triage N" mailboxes/{you}/inbox/{f} mailboxes/{you}/read/{f}`. Never `git add`/`git commit` a mailbox path. Do not cc PM or address mail to PM (route PM-needed items to `exec`). Full workflow: CLAUDE.md, "The mailbox workflow" (refreshed 2026-10-05 by Docs, #1909 skills review).

### Step 4: Handle Response-Requested

If `Response-Requested: yes`:

1. **Create response** in sender's inbox:
   ```
   mailboxes/{sender-slug}/inbox/{your-response-filename}.md
   ```

2. **Use response format**:
   ```markdown
   # Re: [Original Subject]

   **From**: {your-slug}
   **To**: {sender-slug}
   **Date**: YYYY-MM-DD HH:MM
   **In-Reply-To**: {original-filename}
   **Response-Requested**: no
   **Priority**: medium

   ---

   [Your response]
   ```

3. **If you can't respond yet**: Note in session log as pending action item.

### Step 5: Note Action Items

In your session log, record:
- Messages received (count and from whom)
- Key decisions or information
- Any action items for this session
- Pending responses needed

## Anti-Patterns to Avoid

| Don't Do This | Why | Do This Instead |
|---------------|-----|-----------------|
| Skip mailbox check | Miss important context or assignments | Always check at session start |
| Leave messages in inbox | Re-read same messages next session | Move to read/ after processing |
| Ignore Response-Requested | Sender waiting indefinitely | Respond or note as pending |
| Read but don't log | No record of what you learned | Note key points in session log |

## Example: Full Mailbox Check

```bash
# 1. Check inbox
ls mailboxes/docs/inbox/
# Output: memo-cio-skill-response-2026-01-21.md

# 2. Read message
# [Use Read tool on the file]

# 3. Move to read/
mv mailboxes/docs/inbox/memo-cio-skill-response-2026-01-21.md mailboxes/docs/read/

# 4. If Response-Requested: yes, create response in sender's inbox
# [Create response file in mailboxes/cio/inbox/]

# 5. Log in session log:
# "### 8:00 AM - Mailbox Check
# - Received 1 message from CIO re: skill adoption
# - Decision: Approved with guidance
# - Action: Proceed with Tier 1 skills"
```

## Example: Empty Mailbox

```bash
# 1. Check inbox
ls mailboxes/lead/inbox/
# Output: (empty)

# 2. Log in session log:
# "### 9:00 AM - Mailbox Check
# - Mailbox empty, no pending messages"
```

## Quality Checklist

After checking mailbox:
- [ ] Listed inbox contents
- [ ] Read all messages
- [ ] Moved all to `read/` folder
- [ ] Created responses where `Response-Requested: yes`
- [ ] Noted messages in session log
- [ ] Identified action items for session

## Reference

- **Mailbox system docs**: `mailboxes/DIRECTORY.md`
- **Message format**: See README for full header spec
- **Role slugs**: `arch`, `cio`, `ceo`, `lead`, `comms`, `ppm`, `cxo`, `host`, `exec`, `spec`, `docs`
