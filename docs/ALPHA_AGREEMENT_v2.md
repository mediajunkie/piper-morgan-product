# ALPHA TESTING AGREEMENT v2.0

**Effective Date: December 11, 2025**
**Software: Piper Morgan AI PM Assistant**
**Version: 0.8.9.1-alpha**

## 1. Acceptance of Terms

By cloning, downloading, installing, or using this software, you acknowledge that you have read, understood, and agree to be bound by this Alpha Testing Agreement.

## 2. Alpha Software Status

You acknowledge that:

- This is pre-release, experimental software (version 0.8.9.1-alpha)
- It contains known and unknown bugs, errors, and incomplete features
- It may crash, lose data, or behave unpredictably
- Features may be added, removed, or changed without notice
- Documentation may be incomplete or incorrect
- The GUI setup wizard, preference system, and workflow features are part of the alpha test
- **Data is not yet fully encrypted at rest** (use test data only, no sensitive information)

## 3. Acceptable Use

**You MAY:**

- Use the software for personal testing and evaluation
- Use the software for non-critical hobby projects
- Provide feedback and bug reports
- Modify the code for your own testing purposes
- Use the interactive setup wizard and preference configuration

**You MAY NOT:**

- Use the software for production or mission-critical tasks
- Use the software for any commercial purposes during alpha
- Install on employer systems without explicit written permission
- Process sensitive, confidential, or regulated data
- Rely on the software for time-sensitive or important work
- Redistribute the software without permission

## 4. Your Responsibilities

You are solely responsible for:

- All API charges incurred (OpenAI, Anthropic, etc.)
- Backing up any data before use
- Security of your own systems and data
- Verifying outputs before use
- Compliance with your employer's policies
- Compliance with all applicable laws and regulations
- Proper use of Docker and system resources

## 5. No Warranty Disclaimer

THIS SOFTWARE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO:

- MERCHANTABILITY
- FITNESS FOR A PARTICULAR PURPOSE
- NON-INFRINGEMENT
- ACCURACY OR RELIABILITY
- UNINTERRUPTED OR ERROR-FREE OPERATION
- FUNCTIONALITY OF SETUP WIZARD OR PREFERENCE SYSTEM

## 6. Limitation of Liability

IN NO EVENT SHALL THE DEVELOPERS BE LIABLE FOR:

- Any direct, indirect, incidental, special, or consequential damages
- Loss of data, profits, or business opportunities
- API charges or costs incurred
- Any damages resulting from use or inability to use the software
- Docker or system configuration issues

This limitation applies even if advised of the possibility of such damages.

## 7. Indemnification

You agree to indemnify and hold harmless the developers from any claims, damages, losses, or expenses arising from your use of the software.

## 8. Data Collection and Privacy

The software may collect the following data:

- Anonymous usage analytics for product improvement
- Error logs for debugging (no personal data included)
- User preferences configured through the preference questionnaire
- System health and performance metrics
- Setup wizard completion statistics

**Your API keys and personal data:**

- Passwords are hashed with bcrypt (12 rounds) and stored locally ✅
- API keys are encrypted in your system keychain and never transmitted ✅
- User preferences are stored locally in your database
- Resources (Lists, Todos, Projects, Files) use owner-based access control
- Sharing permissions are stored locally with explicit grants
- **Data at rest is NOT yet fully encrypted** ❌ (planned for beta 0.9.0)
- **IMPORTANT**: Use test data only. Do NOT process sensitive, confidential, or personal information
- You may opt out of analytics collection in settings
- No personal or sensitive data is transmitted to our servers

## 9. Termination

- This agreement is effective until terminated
- Your access may be revoked at any time without notice
- Upon termination, you must cease all use of the software
- Local data (preferences, API keys) remains under your control

## 10. Feedback and Contributions

- Any feedback you provide may be used without compensation
- Contributions to the codebase are subject to the project's open source license
- You grant permission to use your feedback for product improvement
- Preference data and usage patterns may inform product development

## 11. Third-Party Services

- The software integrates with third-party services (OpenAI, Anthropic, Docker, etc.)
- You are responsible for compliance with their terms of service
- The developers are not responsible for third-party service issues
- Docker usage is required for database and service management

## 12. System Requirements and Setup

- The software requires Docker, Python 3.11 or 3.12, and other system dependencies
- The interactive setup wizard will verify system requirements
- You are responsible for maintaining proper system configuration
- Database and service management is handled automatically

## 13. Changes to Agreement

This agreement may be updated at any time. Continued use constitutes acceptance of changes.

## 14. Governing Law

This agreement is governed by the laws of California, USA, without regard to conflict of law provisions.

## 15. Contact

For questions about this agreement or the software:
Email: [contact email]
GitHub: https://github.com/mediajunkie/piper-morgan-product

---

**BY USING THIS SOFTWARE, YOU ACKNOWLEDGE THAT YOU HAVE READ THIS AGREEMENT, UNDERSTAND IT, AND AGREE TO BE BOUND BY ITS TERMS.**

---

_Last Updated: March 4, 2026_
_Version: 2.3_
_Software Version: 0.8.9.1-alpha_
