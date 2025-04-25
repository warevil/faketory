#!/bin/bash

# Create virtual environment and then activate it
python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
# Install uv
pip install uv
uv sync
