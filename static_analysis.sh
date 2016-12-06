#!/bin/sh

################################################################
# Simple way to run python static analysis check on your code. #
# This checks against pylint and pep8 standards.               #
################################################################

EXCLUDE_FOLDERS=build,dist,aws
echo "Running pylint.."
pylint --rcfile pylintrc *.py
echo "Running PEP8..."
pep8 --exclude=${EXCLUDE_FOLDERS} .
