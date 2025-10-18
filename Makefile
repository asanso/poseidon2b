# Define Virtual environment state directory along with path to executables inside venv
VENV := .venv
VENV_PYTHON := $(VENV)/bin/python
VENV_PIP := $(VENV)/bin/pip
VENV_PYTEST := $(VENV)/bin/pytest
VENV_BLACK := $(VENV)/bin/black

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup: install ## Sets up virtual environment and installs dependencies
	@echo "\n✅ Virtual environment is ready."
	@echo "To activate it, run: source $(VENV)/bin/activate"
	@echo "After activated, to deactivate it, run: deactivate"

# The install target now depends on the venv being created
.PHONY: install
install: $(VENV)/bin/activate ## Install dependencies using `pip`
	@echo "Installing dependencies..."
	$(VENV_PIP) install -r ref_impl/requirements.txt

# This target creates the virtual environment
$(VENV)/bin/activate: ref_impl/requirements.txt
	@echo "Setting up environment with venv..."
	python3 -m venv $(VENV)

.PHONY: test
test: ## Run tests using `pytest`
	@echo "Running tests..."
	$(VENV_PYTEST) -v

.PHONY: gen_params
gen_params: ## Generates all Poseidon2b parameters
	$(VENV_PYTHON) ref_impl/gen_params.py | tee ref_impl/poseidon2b_parameters.txt

.PHONY: format
format: ## Formats code using `black`
	@echo "Formatting code..."
	$(VENV_BLACK) .

.PHONY: clean
clean:	## Deletes virtual environment setup directory
	@echo "Removing virtual environment directory..."
	rm -rf $(VENV)
