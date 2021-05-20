from zipfile import ZipFile
from pathlib import Path as path_lib
import os

#
# MIT License
#
# Copyright (c) 2021 ezrashare21
#

print("getting data...")

# the most useful code snippet in the world

def cleanDir(input_):
    
    for root, dirs, files in os.walk(input_):
     for name in files:
      os.remove(os.path.join(root, name))
    
    
    dirsFound = []
    for root, dirs, files in os.walk(input_):
        for name in dirs:
            dirsFound.append(os.path.join(root, name))
    
    
    dirsToDelete = []
    
    num = len(dirsFound) - 1
    while num != -1:
        dirsToDelete.append(dirsFound[num])
        num = num - 1
    
    
    for x in dirsToDelete:
        try:
            os.rmdir(x)
        except NotADirectoryError:
            os.remove(x)

def removeNS(input_):
    output_ = []
    number = 0
    num = 0
    
    print("rmns")
    for x in input_:
        num += 1
        
        print(num)
        print(len(input_))
        if num != len(input_):
            number = 0
            string = ""
            while number != len(x) - 1:
                number += 1
                string = string + x[number - 1]
            output_.append(string)
        else:
           output_.append(x) 
    print("end")
    return(output_)

#extract main
with ZipFile("pkg.zip", "r") as zip:
    data = zip.extract("data.txt")
    data = open("data.txt")
    
    filesList = removeNS(data.readlines())
    
    filesNum = int(filesList[0])
    print(filesNum)
    
    data.close()
    
    os.remove("data.txt")

print("creating list...")

number = 0
files = []
while number != filesNum:
    number += 1
    files.append(number)

print(len(files))

print("getting data...")

downloadfiledata = []

for x in files:
    with ZipFile("pkg.zip", "r") as zip:
        try:
            isFile = True
            custom = ""
            isCustom = False
            data = zip.extract(str(x) + "/data.txt")
        except KeyError:
            try:
                data = zip.extract(str(x) + "/folder.txt")
                os.rename(str(x) + "/folder.txt", str(x) + "/data.txt")
                isFile = False
            except KeyError:
                data = zip.extract(str(x) + "/custom.txt")
                isFile = False
                os.rename(str(x) + "/custom.txt", str(x) + "/data.txt")
                isCustom = True
        
        data = open(str(x) + "/data.txt")
        
        filedata = data.readlines()
        
        if isCustom:
            custom = filedata[0]
        
        print(filedata)
        if isFile:
            filedata = removeNS(filedata)
            print(filedata)
            
            filedata.append(str(x) + "/file." + filedata[1])
            filedata.append(x)
            
            downloadfiledata.append(filedata)
            
            os.remove(str(x) + "/data.txt")
            os.rmdir(str(x))
        elif isFile == False and isCustom == False:
            downloadfiledata.append(filedata)
            os.remove(str(x) + "/data.txt")
        else:
            if custom == "script-python":
                downloadfiledata.append(["custom", "py-scpt", x])
        
        print(filedata)

print(downloadfiledata)

print("installing pkg...")

def formatPath(path):
    number = -1
    string = ""
    for x in path:
        number += 1
        if path[number - 1] != "\\" and path[number] == "~":
            string = string + str(path_lib.home())
        else:
            string = string + path[number]
    print(string)
    return(string)

def moveFile(path, moveTo):
    moveTo = formatPath(moveTo)
    os.system("mv \"" + path + "\" \"" + moveTo + "\"")

def makeFolder(folder):
    folder = formatPath(folder)
    os.system("mkdir -p \"" + folder + "\"")

for x in downloadfiledata:
    if len(x) == 1:
        try:
            makeFolder(x[0])
            print("installed")
        except FileExistsError:
            print("folder failed to install")
    elif x[0] == "custom":
        if x[1] == "py-scpt":
            with ZipFile("pkg.zip", "r") as zip:
                zip.extract(str(x[2]) + "/scpt.py")
            
            os.system("python3 " + str(x[2]) + "/scpt.py")
    else:
        if len(x[1]) == 0:
            mainFile = str(x[4]) + "/" + x[0]
        else:
            mainFile = "file: " + x[2] + "/" + x[0] + "." + x[1]
        
        print(mainFile)
        
        if os.path.isfile(mainFile):
            print("file failed to install")
        else:
            filename = x[0]
            print(filename)
            extension = x[1]
            print(extension)
            install = x[2]
            print(install)
            zipLocation = x[3]
            print(zipLocation)
            number = x[4]
            print(number)
            
            with ZipFile("pkg.zip", "r") as zip:
                zip.extract(str(number) + "/file." + extension)
                if len(extension) == 0:
                    mainFile = str(number) + "/" + filename
                else:
                    mainFile = str(number) + "/" + filename + "." + extension
                
                os.rename(str(number) + "/file." + extension, mainFile)
                
                moveFile(mainFile, install)

for x in files:
    try:
        cleanDir(str(x))
        os.rmdir(str(x))
    except FileNotFoundError:
        print("...")
    except OSError:
        print("osError")
