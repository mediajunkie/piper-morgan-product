# Claude directory submission — which tier is actually required (RESOLVED 2026-07-26)

**Status**: Resolved against Anthropic's official documentation, 2026-07-26. **Supersedes both prior
claims** — the 7/19 research memo *and* the in-chat retraction of it.
**Why this file exists**: this question has been answered wrong twice in eight days, in opposite
directions, and neither answer lived anywhere durable. This is the canonical home.

## The short answer

**PM's recent research is correct for connectors. The retraction was correct for plugins. Both were
over-generalized to the other track, and that's the whole confusion.**

| Track | Submit via | Requirement | Max plan enough? |
|---|---|---|---|
| **A — Connector directory** (remote MCP server) | `claude.ai/admin-settings/directory/submissions/new` | **Team or Enterprise org.** "Admin settings aren't available on individual plans." | ❌ **No** |
| **B — Plugin directory**, claude.ai path | `claude.ai/settings/plugins/submit` | Team/Enterprise + Directory-management access | ❌ **No** |
| **B — Plugin directory, CONSOLE path** | `platform.claude.com/plugins/submit` | **Developer, Admin, or Owner role on a *Console* organization** | ✅ **Yes** |
| **B — Plugin directory**, form path | `clau.de/plugin-directory-submission` | Public GitHub repo | ✅ Yes |

**The load-bearing distinction**: a **Console organization** (the developer/API platform,
`platform.claude.com` / `console.anthropic.com`) is **not** a claude.ai chat subscription tier. It is a
separate account object with its own roles. That's why the Console path sidesteps the Team requirement —
**not** because Max was ever sufficient for the admin portal. It never was.

## Where each prior claim went wrong

- **7/19 research memo — "Team/Enterprise required, Max blocked, full stop."** ✅ **Right about Track A.**
  ❌ Wrong to state it as a blanket gate on *directory submission*, because it missed the Console plugin
  path entirely.
- **The in-chat retraction — "two paths exist, Max users can submit."** ✅ **Right that the Console path
  exists and clears the Team requirement.** ❌ Wrong to generalize it to submission overall: it applies
  to **plugins only**, and the gating credential is a **Console org role**, not the Max plan.
- **The likely seed of the whole muddle**: a *listed* connector installs one-click for **Pro, Max, Team,
  and Enterprise** users. **Installing is not submitting.** PM's screenshot showing "Piper morgan"
  already present with an "Upload plugin" option is consistent with install/personal-upload UI, which
  works on Max — and is a different thing from a directory submission.

## What this changes operationally

1. ❌ **Track A (connector listing) is genuinely blocked on Max.** There is no workaround in the docs.
   It's a purchase decision — Team — not a lookup. **Stop treating "verify the tier" as a 5-minute task;
   the answer is known.**
2. ✅ **Track B (plugin listing) is available today on Max**, via the Console path or the `clau.de` form.
3. 🔺 **Therefore the open-source decision is now the live gate, not a deferrable one.** Track B requires
   a **public GitHub repo** — closed-source plugins are not accepted. **This reverses PA's earlier advice
   to defer it.** With Track A behind a paid upgrade, Track B is the only Claude-side route currently
   open, and open-sourcing is what unlocks it.
4. ➡️ **ChatGPT / OpenAI is untouched by any of this.** Still the only item with an external clock, still
   unstarted.

## Requirements that apply regardless of track

Tool annotations (`title` + `readOnlyHint`/`destructiveHint` on every tool) · OAuth 2.0 for
authenticated services · **public HTTPS privacy policy — missing or incomplete is an immediate
rejection** · documentation URL · test-account credentials without MFA, on a populated account ·
support contact · icon. URL slug is permanent once published. Run `claude plugin validate` before a
plugin submission.

## Open, needs PM's eyes (30 seconds, not research)

- **Does Piper Morgan already have a Console organization, and what's your role on it?** Almost
  certainly yes if the API has ever been used — but "almost certainly" is not verified, and it is the
  single credential Track B's Console path depends on.
- **What exactly is the "Piper morgan" entry in your screenshot** — an installed connector, a personal
  plugin upload, or a directory listing? Determines whether anything is already live.

## Sources

- [Submitting to the Connectors Directory — Claude docs](https://claude.com/docs/connectors/building/submission) *(authoritative for the Track A Team/Enterprise requirement)*
- [Submitting your plugin — Claude docs](https://claude.com/docs/plugins/submit)
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- [anthropics/claude-plugins-community](https://github.com/anthropics/claude-plugins-community)
- [Anthropic Software Directory Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy)

*PA, 2026-07-26. Route corrections here — and commit them, per
`feedback_a_correction_not_committed_has_not_happened`.*
