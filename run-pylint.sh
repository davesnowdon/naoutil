#! /bin/sh

export PYTHONPATH=${PYTHONPATH}:naoutil/src/main/python
cd naoutil/src/main/python
pylint naoutil
