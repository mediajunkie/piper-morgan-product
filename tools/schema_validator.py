#!/usr/bin/env python3
"""
PM-056: Domain/Database Schema Validator (Enhanced with Architectural Awareness)

Automated tool to prevent domain/database model drift by comparing:
- Field names and types between domain models and SQLAlchemy database models
- Enum usage consistency
- Relationship mapping validation
- Type compatibility verification

ENHANCED FEATURES (2025-07-31):
- Architectural awareness through FIELD_MAPPINGS configuration
- Zero false positive guarantee via intelligent field mapping detection
- ARCHITECTURAL_EXCEPTIONS for intentional design decisions
- 100% tool reliability - never cries wolf

This prevents issues like the object_id vs object_position mismatch that caused
Slack debugging complexity in PM-078, while eliminating false positives from
SQLAlchemy reserved name conflicts.

Usage:
    python tools/schema_validator.py                    # Validate all models
    python tools/schema_validator.py --model Product    # Validate specific model
    python tools/schema_validator.py --fix             # Auto-fix simple issues
    python tools/schema_validator.py --ci              # CI mode with exit codes

Configuration:
    FIELD_MAPPINGS: Maps domain fields to different database column names
    ARCHITECTURAL_EXCEPTIONS: Documents intentional architectural decisions
"""

import argparse
import inspect
import sys
import typing
from dataclasses import fields, is_dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, get_args, get_origin, get_type_hints

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import inspect as sql_inspect
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import relationship

import services.database.models as db_models

# Import models
import services.domain.models as domain_models
from services.shared_types import (
    IntegrationType,
    IntentCategory,
    TaskStatus,
    TaskType,
    WorkflowStatus,
    WorkflowType,
)

# ===============================================================================
# ARCHITECTURAL AWARENESS CONFIGURATION
# ===============================================================================

# Field mappings: Domain field -> Database column mappings
# These handle cases where SQLAlchemy reserved names require different column names
FIELD_MAPPINGS = {
    "WorkItem.metadata": "item_metadata",  # metadata is SQLAlchemy reserved
    "UploadedFile.metadata": "file_metadata",  # metadata is SQLAlchemy reserved
}

# Architectural exceptions: Intentional design decisions
# These are fields that appear "missing" but are intentional architectural choices
ARCHITECTURAL_EXCEPTIONS = {
    "Feature.product": "optional_relationship_by_design",
    # MUX additive fields (#433) are in-memory-only by ratified design. The persistence
    # deferral is recorded in docs/internal/architecture/current/artifact-model-design-952.md
    # ("lifecycle_history + mux_ownership are NOT yet DB columns (deferred, mirroring
    # UploadedFileDB dropping metadata)"), restated in the ArtifactDB docstring
    # (services/database/models.py) and in the PM-reviewed #952 closing record.
    # lifecycle_state (the current state) IS persisted; only the transition log is deferred.
    "Feature.lifecycle_history": "mux_lifecycle_history_deferred_952",
    "WorkItem.lifecycle_history": "mux_lifecycle_history_deferred_952",
    "Project.mux_ownership": "mux_ownership_deferred_952",
    "WorkItem.mux_ownership": "mux_ownership_deferred_952",
}

# Domain fields that are persisted through a SQLAlchemy *relationship* rather than a
# column on the model's own table. Key is "DomainModel.domain_field", value is the
# relationship attribute on the database model that carries it.
RELATIONSHIP_MAPPINGS = {
    # Project.repositories round-trips through the project_repository_links association
    # table (#866); ProjectDB.to_domain populates it from self.repository_links.
    "Project.repositories": "repository_links",
}

# Columns that exist on the database model by design and are intentionally absent from the
# pure domain model (services/domain/models.py is documented as "Pure business logic with no
# persistence concerns"). These are persistence/authorization anchors, not schema drift.
PERSISTENCE_ONLY_COLUMNS = {
    # Owner anchor per ADR-071 D2 / #1252 D2 fold; nullable for m-40 grace.
    "ProjectIntegration.owner_id": "owner_anchor_adr_071_d2",
}

