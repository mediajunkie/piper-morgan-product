#!/usr/bin/env python3
"""
PM-056: Conversion Methods Checker
Checks for missing to_domain/from_domain methods in database models.
"""

import ast
import importlib
import inspect
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def find_database_models() -> List[str]:
    """Find all database model classes"""
    try:
        from services.database import models
        from services.database.models import Base

        database_models = []
        for name, obj in inspect.getmembers(models):
            if inspect.isclass(obj) and issubclass(obj, Base) and obj != Base:
                database_models.append(name)

        return database_models
    except ImportError as e:
        print(f"❌ Error importing database models: {e}")
        return []


def find_domain_models() -> List[str]:
    """Find all domain model classes"""
    try:
        import services.domain.models as domain_models

        domain_classes = []
        for name, obj in inspect.getmembers(domain_models):
            if inspect.isclass(obj) and hasattr(obj, "__dataclass_fields__"):
                domain_classes.append(name)

        return domain_classes
    except ImportError as e:
        print(f"❌ Error importing domain models: {e}")
        return []


def check_conversion_methods(database_model_name: str) -> Tuple[bool, List[str]]:
    """Check if database model has proper conversion methods.

    Detection note: `from_domain` is a @classmethod, and a classmethod accessed on the class
    is a *bound method*, not a function. The previous implementation enumerated members with
    `predicate=inspect.isfunction`, so every correctly-written `from_domain` classmethod was
    reported as "Missing" -- 24 false positives, including ProjectDB and WorkItem, whose
    from_domain implementations are plainly present in services/database/models.py.
    Membership is now tested with getattr/callable, and the shape checks distinguish
    instance methods from classmethods via inspect.ismethod on the class object.
    """
    try:
        from services.database import models

        db_model = getattr(models, database_model_name)

        to_domain = getattr(db_model, "to_domain", None)
        from_domain = getattr(db_model, "from_domain", None)

        issues = []

        if not callable(to_domain):
            issues.append("Missing to_domain() method")
        elif inspect.ismethod(to_domain):
            # Bound to the class => declared as a classmethod; to_domain needs instance state.
            issues.append("to_domain() should be an instance method, not a class method")

        if not callable(from_domain):
            issues.append("Missing from_domain() method")
        elif not inspect.ismethod(from_domain):
            # Plain function on the class => not decorated as a classmethod.
            issues.append("from_domain() should be a class method")

        return len(issues) == 0, issues

    except Exception as e:
        return False, [f"Error checking {database_model_name}: {e}"]


def main():
    """Main validation function"""
    print("🔍 PM-056: Checking Conversion Methods")
    print("=" * 50)

    # Find models
    database_models = find_database_models()
    domain_models = find_domain_models()

    print(f"📊 Found {len(database_models)} database models")
    print(f"📊 Found {len(domain_models)} domain models")
    print()

    # Only database models that HAVE a domain counterpart can have a conversion layer.
    # Pure-persistence entities (TokenBlacklist, PasswordResetToken, InviteToken, SlackLinkCode,
    # AuditLog, User, ...) have no domain dataclass to convert to or from, so demanding
    # to_domain()/from_domain() on them is not a drift signal -- it is noise that kept this
    # gate permanently red (46 of 47 models reported) and therefore unusable as a regression
    # detector. Scoped by exact name match or the `<Name>DB` suffix convention.
    domain_set = set(domain_models)
    in_scope = [
        name
        for name in database_models
        if name in domain_set or (name.endswith("DB") and name[:-2] in domain_set)
    ]
    skipped = sorted(set(database_models) - set(in_scope))

    print(f"📊 {len(in_scope)} model(s) have a domain counterpart and are in scope")
    print(f"📊 {len(skipped)} persistence-only model(s) skipped (no domain counterpart)")
    print()

    # Check each in-scope database model
    all_passed = True
    total_issues = 0

    for db_model_name in in_scope:
        passed, issues = check_conversion_methods(db_model_name)

        if passed:
            print(f"✅ {db_model_name}: All conversion methods present")
        else:
            print(f"❌ {db_model_name}:")
            for issue in issues:
                print(f"   - {issue}")
            all_passed = False
            total_issues += len(issues)

    print()
    print("=" * 50)

    if all_passed:
        print("✅ All database models have proper conversion methods!")
        print("✅ Domain/database conversion layer is complete")
        return 0
    else:
        print(f"❌ Found {total_issues} conversion method issues")
        print("❌ Some database models are missing conversion methods")
        print()
        print("💡 To fix:")
        print("   - Add to_domain() class method to database models")
        print("   - Add from_domain() class method to database models")
        print("   - Ensure methods are properly decorated as @classmethod")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
