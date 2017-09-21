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
LastDraw = 0
uniqueDraw = True
mode = 0
modechange = '0'


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
    results = doc['draw']['result']
    LastDraw = int(doc['draw']['drawNo'])
    i = 0
    print '-' * 50
    print 'Winning Numbers:'
    while i<20 :
        lnum[i] = int(results[i])
        addCounter(lnum[i])
        print lnum[i]
        i = i + 1
    print '-' * 50
    
    
#This function checks to see if the current draw is the same with the last one            
def checkLastDraw():
    global LastDraw
    u = urllib.urlopen('http://applications.opap.gr/DrawsRestServices/kino/last.xml')
    doc = xmltodict.parse(u)
    if LastDraw!=int(doc['draw']['drawNo']):
        return True
    else:
        return False
        

#This fuction show the current percentage of each number
def showresults():
    global drawNo
    print 'Showing result for', drawNo, 'draws.'
    time.sleep(2)
    print '-' * 50
    j=0
    while j<80 :
        percent = numbers[j] / float(drawNo) * 100
        print j + 1, ":","{0:.2f}".format(percent), "%"
        j = j + 1
    print "-" * 50


#This function loads as much draws requested from the website instead of loading your last data. It overrides your last data but then keeps working normally
def loadHistoryDraws(amount=100):
    global LastDraw
    global drawNo
    drawNo = amount
    u = urllib.urlopen('http://applications.opap.gr/DrawsRestServices/kino/last.xml')
    doc = xmltodict.parse(u)
    LastDraw = int(doc['draw']['drawNo'])
    i = 0
    while i < amount :
        FirstDraw = LastDraw - amount + 1 + i
        FirstDrawStr = str(FirstDraw)
        opapUrl = 'http://applications.opap.gr/DrawsRestServices/kino/' + FirstDrawStr + '.xml'
        usite = urllib.urlopen(opapUrl)
        docsite = xmltodict.parse(usite)
        results = docsite['draw']['result']
        rNo= i + 1
        print rNo, 'Out of', amount
        i = i + 1
        j = 0
        while j<20 :
            lnum[j] = int(results[j])
            addCounter(lnum[j])
            j = j + 1
    print '-' * 50
        
        
'''
This is the main structure of the program
'''

print 'Welcome to KinoStats!'
mode = raw_input('Would you like to monitor the draws live or download previous results?\nExample: last 100 results, the amount is asked.\nIf you choose download mode you can continue monitoring after if you want\n(1 for monitor mode, 2 for download mode)\n')
if mode == '2':
    amount = raw_input('How many draws would you like to load?(If you do not enter a value it will be set as default, which is 100)')
    if amount == "":
        amount = 100
    amount = int(amount)
    
    while True:
        try:    
            Connection = internet()
            if Connection == True:
                print 'Connected to the internet.'
                loadHistoryDraws(amount)
                showresults()
                saveData()
                break
            else:
                print 'No connection to the internet\nTrying again...'
                print '-' * 50
                time.sleep(10)
                
        except KeyboardInterrupt:
            break

    modechange = raw_input('Would you like to continue monitoring?(1 for Yes,2 for No)\n')
    if modechange == '1':
        mode = '1'
    
    
if modechange == '0':
    loadData()

if mode == '1':
    while True:
        try:
            Connection = internet()
            if Connection == True:
                uniqueDraw = checkLastDraw()
                print 'Connected to the internet.'
                if uniqueDraw == True:
                    getDraw()
                    drawNo = drawNo + 1
                    showresults()
                    saveData()
                    time.sleep(300)
                else:
                    print 'This draw has been already stated\nTrying again...'
                    print '-' * 50
                    time.sleep(20)
            else:
                print 'No connection to the internet\nTrying again...'
                print '-' * 50
                time.sleep(10)
        except KeyboardInterrupt:
            break

print 'Program finished'
