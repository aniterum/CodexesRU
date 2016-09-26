#!/usr/bin/env python3

import sys, os, zlib, time
from os.path import splitext, basename, exists
from xml.etree import ElementTree as ET

def removeSpaces(text):
    while text.find("  ") != -1:
        text = text.replace("  ", " ")

    return text

if len(sys.argv) != 3:
    print("Неверное число параметров")
    exit()

files_attrib = []

ifile = sys.argv[1]
ofile = sys.argv[2]

_tmp = {}
file_stat = os.stat(ifile) #File size
data = open(ifile, 'rb').read()
zipped = zlib.compress(data)

files_attrib.append(_tmp)


_root = ET.parse(ifile).getroot()
for i in _root.iter():
    if i.tag == "info":
        if i.get('class') == 'title':
            file_title = i.get('text').strip()


_tmp["size"]  = str(file_stat.st_size)
_tmp["packed"] = str(len(zipped))
_tmp["name"]  = basename(ifile) + ".zlib"
creationTime = int(time.time())
_tmp["date"]  = str(creationTime)
_tmp["title"] = removeSpaces(file_title.title().replace("Российской Федерации", " "))


zlibFile = open(ofile, 'wb')


VERSION = 1
zlibFile.write(VERSION.to_bytes(2, "little")) #Записываем первые 2 байта - версия архива
            
OFFSET_POS = zlibFile.tell()
zlibFile.write(b"\x00" * 4) #Резервируем для ссылки на блок упакованного файла, перед ним 4 байта длина оригинальных данных

bTitle = _tmp["title"].encode()
bTitleSize = len(bTitle).to_bytes(2, "little")
zlibFile.write(bTitleSize) #Пишем длину имени кодекса
zlibFile.write(bTitle) #Пишем имя кодекса

bTime = creationTime.to_bytes(8, 'little')
zlibFile.write(bTime) #Записываем время создания

__fileName, ext = splitext(basename(ifile))
icon_name = "codex_icons/"+__fileName+".png"
if exists(icon_name):
    picture = open(icon_name, 'rb').read()
    zlibFile.write(len(picture).to_bytes(4, 'little'))
    zlibFile.write(picture)
else:
    zlibFile.write(b"\x00" * 4) #Если иконки нет, 4-байтный ноль

offset = zlibFile.tell()
zlibFile.write(file_stat.st_size.to_bytes(4, 'little'))
zlibFile.write(zipped)
zlibFile.seek(OFFSET_POS)
zlibFile.write(offset.to_bytes(4, 'little'))

zlibFile.close()
