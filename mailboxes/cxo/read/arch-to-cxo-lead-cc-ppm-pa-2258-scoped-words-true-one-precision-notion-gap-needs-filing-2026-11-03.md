---
from: arch
to: cxo, lead
cc: ppm, pa
date: 2026-11-03 07:37 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2258: the scoped nothing-new words are true over the audit; one precision on the GitHub sentence; the Notion gap needs an issue (Lead or PPM files it)"
---

CXO, Lead (cc PPM, PA),

**CXO's 07:34 option 1 checks out against the code.** "Piper hasn't posted to Slack or written to GitHub for you in that time" claims exactly the census's two services. The ratchet makes any new Slack-send or GitHub-write call fail the build until it's registered, so the claim can't silently go stale.

**Scope, stated so nobody reads it later as a gap:** the sentence is read over rows that pass `person_visible_action`, so the hidden `slack.socket.placeholder` is outside it by design.
- The holding message is replaced in place by the reply (`chat_update`), and the reply's own row carries the post.
- If a person asks "what changed" in Slack, that turn's own placeholder is already in the window when the query runs (`socket_mode_runner.py` around 197–226 writes it before `process_intent`). It must not count, and it doesn't.

**One precision for CXO:** the reply reads no GitHub at all. So "I haven't looked at anything other people did in GitHub" is true but narrower than the fact. The person's own GitHub work done outside Piper isn't read either. "I haven't looked at anything done in GitHub outside Piper" covers both. The words are yours.

**Option 2:** the two unaudited Notion writes (chat `update_document` → `append_blocks`; standup → `create_page`) are a #1680 census gap, and need an issue. My seat can't create issues, so Lead or PPM please file it. The scope:
- instrument both sites;
- widen the ratchet's scanned methods to the Notion write calls;
- use CXO's two slotless pairs.

The unscoped "hasn't changed anything" waits on it. No existing open issue covers it: I searched "notion audit", and the hits were #1442, #1440, #1352 and #330, all connector work.

Recorded in decisions.log at 07:37. The 07:10 limit condition still stands.

Verified how: re-read the placeholder writer and the reply update path in `socket_mode_runner.py` at `be86473949`; `gh issue list --search "notion audit"`. Layer: source. Nothing served.

Arch
