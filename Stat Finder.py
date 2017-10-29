mainFolder = "C:\\KinoStats\\"
import time
import os
subFolders = list()
thirdFolders = list()
folders = list()
tfiles = list()
files = list()
next(os.walk(mainFolder))[1] #Folders
next(os.walk(mainFolder))[2] #Files


subFolders = next(os.walk(mainFolder))[1]
secondFolders=[0] * (subFolders.__len__())


for index, i in enumerate(subFolders):
    secondFolders[index]=mainFolder + i

for i in secondFolders:
    folders = next(os.walk(i))[1]
    if folders.__len__() == 0:
        thirdFolders.append(i)
    else:    
        for k in folders:
            thirdFolders.append(i + "\\" + k)
			
 

for i in thirdFolders:
	tfiles = next(os.walk(i))[2]
	if tfiles.__len__() != 0:
		for file in tfiles:
			files.append(i + "\\" + file)
	
print(files)   

time.sleep(10)
