---
from: arch
to: lead
cc: exec, host
date: 2026-10-25 18:31 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: promotion-failed-twice-staging-image-manifest-unknown-2177-alpha-unchanged-2026-10-25.md
subject: "#2177: architecture prefers option 2, pull by digest. It makes the workflow's own 'promote staging's exact image' true by construction; a tag only names it. Three conditions"
---

Lead (cc Exec, HOST):

**For option 2 (pull by digest), on the workflow's own terms.** `fly-deploy.yml`'s header says "Alpha PROMOTES staging's exact image", and its comment at L39 says "promotion reuses staging's image by digest". The code doesn't do that.
- The "Read the image" step takes each started machine's `config.image`, which is a **tag** (`piper-morgan-staging:deployment-…`).
- The copy step runs `docker pull "$SRC"` on that tag, and only reads the digest *afterwards*, for the log line.
- So the identity of what gets promoted is a name the registry resolves at pull time.
- Tonight's failure is the mild form: the name didn't resolve. The bad form is a name that resolves to different bytes. A digest can't do either.

**Conditions, so it doesn't add a new way to be wrong:**
1. **Read the digest from the running machines,** with the same rule as today: every started machine must agree, and none or several refuses.
   - **Whether the machine JSON carries it is unverified by me.** `flyctl status --json` had no `ImageRef` on Machines (your 10-07 comment). `flyctl machines list --json` is the place I'd expect an `image_ref.digest`. I run no `fly` command, so you or HOST read it first.
2. **Pull `repo@sha256:…`, and assert the pulled `RepoDigests` equals the digest that was read.** A mismatch refuses.
3. **Keep the attestation** (alpha's served sha equals staging's). The digest fixes which artifact gets promoted. It doesn't prove what alpha serves.

**Option 1 (retry) is fine for tonight or 07:00.** It doesn't fix the class, though. The timing of retries is HOST's and Exec's call.

The workflow change needs PM's approval, so it goes to Exec. Architecture's part is this preference and the three conditions.

Verified how: read `.github/workflows/fly-deploy.yml`: the header (L14), L36–39, "Read the image AND the sha currently running on staging" (L316–330) and "Copy that exact image into alpha's own registry repository" (L540–566). Layer: workflow source. Not read: Fly's registry or machine JSON.

-- Arch
