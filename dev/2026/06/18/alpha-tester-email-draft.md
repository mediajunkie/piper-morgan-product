# Alpha tester email — draft

**From**: xian (Christian Crumlish)
**To**: [alpha tester list]
**Subject**: Piper Morgan skills — try these in Claude Code

---

Hey,

Quick note — I've been building something I think you'll find useful and wanted to give you a first look before it's more broadly available.

**Piper Morgan skills** are a set of slash commands for Claude Code that make product management work faster. They're calibrated for how I actually work — direct, no fluff, action-oriented. I'm sharing them now because I want real feedback, not a polished launch.

**What's included:**

- `/sprint-plan` — given your current issues/backlog, help you decide what to tackle and in what order
- `/stakeholder-update` — turn rough notes about what happened into a clear stakeholder update
- `/propose-feature` — articulate a feature idea with context, rationale, and scope
- `/draft-issue` — structure a rough idea into a properly scoped GitHub issue
- `/trust-check` — check whether an AI assistant is operating within appropriate bounds (this one's meta and interesting)
- `/brief-coding-agent` — write a clear brief for an AI coding agent on a specific task
- `/synthesize-feedback` — take raw user feedback and extract actionable patterns

**To install (Claude Code only for now):**

```bash
curl -sSL https://raw.githubusercontent.com/mediajunkie/piper-morgan-product/main/scripts/install-skills.sh | bash
```

That installs the skills into `~/.claude/skills/`. Restart Claude Code and you'll see them as slash commands.

**What I'm looking for:**
- Do they actually save you time?
- Do they feel right, or do they feel generic?
- Which ones do you reach for and which ones sit unused?
- What's missing?

You don't need to be systematic — just use them when they naturally fit and let me know what you notice. Honest takes only, please.

If you hit any weirdness, just reply to this email.

Thanks for being part of this,
xian

---

*Piper Morgan is a PM-specific AI assistant I've been building. The skills are the first distributable piece — the full assistant (profile-aware, connected to your tools) is coming. More soon.*
