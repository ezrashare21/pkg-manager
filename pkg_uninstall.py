from zipfile import ZipFile
from pathlib import Path as path_lib
import os

def cleanDir(input_):
    print("clearing files....")
    
    for root, dirs, files in os.walk(input_):
     for name in files:
      print(os.path.join(root, name))
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
    
    print(dirsToDelete)
    
    for x in dirsToDelete:
        try:
            os.rmdir(x)
        except NotADirectoryError:
            os.remove(x)
    

print("getting data...")

#extract main
with ZipFile("pkg.zip", "r") as zip:
    data = zip.extract("data.txt")
    data = open("data.txt")
    
    filesNum = int(data.read())
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

def removeNS(input_):
    output_ = []
    
    num = 0
    
    for x in input_:
        num += 1
        if num != len(input_):
            number = 0
            string = ""
            while number != len(x) - 1:
                number += 1
                string = string + x[number - 1]
            output_.append(string)
        else:
            output_.append(x)
    return(output_)

downloadfiledata = []

for x in files:
    with ZipFile("pkg.zip", "r") as zip:
        try:
            isFile = True
            doNothing = False
            data = zip.extract(str(x) + "/data.txt")
        except KeyError:
            isFile = False
            doNothing = False
            try:
                data = zip.extract(str(x) + "/folder.txt")
                os.rename(str(x) + "/folder.txt", str(x) + "/data.txt")
            except KeyError:
                doNothing = True
        
        if doNothing == False:
            
            data = open(str(x) + "/data.txt")
            
            filedata = data.readlines()
            
            print(filedata)
            if isFile:
                filedata = removeNS(filedata)
                
                filedata.append(str(x) + "/file." + filedata[1])
                filedata.append(x)
                
                downloadfiledata.append(filedata)
                
                os.remove(str(x) + "/data.txt")
                os.rmdir(str(x))
            else:
                downloadfiledata.append(filedata)
                os.remove(str(x) + "/data.txt")
                os.rmdir(str(x))
            
            print(filedata)
        else:
            print("did nothing")

print(downloadfiledata)

print("ordering lists...")

output = []

with ZipFile("pkg.zip", "r") as zip:
    zip.extract("uninstall.txt")
    makeFile = open("uninstall.txt")
    makeFile = makeFile.readlines()
    makeFile = removeNS(makeFile)

for x in makeFile:
    x = int(x)
    
    output.append(downloadfiledata[x - 1])
    print(x)

print(output)

downloadfiledata = list(output)

print("uninstalling pkg...")

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

for x in downloadfiledata:
    if len(x) == 1:
        print(x)
        try:
            x[0] = formatPath(x[0])
            cleanDir(x[0])
            os.rmdir(x[0])
        except FileNotFoundError:
            print("could not remove folder:" + x[0])
        print(x[0])
    else:
        filename = x[0]
        print(filename)
        extension = x[1]
        print(extension)
        install = formatPath(x[2])
        print(install)
        zipLocation = x[3]
        print(zipLocation)
        number = x[4]
        print(number)
        
        if len(x[1]) == 0:
            mainFile = install + "/" + filename
        else:
            mainFile = install + "/" + filename + "." + extension
        
        try:
            os.remove(mainFile)
        except FileNotFoundError:
            print("could not remove file: " + mainFile)

os.remove("uninstall.txt")