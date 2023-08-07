# Makefile for running the Python script with arguments

# Set the default target to 'run'
default: run

# Define the Python executable (change it if needed)
PYTHON = venv/bin/python

# Define the Python script file
SCRIPT_FILE = main.py

# Define the default arguments for the Python script
ARGS = --token mymagik_token --log_file ./mylogger.log

# Target to run the Python script with the specified arguments
.PHONY: run
run:
	$(PYTHON) $(SCRIPT_FILE) $(ARGS)

.PHONY: install_requirements
install_requirements:
    pip install -r requirements.txt
