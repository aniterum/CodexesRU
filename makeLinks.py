#!/usr/bin/env python3
#<links EXTRA="">
'''
<codex date="1473712860"
       name="civil_proc.xml.zlib"
       packed="163767"
       size="1061980"
       title="Гражданский Процессуальный Кодекс"/>
'''
import os, sys
import testZlib
from xml.etree import ElementTree as ET
    
parsed_dir = "laws_zlib/"

links = ET.Element("links")

for root, dirs, files in os.walk(parsed_dir):
    for file in files:
        fullName = parsed_dir + file
        codex = ET.Element("codex")
        links.append(codex)
        attrs = testZlib.testFile(fullName)
        for attr in attrs:
            codex.set(attr, str(attrs[attr]).strip())
            
tree = ET.ElementTree(links)
tmpFile = "/tmp/tmp_xml.xml"

try:
    tree.write(tmpFile, encoding="utf-8", xml_declaration=True)

    command = 'xmllint -format  "%s" > "%s"'
    os.system(command % (tmpFile, 'links.xml'))
except:
    ET.dump(links)
