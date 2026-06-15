---
name: update-piper
description: Refresh Piper's understanding of the PM's world when things have changed
  — new projects, team changes, shifted focus, new tools. Shows PM what Piper currently
  knows, then updates only the sections that are stale. Prevents meet-piper from
  becoming a one-shot interview that degrades over time. Trigger phrases: "Piper
  doesn't know about X", "things have changed", "update my profile", "I need to
  tell you something new", "you have outdated info about".
scope: cross-role
version: 1.0
created: 2026-06-15
---

# update-piper

Keep Piper's understanding of the PM's world current as things change — without making PM re-do the full `meet-piper` interview.

`meet-piper` is a one-time conversation. The PM's world isn't. Projects end, teams shift, priorities change, new tools get wired in. Without `update-piper`, Piper's context degrades silently: it keeps referencing a project that shipped, a team member who left, a goal that no longer applies. The quality of Piper's answers depends on the quality of its model of who PM is and what they're working on.

## When to Use

- Piper references something that's changed (old project, departed team member, stale focus)
- PM says "things have changed" or "Piper doesn't know about X"
- PM joined a new project, shipped a major milestone, or changed role
- A new integration is available that wasn't wired in `meet-piper`
- PM's goals or priorities have shifted (new quarter, new strategy, new constraints)
- It's been 4+ weeks since `meet-piper` or the last `update-piper` — Piper prompts proactively

**Not for**: the full initial interview (use `meet-piper`). Not for wiring new connectors (use `connect-piper`). Not for one-off corrections in a conversation ("actually that project is done" — just tell Piper inline).

## The Core Principle

**Show before asking.** Before asking PM what's changed, show what Piper currently knows. PM can't tell you what's stale if they don't know what you have. The "show first" step also catches drift PM didn't notice — Piper may have a subtly wrong model that PM hasn't had reason to correct.

**Update sections, not the whole profile.** A full re-interview is slow and wastes PM's time on things that haven't changed. Update only what's different; leave the rest alone.

## Profile sections

The PM profile covers six areas. Each can be updated independently:

| Section | What it covers | Common staleness triggers |
|---|---|---|
| **Projects** | Active projects, their status, goals, and maturity | Project shipped, new project started, project paused |
| **Team** | People PM works with, their roles, and how they fit | New hire, departure, role change, new collaboration |
| **Focus** | Current priorities, what PM is spending time on | New quarter, strategy shift, crisis re-prioritization |
| **Working style** | How PM likes to work, communication preferences, decision patterns | Rarely changes — usually stable after `meet-piper` |
| **Tools & integrations** | GitHub repos, calendars, Notion, Slack workspaces | New repo, new tool adopted, integration added |
| **Goals** | What PM is trying to accomplish (90-day, annual, or product goals) | New OKRs, shipped goal, goal abandoned |

## Procedure

### Step 1 — Load current profile

Retrieve what Piper currently knows about this PM.

**With server access** (Plugin path):
```
get_profile() → returns stored PM profile JSON
```

**Without server access** (Native path): summarize what's been established in prior conversations. Be explicit about what you're working from.

If no profile exists at all: redirect to `meet-piper` — `update-piper` updates an existing profile, not creates one from scratch.

### Step 2 — Show PM a profile snapshot

Before asking any questions, give PM a clear summary of what Piper currently knows. Use this format:

```
Here's what I currently know about your world. Tell me what's changed.

**Projects**
- [Project name] — [one-line status: active / in-flight / launched / paused]
- [Project name] — [status]

**Team**
- [Name] ([role]) — [one line on what they do]
- [Name] ([role]) — [one line]

**Current focus**
[2-3 sentences on what Piper understands PM is prioritizing]

**Tools**
- GitHub: [repos]
- Calendar: [connected / not connected]
- [Other tools]

**Goals (as I understand them)**
- [Goal 1]
- [Goal 2]
```

Follow immediately with: **"What's changed, or what have I got wrong?"**

Let PM respond naturally — they'll tell you what's stale. Don't ask a long structured questionnaire; let PM lead.

### Step 3 — Probe the changed areas

Once PM identifies what's changed, ask targeted follow-up questions for each area they flagged. Don't probe areas they didn't flag (those are still current).

**For a changed project:**
- What's the new status? (active / shipped / paused / cancelled)
- If new: what's it called, what problem does it solve, what's the milestone?
- If shipped: is there a follow-on, or is that area complete?

**For a team change:**
- Who joined / left / changed role?
- What does their new role cover?
- Anyone new that Piper should know about?

**For a focus shift:**
- What are you spending most of your time on now?
- What shifted — new priority pushed in, old one resolved, or external change?

**For new tools:**
- What tool or integration got added?
- Which connector does it map to (GitHub / Calendar / Notion / other)?
- Should Piper start pulling context from it? (→ `connect-piper` if needed)

