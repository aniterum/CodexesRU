#!/usr/bin/env python3


import sys
from os.path import exists
import re
from xml.etree import ElementTree as ET


if len(sys.argv) != 2:
    print("Неверное число параметров")
    exit()

def errexit(item, leave=True):
    print("->", item)
    if leave:
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
    errexit("text no child")

if len(docinfo.getchildren()) == 0:
    errexit("docinfo no child")

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
    errexit("no getpower", False)

if approved == None:
    errexit("no approved", False)

if date == None:
    errexit("no date", False)

if number == None:
    errexit("no number", False)

if title == None:
    errexit("no title", False)

if changes == None:
    errexit("no changes", False)

re_num = re.compile("(\d+)\.*-*(\d*)-*(\d*)-*(\d*)")
def procChapter(child):
    artIDS = {}
    print("    chapter", child.get("id"))
    int_art_id = 0
    ch_id = child.get("id")
    ch_text = child.get("text")
    if ch_id == None:
        print("no chapter id")
    else:
        pass
        #print("Chapter", ch_id)
        
    if ch_text == None:
        print("no chapter text")
        
    for article in child.getchildren():
        art_id = article.get("id")
        art_title = article.get("text")
        if art_id == None:
            print("article no id")
        else:
            ID, ID_1, ID_2, ID_3 = re_num.findall(art_id)[0]
            if artIDS.get(ID) != None:
                #print(20*" " + "\\" , ID_1, ID_2, ID_3)
                pass
            else:
                artIDS[ID] = [ID_1, ID_2, ID_3]
            print("         article", "|".join([ID, ID_1, ID_2, ID_3]) )

                
        if art_title == None:
            print("article title")

#Тест глав
if len(text.getchildren()) == 0:
    errexit("no razdels, chapters")

for razdel_chapter in text.getchildren():
    if razdel_chapter.tag == "razdel":
        print("razdel", razdel_chapter.get("id"))
        if len(razdel_chapter.getchildren()) == 0:
            print("---> razdel no children")

        if razdel_chapter.getchildren()[0].tag == "chapter":
            for chapter in razdel_chapter.getchildren():
                procChapter(chapter)
        else:
            procChapter(razdel_chapter)
                
    elif razdel_chapter.tag == "chapter":
        procChapter(razdel_chapter)
    else:
        print("---- ", razdel_chapter.tag, razdel_chapter.get("text"))
            





    

