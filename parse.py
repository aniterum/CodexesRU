#!/usr/bin/env python3

import re
import os
from os.path import splitext
from xml.etree import ElementTree as ET

names = {
"admin":"Кодекс Российской Федерации об административных правонарушениях",
"admin_proc":"Кодекс административного судопроизводства",
"civil_1":"Гражданский кодекс Российской Федерации. Часть первая",
"civil_2":"Гражданский кодекс Российской Федерации. Часть вторая",
"civil_3":"Гражданский кодекс Российской Федерации. Часть третья",
"civil_4":"Гражданский кодекс Российской Федерации. Часть четвертая",
"civil_proc":"Гражданский процессуальный кодекс Российской Федерации",
"wood":"Лесной кодекс Российской Федерации",
"water":"Водный кодекс Российской Федерации",
"city_build":"Градостроительный кодекс Российской Федерации",
"housing":"Жилищный кодекс Российской Федерации",
"arbitraje_proc":"Арбитражный процессуальный кодекс Российской Федерации",
"ground":"Земельный кодекс Российской Федерации",
"water_transport":"Кодекс внутреннего водного транспорта Российской Федерации",
"seafaring_trade":"Кодекс торгового мореплавания Российской Федерации",
"air":"Воздушный кодекс Российской Федерации",
"taxing_1":"Налоговый кодекс Российской Федерации. Часть первая",
"taxing_2":"Налоговый кодекс Российской Федерации. Часть вторая",
"budget":"Бюджетный кодекс Российской Федерации",
"criminal":"Уголовный кодекс Российской Федерации",
"criminal_exec":"Уголовно-процессуальный кодекс Российской Федерации",
"criminal_proc":"Уголовно-исполнительный кодекс Российской Федерации",
"family":"Семейный кодекс Российской Федерации",
"job":"Трудовой кодекс Российской Федерации",
}

TXTDIR = "laws_txt/"

fileName = "air.txt"

file = open(TXTDIR + fileName, 'rt').readlines()
lines = [i for i in file if i != "\n" ]
index = -1

data = {}

re_words = "(\w+\s*(?: \w+)*)"

prin = re.compile("\s+Принят Государственной Думой\s+(.+)$")
odob = re.compile("\s+Одобрен Советом Федерации\s+(.+)$")
chapt = re.compile("\s+(?:Глава|ГЛАВА) ((?:\d+)|(?:\w+))\. (.+)$")
razdel = re.compile("\s+(?:Раздел|РАЗДЕЛ) (\w+)\. (.+)$")
article = re.compile("\s+Статья ((?:\d+\.)*(?:\d+-\d+\.*)*) (.+)$")
num = re.compile("\s{10}(N \d+-ФЗ)")
date = re.compile("\s+\d+\s\S+\s\d+ года")
dummy1 = re.compile("\s+Москва, Кремль")

regulars = {prin:"prin", odob:"odob",
            chapt:"chapt", razdel:"razdel",
            article:"article", num:"num",
            dummy1:"dummy",  date:"date"}

global doc, info, text, currentRazdel, currentChapter, currentArticle, currentLine

doc = ET.Element("document")
info = ET.Element("docinfo")
text = ET.Element("text")

doc.append(text)
doc.append(info)
currentRazdel = None
currentChapter = None
currentArticle = None
currentLine = None



def proc(line):
    global doc, info, text, currentRazdel, currentChapter, currentArticle, currentLine
    for reg in regulars:
        if reg.match(line) != None:
            data = reg.findall(line)[0]
            _type_ = regulars.get(reg)
            if _type_ == "razdel":
                currentChapter = None
                currentArticle = None
                currentLine = None
                currentRazdel = ET.Element("razdel")
                currentRazdel.set("id", data[0])
                currentRazdel.set("text", removeSpaces(data[1].rstrip()))
                text.append(currentRazdel)
            elif _type_ == "chapt":
                currentArticle = None
                currentLine = None
                currentChapter = ET.Element("chapter")
                currentChapter.set("id", data[0])
                currentChapter.set("text", removeSpaces(data[1].rstrip()))
                if currentRazdel != None:
                    currentRazdel.append(currentChapter)
                else:
                    text.append(currentChapter)
            elif _type_ == "article":
                currentLine = None
                currentArticle = ET.Element("article")
                if data[0].endswith("."):
                    currentArticle.set("id", data[0][:-1])
                else:
                    currentArticle.set("id", data[0])
                currentArticle.set("text", removeSpaces(data[1].rstrip()))
                if currentChapter != None:
                    currentChapter.append(currentArticle)
                elif currentRazdel != None:
                    currentRazdel.append(currentArticle)
                else:
                    text.append(currentArticle)
            elif _type_ == "prin":
                info_prin = ET.Element("info")
                info_prin.set("class", "getpower")
                info_prin.set("text", removeSpaces(data.rstrip()))
                info.append(info_prin)
            elif _type_ == "odob":
                info_approve = ET.Element("info")
                info_approve.set("class", "approved")
                info_approve.set("text", removeSpaces(data.rstrip()))
                info.append(info_approve)
            elif _type_ == "num":
                info_num = ET.Element("info")
                info_num.set("class", "number")
                info_num.set("text", removeSpaces(data.rstrip()))
                info.append(info_num)
            elif _type_ == "date":
                info_date = ET.Element("info")
                info_date.set("class", "date")
                info_date.set("text", removeSpaces(data.rstrip()))
                info.append(info_date)
                


def processArticle(lines, i):
    print(lines[i].rstrip())

def removeSpaces(text):
    while text.find("  ") != -1:
        text = text.replace("  ", " ")

    return text

SPACES = " " * 12
NL = " " * 10


def getType(line):
    for reg in regulars:
        if reg.match(line) != None:
            return regulars.get(reg)

    return None

i = -1
while i < len(lines):
    if (i+1) >= len(lines):
        break
    i += 1
    ans = getType(lines[i])
    if ans != None:
        inline = lines[i].rstrip() + " "
        
        addIndex = 1
        while True:
            if i+addIndex >= len(lines):
                break
            if lines[i + addIndex].startswith(SPACES):
                if (i + addIndex) >= len(lines):
                    break
                inline += " " + lines[i + addIndex].strip()
                addIndex += 1
            else:
                i = i + addIndex - 1
                break
            
        proc(inline)

    else:
        if currentArticle != None:
            if currentLine == None:
                currentLine = ET.Element("p")
                currentLine.set("text", lines[i].strip())
                currentArticle.append(currentLine)
            else:
                if lines[i].startswith(NL):
                    currentLine = ET.Element("p")
                    currentLine.set("text", removeSpaces(lines[i].strip()))
                    currentArticle.append(currentLine)
                else:
                    par = currentLine.get("text")
                    currentLine.set("text", removeSpaces(par + " " + lines[i].strip()))
        else:
            pass
            #print(lines[i].strip())




name, _ = splitext(fileName)

title = names.get(name)
if title != None:
    info_title = ET.Element("info")
    info_title.set("class", "title")
    info_title.set("text", title)
    info.append(info_title)

tree = ET.ElementTree(doc)
tmpFile = '/tmp/tmp_xml.xml'
ofile = "out.xml"

tree.write(tmpFile, encoding="utf-8", xml_declaration=True)

command = 'xmllint -format -recover "%s" > "%s"'
os.system(command % (tmpFile, ofile))


