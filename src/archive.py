#! /usr/bin/env python3

import os, sys, re

def addTitle(srcName, resFile):
    titleSize = len(srcName.encode())
    resFile.write(f'TitleSize: {titleSize}\n'.encode())
    resFile.write(f'Title: {srcName}\n'.encode())

def addContents(srcName, srcFile, resFile):
    contentsSize = os.stat(srcName).st_size
    resFile.write(f'ContentsSize: {contentsSize}\n'.encode())
    resFile.write(f'Contents:\n'.encode())
    resFile.write(os.read(srcFile, contentsSize))
    
def storeFile(srcName, resFile):
    try:
        srcFile = os.open(srcName, os.O_RDONLY)
        addTitle(srcName, resFile)
        addContents(srcName, srcFile, resFile)
        os.close(srcFile)
    except OSError:
        os.write(1, (f"File {srcName} was not found.\n").encode())
        return

def main():
    # Opening output file
    with open("output",'ab') as resFile:
        for source in sys.argv[1:]:
            storeFile(source, resFile)
    

if __name__ == "__main__":
    main()

"""
Suggested methods:
writeByteArray(fd, byteArray)
readByteArray(fd)
"""
