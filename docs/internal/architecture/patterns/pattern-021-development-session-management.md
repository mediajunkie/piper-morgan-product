# Pattern-021: Development Session Management Pattern

## Status

**Proven**

## Context

> **⚠️ Disambiguation Note**: This pattern covers development workflow session logging and tracking. For database/user application sessions, see [Pattern-013: Session Management Pattern](pattern-013-session-management.md).

Development teams need to track progress across complex, multi-step development tasks that span multiple sessions and agents. Without systematic session management, development work lacks accountability, progress tracking, and historical context. The Development Session Management Pattern addresses:

- What challenges does this solve? Provides structured logging and progress tracking for development workflows and agent coordination
- When should this pattern be considered? When managing complex development tasks that require progress tracking and accountability
- What are the typical scenarios where this applies? Multi-agent development workflows, long-running tasks, progress reporting, development audit trails

## Pattern Description

The Development Session Management Pattern manages development session logging and progress tracking for workflow accountability, agent coordination, and development audit trails.

Core concept:
- Structured session logging with phases and evidence
- Progress tracking across development workflows
- Agent coordination and handoff documentation
- Audit trails for development accountability

## Implementation

### Development Session Manager

```python
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import json

class DevelopmentSessionManager:
    """Manages development session logging and progress tracking"""

    def __init__(self, session_logs_dir: Path):
        self.logs_dir = Path(session_logs_dir)
        self.logs_dir.mkdir(exist_ok=True)
        self.current_session: Optional[Dict[str, Any]] = None

    def start_session(self, agent_name: str, mission: str, issue_ref: str = None) -> str:
        """Start new development session"""
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
        session_id = f"{timestamp}-{agent_name.lower().replace(' ', '-')}-log"

        session_data = {
            "session_id": session_id,
            "agent": agent_name,
            "mission": mission,
            "issue_ref": issue_ref,
            "started_at": datetime.now().isoformat(),
            "phases": [],
            "evidence": [],
            "deliverables": [],
            "status": "active"
        }

        self.current_session = session_data
        self._save_session()
        return session_id

    def log_phase(self, phase_name: str, description: str, evidence: Dict[str, Any] = None):
        """Log development phase with evidence"""
        if not self.current_session:
            raise ValueError("No active session. Call start_session() first.")

        phase_data = {
            "phase": phase_name,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "evidence": evidence or {}
        }

        self.current_session["phases"].append(phase_data)
        if evidence:
            self.current_session["evidence"].append({
                "phase": phase_name,
                "timestamp": datetime.now().isoformat(),
                **evidence
            })

        self._save_session()

    def log_terminal_output(self, command: str, output: str, phase: str = None):
        """Log terminal command and output as evidence"""
        evidence = {
            "type": "terminal_output",
            "command": command,
            "output": output,
            "phase": phase or "current"
        }

        if self.current_session:
            self.current_session["evidence"].append({
                "timestamp": datetime.now().isoformat(),
                **evidence
            })
            self._save_session()

    def add_deliverable(self, file_path: str, description: str, type: str = "file"):
        """Add deliverable to current session"""
        if not self.current_session:
            raise ValueError("No active session")

        deliverable = {
            "path": file_path,
            "description": description,
            "type": type,
            "timestamp": datetime.now().isoformat()
        }

        self.current_session["deliverables"].append(deliverable)
        self._save_session()

    def complete_session(self, summary: str, next_steps: List[str] = None):
        """Complete development session"""
        if not self.current_session:
            raise ValueError("No active session")

        self.current_session.update({
            "completed_at": datetime.now().isoformat(),
            "status": "completed",
            "summary": summary,
            "next_steps": next_steps or [],
            "total_phases": len(self.current_session["phases"]),
            "total_evidence": len(self.current_session["evidence"])
        })

        self._save_session()
        completed_session = self.current_session
        self.current_session = None
        return completed_session

    def create_handoff_prompt(self, target_agent: str, context: str = None) -> str:
        """Create handoff prompt for next agent"""
        if not self.current_session:
            raise ValueError("No active session")

        handoff_data = {
            "from_agent": self.current_session["agent"],
            "to_agent": target_agent,
            "session_id": self.current_session["session_id"],
            "mission": self.current_session["mission"],
            "completed_phases": self.current_session["phases"],
            "deliverables": self.current_session["deliverables"],
            "context": context,
            "handoff_time": datetime.now().isoformat()
        }

        # Save handoff documentation
        handoff_file = self.logs_dir / f"{self.current_session['session_id']}-handoff.json"
        with open(handoff_file, 'w') as f:
            json.dump(handoff_data, f, indent=2)

        return self._format_handoff_prompt(handoff_data)

    def _format_handoff_prompt(self, handoff_data: Dict[str, Any]) -> str:
        """Format handoff data into prompt"""
        phases_summary = "\n".join([
            f"- {phase['phase']}: {phase['description']}"
            for phase in handoff_data["completed_phases"]
        ])

        deliverables_summary = "\n".join([
            f"- {d['path']}: {d['description']}"
            for d in handoff_data["deliverables"]
        ])

        return f"""
# Agent Handoff: {handoff_data['from_agent']} → {handoff_data['to_agent']}

## Mission
{handoff_data['mission']}

## Completed Work
{phases_summary}

## Deliverables
{deliverables_summary}

## Context
{handoff_data.get('context', 'No additional context provided')}

## Session Reference
{handoff_data['session_id']}

Please continue from where {handoff_data['from_agent']} left off.
"""

    def _save_session(self):
        """Save session to file"""
        if not self.current_session:
            return

        session_file = self.logs_dir / f"{self.current_session['session_id']}.json"
        with open(session_file, 'w') as f:
            json.dump(self.current_session, f, indent=2)

    def get_session_history(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get recent session history"""
        cutoff_date = datetime.now() - timedelta(days=days)
        sessions = []

        for session_file in self.logs_dir.glob("*.json"):
            if session_file.name.endswith("-handoff.json"):
                continue

            try:
                with open(session_file, 'r') as f:
                    session = json.load(f)

                session_date = datetime.fromisoformat(session["started_at"])
                if session_date >= cutoff_date:
                    sessions.append(session)
            except (json.JSONDecodeError, KeyError):
                continue

        return sorted(sessions, key=lambda s: s["started_at"], reverse=True)
```

