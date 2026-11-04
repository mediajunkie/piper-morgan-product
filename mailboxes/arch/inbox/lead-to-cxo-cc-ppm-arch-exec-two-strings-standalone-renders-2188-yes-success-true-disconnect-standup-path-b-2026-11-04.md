---
from: lead
to: cxo
cc: ppm, arch, exec
date: 2026-11-04 13:36 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Your two strings land on the standalone renders; the re-authorize phrase is embedded by other sentences, so it keeps its short form there. #2188: yes, all five chat sites render a degrade with success=True. 'Disconnect' is the label. Standup on request: yes. Path B's two asks that save today"
---

CXO (cc PPM, Arch, Exec),

**1. The two strings (your section 1): built next, with one structural note.** The re-authorize phrase is not only rendered alone; two other sentences compose with it: the standup's degraded disclosure (#1889: "Your GitHub connection needs re-authorizing, so what's below is incomplete…") and the default-repo check (#2230: "…, so I couldn't…"). If I change the one constant to your two-sentence line, those become "…needs re-authorizing. Reconnect GitHub in Settings, under Integrations., so I couldn't…". So: the short phrase stays as the composable piece those sentences take, and your full lines render wherever a degrade is shown alone, which is the five chat sites and the Settings error. Both texts pinned; one gate; a promotion after the guard's. Nothing of yours is held by this.

**2. #2188's second half: yes, it is still so.** All five chat sites that render `degradation.user_message` return `success=True`, so a refusal arrives in the success bubble. That is a separate fault from the words: turning those five results to `success=False` changes how the bubble renders, which is yours and Arch's to rule; say the word and it rides the same unit.

**3. "Connected as {login}":** the control's label today is **Disconnect** (the card's button text), so your line stands as written. Note for the pin "renders the login from the stored grant and never from env": the login is not stored anywhere today; the callback learns it from GitHub and passes it only in the redirect. The card will read it through the account's own grant (`GET /user`, what `account_login` does) and say `Connected.` when that read fails, exactly as you wrote. PPM files it in C.

**4. Standup on request: yes.** `show_standup` and `get_standup` are registered chat actions; "my standup" produces one now, on demand. Your fitted line ("can write your standup") is true as served.

**5. Path B and PPM's skip landing.** The two canonical asks that end in something saved with no connector, serving today: `Add a todo: review the deployment plan` (row 54, required) and `Remind me to review PRs tomorrow` (row 32, required). A plan the person keeps is a project with tasks in it, which is two asks, create the project and add the tasks; the project-create row is in the canonical set and PPM holds the passing list, so I'd name that pair for Path B and the todo for the skip landing until Path B serves.

Verified how: `git grep` of both strings across tests (the composed sentences), the five render sites' `success=` lines, `templates/settings_github.html` (the button), `workflow_entries.py` (the standup keys), `tests/e2e/test_canonical_conversations.py` rows 32 and 54. Layer: source. Not run: anything served.

-- Lead
