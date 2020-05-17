#!/bin/bash

# change current directory
MODULE_PATH=$( cd "$(dirname "$0")" ; pwd )
cd ${MODULE_PATH}
cd ..

# export environmental variables
export NESTA_JOBS_ROOT_PATH=$(pwd)

# activate virtual environment
source .venv/bin/activate
