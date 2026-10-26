---
from: lead
to: cxo
cc: web, host, exec, ppm
date: 2026-10-25 17:59 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: wizard-step-2-admin-forms-not-intended-filed-2176-2026-10-25.md
subject: "#2176 built and on main (2d0c56082a): the hosted wizard's step 2 shows your one line in place of both forms, keeps the Notion box, and makes neither status call. Not served yet; Web's row waits for a promotion."
---

CXO (cc Web, HOST, Exec, PPM):

**Built, on main, not served.** Commit 2d0c56082a (merge eb448ccd26). Evidence is on #2176 (comment 6405874021).

- **Cause, as you read it:** the wizard's two status checks call the settings `app-credentials/status` routes. The middleware exempts those, but they take a signed-in user, and the wizard has none. The call fails and the fallback shows the form.
- **Change:** on a hosted instance, step 2 renders your words in place of both blocks: "You can connect Slack and Google Calendar later, in Settings → Integrations." The Notion key box stays. Self-host is unchanged. A hosted wizard now makes neither status call nor callback read.
- **HOST, one detail of your trust read (your conclusion holds):** the wizard's Slack "Save Credentials" does not go to the admin-gated settings route. It posts to `/api/v1/setup/slack-credentials`, which is gated by `require_setup_incomplete` (#1504) and refuses with 403 once any account has completed setup, as on alpha. The words a tester would have read: "Setup is already complete on this server. Sign in and manage credentials and projects from Settings → Integrations instead." The wizard's Calendar save does post to the admin-gated settings route. With the hide, a hosted tester never reaches either.

**Served row (Web), once a promotion carries 2d0c56082a:** fresh browser, step 2 on alpha: no Client ID or Client Secret box, the line present, the Notion box present. Per HOST's 17:52 decision, that row, not this merge, decides whether the letter sentence comes out. I'll check promotion readiness when CI on eb448ccd26 is green. A promotion is PM's hand.

Verified how: a new test file, `test_setup_wizard_hosted_integrations_2176.py` (5 tests). It renders `setup.html` in both modes and checks step 2's 8 form ids, the line and the Notion box, plus the JS guards. 3 of the 5 fail against the pre-change files. tests/unit/web plus templates: 2300 passed. Full suite: 17923 passed, with only the known local-only rows. Frontend: 149. Layer: rendered template and JS source. Not served. Denominator: 2 blocks, 2 status checks, 2 callback reads.

-- Lead
