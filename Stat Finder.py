mainFolder = "C:\\KinoStats\\"
import time
import os
subFolders = list(list())

next(os.walk(mainFolder))[1] #Folders
next(os.walk(mainFolder))[2] #Files


subFolders = next(os.walk(mainFolder))[1]
secondFolders=[0] * (subFolders.__len__())


j = 0
for i in subFolders:
    secondFolders[j]=mainFolder + i
    j += 1

    
print(secondFolders)
time.sleep(10)
