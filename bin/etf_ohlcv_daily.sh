#!/bin/bash

source `dirname $0`/conf.sh

python ${NESTA_JOBS_ROOT_PATH}/src/etf_ohlcv_daily/main.py --config_path=${NESTA_JOBS_ROOT_PATH}/configs/prod.yml
