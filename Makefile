# Root Makefile - The "Commander"
# Orchestrates build and quality checks across all homework assignments.

# Define all homework directories here (add "Homework 2" when ready)
# We use wildcard to handle spaces, or just quote them explicitly
PROJECTS = "Homework 1"

.PHONY: all lint test clean help

help:
	@echo "Available commands:"
	@echo "  make lint   - Run Pylint across all projects"
	@echo "  make test   - Run unit tests for all projects"
	@echo "  make check  - Run full verification (lint + test)"
	@echo "  make clean  - Remove artifacts"

# 1. Repo-Wide Linting
# Runs pylint using the root .pylintrc configuration
lint:
	@echo "\n>>> 🔍 Running Global Lint Check..."
	pylint $(PROJECTS) --rcfile=.pylintrc

# 2. Repo-Wide Testing
# Iterates through directories and runs their specific test suites
test:
	@echo "\n>>> 🧪 Running Unit Tests..."
	for dir in $(PROJECTS); do \
		echo "Testing $$dir..."; \
		$(MAKE) -C "$$dir" check || exit 1; \
	done

# 3. Full Check (CI Simulation)
check: lint test
	@echo "\n>>> ✅ All Systems Go!"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -f "Homework 1/before.txt" "Homework 1/after.txt"
