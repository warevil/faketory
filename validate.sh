#! /bin/bash

uv run ruff check --fix
uv run pytest --cov=faketory tests
rm -f .coverage*;
