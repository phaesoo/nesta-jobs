#!/bin/bash

source `dirname $0`/conf.sh

python ${MODULE_PATH}/main.py --config_path=${MODULE_PATH}/prod.yml
