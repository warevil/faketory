#!/bin/bash

# Create virtual environment and then activate it
python -m venv _faketory
source _faketory/bin/activate

pip install --upgrade pip
# Install poetry, then use it to install dependencies
pip install poetry
poetry install
poetry run pre-commit install