**For a goal change:**
- What's the current horizon (90-day / annual / product)?
- What's the primary outcome you're working toward?

Keep probes short. One area at a time. Stop when PM indicates you have what you need.

### Step 4 — Update the profile

Write the updated sections back.

**With server access** (Plugin path):
```
save_profile(updated_sections) → confirms save
```

**Without server access** (Native path): state the updates explicitly in conversation so they're in context. Offer to save them to a profile file PM can reference later.

### Step 5 — Confirm and close

Summarize what changed:

```
Updated. Here's what I've revised:

✅ Projects: [what changed]
✅ Team: [what changed]
[Only list sections that were updated]

Everything else is unchanged. What would you like to do next?
```

If a change revealed a connector that should be wired (new GitHub repo, new calendar), offer to run `connect-piper` now.

---

## Proactive freshness check

Piper should prompt PM to run `update-piper` when:
- It's been **4+ weeks** since the last profile update (proactive nudge at session start)
- Piper notices a **reference inconsistency** — PM mentions something that contradicts the stored profile (e.g., "we shipped that last month" when Piper has it as in-flight)
- A connected **integration fails** — may indicate PM changed repos or revoked a token

The nudge should be brief and non-blocking:

> "Quick note — my profile for you was last updated [date]. Want to take 2 minutes to refresh it? Just say 'update my profile' when you're ready."

Don't block PM's current request to do the update. Note it; let PM choose when.

---

## Anti-patterns to avoid

| Don't | Why | Instead |
|---|---|---|
| Ask for updates without showing current state first | PM can't identify what's stale if they don't know what you have | Show → ask, every time |
| Re-run the full meet-piper interview | Wastes PM's time on unchanged sections | Update sections, not the whole profile |
| Update silently without confirming | PM doesn't know what changed; can't verify accuracy | Always confirm what was updated |
| Accept "things have changed" without probing | Too vague to update correctly | Ask targeted questions per section |
| Prompt for updates every session | Interrupts flow; teaches PM to ignore it | Wait for PM to flag, or nudge at 4-week mark |
| Mix connector setup into this skill | Separate concerns; different flow | Redirect to `connect-piper` for new integrations |

---

## Quality checklist

After running update-piper:
- [ ] Showed PM the current profile before asking what changed
- [ ] Updated only the sections PM flagged (didn't touch stable sections)
- [ ] Confirmed what changed in a closing summary
- [ ] Offered `connect-piper` if a new tool was mentioned
- [ ] Profile is now internally consistent (no reference to shipped projects as active, etc.)

---

## Example

**Trigger** (from PM):
> "I need to update you — we launched the GitHub connector last week so that project is done, and I have a new team member joining, Sara, who's going to own the analytics work."

**Step 2 — Show current profile:**
```
Here's what I currently know about your world. Tell me what's changed.

**Projects**
- GitHub connector — active, in-flight (Wave 1)
- Weekly digest — spec drafted, not yet in roadmap
- Piper plugin (BYOC) — planning, Track 5

**Team**
- You (xian) — PM/founder
- Lead Dev — engineering
- CXO — experience design
- (others)

**Current focus**
Wave 1 PM skills build-out, BYOC architecture, alpha testing

**Tools**
- GitHub: mediajunkie/piper-morgan-product ✅
- Calendar: not connected
- Notion: not connected

**Goals**
- Ship BYOC alpha to first external PMs
- Build Wave 1 PM skills (5 of 5)
- Establish Piper's differentiated value vs. generic AI tools
```
What's changed, or what have I got wrong?

**PM says**: "GitHub connector shipped, that project is done. And Sara is joining to own analytics."

**Step 3 — Probe:**
> "Got it — a couple of quick follow-ups:
> - Is the GitHub connector work completely wrapped up, or is there a Phase 2 / follow-on?
> - For Sara: what's her full role, and is analytics a new area for the team or something that already existed informally?"

**PM says**: "Connector is done, no follow-on yet. Sara is a new hire, data/analytics, first dedicated analytics person we've had."

**Step 4 — Update:**
- Projects: GitHub connector → status: SHIPPED (no follow-on tracked)
- Team: Sara added — data/analytics lead, first dedicated analytics hire

**Step 5 — Confirm:**
```
Updated. Here's what I've revised:

✅ Projects: GitHub connector → SHIPPED (no active follow-on)
✅ Team: Sara added — analytics lead (first dedicated analytics person)

Everything else is unchanged. Also — now that the connector is shipped, 
want to make sure it's wired properly? We can run connect-piper to verify 
the token is still active and pull a quick test.
```

---

## Changelog

- **v1.0** (2026-06-15): Initial version. Wave 1 PM skill #5. Generalizes meet-piper's one-time interview into a maintainable profile lifecycle. Core discipline: show before asking; update sections, not whole profile. Deployment: Native + Plugin (server-side profile storage for Plugin path).
