import os
import logging

def m4aFinder(artist, album, name, pathToMusic):

    logging.info("\n Searching for Artist: " + artist + " Album: " + album + " Song: " + name)

    dirList = os.listdir(pathToMusic)

    dirList = dirList.sort()

    for i in dirList:
        print(i)