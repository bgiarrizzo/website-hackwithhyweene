.DEFAULT_GOAL := help
VENV_PATH := $(shell pwd)/.venv
VENV_BIN := $(VENV_PATH)/bin
PYTHON := $(VENV_BIN)/python
UV := uv

help:
	@grep -E '(^[a-zA-Z0-9_-]+:.*?##)|(^##)' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "; printf "Usage: make \033[32m<target>\033[0m\n"}{printf "\033[32m%-20s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m## /\n[33m/'

install: ## Install dependencies
	$(UV) sync

install_dev: ## Install development dependencies
	$(UV) sync --dev

venv: ## Create virtual environment
	. $(VENV_BIN)/activate

build: venv install ## Build the project
	. $(VENV_BIN)/activate; $(PYTHON) src/main.py

serve: venv install build ## Run a local server
	. $(VENV_BIN)/activate; $(PYTHON) -m http.server 8000 --directory build/

html5validator: venv install_dev build ## Validate HTML files in the build directory
	. $(VENV_BIN)/activate; html5validator --root build/

generate_docstrings: venv install_dev ## Generate modules/classes/functions docstrings
	. $(VENV_BIN)/activate; pyment -f false -o numpydoc -w src