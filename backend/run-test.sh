#!/bin/bash   
set -x
pip install ".[dev]"
ruff .
black . --check
mypy .
python -m pytest .
