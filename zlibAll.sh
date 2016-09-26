#!/bin/bash

XMLDIR="laws_xml"
ZLIBDIR="laws_zlib"

for i in $XMLDIR/*
do
    echo $i
    NAME=$(basename $i)
    ./makeZlib.py $i $ZLIBDIR/$NAME.zlib
done
