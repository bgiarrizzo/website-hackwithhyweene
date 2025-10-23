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
	@if [ ! -d "$(VENV_FOLDER)" ]; then \
		if ! command -v python &> /dev/null; then \
			python3 -m venv $(VENV_FOLDER); \
		else \
			python -m venv $(VENV_FOLDER); \
		fi \
	else \
		echo "Virtual environment already exists at $(VENV_PATH)"; \
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

top_50_pages: ## Show top 50 requested pages from access.log
	sudo zcat -f -- /var/log/nginx/hack-with-hyweene.com/access.* | grep -v 404| awk '{ print $$7 }' | sort | uniq -c | grep -Ev "static|xml|html|400|stats|php|wp-|wordpr|\.env|\.git|\.txt" | sort -nr | head -n 50

top_10_blog_posts: ## Show top 10 requested blog posts from access.log
	sudo zcat -f -- /var/log/nginx/hack-with-hyweene.com/access.* | grep -v 404| awk '{ print $$7 }' | sort | uniq -c | grep "/blog/" | grep -Ev "static|xml|html|400|stats|php|wp-|wordpr|\.env|\.git|\.txt" | sort -nr | head -n 10

top_10_links: ## Show top 10 requested links from access.log
	sudo zcat -f -- /var/log/nginx/hack-with-hyweene.com/access.* | grep -v 404| awk '{ print $$7 }' | sort | uniq -c | grep "/liens/" | grep -Ev "static|xml|html|400|stats|php|wp-|wordpr|\.env|\.git|\.txt" | sort -nr | head -n 10

top_50_requesters: ## Show top 50 IP addresses from access.log
	sudo zcat -f -- /var/log/nginx/hack-with-hyweene.com/access.* | grep -v 404| awk '{ print $$1 }' | sort | uniq -c | sort -nr | head -n 50

top_15_referrers: ## Show top 50 referrers from access.log
	sudo zcat -f -- /var/log/nginx/hack-with-hyweene.com/access.* | grep -v 404| awk '{ print $$11 }' | sort | uniq -c | grep -v "-" | sort -nr | head -n 15