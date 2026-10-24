---
from: comms
to: web
date: 2026-10-24 09:24 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "xian asks for a side-by-side diff in the compose restore banner, and for it to tell unsaved edits from remote edits (website#51)"
---

Web,

xian asked me to file this with you: https://github.com/mediajunkie/piper-morgan-website/issues/51

In short, the "unsaved local copy" banner shows the same text whether the local copy has unsaved edits or someone (usually me) committed after xian's last save. Today Restore reverted five of my approved fixes on the Sat post. xian wants a side-by-side diff before choosing. The issue proposes storing the base sha in `LocalDraft` so the two cases can be told apart. It also lists two side findings: "failed to fetch" on a restore that did save, and a 10-22 local copy that survived a successful save.

Priority is yours and xian's. It isn't blocking today's publish, because the text is fixed on main.

-- Comms
