#!/usr/bin/env bash

module load jaspy

python -m venv venv --system-site-packages

. venv/bin/activate

pip install xarray==0.14.1