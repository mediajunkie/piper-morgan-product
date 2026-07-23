"""
PM-056 Schema Validator Tool Tests
Comprehensive testing of domain/database schema consistency validation
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.check_domain_db_consistency import FieldInfo, ModelComparison, SchemaValidator


class TestSchemaValidator:
    """Test the schema validator functionality"""

    @pytest.fixture
    def validator(self):
        """Provide SchemaValidator instance for tests"""
        return SchemaValidator()

    def test_extract_domain_fields(self, validator):
        """Test extraction of fields from domain dataclasses"""
        # Mock a domain dataclass
        from dataclasses import dataclass

        from typing import Optional

        @dataclass
        class TestDomainModel:
            id: str
            name: str
            description: str
            # #1452: the validator derives nullability from the TYPE — a bare
            # `str = None` is a typing lie and correctly reads non-nullable.
            optional_field: Optional[str] = None

        fields = validator.extract_domain_fields(TestDomainModel)

        # Verify field extraction
        assert "id" in fields
        assert "name" in fields
        assert "description" in fields
        assert "optional_field" in fields

        # Check field info
        assert fields["id"].type == "str"
        assert fields["name"].type == "str"
        assert fields["optional_field"].nullable is True

    def test_extract_database_fields(self, validator):
        """Test extraction of fields from SQLAlchemy models"""
        # Mock SQLAlchemy model
        from sqlalchemy import Boolean, Column, Integer, String
        from sqlalchemy.ext.declarative import declarative_base

        Base = declarative_base()

        class TestDBModel(Base):
            __tablename__ = "test_table"

            id = Column(String, primary_key=True)
            name = Column(String, nullable=False)
            count = Column(Integer, nullable=True)
            active = Column(Boolean, default=True)

        fields = validator.extract_database_fields(TestDBModel)

        # Verify field extraction
        assert "id" in fields
        assert "name" in fields
        assert "count" in fields
        assert "active" in fields

        # Check field info
        assert fields["id"].type == "str"
        assert fields["id"].is_primary_key is True
        assert fields["name"].type == "str"
        assert fields["name"].nullable is False
        assert fields["count"].type == "int"
        assert fields["count"].nullable is True

    def test_compare_models_matching(self, validator):
        """Test model comparison with matching fields"""
        # Mock domain model
        from dataclasses import dataclass

        @dataclass
        class TestDomain:
            id: str
            name: str
            description: str

        # Mock database model
        from sqlalchemy import Column, String
        from sqlalchemy.ext.declarative import declarative_base

        Base = declarative_base()

        class TestDB(Base):
            __tablename__ = "test_table"
            id = Column(String, primary_key=True)
            name = Column(String, nullable=False)
            description = Column(String, nullable=True)

        # Mock the validator's model storage
        validator.domain_models["TestDomain"] = TestDomain
        validator.database_models["TestDB"] = TestDB

        comparison = validator.compare_models("TestDomain", "TestDB")

        # Verify comparison
        assert comparison.domain_model == "TestDomain"
        assert comparison.database_model == "TestDB"
        assert "id" in comparison.matching_fields
        assert "name" in comparison.matching_fields
        assert "description" in comparison.matching_fields
        assert len(comparison.matching_fields) == 3
        assert len(comparison.missing_in_domain) == 0
        assert len(comparison.missing_in_database) == 0
        assert len(comparison.type_mismatches) == 0

    def test_compare_models_missing_fields(self, validator):
        """Test model comparison with missing fields"""
        # Mock domain model with fewer fields
        from dataclasses import dataclass

        @dataclass
        class TestDomain:
            id: str
            name: str

        # Mock database model with more fields
        from sqlalchemy import Column, Integer, String
        from sqlalchemy.ext.declarative import declarative_base

        Base = declarative_base()

        class TestDB(Base):
            __tablename__ = "test_table"
            id = Column(String, primary_key=True)
            name = Column(String, nullable=False)
            description = Column(String, nullable=True)
            count = Column(Integer, nullable=True)

        # Mock the validator's model storage
        validator.domain_models["TestDomain"] = TestDomain
        validator.database_models["TestDB"] = TestDB

        comparison = validator.compare_models("TestDomain", "TestDB")

        # Verify comparison
        assert "id" in comparison.matching_fields
        assert "name" in comparison.matching_fields
        assert "description" in comparison.missing_in_domain
        assert "count" in comparison.missing_in_domain
        assert len(comparison.missing_in_database) == 0

    def test_compare_models_type_mismatches(self, validator):
        """Test model comparison with type mismatches"""
        # Mock domain model
        from dataclasses import dataclass

        @dataclass
        class TestDomain:
            id: str
            count: int
            name: str

        # Mock database model with different types
        from sqlalchemy import Column, Float, Integer, String
        from sqlalchemy.ext.declarative import declarative_base

        Base = declarative_base()

        class TestDB(Base):
            __tablename__ = "test_table"
            id = Column(String, primary_key=True)
            count = Column(Float, nullable=True)  # Different type
            name = Column(String, nullable=False)

        # Mock the validator's model storage
        validator.domain_models["TestDomain"] = TestDomain
        validator.database_models["TestDB"] = TestDB

        comparison = validator.compare_models("TestDomain", "TestDB")

        # Verify type mismatches
        assert len(comparison.type_mismatches) == 1
        mismatch = comparison.type_mismatches[0]
        assert mismatch["field_name"] == "count"
        assert mismatch["domain_type"] == "int"
        assert mismatch["database_type"] == "float"

    def test_check_specific_issues(self, validator):
        """Test checking for specific known issues"""
        # Mock comparison with object_id vs object_position issue
        from dataclasses import dataclass

        @dataclass
        class TestDomain:
            id: str
            object_id: str  # Domain has object_id

        from sqlalchemy import Column, String
        from sqlalchemy.ext.declarative import declarative_base

        Base = declarative_base()

        class TestDB(Base):
            __tablename__ = "test_table"
            id = Column(String, primary_key=True)
            object_position = Column(String, nullable=True)  # DB has object_position

        # Mock the validator's model storage
        validator.domain_models["TestDomain"] = TestDomain
        validator.database_models["TestDB"] = TestDB

        # Create comparison
        comparison = validator.compare_models("TestDomain", "TestDB")
        validator.comparisons.append(comparison)

        # Check for specific issues
        validator.check_specific_issues()

        # Verify error was detected
        assert len(validator.errors) == 1
        assert "object_id vs object_position" in validator.errors[0]

    def test_generate_report(self, validator):
        """Test report generation"""
        # Mock some comparisons
        comparison1 = ModelComparison(
            domain_model="Test1",
            database_model="TestDB1",
            matching_fields=["id", "name"],
            missing_in_domain=["description"],
            missing_in_database=[],
            type_mismatches=[],
            field_count_domain=2,
            field_count_database=3,
        )

        comparison2 = ModelComparison(
            domain_model="Test2",
            database_model="TestDB2",
            matching_fields=["id"],
            missing_in_domain=[],
            missing_in_database=["extra_field"],
            type_mismatches=[
                {"field_name": "count", "domain_type": "int", "database_type": "float"}
            ],
            field_count_domain=1,
            field_count_database=2,
        )

        validator.comparisons = [comparison1, comparison2]
        validator.errors = ["Test error"]
        validator.warnings = ["Test warning"]

        report = validator.generate_report()

        # Verify report structure
        assert "PM-056 Schema Validation Report" in report
        assert "Total model comparisons: 2" in report
        assert "Test error" in report
        assert "Test warning" in report
        assert "Test1 vs TestDB1" in report
        assert "Test2 vs TestDB2" in report

    def test_load_domain_models(self, validator):
        """Test loading domain models.

        #1452: sys is a singleton — patching tools....sys.modules swaps the
        REAL sys.modules process-wide, and any dataclass defined inside the
        patch window resolves its annotations against the fake module
        (AttributeError: KW_ONLY). Define classes first; patch only around
        the loader call.
        """
        import types
        from dataclasses import dataclass
        from unittest.mock import patch as _patch

        @dataclass
        class TestDomain1:
            id: str

        @dataclass
        class TestDomain2:
            name: str

        class NotADataclass:
            pass

        fake = types.ModuleType("fake_domain_models")
        for _name, _obj in {
            "TestDomain1": TestDomain1,
            "TestDomain2": TestDomain2,
            "NotADataclass": NotADataclass,
            "FieldInfo": Mock(),  # Should be excluded
            "ModelComparison": Mock(),  # Should be excluded
        }.items():
            setattr(fake, _name, _obj)

        with _patch.dict(
            "sys.modules", {"services.domain.models": fake}
        ):
            validator.load_domain_models()

        # Verify domain models loaded
        assert "TestDomain1" in validator.domain_models
        assert "TestDomain2" in validator.domain_models
        assert "NotADataclass" not in validator.domain_models
        assert "FieldInfo" not in validator.domain_models
        assert "ModelComparison" not in validator.domain_models


    def test_load_database_models(self, validator):
        """Test loading database models (#1452: patch.dict on the real
        sys.modules, classes defined outside the patch window — see above)."""
        import types
        from unittest.mock import patch as _patch

        from sqlalchemy import Column, String
        from sqlalchemy.ext.declarative import declarative_base

        Base = declarative_base()

        class TestDB1(Base):
            __tablename__ = "test1"
            id = Column(String, primary_key=True)

        class TestDB2(Base):
            __tablename__ = "test2"
            id = Column(String, primary_key=True)

        class NotAModel:
            pass

        fake = types.ModuleType("fake_db_models")
        for _name, _obj in {
            "TestDB1": TestDB1,
            "TestDB2": TestDB2,
            "NotAModel": NotAModel,
            "Base": Mock(),  # Should be excluded
            "TimestampMixin": Mock(),  # Should be excluded
        }.items():
            setattr(fake, _name, _obj)

        with _patch.dict(
            "sys.modules", {"services.database.models": fake}
        ):
            validator.load_database_models()

        # Verify database models loaded
        assert "TestDB1" in validator.database_models
        assert "TestDB2" in validator.database_models
        assert "NotAModel" not in validator.database_models
        assert "Base" not in validator.database_models
        assert "TimestampMixin" not in validator.database_models


class TestFieldInfo:
    """Test FieldInfo dataclass"""

    def test_field_info_creation(self):
        """Test creating FieldInfo instances"""
        field = FieldInfo(
            name="test_field",
            type="str",
            nullable=True,
            default="default_value",
            is_primary_key=False,
            is_foreign_key=False,
        )

        assert field.name == "test_field"
        assert field.type == "str"
        assert field.nullable is True
        assert field.default == "default_value"
        assert field.is_primary_key is False
        assert field.is_foreign_key is False


class TestModelComparison:
    """Test ModelComparison dataclass"""

    def test_model_comparison_creation(self):
        """Test creating ModelComparison instances"""
        comparison = ModelComparison(
            domain_model="TestDomain",
            database_model="TestDB",
            matching_fields=["id", "name"],
            missing_in_domain=["description"],
            missing_in_database=["extra_field"],
            type_mismatches=[
                {"field_name": "count", "domain_type": "int", "database_type": "float"}
            ],
            field_count_domain=2,
            field_count_database=3,
        )

        assert comparison.domain_model == "TestDomain"
        assert comparison.database_model == "TestDB"
        assert comparison.matching_fields == ["id", "name"]
        assert comparison.missing_in_domain == ["description"]
        assert comparison.missing_in_database == ["extra_field"]
        assert len(comparison.type_mismatches) == 1
        assert comparison.field_count_domain == 2
        assert comparison.field_count_database == 3
