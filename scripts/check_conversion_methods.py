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


# ---------------------------------------------------------------------------
# Explicit, documented exceptions (#1788 AC-3 — registered here, never silently
# skipped; every entry below is PRINTED with its reason on every run).
#
# Ruling: Arch, 2026-09-13 (`mailboxes/arch/sent/ruling-arch-to-lead-cc-ppm-pm-1788-
# two-converters-five-checker-offs-...-2026-09-13.md`). The discriminator is NOT
# name-matching a DB class to a domain class -- it is "does any live path actually
# round-trip this row." Writing a converter where nothing round-trips asserts a
# correspondence the product does not have: a lie with a type signature.
#
# These five are create-all-era persistence twins. Their DOMAIN namesakes are alive
# (domain `Intent` has 26 importing files -- it is the classifier spine); the DB
# twins are not. #1273 already found their tables never got create-migrations.
#
# Census re-run by the executing lane 2026-09-13 (denominator: services/ + web/,
# tests excluded). Each of the five has only in-package importers, and those form a
# CLOSED DEAD SUBGRAPH -- nothing anywhere imports `from services.database import ...`,
# so the `services/database/__init__.py` re-export surface has zero consumers, and
# ProductRepository / FeatureRepository / TaskRepository / RepositoryFactory have zero
# callers outside services/database/. Precise claim: zero LIVE CONSUMERS.
#
# Disposal (tables, migrations, possible stray rows) is tracked separately -- deleting
# a DB model has its own discipline and does not belong to this checker's lane.
# TWO distinct sub-shapes live here, and the reason lines must let a reader tell
# them apart (Arch, 2026-09-14 re-ruling):
#   * "dead persistence twin"  -- the DB class is dead, the domain class may be
#     very much alive (domain Intent has 26 importers; its DB twin has none).
#   * "live owner-anchor row"  -- the INVERSE: the DB class is live and the
#     name-matched domain class is the dead one. DocumentDB is this shape.
#
# The generalizable rule the second shape produced, now part of the ruling:
# LIVENESS MUST BE MEASURED ON BOTH SIDES. A live DB class with a dead domain
# twin fails the round-trip test exactly as a dead DB class with a live domain
# twin does -- measuring one side answers the wrong question.
DEAD_PERSISTENCE_TWINS: Dict[str, str] = {
    "DocumentDB": (
        "live owner-anchor row with no domain counterpart -- the name-matched "
        "domain class is a different, dead object (content-bearing vs anchor-only); "
        "a from_domain would have to invent chromadb_base_id and drop the ADR-071 "
        "D1/D2 security fields (owner_id, is_global_pm_domain). See #1797."
    ),
    "Feature": "dead persistence twin, zero importers, see #1273",
    "Intent": "dead persistence twin, zero importers, see #1273",
    "Product": "dead persistence twin, zero importers, see #1273",
    "Stakeholder": "dead persistence twin, zero importers, see #1273",
    "Task": "dead persistence twin, zero importers, see #1273",
}


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
    name_matched = [
        name
        for name in database_models
        if name in domain_set or (name.endswith("DB") and name[:-2] in domain_set)
    ]
    in_scope = [name for name in name_matched if name not in DEAD_PERSISTENCE_TWINS]
    skipped = sorted(set(database_models) - set(name_matched))

    print(f"📊 {len(in_scope)} model(s) have a domain counterpart and are in scope")
    print(f"📊 {len(skipped)} persistence-only model(s) skipped (no domain counterpart)")
    print()

    # #1788 AC-3: registered exceptions are announced with their reason on every
    # run, so "off" is visible in the log rather than silent.
    registered = sorted(set(name_matched) & set(DEAD_PERSISTENCE_TWINS))
    if registered:
        print(f"🔕 {len(registered)} registered exception(s) (name-matched but not round-tripped):")
        for name in registered:
            print(f"   - {name}: {DEAD_PERSISTENCE_TWINS[name]}")
        print()

    # A registry that outlives its models is how a config file becomes a graveyard.
    # If an entry no longer names a real DB model, fail loudly rather than pass
    # quietly on a stale exception (m-44: a "clear" that measured nothing).
    stale = sorted(set(DEAD_PERSISTENCE_TWINS) - set(database_models))
    if stale:
        print("❌ Stale entries in DEAD_PERSISTENCE_TWINS (no such database model):")
        for name in stale:
            print(f"   - {name}")
        print("   Remove the entry -- the model it excused is gone.")
        print()
        return 1

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
