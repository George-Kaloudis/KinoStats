import urllib
import xmltodict
import os.path
import time
import socket
from xml.etree.ElementTree import parse

numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lnum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
drawNo = 0
Conection = True

#I

def internet(host="8.8.8.8", port=53, timeout=5):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print ex.message
        return False

def loadData():
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
                time.sleep(2)
            

def resultprint(nr):
    numbers[nr - 1] = numbers[nr - 1] + 1


def monitor():
    u = urllib.urlopen('http://applications.opap.gr/DrawsRestServices/kino/last.xml')
    doc = xmltodict.parse(u)
    results = doc['draw']['result']
    i=0
    while i<20 :
        lnum[i] = int(results[i])
        resultprint(lnum[i])
        i = i + 1
    

def showresults():
    j=0
    while j<80 :
        print j + 1, ":", numbers[j]
        j = j + 1
    print "-"*50


def saveData():
    file = open("kino.txt","w")
    j=0
    while j<80 :
            file.write(str(numbers[j]))
            file.write(" ")
            j = j + 1
    file.write(str(drawNo))
    file.close()


loadData()
while True:
    try:
        internet()
        Conection = internet()
        if Conection == True:
            monitor()
            drawNo = drawNo + 1
            showresults()
            saveData()
            time.sleep(300)
        else:
            print 'No conection to the internet'
            print 'Trying again...'
            time.sleep(10)
    except KeyboardInterrupt:
        break