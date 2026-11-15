# Alpha Onboarding Email Templates

**Version**: 2.6
**For**: Piper Morgan 0.8.6 Alpha Release
**Last Updated**: February 6, 2026

---

## Email Templates

| Template | Purpose | When to Send |
|----------|---------|--------------|
| [email-1-pre-qualification.md](email-1-pre-qualification.md) | Initial outreach with prerequisites | When someone expresses interest |
| [email-2-confirmation.md](email-2-confirmation.md) | Confirm access and schedule setup | After they confirm prerequisites |

**Usage**: Open the template file, copy the content, paste into your email client. The files render as plain text suitable for email.

---

## Subject Lines (A/B test these)

**Pre-qualification:**
- "Ready to test Piper Morgan? Check requirements first"
- "Piper Morgan alpha access - Prerequisites inside"
- "[Name], before we set up Piper Morgan..."

**Confirmation:**
- "You're in! Piper Morgan alpha setup next steps"
- "[Name], your Piper Morgan alpha access is confirmed"

---

## Template Variables

Customize these for each tester:

| Variable | Description |
|----------|-------------|
| `[Name]` | Tester's first name |
| `[DATE/TIME]` | Scheduled setup call |

---

## Sending Checklist

Before sending pre-qualification:
- [ ] Personalize name
- [ ] Verify technical claims match current version

Before sending confirmation:
- [ ] Schedule setup call first
- [ ] Attach current documentation from `docs/`:
  - BETA_TESTING_GUIDE.md
  - ALPHA_AGREEMENT_v2.md
  - BETA_QUICKSTART.md
  - BETA_KNOWN_ISSUES.md
- [ ] Update internal tracking (who's in alpha cohort)

---

## Notes

**Email Tone**: Friendly but honest about alpha status. Set realistic expectations upfront.

**Support Commitment**: Only promise what you can deliver. Small cohort (2-5) is manageable for close support.

**Technical Prerequisites**: Don't sugarcoat - command line comfort is required. Better to filter out now than frustrate later.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.5 | 2026-02-01 | Split into separate template files, updated disk space (1GB → 200MB) |
| 2.4 | 2026-01-31 | Updated for v0.8.5.1 |
| 2.3 | 2026-01-27 | Added accessibility notes |

---

## See Also

- `../../BETA_TESTING_GUIDE.md` - Reference for what testers will receive
- `../../ALPHA_AGREEMENT_v2.md` - Legal terms testers will see
- `../../BETA_QUICKSTART.md` - Quick reference guide for testers
- `../../BETA_KNOWN_ISSUES.md` - Current bugs and limitations
