#!/bin/bash

ZLIBDIR="laws_zlib"

for i in $ZLIBDIR/*
do
    ./testZlib.py $i
done
