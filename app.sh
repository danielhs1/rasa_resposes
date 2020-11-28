#!/bin/sh

export PYTHONPATH=$(pwd)

gunicorn -c ./src/gunicorn.py src.app:app
