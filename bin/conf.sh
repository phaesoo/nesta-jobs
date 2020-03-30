#!/bin/bash

# change current directory
MODULE_PATH=$( cd "$(dirname "$0")" ; pwd )
cd ${MODULE_PATH}
cd ..

# activate virtual environment
source .venv/bin/activate
