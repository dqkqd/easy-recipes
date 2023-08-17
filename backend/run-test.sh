#!/bin/bash   
set -x

vulture .
ruff .
black . --check
dmypy run .
python -m pytest .
