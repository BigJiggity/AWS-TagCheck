#!/bin/bash
virtualenv --no-site-packages ./aws
source ./aws/bin/activate
pip install -r requirements.txt
