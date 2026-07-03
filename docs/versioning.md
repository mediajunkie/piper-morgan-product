# Piper Morgan Versioning Strategy

## Current Version: 0.8.9.1

## Versioning Scheme

Piper Morgan follows [Semantic Versioning (SemVer)](https://semver.org/) with the following format:

```
MAJOR.MINOR.PATCH[-PRERELEASE]
```

### Version Components

- **MAJOR**: Incremented for incompatible API changes
- **MINOR**: Incremented for backwards-compatible functionality additions
- **PATCH**: Incremented for backwards-compatible bug fixes
- **PRERELEASE**: Optional suffix for pre-release versions (alpha, beta, rc)

### Current Versioning Strategy

#### Pre-1.0 (Alpha Phase)

- **0.x.y-alpha**: Alpha releases leading to MVP
- **0.x.y-beta**: Beta releases for final testing before MVP
- **1.0.0**: First MVP release

#### Post-1.0 (Production)

- **1.x.y**: Production releases following standard SemVer
- **2.0.0+**: Major version increments for breaking changes

## Version Sources of Truth

### Primary Version Definition

- **`VERSION` file**: Single source of truth in project root
- **`pyproject.toml`**: Python package version (must match VERSION file)

### Version References

- **Alpha documents**: Reference current semantic version
- **API responses**: Include version in metadata
- **Documentation**: Version-specific guides and references

## Roadmap vs. Version Separation

**Important**: Roadmap positions (e.g., "2.7.5", "Sprint A8") are **separate** from software versions.

- **Roadmap positions**: Track project progress and sprint completion
- **Software versions**: Track actual software releases and compatibility

This separation allows:

- Flexible roadmap adjustments without version confusion
- Clear software compatibility communication
- Independent roadmap and release planning

## Version Management

### Manual Process (Current)

1. Update `VERSION` file
2. Update `pyproject.toml` version field
3. Update relevant documentation
4. Create git tag for releases

### Future Automation (Planned)

- Automated version bumping scripts
- CI validation of version consistency
- Automatic changelog generation
- Integration with release workflows

## Alpha Testing Versions

During alpha testing, versions follow this pattern:

- `0.8.0-alpha`: Current alpha version
- `0.8.1-alpha`: Bug fixes and minor improvements
- `0.9.0-alpha`: New features and capabilities
- `1.0.0-beta`: Beta testing before MVP
- `1.0.0`: MVP release

## Version History

| Version | Date       | Milestone | Notes                                          |
| ------- | ---------- | --------- | ---------------------------------------------- |
| 0.8.9.1 | Jul 2026   | Patch     | Security fix (#1343) — anonymous LLM-key billing exposure closed |
| 0.8.9   | Jun 2026   | RECONNECT | RECONNECT WS-1 + security + design D2 — connector infra, field encryption, token system |
| 0.8.8   | Jun 2026   | RECONNECT | D1/RECONNECT — BYOC keys, Radar default, nav IA, home UX |
| 0.8.7   | Jun 2026   | M1+M2+M3  | Conscious Floor, dispatch rail complete, files UX, Slack inbound |
| 0.8.6   | Mar 2026   | M0 Sprint | M0 Conversational Glue, 27 issues resolved     |
| 0.8.5.3 | Feb 2026   | Patch     | Windows compatibility, setup UX, 14 issues resolved |
| 0.8.5.2 | Feb 2026   | Patch     | Chat persistence, date formatting, calendar fixes |
| 0.8.5.1 | Jan 2026   | Patch     | 14 alpha testing bug fixes                     |
| 0.8.5   | Jan 2026   | MUX       | MUX-IMPLEMENT complete, WCAG 2.1 AA accessibility |
| 0.8.4.3 | Jan 2026   | Sprint A20| Fresh install fixes (#605-#609), UI polish     |
| 0.8.4.2 | Jan 2026   | Sprint A20| Calendar bug fixes (#596, #588)                |
| 0.8.4.1 | Jan 2026   | Sprint A20| Calendar/TEMPORAL timezone fixes               |
| 0.8.4   | Jan 2026   | Sprint B1 | Integration Settings, Portfolio Onboarding     |
| 0.8.3.2 | Jan 2026   | Sprint B1 | Interactive Standup Assistant (Epic #242)      |
| 0.8.3.1 | Jan 2026   | Sprint B1 | FTUX improvements                              |
| 0.8.3   | Jan 2026   | Sprint A17| Epic #314 CONV-UX-PERSIST complete             |
| 0.8.2   | Dec 2025   | Sprint A13| UX polish, accessibility improvements          |
| 0.8.1   | Nov 2025   | Sprint A9 | Bug fixes and improvements from alpha testing  |
| 0.8.0   | Oct 2025   | Sprint A8 | Alpha tester onboarding preparation            |
| 1.0.0   | TBD        | MVP       | Target MVP release                             |

## Guidelines for Contributors

1. **Never tie versions to roadmap positions**
2. **Update VERSION file first, then pyproject.toml**
3. **Use semantic versioning principles**
4. **Document breaking changes clearly**
5. **Test version references in documentation**

---

_Last updated: July 2, 2026_
_Current version: 0.8.9.1_