# Database column types that legitimately back a domain `str` field. UUID-valued columns
# are carried as strings in the domain layer (e.g. ProjectDB.to_domain does
# `owner_id=self.owner_id or ""`); EncryptedString is a TypeDecorator over a text column.
STR_COMPATIBLE_DB_TYPES = [
    "String",
    "Text",
    "VARCHAR",
    "CHAR",
    "UUID",
    "Uuid",
    "GUID",
    "CrossDialectUUID",
    "EncryptedString",
]


class ValidationIssue:
    """Represents a schema validation issue"""

    def __init__(
        self,
        severity: str,
        category: str,
        model: str,
        field: str,
        description: str,
        suggestion: Optional[str] = None,
    ):
        self.severity = severity  # 'error', 'warning', 'info'
        self.category = category  # 'field_missing', 'type_mismatch', 'enum_inconsistency', etc.
        self.model = model
        self.field = field
        self.description = description
        self.suggestion = suggestion

    def __str__(self) -> str:
        prefix = f"[{self.severity.upper()}] {self.model}.{self.field}"
        result = f"{prefix}: {self.description}"
        if self.suggestion:
            result += f"\n  Suggestion: {self.suggestion}"
        return result


class SchemaValidator:
    """Main schema validation engine"""

    def __init__(self):
        self.issues: List[ValidationIssue] = []
        self._globalns_cache: Optional[Dict[str, Any]] = None
        self._hints_cache: Dict[str, Dict[str, Any]] = {}
        self.domain_models = self._discover_domain_models()
        self.db_models = self._discover_db_models()
        self.model_mappings = self._create_model_mappings()

    def _discover_domain_models(self) -> Dict[str, type]:
        """Discover all domain model dataclasses"""
        models = {}
        for name, obj in inspect.getmembers(domain_models):
            if is_dataclass(obj) and not name.startswith("_"):
                models[name] = obj
        return models

    def _discover_db_models(self) -> Dict[str, type]:
        """Discover all SQLAlchemy database models"""
        models = {}
        for name, obj in inspect.getmembers(db_models):
            if inspect.isclass(obj) and hasattr(obj, "__tablename__") and not name.startswith("_"):
                models[name] = obj
        return models

    def _create_model_mappings(self) -> Dict[str, str]:
        """Create mappings between domain and database models"""
        mappings = {}

        # Direct name mappings
        for domain_name in self.domain_models:
            if domain_name in self.db_models:
                mappings[domain_name] = domain_name

        # Special mapping patterns
        domain_to_db_patterns = {
            "Project": "ProjectDB",
            "ProjectIntegration": "ProjectIntegrationDB",
            "UploadedFile": "UploadedFileDB",
        }

        for domain_name, db_name in domain_to_db_patterns.items():
            if domain_name in self.domain_models and db_name in self.db_models:
                mappings[domain_name] = db_name

        return mappings

    def check_field_mapping(self, model_name: str, field_name: str, db_model: Any) -> bool:
        """Check if domain field maps to different database column"""
        mapping_key = f"{model_name}.{field_name}"
        if mapping_key in FIELD_MAPPINGS:
            mapped_column = FIELD_MAPPINGS[mapping_key]
            return hasattr(db_model, mapped_column)
        return False

    def is_architectural_exception(self, model_name: str, field_name: str) -> Optional[str]:
        """Check if this is an intentional architectural decision"""
        exception_key = f"{model_name}.{field_name}"
        return ARCHITECTURAL_EXCEPTIONS.get(exception_key)

    def validate_all_models(self) -> List[ValidationIssue]:
        """Validate all mapped domain/database model pairs"""
        self.issues.clear()

        for domain_name, db_name in self.model_mappings.items():
            domain_model = self.domain_models[domain_name]
            db_model = self.db_models[db_name]

            self._validate_model_pair(domain_name, domain_model, db_name, db_model)

        return self.issues

    def validate_model(self, model_name: str) -> List[ValidationIssue]:
        """Validate a specific model pair"""
        self.issues.clear()

        if model_name not in self.model_mappings:
            self.issues.append(
                ValidationIssue(
                    "error",
                    "mapping_missing",
                    model_name,
                    "",
                    f"No database model mapping found for domain model '{model_name}'",
                )
            )
            return self.issues

        db_name = self.model_mappings[model_name]
        domain_model = self.domain_models[model_name]
        db_model = self.db_models[db_name]

        self._validate_model_pair(model_name, domain_model, db_name, db_model)
        return self.issues

    def _validate_model_pair(
        self, domain_name: str, domain_model: type, db_name: str, db_model: type
    ):
        """Validate a specific domain/database model pair"""

        # Get field information
        domain_fields = self._get_domain_fields(domain_model)
        db_fields = self._get_db_fields(db_model)
        db_relationships = self._get_db_relationships(db_model)

        # Check field presence
        self._validate_field_presence(domain_name, domain_fields, db_fields, db_relationships)

        # Check field types
        self._validate_field_types(domain_name, domain_fields, db_fields)

        # Check enum consistency
        self._validate_enum_usage(domain_name, domain_fields, db_fields)

        # Check relationship consistency
        self._validate_relationships(domain_name, domain_model, db_model)

    def _domain_globalns(self) -> Dict[str, Any]:
        """Namespace for resolving domain-model annotations.

        services/domain/models.py uses `from __future__ import annotations` (PEP 563), so
        dataclasses.fields(...).type is a *string* for every field. Resolving those strings
        requires the module namespace -- but that module also defines `@dataclass class List`
        (the "Universal List model"), which shadows the `typing.List` imported at the top of
        the same module. Left unhandled, get_type_hints() raises
        "TypeError: type 'List' is not subscriptable" on 24 of 55 domain dataclasses.

        No field in that module is annotated with the bare domain `List` type -- even `class
        List` itself writes `tags: List[str]` meaning typing.List -- so restoring the typing
        names is what every annotation in the module actually intends.
        """
        if self._globalns_cache is None:
            ns = dict(vars(domain_models))
            for typing_name in ("List", "Dict", "Set", "Tuple", "Type", "Union", "Optional", "Any"):
                typing_obj = getattr(typing, typing_name, None)
                if typing_obj is not None:
                    ns[typing_name] = typing_obj
            self._globalns_cache = ns
        return self._globalns_cache

    def _resolve_hints(self, domain_model: type) -> Dict[str, Any]:
        """Resolve a domain dataclass's string annotations to real types.

        Falls back to the raw string annotation for any model that cannot be resolved, so a
        resolution failure degrades to the old (weaker) behaviour instead of crashing.
        """
        key = domain_model.__name__
        if key not in self._hints_cache:
            try:
                self._hints_cache[key] = get_type_hints(
                    domain_model, globalns=self._domain_globalns()
                )
            except Exception:
                self._hints_cache[key] = {}
        return self._hints_cache[key]

    def _get_domain_fields(self, domain_model: type) -> Dict[str, Any]:
        """Extract field information from domain model"""
        if not is_dataclass(domain_model):
            return {}

        hints = self._resolve_hints(domain_model)

        domain_fields = {}
        for field in fields(domain_model):
            domain_fields[field.name] = {
                # Resolved type when available; raw annotation string otherwise.
                "type": hints.get(field.name, field.type),
                "default": field.default,
                "default_factory": field.default_factory,
            }
        return domain_fields

    def _get_db_fields(self, db_model: type) -> Dict[str, Any]:
        """Extract field information from SQLAlchemy model"""
        db_fields = {}

        # Use SQLAlchemy's mapper to get actual columns
        try:
            from sqlalchemy.inspection import inspect as sqla_inspect

            mapper = sqla_inspect(db_model)

            # Get all columns from the mapped table
            for column in mapper.columns:
                db_fields[column.name] = {
                    "column": column,
                    "type": column.type,
                    "nullable": column.nullable,
                    "default": column.default,
                    "primary_key": column.primary_key,
                }
        except Exception:
            # Fallback to manual inspection
            for attr_name in dir(db_model):
                attr = getattr(db_model, attr_name)
                if isinstance(attr, Column):
                    db_fields[attr_name] = {
                        "column": attr,
                        "type": attr.type,
                        "nullable": attr.nullable,
                        "default": attr.default,
                        "primary_key": attr.primary_key,
                    }

        return db_fields

    def _get_db_relationships(self, db_model: type) -> Set[str]:
        """Names of SQLAlchemy relationship attributes on a database model.

        A domain field can be persisted through a relationship (association table) rather
        than a column on the model's own table; mapper.columns does not see those.
        """
        relationships: Set[str] = set()
        try:
            from sqlalchemy.inspection import inspect as sqla_inspect

            for rel in sqla_inspect(db_model).relationships:
                relationships.add(rel.key)
        except Exception:
            pass
        return relationships

    def _validate_field_presence(
        self,
        model_name: str,
        domain_fields: Dict[str, Any],
        db_fields: Dict[str, Any],
        db_relationships: Optional[Set[str]] = None,
    ):
        """Validate that fields exist in both models"""

        db_relationships = db_relationships or set()

        domain_field_names = set(domain_fields.keys())
        db_field_names = set(db_fields.keys())

        # Skip automatic/relationship fields
        skip_fields = {
            "features",
            "stakeholders",
            "metrics",
            "dependencies",
            "risks",
            "tasks",
            "integrations",
            "intent",
            "workflow",
            "product",
            "feature",
            "work_items",
            "project",
        }

        domain_field_names -= skip_fields
        db_field_names -= skip_fields

        # Fields missing in database model (with architectural awareness)
        missing_in_db = domain_field_names - db_field_names
        for field_name in missing_in_db:
            # Check if field maps to different database column
            if self.check_field_mapping(
                model_name, field_name, self.db_models[self.model_mappings[model_name]]
            ):
                # Field is correctly mapped - no issue
                continue

            # Check if the field is persisted through a relationship rather than a column
            rel_name = RELATIONSHIP_MAPPINGS.get(f"{model_name}.{field_name}", field_name)
            if rel_name in db_relationships:
                # Relationship-backed field - persisted, just not as a column on this table
                continue

            # Check if this is an intentional architectural exception
            exception_reason = self.is_architectural_exception(model_name, field_name)
            if exception_reason:
                # Report as INFO instead of ERROR
                self.issues.append(
                    ValidationIssue(
                        "info",
                        "architectural_choice",
                        model_name,
                        field_name,
                        f"Field '{field_name}' intentionally differs between domain and database models",
                        f"Architectural decision: {exception_reason}",
                    )
                )
            else:
                # Genuine missing field - report as error
                self.issues.append(
                    ValidationIssue(
                        "error",
                        "field_missing_db",
                        model_name,
                        field_name,
                        f"Field '{field_name}' exists in domain model but not in database model",
                        f"Add Column('{field_name}', ...) to {model_name} database model",
                    )
                )

        # Fields missing in domain model
        missing_in_domain = db_field_names - domain_field_names
        for field_name in missing_in_domain:
            # Persistence/authorization anchors are intentionally absent from the pure
            # domain layer. Reported as INFO so the decision stays visible without failing.
            persistence_reason = PERSISTENCE_ONLY_COLUMNS.get(f"{model_name}.{field_name}")
            if persistence_reason:
                self.issues.append(
                    ValidationIssue(
                        "info",
                        "persistence_only_column",
                        model_name,
                        field_name,
                        f"Column '{field_name}' is a persistence-layer concern, intentionally "
                        f"absent from the domain model",
                        f"Architectural decision: {persistence_reason}",
                    )
                )
                continue

            self.issues.append(
                ValidationIssue(
                    "warning",
                    "field_missing_domain",
                    model_name,
                    field_name,
                    f"Field '{field_name}' exists in database model but not in domain model",
                    f"Add '{field_name}' field to {model_name} domain model",
                )
            )

    def _validate_field_types(
        self, model_name: str, domain_fields: Dict[str, Any], db_fields: Dict[str, Any]
    ):
        """Validate field type compatibility"""

        # Common field type mappings
        type_mappings = {
            str: STR_COMPATIBLE_DB_TYPES,
            int: ["Integer", "INTEGER"],
            float: ["Float", "FLOAT", "REAL"],
            bool: ["Boolean", "BOOLEAN"],
            datetime: ["DateTime", "DATETIME"],
            dict: ["JSON"],
            list: ["JSON", "ARRAY"],  # ARRAY is valid for list types (e.g., embedding vectors)
        }

        common_fields = set(domain_fields.keys()) & set(db_fields.keys())

        for field_name in common_fields:
            domain_type = domain_fields[field_name]["type"]
            db_column = db_fields[field_name]["column"]
            db_type_name = type(db_column.type).__name__

            # Handle Optional types (Union[T, None])
            origin = get_origin(domain_type)
            if origin is not None:
                args = get_args(domain_type)
                if len(args) == 2 and any(arg is type(None) for arg in args):
                    # This is Optional[T] which is Union[T, None]
                    domain_type = next((arg for arg in args if arg is not type(None)), domain_type)

            # Reduce a remaining generic (List[str], Dict[str, Any], ...) to its origin so it
            # can be matched against type_mappings. Without this the check silently skips
            # every container-typed field.
            origin = get_origin(domain_type)
            if origin is not None:
                domain_type = origin

            # Enum-typed fields are the job of _validate_enum_usage, not the scalar check.
            if isinstance(domain_type, type) and issubclass(domain_type, Enum):
                continue

            # Check type compatibility
            if isinstance(domain_type, type) and domain_type in type_mappings:
                expected_db_types = type_mappings[domain_type]
                if db_type_name not in expected_db_types:
                    self.issues.append(
                        ValidationIssue(
                            "error",
                            "type_mismatch",
                            model_name,
                            field_name,
                            f"Type mismatch: domain expects {domain_type.__name__}, "
                            f"database has {db_type_name}",
                            f"Change database column to one of: {expected_db_types}",
                        )
                    )

    def _validate_enum_usage(
        self, model_name: str, domain_fields: Dict[str, Any], db_fields: Dict[str, Any]
    ):
        """Validate consistent enum usage"""

        common_fields = set(domain_fields.keys()) & set(db_fields.keys())

        for field_name in common_fields:
            domain_type = domain_fields[field_name]["type"]
            db_column = db_fields[field_name]["column"]

            # Unwrap Optional[Enum] -- enum-valued columns are routinely nullable.
            if get_origin(domain_type) is not None:
                args = get_args(domain_type)
                if len(args) == 2 and any(arg is type(None) for arg in args):
                    domain_type = next((arg for arg in args if arg is not type(None)), domain_type)

            domain_is_enum = isinstance(domain_type, type) and issubclass(domain_type, Enum)
            db_enum_class = getattr(db_column.type, "enum_class", None)
            db_type_name = type(db_column.type).__name__

            # Check if domain uses enum but database doesn't
            if domain_is_enum and db_enum_class is None:
                if db_type_name in ("String", "Text", "VARCHAR", "CHAR"):
                    # Deliberate pattern in this codebase: store the enum's value as a string
                    # and convert at the persistence boundary (e.g. ProjectDB.to_domain does
                    # `LifecycleState(self.lifecycle_state)`). Avoids DB-level enum migrations
                    # and keeps models SQLite-testable. Informational, not drift.
                    self.issues.append(
                        ValidationIssue(
                            "info",
                            "enum_stored_as_string",
                            model_name,
                            field_name,
                            f"Domain enum {domain_type.__name__} is persisted as "
                            f"{db_type_name}; conversion handled at the converter boundary",
                            "No action needed unless the converter stops coercing the value",
                        )
                    )
                else:
                    self.issues.append(
                        ValidationIssue(
                            "error",
                            "enum_missing_db",
                            model_name,
                            field_name,
                            f"Domain model uses enum {domain_type.__name__} but database uses {db_type_name}",
                            f"Change database column to Enum({domain_type.__name__})",
                        )
                    )

            # Check if database uses enum but domain doesn't
            if db_enum_class is not None and not domain_is_enum:
                self.issues.append(
                    ValidationIssue(
                        "warning",
                        "enum_missing_domain",
                        model_name,
                        field_name,
                        f"Database uses enum but domain model uses {domain_type}",
                        f"Change domain field to use {db_enum_class.__name__} enum",
                    )
                )

            # Both are enums but not the same one -- a genuine mismatch the old code missed.
            if domain_is_enum and db_enum_class is not None and db_enum_class is not domain_type:
                self.issues.append(
                    ValidationIssue(
                        "error",
                        "enum_class_mismatch",
                        model_name,
                        field_name,
                        f"Domain uses enum {domain_type.__name__} but database column uses "
                        f"{db_enum_class.__name__}",
                        "Align the two enum classes",
                    )
                )

    def _validate_relationships(self, model_name: str, domain_model: type, db_model: type):
        """Validate relationship consistency between models"""

        # Get relationships from SQLAlchemy model
        db_relationships = {}
        for attr_name in dir(db_model):
            attr = getattr(db_model, attr_name)
            if hasattr(attr, "property") and hasattr(attr.property, "mapper"):
                db_relationships[attr_name] = attr

        # Check if domain model has corresponding fields for relationships
        if is_dataclass(domain_model):
            domain_field_names = {field.name for field in fields(domain_model)}

            # Relationships that already back a domain field are not "missing" -- reporting
            # them would double-report the same fact from the other direction.
            rel_backed = {
                RELATIONSHIP_MAPPINGS[key]
                for key in RELATIONSHIP_MAPPINGS
                if key.split(".", 1)[0] == model_name
            }

            for rel_name in db_relationships:
                if rel_name not in domain_field_names and rel_name not in rel_backed:
                    self.issues.append(
                        ValidationIssue(
                            "info",
                            "relationship_missing_domain",
                            model_name,
                            rel_name,
                            f"Database has relationship '{rel_name}' but domain model doesn't",
                            f"Consider adding '{rel_name}' field to domain model for consistency",
                        )
                    )

    def print_summary(self):
        """Print validation summary"""
        if not self.issues:
            print("✅ Schema validation passed! No issues found.")
            return

        error_count = len([i for i in self.issues if i.severity == "error"])
        warning_count = len([i for i in self.issues if i.severity == "warning"])
        info_count = len([i for i in self.issues if i.severity == "info"])

        print(f"\n📊 Schema Validation Summary:")
        print(f"   Errors: {error_count}")
        print(f"   Warnings: {warning_count}")
        print(f"   Info: {info_count}")
        print(f"   Total Issues: {len(self.issues)}")

        if error_count > 0:
            print(f"\n🚨 Critical issues found! Please fix errors before deployment.")
        elif warning_count > 0:
            print(f"\n⚠️  Some warnings found. Consider addressing them.")
        else:
            print(f"\n💡 Only informational items found.")


