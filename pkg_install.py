from zipfile import ZipFile
import os

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

downloadfiledata = []

for x in files:
    with ZipFile("pkg.zip", "r") as zip:
        try:
            isFile = True
            data = zip.extract(str(x) + "/data.txt")
        except KeyError:
            isFile = False
            data = zip.extract(str(x) + "/folder.txt")
            os.rename(str(x) + "/folder.txt", str(x) + "/data.txt")
        
        data = open(str(x) + "/data.txt")
        
        filedata = data.readlines()
        
        print(filedata)
        if isFile:
            filedata = removeNS(filedata)
            print(filedata)
            
            filedata.append(str(x) + "/file." + filedata[1])
            filedata.append(x)
            
            downloadfiledata.append(filedata)
            
            os.remove(str(x) + "/data.txt")
            os.rmdir(str(x))
        else:
            downloadfiledata.append(filedata)
            os.remove(str(x) + "/data.txt")
        
        print(filedata)

print(downloadfiledata)

print("installing pkg...")

def moveFile(path, moveTo):
    os.system("mv \"" + path + "\" \"" + moveTo + "\"")

for x in downloadfiledata:
    if len(x) == 1:
        try:
            os.mkdir(x[0])
            print("installed")
        except FileExistsError:
            print("folder failed to install")
    else:
        if os.path.isfile(x[2] + "/" + x[0] + "." + x[1]):
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
                
                mainFile = str(number) + "/" + filename + "." + extension
                
                os.rename(str(number) + "/file." + extension, mainFile)
                
                moveFile(mainFile, install)

for x in files:
    try:
        os.rmdir(str(x))
    except FileNotFoundError:
        print("...")
