#! /bin/bash

source _faketory/bin/activate


black --line-length=95 --skip-string-normalization faketory/ tests/
flake8 faketory/ tests/
isort faketory/ tests/
pytest --cov=faketory tests
rm -f .coverage*;
