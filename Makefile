# Piper Morgan 1.0 - Makefile
# PM-056 Schema Validation Integration

.PHONY: help test validate-schema validate-all clean install

help:
	@echo "Piper Morgan 1.0 - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  install     - Install dependencies"
	@echo "  test        - Run all tests"
	@echo "  test-unit   - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo ""
	@echo "PM-056 Schema Validation:"
	@echo "  validate-schema    - Run domain/database schema validation"
	@echo "  validate-all       - Run all validation checks"
	@echo "  check-conversions  - Check to_domain/from_domain methods"
	@echo ""
	@echo "CI/CD:"
	@echo "  ci-test     - Run tests for CI environment"
	@echo "  ci-validate - Run validation for CI environment"
	@echo ""
	@echo "Utilities:"
	@echo "  clean       - Clean up temporary files"
	@echo "  format      - Format code with black and isort"

# Development Commands
install:
	pip install -r requirements.txt

test:
	python -m pytest tests/ -v

test-unit:
	python -m pytest tests/unit/ -v

test-integration:
	python -m pytest tests/integration/ -v

# PM-056 Schema Validation Commands
validate-schema:
	@echo "🔍 Running PM-056 Schema Validation..."
	PYTHONPATH=. python3 tools/schema_validator.py

validate-all:
	@echo "🔍 Running All Validation Checks..."
	@$(MAKE) validate-schema
	@$(MAKE) check-conversions
	@echo "✅ All validations passed!"

check-conversions:
	@echo "🔍 Checking to_domain/from_domain methods..."
	PYTHONPATH=. python scripts/check_conversion_methods.py

# CI/CD Commands
ci-test:
	python -m pytest tests/ --cov=services --cov-report=xml

ci-validate:
	@echo "🔍 Running CI Schema Validation..."
	PYTHONPATH=. python3 tools/schema_validator.py --ci

# Utility Commands
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

format:
	black services/ tests/ scripts/
	isort services/ tests/ scripts/

# PM-056 Validation with Intentional Mismatches (for testing)
test-validator-with-mismatches:
	@echo "🧪 Testing validator with intentional mismatches..."
	@echo "This will temporarily add mismatches to test validation..."
	# Add temporary field to domain model
	@echo "  # Temporary test field" >> services/domain/models.py
	@echo "  test_field: str = ''" >> services/domain/models.py
	@$(MAKE) validate-schema || echo "✅ Validator correctly caught mismatch"
	# Remove temporary field
	@sed -i '' '/test_field: str = '\'\''/d' services/domain/models.py
	@echo "🧹 Cleaned up test field"
