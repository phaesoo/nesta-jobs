#!/bin/bash

source `dirname $0`/conf.sh

python ${NESTA_JOBS_ROOT_PATH}/src/snp500_companies/main.py --config_path=${NESTA_JOBS_ROOT_PATH}/src/snp500_companies/prod.yml
