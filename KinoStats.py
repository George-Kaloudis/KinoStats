'''
KinoStats
'''
import urllib
import xmltodict
import os.path
import time
import socket
from xml.etree.ElementTree import parse

numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lnum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
drawNo = 0
Connection = True
LastDraw=0


#This function checks to see if you have connection to the internet
def internet(host="8.8.8.8", port=53, timeout=5):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print ex.message
        return False


#This function loads previous data, if it exists
def loadData():
    global LastDraw
    global drawNo
    global numbers
    j = 0
    if os.path.exists("kino.txt"):
        with open("kino.txt", "r") as f:
            data = f.read()
            load = data.split()
            while j<80 :
                numbers[j] = int(load[j])
                j = j + 1
            if j == 80:
                drawNo = int(load[j])
                print "Data loaded!"
                j = j + 1
                LastDraw = int(load[j])
                time.sleep(2)


#This function saves your data
def saveData():
    file = open("kino.txt","w")
    j=0
    while j<80 :
            file.write(str(numbers[j]))
            file.write(" ")
            j = j + 1
    file.write(str(drawNo))
    file.write(" ")
    file.write(str(LastDraw))
    file.close()


#This function adds a counter for the numbers in the draw    
def addCounter(nr):
    numbers[nr - 1] = numbers[nr - 1] + 1


#This function contacts the internet page to get the draw numbers
def getDraw():
    global LastDraw
    u = urllib.urlopen('http://applications.opap.gr/DrawsRestServices/kino/last.xml')
    doc = xmltodict.parse(u)
    if LastDraw!=int(doc['draw']['drawNo']):
        results = doc['draw']['result']
        LastDraw = int(doc['draw']['drawNo'])
        i=0
        while i<20 :
            lnum[i] = int(results[i])
            addCounter(lnum[i])
            i = i + 1
    else:
        print 'This draw has been already stated\nTrying again...'
        time.sleep(10)
        getDraw()
            

#This fuction show the current percentage of each number
def showresults():
    j=0
    while j<80 :
        percent = numbers[j] / float(drawNo) * 100
        print j + 1, ":","{0:.2f}".format(percent), "%"
        j = j + 1
    print "-"*50


#This function loads as much draws requested from the website instead of loading your last data. It overrides your last data but then keeps working normally
#def loadHistoryDraws(amount):



    
'''
This is the main structure of the program
'''

loadData()
while True:
    try:
        Connection = internet()
        if Connection == True:
            getDraw()
            drawNo = drawNo + 1
            showresults()
            saveData()
            time.sleep(300)
        else:
            print 'No connection to the internet\nTrying again...'
            time.sleep(10)
    except KeyboardInterrupt:
        break

print 'Program finished'
