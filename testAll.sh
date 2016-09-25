#!/usr/bin/env bash

#IFS=$(echo -en "\n\b")
XMLDIR="laws_xml"

for i in $XMLDIR/*.xml
do
 echo "TEST $i"
 ./xmltest.py $i
done
