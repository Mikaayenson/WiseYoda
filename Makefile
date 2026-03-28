# WiseYoda — use uv for envs and tasks (https://docs.astral.sh/uv/)
UV ?= uv
PYTHON_VERSION ?= 3.12
# Keep `uv run` on the same interpreter as `make sync` (avoids mismatch with `.python-version`).
export UV_PYTHON := $(PYTHON_VERSION)

.PHONY: help
help: ## Show targets
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z0-9_.-]+:.*?##/ { printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)

##@ Setup

.PHONY: sync
sync: ## Install runtime + dev + api deps (creates .venv; api needed for HTTP tests)
	$(UV) sync --extra dev --extra api --python $(PYTHON_VERSION)

##@ Quality

.PHONY: check
check: ## Ruff lint + format check
	$(UV) run ruff check wise_yoda tests
	$(UV) run ruff format --check wise_yoda tests

.PHONY: format
format: ## Ruff format (write)
	$(UV) run ruff format wise_yoda tests
	$(UV) run ruff check --fix wise_yoda tests

##@ Tests

.PHONY: test
test: ## Pytest with coverage
	$(UV) run pytest

##@ Build

.PHONY: build
build: ## Build wheel + sdist
	$(UV) build

.PHONY: ci
ci: check test build ## Local gate matching CI (lint, format check, tests, build)
