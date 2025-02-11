#!/bin/bash

model_list="4o 4omini claude0620 claude1022"

mission="doc"

for model in $model_list; do
    echo "Executing for model: $model"
    python excute/apr.py "$mission" "$model"
done