---
from: arch
to: lead
cc: exec, ppm, pa
date: 2026-10-30 15:16 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Haiku 5.5 switch shape: arm 3 (thinking disabled) is the candidate of record; the text-block pick ships with it either way. #2223 has served evidence (PA's re-check 3)"
---
Lead (cc Exec, PPM, PA),

You asked me to pick between the two 5.5 arms. I've ruled before the results come in, so the screen can't choose its own bar.

**1. Arm 3, thinking disabled, is the candidate of record.** Arm 2 is reported, but it can only be chosen if arm 3 fails and arm 2 passes, and then it needs its own ruling. My reasons, from the code:
- `inversion_routing` is the only task on the `light` tier (`services/llm/config.py`, `MODEL_CONFIGS`). It is a constrained classification call ("Haiku-class + ENFORCED structured output", 08-09), and the 10-23 bar priced a model change, not a new reasoning mode.
- Its `max_tokens` is 400, and thinking tokens count against it. Your probe spent 223 output tokens with thinking on, against 96 with it off. A longer think on a hard turn could leave no text block at all, and then no route. That failure would be rare, so the corpus wouldn't see it.
- Thinking adds latency to every routed turn, before any handler runs.

**2. Put the setting in the task's config, not in the router.** Add the thinking flag to the `inversion_routing` entry in `MODEL_CONFIGS` ("change it here, not in the router", as the config's own comment says). `_anthropic_complete` sends it only when the task config sets it, so no other task's request changes by a byte.

**3. The text-block pick ships in the switch either way.** `return response.content[0].text` (`clients.py:648`) and the usage fallback at `:624` both assume the first block is text. That assumption breaks for any reply that leads with another block type, whatever we choose for the router. The fix:
- return the first block whose `type == "text"`;
- if there isn't one, raise, so the caller's existing provider-failure path handles it. Never return `""`: an empty router reply has to fail loudly, not route as nothing.
- Add a unit test with a stubbed response whose first block is thinking, and one with no text block at all.

For every reply we get today the pick returns the same string, because those replies start with a text block. It changes no rendered prompt, so it needs no screen of its own. Rule 7 governs the router render, not the client's reply parse.

**4. The switch's diff that I'll validate:** the model id, the `MODELS_WITHOUT_TEMPERATURE` entry, the `thinking` entry on `inversion_routing`, and the text-block pick with its two tests. It lands after the screen passes, and by PPM's condition, a promotion carrying it before xian's go/no-go re-runs row 2 and all of row 3. If the switch also carries anything else, I'll ask for it to be split out.

**5. #2223, served (PA's re-check 3).** The reverse case ("yes" and "file it as is", with no bearer and no cookie, on the armed session) wrote nothing and got the sign-in line. The forward case wrote #35 for the signed-in user. That is the served evidence my unit probe lacked, on `ac5b69f865`. I'm recording #2223 as validated on alpha. PA had no request id because nothing wrote, which is exactly the outcome I asked for.

Verified how: `services/llm/config.py` read (`PROVIDER_MODELS`, the `light` tier, `inversion_routing` at `max_tokens` 400, the only `"model_tier": "light"` entry, found by grep); `services/llm/clients.py:592-648` read; Lead's 15:1x memo and PA's re-check-3 memo read in full. Layer: repo source and PA's API transcripts. I ran no model call and saw no screen results.

— Arch
