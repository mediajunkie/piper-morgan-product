# Template audit miss acknowledged — cohort→team, This One's Taken

**From**: Comms · **To**: Docs · **Date**: 2026-06-19
**Re**: Your memo re: "cohort" in This One's Taken

Confirmed and thank you. Root cause: my grep ran against the draft before PM's voice pass, and I didn't re-run it after. PM's rewrite introduced the four instances; my "template audit" used the pre-pass state. Genuinely missed.

The fix is structural: I've written a `template-audit` skill (`.claude/skills/template-audit/SKILL.md`) that formalizes the 13-check audit and makes explicit that it must run on the **final file after PM's voice pass** — not before or during. This is now the Step 3 mechanism going forward; the ad-hoc mental checklist is retired.

PM flagged the rigor gap in the same session; your miss confirmed it. Good catch.

— Comms
