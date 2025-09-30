.DEFAULT_GOAL := help
VENV_FOLDER := .venv
VENV_PATH := $(shell pwd)/$(VENV_FOLDER)
VENV_BIN := $(VENV_PATH)/bin
PYTHON := $(VENV_BIN)/python
PACKAGER := uv

help:
	@grep -E '(^[a-zA-Z0-9_-]+:.*?##)|(^##)' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "; printf "Usage: make \033[32m<target>\033[0m\n"}{printf "\033[32m%-20s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m## /\n[33m/'

install: install_uv ## Install dependencies
	$(PACKAGER) sync

install_dev: install_uv ## Install development dependencies
	$(PACKAGER) sync --dev

install_uv: ## Install the packager
	@if ! command -v uv >/dev/null 2>&1; then \
		if ! command -v curl >/dev/null 2>&1; then \
			echo "curl could not be found, please install it first."; \
			exit 1; \
		else \
			echo "Installing uv..."; \
			curl -LsSf https://astral.sh/uv/install.sh | sh; \
		fi; \
	else \
		echo "uv is already installed."; \
	fi


create_venv: ## Create virtual environment
	@if ! command -v python &> /dev/null; then \
		python3 -m venv $(VENV_FOLDER); \
	else \
		python -m venv $(VENV_FOLDER); \
	fi

venv: create_venv ## Load virtual environment
	. $(VENV_BIN)/activate

build: venv install ## Build the project
	. $(VENV_BIN)/activate; $(PYTHON) src/main.py

serve: venv install build ## Run a local server
	. $(VENV_BIN)/activate; $(PYTHON) -m http.server 8000 --directory build/

html5validator: venv install_dev build ## Validate HTML files in the build directory
	. $(VENV_BIN)/activate; html5validator --root build/

generate_docstrings: venv install_dev ## Generate modules/classes/functions docstrings
	. $(VENV_BIN)/activate; pyment -f false -o numpydoc -w src