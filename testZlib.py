#!/usr/bin/env python3

import zlib, os, sys
from os.path import exists, basename
from PIL import Image
from io import BytesIO

zlib_dir = "laws_zlib"

bytesToInt = lambda x: int.from_bytes(x, "little")

def testPicture(picture, verbose):
    if verbose:
        print("    Test Picture Size", len(picture))
    picBuf = BytesIO()
    picBuf.write(picture)
    picBuf.seek(0)
    img = Image.open(picBuf)
    if verbose:
        print("    Icon Picture OK!")
    

   

def testFile(filePath, verbose=False):
    if verbose:
        print(filePath)
    file = open(filePath, "rb")
    version = bytesToInt(file.read(2))
    if verbose:
        print("    Version", version)
    offset = bytesToInt(file.read(4))
    titleSize = bytesToInt(file.read(2))
    title = file.read(titleSize).decode()
    if verbose:
        print("    Title", title)
    date = bytesToInt(file.read(8))
    if verbose:
        print("    Date", date)
    picSize = bytesToInt(file.read(4))
    if picSize != 0:
        picture = file.read(picSize)
        testPicture(picture, verbose)
    else:
        if verbose:
            print("    --> No Icon", filePath)
        
    file.seek(0)

    file.seek(offset)
    origSize = bytesToInt(file.read(4))
    zlibbed = file.read()

    origFile = zlib.decompress(zlibbed)
    if origSize != len(origFile):
        if verbose:
            print("!!!!Orig size not equalent!")
    else:
        if verbose:
            print("    Zlib Test OK!")

    return {"version":version,
            "title":title,
            "date":date,
            "size":len(origFile),
            "packed":os.stat(filePath).st_size,
            "name":basename(filePath)}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Неверное число параметров")

    ifile = sys.argv[1]
    if not exists(ifile):
        print("Входящий файл %s не найден" % ifile)

    testFile(ifile, True)


