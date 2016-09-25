#!/usr/bin/env python3


import sys
from os.path import exists
from xml.etree import ElementTree as ET


if len(sys.argv) != 2:
    print("Неверное число параметров")
    exit()

def errexit(item):
    print("->", item)
    exit()

#inFile = "laws_xml/air.xml"
inFile = sys.argv[1]
if not exists(inFile):
    errexit(inFile, "file not found")


xmlData = ET.parse(inFile).getroot()

if xmlData.tag != 'document':
    errexit("document")

childs = xmlData.getchildren()

text = None
docinfo = None

for child in childs:
    if child.tag == "text":
        text = child
    elif child.tag == "docinfo":
        docinfo = child

if text == None:
    errexit("text")
    
if docinfo == None:
    errexit("docinfo")

if len(text.getchildren()) == 0:
    errexit("text No child")

if len(docinfo.getchildren()) == 0:
    errexit("docinfo No child")

if len(docinfo.getchildren()) > 6:
    print("->", "docinfo has MORE than 6 subelements")
#if len(docinfo.getchildren()) < 6:
#    print("->", "docinfo has LESS than 6 subelements")

getpower = None
approved = None
date = None
number = None
title = None
changes = None

for item in docinfo.getchildren():
    if item.tag != "info":
        errexit("docinfo has item with NOT INFO TAG")
    item_class = item.get("class")
    item_text = item.get("text")
    
    if (item_class != None) and (item_text != None):
        if item_class == "getpower":
            getpower = item_text
        elif item_class == "approved":
            approved = item_text
        elif item_class == "number":
            number = item_text
        elif item_class == "date":
            date = item_text
        elif item_class == "title":
            title = item_text
        elif item_class == "changes":
            changes = item_text

if getpower == None:
    errexit("NO getpower")

if approved == None:
    errexit("NO approved")

if date == None:
    errexit("NO date")

if number == None:
    errexit("NO number")

if title == None:
    errexit("NO title")

if changes == None:
    errexit("NO changes")








    