### Session Integration with Agents

```python
class AgentSessionIntegration:
    """Integration layer for agents to use session management"""

    def __init__(self, session_manager: DevelopmentSessionManager):
        self.session_manager = session_manager

    def start_agent_session(self, agent_name: str, task_description: str, issue_ref: str = None):
        """Start session for agent work"""
        session_id = self.session_manager.start_session(
            agent_name=agent_name,
            mission=task_description,
            issue_ref=issue_ref
        )

        self.session_manager.log_phase(
            "initialization",
            f"Agent {agent_name} started work on: {task_description}"
        )

        return session_id

    def log_work_phase(self, phase_name: str, description: str, files_modified: List[str] = None):
        """Log a work phase with file modifications"""
        evidence = {}
        if files_modified:
            evidence["files_modified"] = files_modified

        self.session_manager.log_phase(phase_name, description, evidence)

    def log_verification_step(self, verification_type: str, result: bool, details: str = None):
        """Log verification steps for accountability"""
        self.session_manager.log_phase(
            "verification",
            f"{verification_type}: {'✅ PASSED' if result else '❌ FAILED'}",
            {
                "verification_type": verification_type,
                "result": result,
                "details": details or "No additional details"
            }
        )

# Usage example
session_manager = DevelopmentSessionManager(Path("docs/development/session-logs"))
agent_integration = AgentSessionIntegration(session_manager)

# Agent starts work
session_id = agent_integration.start_agent_session(
    "Code Agent",
    "Extract patterns 011-015 from dual pattern systems",
    "PM-170"
)

# Log work phases
agent_integration.log_work_phase(
    "pattern_extraction",
    "Extracted Pattern-011: Context Resolution Pattern",
    ["docs/patterns/pattern-011-context-resolution.md"]
)

# Log verification
agent_integration.log_verification_step(
    "template_compliance",
    True,
    "Pattern follows established template structure"
)

# Complete session
session_manager.complete_session(
    "Successfully extracted and documented patterns 011-015",
    ["Cross-validate with Cursor agent", "Update GitHub issue status"]
)
```

## Usage Guidelines

### Session Lifecycle Management
- Start sessions at the beginning of significant development work
- Log phases with clear descriptions and supporting evidence
- Include terminal output and file modifications as evidence
- Complete sessions with comprehensive summaries

### Evidence Collection
- Capture terminal command outputs for verification
- Document file modifications and their purposes
- Include verification steps and their results
- Maintain audit trail for accountability

### Agent Coordination
- Use handoff prompts for agent transitions
- Document context and completed work clearly
- Reference previous sessions for continuity
- Maintain consistent session naming conventions

## Benefits

- Comprehensive audit trail for development work
- Clear progress tracking across long-running tasks
- Effective agent coordination and handoff management
- Accountability through evidence collection
- Historical context for future work

## Trade-offs

- Additional overhead for session management
- Storage requirements for session logs
- Need for consistent logging discipline
- Potential information overload in complex projects

## Anti-patterns to Avoid

- ❌ Starting sessions without clear mission statements
- ❌ Logging phases without supporting evidence
- ❌ Completing sessions without proper summaries
- ❌ Inconsistent session naming or structure
- ❌ Missing verification steps in critical work

## Related Patterns

- [Pattern-013: Session Management Pattern](pattern-013-session-management.md) - Database/user application sessions
- [Pattern-010: Cross-Validation Protocol Pattern](pattern-010-cross-validation-protocol.md) - Cross-validation in development sessions
- [Pattern-008: DDD Service Layer Pattern](pattern-008-ddd-service-layer.md) - Agent coordination workflows

## References

- **Implementation**: Development session logging framework in `docs/development/session-logs/`
- **Usage Example**: Daily session logs with mission tracking and agent handoffs
- **Related ADR**: Session logging framework, development methodology

## Migration Notes

*Split from Pattern-013 Session Management Pattern to focus specifically on development workflow tracking. For database/user sessions, see Pattern-013: Database Session Management Pattern.*