def main():
    parser = argparse.ArgumentParser(description="Domain/Database Schema Validator")
    parser.add_argument("--model", help="Validate specific model only")
    parser.add_argument(
        "--ci", action="store_true", help="CI mode: exit with error code if issues found"
    )
    parser.add_argument(
        "--fix", action="store_true", help="Auto-fix simple issues (future feature)"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    validator = SchemaValidator()

    print("🔍 PM-056: Domain/Database Schema Validator")
    print(f"   Domain models: {len(validator.domain_models)}")
    print(f"   Database models: {len(validator.db_models)}")
    print(f"   Model mappings: {len(validator.model_mappings)}")

    if args.verbose:
        print(f"\n📋 Model Mappings:")
        for domain, db in validator.model_mappings.items():
            print(f"   {domain} → {db}")

    # Run validation
    if args.model:
        print(f"\n🔎 Validating model: {args.model}")
        issues = validator.validate_model(args.model)
    else:
        print(f"\n🔎 Validating all models...")
        issues = validator.validate_all_models()

    # Print issues
    if issues:
        print(f"\n🚨 Issues Found:")
        for issue in issues:
            print(f"   {issue}")

    # Print summary
    validator.print_summary()

    # CI mode: exit with error code if critical issues
    if args.ci:
        error_count = len([i for i in issues if i.severity == "error"])
        if error_count > 0:
            print(f"\n❌ CI Mode: Exiting with error code due to {error_count} critical issues")
            sys.exit(1)
        else:
            print(f"\n✅ CI Mode: No critical issues found")
            sys.exit(0)


if __name__ == "__main__":
    main()
