#!/bin/sh

set -eu

export PYTHONPATH=${PYTHONPATH}:naoutil/src/main/python:naoutil/src/test/python

if command -v nosetests >/dev/null 2>&1; then
    echo "Running tests with nose"
    nosetests -w naoutil/src/test/python/naoutil_tests
else
    echo "Running tests using python unittest"
    python -m unittest naoutil_tests.test_general
    python -m unittest naoutil_tests.test_jsonobj
    python -m unittest naoutil_tests.test_naoenv
fi

