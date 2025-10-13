# Piper Morgan - Project Structure

## Core Application Files
- **main.py**: Application entry point with configuration validation
- **web/app.py**: FastAPI application (467 lines, refactored from 1,052)
- **services/**: Core business logic organized by domain
- **config/PIPER.user.md**: User configuration (Markdown format, not YAML)

## Key Directories
```
services/
├── plugins/                 # Plugin system infrastructure
├── integrations/           # External service integrations
│   ├── slack/             # Slack workspace integration
│   ├── notion/            # Notion workspace integration
│   ├── github/            # GitHub repository integration
│   ├── calendar/          # Google Calendar integration
│   └── demo/              # Template plugin for developers
├── intent/                # Intent classification system
├── domain/                # Domain models and business logic
├── config/                # Configuration services
├── cache/                 # Caching infrastructure
└── shared_types.py        # All enums and shared types

web/
├── app.py                 # FastAPI application
├── assets/                # Static web assets
└── middleware/            # Web middleware

tests/
├── plugins/               # Plugin system tests
├── intent/                # Intent classification tests
├── integration/           # Integration tests
├── unit/                  # Unit tests
├── performance/           # Performance benchmarks
└── regression/            # Regression tests

config/
├── PIPER.user.md         # User configuration
├── PIPER.defaults.md     # Default settings
└── feature_flags/        # Feature toggles

templates/                 # Jinja2 HTML templates
├── home.html             # Home page template
└── standup.html          # Standup UI template
```

## Architecture Layers
1. **Web Layer**: FastAPI routes and middleware
2. **Intent Layer**: Natural language processing and routing
3. **Plugin Layer**: Modular integration system
4. **Domain Layer**: Business logic and models
5. **Infrastructure Layer**: Database, cache, external APIs

## Plugin Architecture
- **PiperPlugin**: Abstract base class for all integrations
- **PluginRegistry**: Singleton registry for plugin management
- **Auto-registration**: Plugins register themselves on module import
- **Lifecycle management**: Initialize/shutdown hooks