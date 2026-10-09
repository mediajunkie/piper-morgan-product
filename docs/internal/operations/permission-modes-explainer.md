# Permission modes, in plain words

*For xian. CIO, 2026-10-09. Facts from Claude Code's own docs (permission-modes and permissions pages, quoted
by Arch), plus what we measured on our seats. Owners of seat permissions: CIO and Pard.*

## The short answer

**Leave HOST on Auto.** Don't switch to Accept Edits. To stay in charge of production, add one **ask** rule:
then every production (`fly`) command HOST tries shows you a prompt, and nothing else changes.

## The modes

| Mode | What happens when an agent wants to run a command |
|---|---|
| **Default** (also called Manual) | Anything not pre-approved by a rule **asks you**. Safest, and the most prompts. |
| **Accept Edits** | Like Default, but it **also auto-approves file edits and common file commands** (`rm`, `mv`, `cp`, `sed`, `mkdir`, `touch`) inside the project. It is *looser* than Default, not a middle ground for production. |
| **Auto** (what our seats run) | Anything not covered by a rule goes to an **automatic reviewer** (Anthropic's classifier), which approves or blocks it without asking you. No prompts for ordinary work. |

## The three kinds of rule (they work in every mode)

Checked in this order, and the first match wins:
1. **Deny**: never allowed. Applies in every mode.
2. **Ask**: always prompts you. **Applies even in Auto**, which is the useful part.
3. **Allow**: runs without asking.

An allow can't override a deny or an ask.

## What this means for HOST's production lookups

- With **Auto plus `ask` on `fly`**: you see each production command before it runs and click once. Lookups are
  rare, so that's a handful of clicks, not a flood. Everything else HOST does stays automatic.
- That also makes it safe to install **before** the last open test (whether production's ssh runs a shell): you see
  the exact command every time.
- One cleanup goes with it. HOST's earlier one-session approval of the mint **wrapper script** runs `fly` inside the
  script, where an ask rule can't see it. It goes away when HOST's session restarts, or Pard removes it. After that,
  the only route to production is a command you approve.

## Which mode each seat should run

All seats: **Auto**, as now. Production access stays limited to the seats that need it (HOST today), and comes
through an **ask** rule, so you are the one who says yes. No seat needs Accept Edits.

## What we haven't tested

- The ask rule itself hasn't been tried on a seat yet. The docs say it prompts in Auto; a single test on HOST's
  seat after Pard installs it will confirm.
- The automatic reviewer's judgments vary. It refused a harmless production echo from Exec's seat today. That's
  why production goes through **ask** rather than through the reviewer.
