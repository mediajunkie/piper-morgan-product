#!/usr/bin/env python3
"""
PM-056 Schema Validator Tool
Automated domain/database schema consistency validator

Compares SQLAlchemy models with domain dataclasses to prevent drift bugs.
Catches issues like object_id vs object_position type mismatches.
"""

import ast
import inspect
import sys
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Type, Union

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeMeta

from services.database.models import Base
from services.domain.models import (
    BoundaryViolation,
    EthicalDecision,
    Feature,
    Intent,
    Product,
    Project,
    ProjectIntegration,
    Stakeholder,
    Task,
    UploadedFile,
    Workflow,
    WorkItem,
)


@dataclass
class FieldInfo:
    """Information about a field in a model"""

    name: str
    type: str
    nullable: bool = False
    default: Optional[Any] = None
    is_primary_key: bool = False
    is_foreign_key: bool = False


@dataclass
class ModelComparison:
    """Comparison result between domain and database models"""

    domain_model: str
    database_model: str
    matching_fields: List[str]
    missing_in_domain: List[str]
    missing_in_database: List[str]
    type_mismatches: List[Dict[str, Any]]
    field_count_domain: int
    field_count_database: int


class SchemaValidator:
    """Validates consistency between domain and database models"""

    def __init__(self):
        self.domain_models = {}
        self.database_models = {}
        self.comparisons = []
        self.errors = []
        self.warnings = []

    def load_domain_models(self) -> None:
        """Load domain models from services.domain.models"""
        domain_module = sys.modules["services.domain.models"]

        for name, obj in inspect.getmembers(domain_module):
            if (
                inspect.isclass(obj)
                and hasattr(obj, "__dataclass_fields__")
                and name not in ["FieldInfo", "ModelComparison"]
            ):
                self.domain_models[name] = obj
                print(f"📋 Loaded domain model: {name}")

    def load_database_models(self) -> None:
        """Load database models from services.database.models"""
        db_module = sys.modules["services.database.models"]

        for name, obj in inspect.getmembers(db_module):
            if (
                inspect.isclass(obj)
                and hasattr(obj, "__tablename__")
                and name not in ["Base", "TimestampMixin"]
            ):
                self.database_models[name] = obj
                print(f"🗄️  Loaded database model: {name}")

    def extract_domain_fields(self, model_class: Type) -> Dict[str, FieldInfo]:
        """Extract field information from a domain dataclass"""
        fields_info = {}

        for field in fields(model_class):
            field_type = self._get_type_name(field.type)

            fields_info[field.name] = FieldInfo(
                name=field.name,
                type=field_type,
                nullable=self._is_optional_type(field.type),
                default=field.default if field.default is not inspect._empty else None,
                is_primary_key=False,  # Domain models don't have primary keys
                is_foreign_key=False,
            )

        return fields_info

    def extract_database_fields(self, model_class: Type) -> Dict[str, FieldInfo]:
        """Extract field information from a SQLAlchemy model"""
        fields_info = {}

        for column_name, column in model_class.__table__.columns.items():
            field_type = self._get_sqlalchemy_type_name(column.type)

            fields_info[column_name] = FieldInfo(
                name=column_name,
                type=field_type,
                nullable=column.nullable,
                default=column.default.arg if column.default else None,
                is_primary_key=column.primary_key,
                is_foreign_key=column.foreign_keys is not None,
            )

        return fields_info

    def _get_type_name(self, type_obj: Any) -> str:
        """Get type name from a type annotation"""
        if hasattr(type_obj, "__origin__"):
            # Handle generic types like List[str], Optional[str]
            origin = type_obj.__origin__
            args = type_obj.__args__

            if origin is Union and len(args) == 2 and args[1] is type(None):
                # Optional[T] -> T
                return self._get_type_name(args[0])
            elif origin is list:
                # List[T] -> list
                return "list"
            elif origin is dict:
                # Dict[K, V] -> dict
                return "dict"
            else:
                return str(origin.__name__)
        else:
            # Handle ForwardRef and other special cases
            if hasattr(type_obj, "__forward_arg__"):
                # ForwardRef object
                return str(type_obj.__forward_arg__)
            elif hasattr(type_obj, "__name__"):
                return str(type_obj.__name__)
            else:
                # Fallback to string representation
                return str(type_obj)

    def _is_optional_type(self, type_obj: Any) -> bool:
        """Check if a type is Optional (Union with None)"""
        if hasattr(type_obj, "__origin__") and type_obj.__origin__ is Union:
            args = type_obj.__args__
            return len(args) == 2 and args[1] is type(None)
        return False

    def _get_sqlalchemy_type_name(self, column_type: Any) -> str:
        """Get type name from a SQLAlchemy column type"""
        type_name = str(column_type.__class__.__name__).lower()

        # Map SQLAlchemy types to domain types
        type_mapping = {
            "string": "str",
            "text": "str",
            "integer": "int",
            "float": "float",
            "boolean": "bool",
            "datetime": "datetime",
            "json": "dict",
            "enum": "enum",
        }

        return type_mapping.get(type_name, type_name)

    def compare_models(self, domain_name: str, database_name: str) -> ModelComparison:
        """Compare a domain model with a database model"""
        domain_model = self.domain_models.get(domain_name)
        database_model = self.database_models.get(database_name)

        if not domain_model or not database_model:
            return ModelComparison(
                domain_model=domain_name,
                database_model=database_name,
                matching_fields=[],
                missing_in_domain=[],
                missing_in_database=[],
                type_mismatches=[],
                field_count_domain=0,
                field_count_database=0,
            )

        domain_fields = self.extract_domain_fields(domain_model)
        database_fields = self.extract_database_fields(database_model)

        # Find matching fields
        matching_fields = []
        missing_in_domain = []
        missing_in_database = []
        type_mismatches = []

        domain_field_names = set(domain_fields.keys())
        database_field_names = set(database_fields.keys())

        # Find matching fields
        for field_name in domain_field_names.intersection(database_field_names):
            matching_fields.append(field_name)

            # Check for type mismatches
            domain_field = domain_fields[field_name]
            database_field = database_fields[field_name]

            if domain_field.type != database_field.type:
                type_mismatches.append(
                    {
                        "field_name": field_name,
                        "domain_type": domain_field.type,
                        "database_type": database_field.type,
                    }
                )

        # Find missing fields
        missing_in_domain = list(database_field_names - domain_field_names)
        missing_in_database = list(domain_field_names - database_field_names)

        return ModelComparison(
            domain_model=domain_name,
            database_model=database_name,
            matching_fields=matching_fields,
            missing_in_domain=missing_in_domain,
            missing_in_database=missing_in_database,
            type_mismatches=type_mismatches,
            field_count_domain=len(domain_fields),
            field_count_database=len(database_fields),
        )

    def validate_all_models(self) -> bool:
        """Validate all domain/database model pairs"""
        print("\n🔍 Starting schema validation...")

        # Define model mappings
        model_mappings = {
            "WorkItem": "WorkItem",
            "Workflow": "Workflow",
            "Task": "Task",
            "Intent": "Intent",
            "Product": "Product",
            "Feature": "Feature",
            "Stakeholder": "Stakeholder",
            "Project": "ProjectDB",
            "ProjectIntegration": "ProjectIntegrationDB",
            "UploadedFile": "UploadedFileDB",
        }

        all_valid = True

        for domain_name, database_name in model_mappings.items():
            print(f"\n📊 Comparing {domain_name} (domain) vs {database_name} (database)")

            comparison = self.compare_models(domain_name, database_name)
            self.comparisons.append(comparison)

            # Report results
            if comparison.missing_in_domain:
                print(f"  ❌ Missing in domain: {comparison.missing_in_domain}")
                all_valid = False

            if comparison.missing_in_database:
                print(f"  ❌ Missing in database: {comparison.missing_in_database}")
                all_valid = False

            if comparison.type_mismatches:
                print(f"  ⚠️  Type mismatches:")
                for mismatch in comparison.type_mismatches:
                    print(
                        f"    - {mismatch['field_name']}: {mismatch['domain_type']} vs {mismatch['database_type']}"
                    )
                all_valid = False

            if comparison.matching_fields:
                print(f"  ✅ Matching fields: {len(comparison.matching_fields)}")

            print(
                f"  📈 Field counts: Domain={comparison.field_count_domain}, Database={comparison.field_count_database}"
            )

        return all_valid

    def generate_report(self) -> str:
        """Generate a detailed validation report"""
        report = []
        report.append("=" * 60)
        report.append("PM-056 Schema Validation Report")
        report.append("=" * 60)

        total_comparisons = len(self.comparisons)
        valid_comparisons = sum(
            1
            for c in self.comparisons
            if not c.missing_in_domain and not c.missing_in_database and not c.type_mismatches
        )

        report.append(f"\n📊 Summary:")
        report.append(f"  Total model comparisons: {total_comparisons}")
        report.append(f"  Valid comparisons: {valid_comparisons}")
        report.append(f"  Invalid comparisons: {total_comparisons - valid_comparisons}")

        if self.errors:
            report.append(f"\n❌ Errors:")
            for error in self.errors:
                report.append(f"  - {error}")

        if self.warnings:
            report.append(f"\n⚠️  Warnings:")
            for warning in self.warnings:
                report.append(f"  - {warning}")

        report.append(f"\n📋 Detailed Results:")
        for comparison in self.comparisons:
            report.append(f"\n  {comparison.domain_model} vs {comparison.database_model}:")

            if comparison.missing_in_domain:
                report.append(f"    Missing in domain: {comparison.missing_in_domain}")

            if comparison.missing_in_database:
                report.append(f"    Missing in database: {comparison.missing_in_database}")

            if comparison.type_mismatches:
                report.append(f"    Type mismatches:")
                for mismatch in comparison.type_mismatches:
                    report.append(
                        f"      {mismatch['field_name']}: {mismatch['domain_type']} vs {mismatch['database_type']}"
                    )

            report.append(
                f"    Field counts: Domain={comparison.field_count_domain}, Database={comparison.field_count_database}"
            )

        return "\n".join(report)

    def check_specific_issues(self) -> None:
        """Check for specific known issues like object_id vs object_position"""
        print("\n🔍 Checking for specific known issues...")

        # Check for object_id vs object_position issues
        for comparison in self.comparisons:
            domain_fields = set()
            database_fields = set()

            # Get domain fields
            domain_model = self.domain_models.get(comparison.domain_model)
            if domain_model:
                domain_fields = {field.name for field in fields(domain_model)}

            # Get database fields
            database_model = self.database_models.get(comparison.database_model)
            if database_model:
                database_fields = {column.name for column in database_model.__table__.columns}

            # Check for object_id vs object_position
            if "object_id" in domain_fields and "object_position" in database_fields:
                self.errors.append(
                    f"Potential object_id vs object_position mismatch in {comparison.domain_model}"
                )
                print(
                    f"  ❌ Found object_id vs object_position mismatch in {comparison.domain_model}"
                )

            if "object_position" in domain_fields and "object_id" in database_fields:
                self.errors.append(
                    f"Potential object_position vs object_id mismatch in {comparison.domain_model}"
                )
                print(
                    f"  ❌ Found object_position vs object_id mismatch in {comparison.domain_model}"
                )


def main():
    """Main entry point for the schema validator"""
    print("🔧 PM-056 Schema Validator Tool")
    print("=" * 40)

    validator = SchemaValidator()

    try:
        # Load models
        print("\n📥 Loading models...")
        validator.load_domain_models()
        validator.load_database_models()

        # Validate all models
        is_valid = validator.validate_all_models()

        # Check for specific issues
        validator.check_specific_issues()

        # Generate report
        report = validator.generate_report()
        print(f"\n{report}")

        # Exit with appropriate code
        if is_valid and not validator.errors:
            print("\n✅ Schema validation passed!")
            sys.exit(0)
        else:
            print("\n❌ Schema validation failed!")
            sys.exit(1)

    except Exception as e:
        print(f"\n💥 Schema validation error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
