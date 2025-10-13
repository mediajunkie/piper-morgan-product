# Piper Morgan - Project Overview

## Purpose
Piper Morgan is an intelligent AI product management assistant that transforms routine PM tasks into natural conversations while providing strategic insights through AI-powered analysis.

## Core Capabilities
- **Natural Language Processing**: Use "that issue", "the document", "my task"
- **10-Turn Context Memory**: Remembers conversation across interactions
- **Sub-150ms Response Times**: Lightning-fast conversational AI
- **Issue Intelligence**: AI-powered GitHub issue analysis and prioritization
- **Morning Standup**: Daily accomplishments with real data from all integrations
- **Web Interface**: Dark mode UI with 4.6-5.1s generation (faster than CLI)
- **Multi-User Configuration**: Teams can customize their own settings

## Architecture
- **Intent Classification System**: 13 intent categories routing to either fast canonical handlers (~1ms) or workflow orchestration (2-3 seconds)
- **Plugin Architecture**: Modular integration system with auto-registration
- **Performance**: 600K+ requests/second sustained, 84.6% cache hit rate
- **Classification Accuracy**: 95%+ accuracy for common query types

## Key Interfaces
- **Web API**: POST to `/api/v1/intent` with natural language messages
- **Slack**: Direct messages and mentions in Slack workspace
- **CLI**: Command-line interface for local development
- **Direct**: Python API for programmatic access