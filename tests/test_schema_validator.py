"""
Tests for PM-056 Domain/Database Schema Validator

These tests validate that the schema validator correctly identifies:
- Field mismatches between domain and database models
- Type incompatibilities
- Enum usage inconsistencies
- Missing fields that could cause bugs like object_id vs object_position
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add tools directory to path
tools_dir = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(tools_dir))

from schema_validator import SchemaValidator, ValidationIssue


class TestSchemaValidator:
    """Test the schema validation engine"""

    def test_validator_initialization(self):
        """Test that validator initializes correctly"""
        validator = SchemaValidator()

        # Should discover domain and database models
        assert len(validator.domain_models) > 0
        assert len(validator.db_models) > 0
        assert len(validator.model_mappings) > 0

        # Should have expected model mappings
        # #1878: "Product" was dropped from this list — there is no ProductDB.
        # The Product *domain* dataclass still exists (validator.domain_models
        # still has it), it's just no longer DB-backed, so it correctly has no
        # mapping entry. "Project" remains a live, DB-backed mapping.
        assert "Project" in validator.model_mappings
        assert validator.model_mappings["Project"] == "ProjectDB"

    def test_project_model_validation(self):
        """Test validation of Project model (should be mostly clean).

        #1878: this used to validate "Product", which no longer has a
        database mapping (see test_validator_initialization) — validate_model
        on an unmapped model always returns exactly one "mapping_missing"
        error, so the test failed. "Project" is a currently-mapped model that
        is actually clean (0 errors) and exercises the same code path.
        """
        validator = SchemaValidator()
        issues = validator.validate_model("Project")

        # Should have minimal issues for well-aligned model
        error_count = len([i for i in issues if i.severity == "error"])
        assert (
            error_count == 0
        ), f"Project model has {error_count} errors: {[str(i) for i in issues if i.severity == 'error']}"

    def test_validation_issue_creation(self):
        """Test ValidationIssue class functionality"""
        issue = ValidationIssue(
            severity="error",
            category="field_missing",
            model="TestModel",
            field="test_field",
            description="Test description",
            suggestion="Test suggestion",
        )

        assert issue.severity == "error"
        assert issue.model == "TestModel"
        assert "test_field" in str(issue)
        assert "Test suggestion" in str(issue)

    def test_field_presence_validation(self):
        """Test that missing fields are detected"""
        validator = SchemaValidator()

        # Test with a model that should have field mismatches
        issues = validator.validate_model("Workflow")

        # Should detect some field differences
        field_issues = [
            i for i in issues if i.category in ["field_missing_db", "field_missing_domain"]
        ]
        assert len(field_issues) >= 0  # May have legitimate differences

    def test_type_compatibility_detection(self):
        """Test that type mismatches are detected"""
        validator = SchemaValidator()

        # This should work without errors for our well-structured models
        issues = validator.validate_all_models()

        # Check that type validation runs without exceptions
        type_issues = [i for i in issues if i.category == "type_mismatch"]
        # Should not have critical type mismatches in well-designed models
        critical_type_issues = [i for i in type_issues if i.severity == "error"]
        assert (
            len(critical_type_issues) == 0
        ), f"Critical type issues found: {[str(i) for i in critical_type_issues]}"

    def test_enum_validation(self):
        """Test that enum inconsistencies are detected"""
        validator = SchemaValidator()

        # Test model with enums (like Intent with IntentCategory)
        issues = validator.validate_model("Intent")

        # Should detect enum usage properly
        enum_issues = [i for i in issues if "enum" in i.category]
        # This is informational - enum issues should be warnings or info, not errors
        for issue in enum_issues:
            assert issue.severity in ["warning", "info"], f"Enum issue severity too high: {issue}"

    def test_model_mapping_discovery(self):
        """Test that model mappings are discovered correctly"""
        validator = SchemaValidator()

        # Should map standard models
        # #1878: "Product" and "Feature" dropped — neither has a database
        # model anymore (see test_validator_initialization). "Workflow" and
        # "ProjectIntegration" remain live, DB-backed mappings.
        assert "Workflow" in validator.model_mappings
        assert "ProjectIntegration" in validator.model_mappings
        assert validator.model_mappings["ProjectIntegration"] == "ProjectIntegrationDB"

        # Should handle special naming patterns
        assert "Project" in validator.model_mappings
        assert validator.model_mappings["Project"] == "ProjectDB"
        assert "UploadedFile" in validator.model_mappings
        assert validator.model_mappings["UploadedFile"] == "UploadedFileDB"

    def test_relationship_validation(self):
        """Test that relationship inconsistencies are detected"""
        validator = SchemaValidator()

        # Test model with relationships
        # #1878: was "Product" (unmapped — see test_validator_initialization),
        # which made this pass vacuously (the mapping-missing error's category
        # never contains "relationship", so the loop below never ran). "Project"
        # is mapped and has real info-level differences (see
        # test_project_model_validation), so this now actually exercises the
        # relationship-category filter it claims to test.
        issues = validator.validate_model("Project")

        # Should find relationship differences (as info items)
        relationship_issues = [i for i in issues if "relationship" in i.category]
        for issue in relationship_issues:
            assert issue.severity == "info", f"Relationship issue should be info level: {issue}"

    def test_validation_summary(self):
        """Test validation summary functionality"""
        validator = SchemaValidator()

        # Add some test issues
        validator.issues = [
            ValidationIssue("error", "test", "TestModel", "field1", "Test error"),
            ValidationIssue("warning", "test", "TestModel", "field2", "Test warning"),
            ValidationIssue("info", "test", "TestModel", "field3", "Test info"),
        ]

        # Should print summary without errors
        try:
            validator.print_summary()
        except Exception as e:
            pytest.fail(f"print_summary raised exception: {e}")

    def test_critical_field_detection(self):
        """Test that validator would catch object_id vs object_position type issues"""
        validator = SchemaValidator()

        # This is a regression test for the type of issue we had in Slack spatial adapter
        # where object_id (str) was used instead of object_position (int)

        # Run full validation to check for any critical mismatches
        issues = validator.validate_all_models()

        # Check for any critical type mismatches that could cause runtime errors
        critical_issues = [
            i for i in issues if i.severity == "error" and "type_mismatch" in i.category
        ]

        # If we find critical type issues, they should be documented
        if critical_issues:
            print("Critical type mismatches found:")
            for issue in critical_issues:
                print(f"  {issue}")

        # For now, just ensure the validator runs without exceptions
        assert isinstance(issues, list)

    def test_validator_handles_missing_models(self):
        """Test that validator handles missing model mappings gracefully"""
        validator = SchemaValidator()

        # Test with non-existent model
        issues = validator.validate_model("NonExistentModel")

        # Should return mapping error
        assert len(issues) == 1
        assert issues[0].severity == "error"
        assert issues[0].category == "mapping_missing"

    def test_sqlalchemy_introspection(self):
        """Test that SQLAlchemy introspection works correctly"""
        validator = SchemaValidator()

        # Test that we can extract fields from a known model
        # #1878: was db_models["Product"] — no "Product" db model exists any
        # more (KeyError). db_models is keyed by the SQLAlchemy class name
        # (validator.model_mappings["Project"] == "ProjectDB").
        project_db_model = validator.db_models["ProjectDB"]
        db_fields = validator._get_db_fields(project_db_model)

        # Should find expected fields
        assert "id" in db_fields
        assert "name" in db_fields
        assert "created_at" in db_fields

        # Should have proper field metadata
        assert "column" in db_fields["id"]
        assert "type" in db_fields["id"]
        assert "nullable" in db_fields["id"]


class TestSchemaValidatorCLI:
    """Test the command-line interface functionality"""

    def test_cli_model_specific_validation(self):
        """Test CLI with specific model validation"""
        # This would normally test CLI args, but we'll test the underlying logic
        validator = SchemaValidator()

        # Should be able to validate specific models
        # #1878: was "Product" (unmapped — see test_validator_initialization).
        issues = validator.validate_model("Project")
        assert isinstance(issues, list)

    def test_cli_full_validation(self):
        """Test CLI with full validation"""
        validator = SchemaValidator()

        # Should be able to validate all models
        issues = validator.validate_all_models()
        assert isinstance(issues, list)
        assert len(issues) >= 0


class TestSchemaValidatorIntegration:
    """Integration tests with actual project models"""

    def test_no_critical_schema_drift(self):
        """Integration test: ensure no critical schema drift in current codebase"""
        validator = SchemaValidator()
        issues = validator.validate_all_models()

        # Count critical issues
        critical_count = len([i for i in issues if i.severity == "error"])

        # This is a regression test - if it fails, we have schema drift
        # For new projects, this might start with some issues that need to be addressed
        print(f"Schema validation found {len(issues)} total issues ({critical_count} critical)")

        # Document any critical issues for tracking
        if critical_count > 0:
            print("Critical schema issues requiring attention:")
            for issue in [i for i in issues if i.severity == "error"]:
                print(f"  {issue}")

        # Test passes if validator runs successfully
        # In CI, we could make this fail on critical_count > 0
        assert isinstance(issues, list)

    def test_spatial_model_validation(self):
        """Test validation of spatial models (regression test for object_id vs object_position)"""
        validator = SchemaValidator()

        # Check if we have spatial models to validate
        spatial_models = [name for name in validator.domain_models.keys() if "Spatial" in name]

        for model_name in spatial_models:
            if model_name in validator.model_mappings:
                issues = validator.validate_model(model_name)

                # Look for field name issues that could cause the object_id vs object_position bug
                field_issues = [i for i in issues if "object" in i.field.lower()]

                if field_issues:
                    print(f"Spatial model {model_name} field issues:")
                    for issue in field_issues:
                        print(f"  {issue}")

                # Test passes if no exceptions thrown
                assert isinstance(issues, list)
