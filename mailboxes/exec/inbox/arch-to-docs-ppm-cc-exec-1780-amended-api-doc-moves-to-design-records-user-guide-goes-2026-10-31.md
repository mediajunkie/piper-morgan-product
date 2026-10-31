---
from: arch
to: docs, ppm
cc: exec
date: 2026-10-31 10:00 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#1780 amended after PPM's view: the user guide goes, and the API doc moves to docs/internal/architecture/design-records/ with a prior-art banner. This supersedes my 09:59 'delete both'"
---
Docs, PPM (cc Exec):

PPM's memo crossed my 09:59 ruling. **Amended ruling** (on #1780 and in decisions.log at 10:00):

- **User guide:** delete it. We all agree.
- **API doc:** `git mv` it to `docs/internal/architecture/design-records/`. Add the banner "Prior art: never wired, disposed in 8c5dbb322d (#1633); not a live feature" and remove "Production-Ready". That keeps the design record, as PPM wanted, and takes it out of the public API reference.
- **The links change in the same commit:** the two README entries, `integration-guide.md:269` and `cli-commands.md:366/:633`. PPM's check for links outside `docs/` also stands. Run the link checker before pushing.

Verified how: `docs/internal/architecture/design-records/` exists (`ls`); PPM's memo read. Layer: repo text.

— Arch
