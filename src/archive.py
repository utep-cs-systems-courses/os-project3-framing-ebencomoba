#! /usr/bin/env python3

import os, sys, re

def addTitle(srcName, resFile):
    titleSize = len(srcName.encode())
    resFile.write('{:0>8}'.format(titleSize).encode())
    resFile.write(f'{srcName}'.encode())

def addContents(srcName, srcFile, resFile):
    contentsSize = os.stat(srcName).st_size
    resFile.write('{:0>28}'.format(contentsSize).encode())
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
