.DEFAULT_GOAL := default
SHELL := /bin/bash

PYTHON_VERSION = 3.8
PROJECT_NAME = BTC_bot

venv_path = ~/.virtualenv/$(PROJECT_NAME)
python = python$(PYTHON_VERSION)


default:
	@echo "Please specify target. Check contents of Makefile to see list of available targets."

create_virtualenv:
	@echo -n "Creating virtual environment..."
	@$(python) -m venv $(venv_path)
	@echo "done."
	@echo "To activate in your shell please run: source $(venv_path)/bin/activate"

pip_install:
	@# DO NOT PUT COMMANDS BELLOW ON SEPARATE LINES
	@# pip WILL NOT work properly in that case
	@source $(venv_path)/bin/activate; pip install -U pip; pip install --force-reinstall -r requirements.txt
