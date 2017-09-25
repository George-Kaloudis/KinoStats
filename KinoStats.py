'''
KinoStats
'''
import urllib
import xmltodict
import os.path
import time
import socket
from xml.etree.ElementTree import parse

numbers = [0] * 80
lnum = [0] * 20
ranks = list()
drawNo = 0
Connection = True
LastDraw = 0
uniqueDraw = True
mode = '0'
modechange = '0'
datenow = time.asctime()

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
                j += 1
            if j == 80:
                drawNo = int(load[j])
                print "Data loaded!"
                j += 1
                LastDraw = int(load[j])
                time.sleep(2)


#This function saves your data
def saveData():
    file = open("kino.txt","w")
    j=0
    while j<80 :
            file.write(str(numbers[j]))
            file.write(" ")
            j += 1
    file.write(str(drawNo))
    file.write(" ")
    file.write(str(LastDraw))
    file.close()


#This function adds a counter for the numbers in the draw    
def addCounter(nr):
    numbers[nr - 1] += 1


#This function contacts the internet page to get the draw numbers
def getDraw():
    global LastDraw
    global amount
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
        i += 1
    if modechange == '3':
        logger(ranks, amount, 6)
        logger(ranks, amount, 9)
        logger(ranks, amount, 7)
    
    
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
def showResults():
    global drawNo
    print 'Showing result for', drawNo, 'draws.'
    time.sleep(2)
    print '-' * 50
    j=0
    while j<80 :
        percent = numbers[j] / float(drawNo) * 100
        print j + 1, ":","{0:.2f}".format(percent), "%"
        j += 1
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
        i += 1
        j = 0
        while j<20 :
            lnum[j] = int(results[j])
            addCounter(lnum[j])
            j += 1
    print '-' * 50
        
        
#This function sort the list and shows the top values. The default value is 10
def rankResults(a ,b=12):
    global ranks
    rankOrder = [0] * len(a)
    rankValues = [0] * len(a)
    for i in range(0,len(a)-1):
        rankValues[i] = a[i]
    k = 0
    while k < len(a):
        rankOrder[k] = k + 1
        k += 1
    for i in range(0, len(a) - 1):
        for j in range(len(a) - 1, i, -1):
            if rankValues[j-1] < rankValues[j]:
                temp = rankValues[j-1]
                rankValues[j-1] = rankValues[j]
                rankValues[j] = temp
                temp = rankOrder[j-1]
                rankOrder[j-1] = rankOrder[j]
                rankOrder[j] = temp
    m=0
    print '-' * 50
    print 'The Top', b, 'numbers in the lottery are:'
    print '-' * 50
    while m < b:
        percent = rankValues[m] / float(drawNo) * 100
        print m + 1,':', rankOrder[m], '-',"{0:.2f}".format(percent), '%'
        m += 1
    ranks = rankOrder
        
        
#This function deletes the first entry if there is a new one keeping the amount the same
def fixedNumberMonitor():
    global amount
    global LastDraw
    u = urllib.urlopen('http://applications.opap.gr/DrawsRestServices/kino/last.xml')
    doc = xmltodict.parse(u)
    RemovedDraw = LastDraw - amount
    RemovedDrawStr = str(RemovedDraw)
    opapUrl = 'http://applications.opap.gr/DrawsRestServices/kino/' + RemovedDrawStr + '.xml'
    usite = urllib.urlopen(opapUrl)
    docsite = xmltodict.parse(usite)
    results = docsite['draw']['result']
    j = 0
    while j<20 :
        lnum[j] = int(results[j])
        remCounter(lnum[j])
        j += 1
    print '-' * 50


#This function removes a counter
def remCounter(nr):
    numbers[nr - 1] -= 1
    
    
#This function takes a list and makes a dictionary counting the occurance of values
def histogram(damount, tnfirst):
    global datenow
    name = str(datenow) + str(tnfirst) + str(damount)
    ofn = open(name, "r")
    st2 = ofn.read()
    s = st2.split()
    ofn.close()
    d = dict()
    for c in s:
        if c not in d:
            d[c] = 1
        else:
            d[c] += 1
    ofn = open(name, "w")
    ofn.write(str(d))
    ofn.close()
    
    
def logger(lista, damount, tnfirst):
    global datenow
    amList = [0] * tnfirst 
    name = str(datenow) + str(tnfirst) + str(damount)
    file = open(name, "a")
    i = 0
    while i < tnfirst:
        amList[i] = lista[i]
        i += 1
    j = 0
    for c in lnum:
        if c in amList:
            j += 1
    file.write(' ')
    file.write(str(j))
    file.close()
        
        
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
                showResults()
                rankResults(numbers)
                saveData()
                break
            else:
                print 'No connection to the internet\nTrying again...'
                print '-' * 50
                time.sleep(10)
                
        except KeyboardInterrupt:
            break

    modechange = raw_input('Would you like to continue monitoring?(1 for Yes,2 for No, 3 for fixed amount monitoring)\n')
    if modechange == '1' or modechange == '3':
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
                    if modechange == '3':
                        fixedNumberMonitor()
                        drawNo -= 1
                    drawNo += + 1
                    showResults()
                    rankResults(numbers)
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

print 'Gathering finished'

topAmount = raw_input('How many top numbers do you want to view?(Number)\n')
topAmount = int(topAmount)
rankResults(numbers, topAmount)
histogram(amount, 6)
histogram(amount, 9)
histogram(amount, 7)
