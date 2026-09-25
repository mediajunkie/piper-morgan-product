"""Tests for files/projects consciousness wrapper. Issue #635."""


class TestProjectsConsciousness:
    """Test consciousness wrapper for project listings."""

    def test_projects_list_has_identity(self):
        """Project listing must have identity voice."""
        from services.consciousness.files_consciousness import format_projects_conscious

        projects = [
            {"name": "piper-morgan", "active": True},
            {"name": "side-project", "active": False},
        ]
        output = format_projects_conscious(projects)
        assert "I" in output or "I'" in output, "Should have identity"

    def test_projects_list_has_invitation(self):
        """Project listing must have dialogue invitation."""
        from services.consciousness.files_consciousness import format_projects_conscious

        projects = [{"name": "project1", "active": True}]
        output = format_projects_conscious(projects)
        assert "?" in output, "Should have invitation"

    def test_projects_highlights_active(self):
        """Active project should be emphasized."""
        from services.consciousness.files_consciousness import format_projects_conscious

        projects = [
            {"name": "active-one", "active": True},
            {"name": "inactive", "active": False},
        ]
        output = format_projects_conscious(projects)
        assert "active-one" in output

    def test_no_projects_has_identity(self):
        """No projects message should have identity."""
        from services.consciousness.files_consciousness import format_projects_conscious

        output = format_projects_conscious([])
        assert "I" in output or "I'" in output


class TestMVCCompliance:
    """Test MVC (Minimum Viable Consciousness) compliance."""

    def test_projects_passes_mvc(self):
        """Project listing should pass MVC validation."""
        from services.consciousness.files_consciousness import format_projects_conscious
        from services.consciousness.validation import validate_mvc

        projects = [{"name": "test-project", "active": True}]
        output = format_projects_conscious(projects)
        result = validate_mvc(output)
        # At minimum, should have identity and invitation
        assert result.checks["identity"], f"Missing identity in: {output}"
        assert result.checks["invitation"], f"Missing invitation in: {output}"
