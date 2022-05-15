#!/bin/bash
while :
do
    pip3 install -r requirements.txt
    sleep(10)
    python main.py
    sleep 3
done
