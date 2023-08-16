#!/bin/bash   
set -x
ruff .
black . --check
dmypy run .
python -m pytest .
