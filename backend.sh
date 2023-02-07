#!/usr/bin/env bash
eval "$(conda shell.bash hook)"
cd flask 
conda activate autogosling 
python main.py
