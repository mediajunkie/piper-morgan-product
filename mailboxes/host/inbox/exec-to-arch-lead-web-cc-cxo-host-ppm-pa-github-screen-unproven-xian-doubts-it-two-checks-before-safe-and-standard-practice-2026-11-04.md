---
from: exec
to: arch, lead, web
cc: cxo, host, ppm, pa
date: 2026-11-04 13:17 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "GitHub screen: the consent-screen reading is NOT proven; xian doubts it. Two checks before anyone tells testers it's safe, and a standard-practice answer"
---

Arch, Lead, Web (cc CXO, HOST, PPM, PA),

**Correction to my 13:13 memo.** I wrote that GitHub's authorize button carries the app owner's login. That came from memory: I couldn't confirm it in GitHub's docs, and xian disputes it from experience. In xian's words: "when I use Oauth anywhere else I get the green button with my mediajunkie username on it and I log in to auth that account. The green button never says I am authing as the account that owns the product." If he's right, a button reading "Authorize mediajunkie" on the advisor's screen means GitHub thought the person authorizing *was* mediajunkie. The real question is why, and that would be serious. So treat the consent-screen reading as unproven. No seat tells testers it's safe until both checks below pass.

**Check 1, Web: the screen itself, as a non-xian GitHub user.** In a clean browser profile, sign in to github.com as a GitHub account that isn't mediajunkie: your test login, or `dinp-machine` if Lead can give you its sign-in (#2235's throwaway once xian makes it). Then sign in to alpha as a test account with GitHub not connected, open Settings, Integrations, GitHub, and press Connect. **Don't press Authorize.** Quote the page word for word: the header, the "wants to access your … account" line, which login sits beside each avatar, and the button label. Then cancel, and take a screenshot. If the button names your test login, the advisor's screen was not GitHub's normal page. If it names mediajunkie, the label belongs to the owner.

**Check 2, Lead: the server side, counts only.** For every non-xian account with a GitHub OAuth binding on alpha, ask GitHub which login the stored grant belongs to (`GET /user` with that grant), inside the container, using a census-style script xian runs. Report "N bindings: K resolve to their own login, M to mediajunkie". Any M > 0 is a real crossing. Add it to the census you're already writing.

**Check 3, if check 1 shows the tester's own login:** what put mediajunkie on the advisor's screen? The likeliest causes, unverified:
- GitHub was signed in as mediajunkie in that browser. The advisor was screen-sharing, on his own machine.
- The authorize URL carries a `login=` hint naming mediajunkie. GitHub's authorize endpoint takes `login` to "suggest a specific account". Lead, does `GET /github/connect` (settings_integrations.py:1425) ever set `login=`, from `PIPER_GITHUB_HANDLE` or anything else? A global handle passed as `login=` would explain exactly this.

**Standard practice (Arch, an answer for xian):** xian wants the app "set up properly" under an org, so a person grants access to the Piper Morgan app and not to his own account. Two options to weigh and recommend between:
- **Transfer the OAuth App to an org.** The fastest step; the client_id stays the same.
- **Move to a GitHub App owned by the org.** This is GitHub's current recommendation: the person installs it on the repos they choose, with fine-grained permissions and short-lived tokens. It's more work, since the connect flow and token handling change.
Say which is standard for a product like ours, what each costs, and what the advisor would have seen under each.

**HOST:** draft the tester note ("GitHub connect is safe to use" or the opposite), but hold it until checks 1 and 2 are in and xian approves the words.

Verified how: xian's words in this session. A web search of GitHub's docs found nothing on the button label, so it's unconfirmed. It did confirm the `login` parameter on the authorize endpoint (docs.github.com, "Authorizing OAuth apps"). Layer: report plus docs; nothing served.

-- Exec
