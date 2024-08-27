import os
import logging
from findAlgo import m4aFinder

def selection(CSVdirLoc, args):
    if os.path.exists(CSVdirLoc):
        fileList = os.listdir(CSVdirLoc)
    else:
        print("Error, no playlist files found, exiting\n")
        exit(1)
    file = ""
    fileList.sort()
    while True:
        for num, f in enumerate(fileList):
            print(str(num + 1) + ". " + f)
        if args.select == 0:
            selection = "all" if args.a else input("\nPlease input a playlist number to convert,"
                          "\n\tif you wish to convert all files,"
                          "\n\tplease type 'all'\n")
        else:
            selection = args.select
        if isinstance(selection, str) and selection.lower() == "all":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Converting " + str(len(fileList)) + " files")
            return fileList
        elif isinstance(selection, str) and selection.isdigit() or isinstance(selection, int):
            for num, f in enumerate(fileList):
                if (int(selection) - 1) == num:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Converting only " + f)
                    file = f
                    return file
        else:
            print("\nUser input did not match expected. \n\n\tError. \n\nPlease try again.")

def Playlist_Extraction(playlistLoc, pathToMusic, fileName, playlistSaveLoc):
    logging.debug(f"Playlist extracting with args: {playlistLoc}, {pathToMusic}, {fileName}")
    fileName = fileName.strip()
    try:
        if os.path.getmtime(playlistLoc + fileName) < os.path.getmtime(playlistSaveLoc + fileName.replace("txt", "m3u8")):
            with open(playlistLoc + fileName) as thing1:
                with open(playlistSaveLoc + fileName.replace("txt", "m3u8")) as thing2:
                    count = sum(1 for _ in thing1) - 2
                    count -= sum(1 for _ in thing2)
                    if count == 0:
                        return count
    except:
        pass
    playlist = []
    playlist.append(fileName)
    artistDirs = os.listdir(pathToMusic)
    artistDirs.sort()
    with open(playlistLoc + fileName) as file:
        count = sum(1 for _ in file)
        file.seek(0)
        for num, line in enumerate(file, start=-1):
            if num <= 1:
                pass
            else:
                print(f"{int((num/count)*100)}%", end="\r")
                splitLine = line.split(",,")
                artistName = splitLine[1]
                albumName = splitLine[2]
                songName = splitLine[3].replace("\n","")
                toAppend = m4aFinder(artistName, albumName, songName, artistDirs, pathToMusic)
                if toAppend is None: logging.error(f"Missing music: %s / %s / %s\n\n", artistName, albumName, songName)
                playlist.append(toAppend)

    return playlist