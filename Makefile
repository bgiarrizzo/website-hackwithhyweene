.DEFAULT_GOAL := help

PROJECT_FOLDER := $(shell pwd)
BIN_FOLDER := bin
BUILD_FOLDER := build
SCRIPTS_FOLDER := scripts
SRC_FOLDER := src
VENV_FOLDER := .venv
DOTENV_FILE := .env

BUILD_PATH := $(PROJECT_FOLDER)/$(BUILD_FOLDER)
DOTENV_PATH := $(PROJECT_FOLDER)/$(DOTENV_FILE)
SCRIPTS_PATH := $(PROJECT_FOLDER)/$(SCRIPTS_FOLDER)
SRC_PATH := $(PROJECT_FOLDER)/$(SRC_FOLDER)
VENV_PATH := $(PROJECT_FOLDER)/$(VENV_FOLDER)

LOG_PATH_SERVER_SIDE := /var/log/nginx/hack-with-hyweene.com
LOG_PARSE_EXCLUDE_PATTERNS := 403|192.168.1.|static|html|400|stats|php|wp-|wordpr|\.env|\.git|\.txt
VENV_BIN := $(VENV_PATH)/$(BIN_FOLDER)
PY_INTERPRETER := $(VENV_BIN)/python

PACKAGER := uv

# Check if .env file exists and load it
ifneq ("$(wildcard $(DOTENV_PATH))","")
	include $(DOTENV_FILE)
	export
endif

.PHONY: help
help:
	@grep -E '(^[a-zA-Z0-9_-]+:.*?##)|(^##)' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "; printf "Usage: make \033[32m<target>\033[0m\n"}{printf "\033[32m%-20s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m## /\n[33m/'

.PHONY: install
install: install_uv ## Install dependencies
	$(PACKAGER) sync

.PHONY: install_dev
install_dev: install_uv ## Install development dependencies
	$(PACKAGER) sync --dev

.PHONY: install_uv
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

.PHONY: install_smolwebvalidator
install_smolwebvalidator: venv ## Install smolweb-validator
	mkdir -p $(BIN_FOLDER)
	@if [ ! -d "$(BIN_FOLDER)/smolweb-validator" ]; then \
		git clone https://codeberg.org/smolweb/smolweb-validator.git $(BIN_FOLDER)/smolweb-validator; \
		cd $(BIN_FOLDER)/smolweb-validator; bash build.sh; \
	else \
		echo "smolweb-validator is already installed in $(BIN_FOLDER)/smolweb-validator"; \
		exit 0; \
	fi

.PHONY: create_venv
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

.PHONY: venv
venv: create_venv ## Load virtual environment
	. $(VENV_BIN)/activate

.PHONY: build
build: venv install ## Build the project
	. $(VENV_BIN)/activate; $(PY_INTERPRETER) src/main.py

.PHONY: serve
serve: venv install build ## Run a local server
	ps -ef | grep '[p]ython -m http.server' | awk '{print $$2}' | xargs -r kill -9
	. $(VENV_BIN)/activate; $(PY_INTERPRETER) -m http.server 8000 --directory build/ > /dev/null 2>&1 &

.PHONY: smolwebvalidator
smolwebvalidator: venv install install_smolwebvalidator serve ## Validate HTML files in the build directory
	echo "SmolWeb Validation ..."

	bash $(SCRIPTS_PATH)/smolweb_validator.sh

	echo "Killing local server..."
	ps -ef | grep '[p]ython -m http.server' | awk '{print $$2}' | xargs -r kill -9 > /dev/null 2>&1

.PHONY: html5validator
html5validator: venv install_dev build ## Validate HTML files in the build directory
	. $(VENV_BIN)/activate; html5validator --root build/

.PHONY: generate_docstrings
generate_docstrings: venv install_dev ## Generate modules/classes/functions docstrings
	. $(VENV_BIN)/activate; pyment -f false -o numpydoc -w src

.PHONY: quick_add_link
quick_add_link: venv install_dev ## Quick add a new link to the website
	. $(VENV_BIN)/activate; $(PY_INTERPRETER) $(SCRIPTS_PATH)/quick_add_link.py $(URL)

.PHONY: top_25_rss_readers
top_25_rss_readers: ## Show top 25 rss readers from access.log
	sudo zcat -f -- $(LOG_PATH_SERVER_SIDE)/access.log | grep -Ev "$(LOG_PARSE_EXCLUDE_PATTERNS)" | grep "feed.xml" | awk -F\" '{ split($$1, a, " "); ip=a[1]; ua=$$6; print ua }' | sort | uniq -c | sort -nr | head -n 25

.PHONY: top_50_pages
top_50_pages: ## Show top 50 requested pages from access.log
	sudo zcat -f -- $(LOG_PATH_SERVER_SIDE)/access.* | grep -Ev "$(LOG_PARSE_EXCLUDE_PATTERNS)"| awk '{ print $$7 }' | sort | uniq -c | sort -nr | head -n 50

.PHONY: top_10_blog_posts
top_10_blog_posts: ## Show top 10 requested blog posts from access.log
	sudo zcat -f -- $(LOG_PATH_SERVER_SIDE)/access.* | grep -Ev "$(LOG_PARSE_EXCLUDE_PATTERNS)"| awk '{ print $$7 }' | sort | uniq -c | grep "/blog/" | sort -nr | head -n 10

.PHONY: top_10_links
top_10_links: ## Show top 10 requested links from access.log
	sudo zcat -f -- $(LOG_PATH_SERVER_SIDE)/access.* | grep -Ev "$(LOG_PARSE_EXCLUDE_PATTERNS)"| awk '{ print $$7 }' | sort | uniq -c | grep "/liens/" | sort -nr | head -n 10

.PHONY: top_50_requesters
top_50_requesters: ## Show top 50 IP addresses from access.log
	sudo zcat -f -- $(LOG_PATH_SERVER_SIDE)/access.* | grep -Ev "$(LOG_PARSE_EXCLUDE_PATTERNS)"| awk '{ print $$1 }' | sort | uniq -c | sort -nr | head -n 50

.PHONY: top_15_referrers
top_15_referrers: ## Show top 50 referrers from access.log
	sudo zcat -f -- $(LOG_PATH_SERVER_SIDE)/access.* | grep -Ev "$(LOG_PARSE_EXCLUDE_PATTERNS)"| awk '{ print $$11 }' | sort | uniq -c | grep -v "-" | sort -nr | head -n 15

.PHONY: top_50_404_file_this_month
top_50_404_file_this_month: ## Show top 50 404 files this month
	sudo zcat -f -- $(LOG_PATH_SERVER_SIDE)/access.log | grep '" 404' | awk '{ print $$7 }' | sort | uniq -c | sort -nr | head -n 50

.PHONY: top_50_404_file_all_time
top_50_404_file_all_time: ## Show top 50 404 files all time
	sudo zcat -f -- $(LOG_PATH_SERVER_SIDE)/access.* | grep '" 404' | awk '{ print $$7 }' | sort | uniq -c | sort -nr | head -n 50

.PHONY: top_50_403_file
top_50_403_file: ## Show top 50 403 files
	sudo zcat -f -- $(LOG_PATH_SERVER_SIDE)/access.* | grep '" 403' | awk '{ print $$7 }' | sort | uniq -c | sort -nr | head -n 50

.PHONY: top_50_403_requester
top_50_403_requester: ## Show top 50 403 requesters
	sudo zcat -f -- $(LOG_PATH_SERVER_SIDE)/access.* | grep '" 403' | awk '{ print $$1 }' | sort | uniq -c | sort -nr | head -n 50
