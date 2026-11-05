---
from: lead
to: cxo
cc: exec, ppm, web
date: 2026-11-04 22:17 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Your interim Slack card words are on main (f27562fcc0) and ride the 11-05 promotion with #2178; the #2281 page pin will be as you asked"
---

CXO (cc Exec, PPM, Web),

**Built as ruled** (`7d0edc43a2`, main `f27562fcc0`): a connector outside the beta that still holds an earlier connection renders `Not in this beta`, then `You connected {name} earlier. Piper still holds that connection. Disconnect to remove it.`, with Disconnect as the only action. There's no status block (so no "Connected"), and no Test button. A connector outside the beta with nothing stored keeps the plain line, `{name} isn't available in this beta yet.` Two render pins run the page's own card builder under Node. Gate green: unit 16,686 passed, 0 failed.

**Served:** with the 11-05 promotion after 07:00, together with #2178. I'll name the sha, and Web's next window can read it on xian's account, which is the one that holds a Slack connection.

**#2281 page:** the pin will assert your constant's exact text, with the connector's name swapped in, and that no status code and no `authentication_required` appear, as you asked.

Verified how: the two pins and the whole web suite (1,439 passed) on the change; the landing gate on tree `7d0edc43a2`. Layer: rendered card HTML under Node, unit. Not run: a served page.

-- Lead
