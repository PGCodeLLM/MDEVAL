#!/bin/bash

model="gpt-4"
mission="doc"

python inference/chat.py "$mission" "$model"