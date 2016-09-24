#!/usr/bin/env bash

#IFS=$(echo -en "\n\b")
XMLDIR="laws_xml"

for i in laws_txt/*.txt
do
 FILENAME=$(basename $i)
 NAME="${FILENAME%.*}"
 echo $i
 ./parse.py $i $XMLDIR/$NAME.xml
done
