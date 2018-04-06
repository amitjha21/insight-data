import sys
import datetime

timestampFormat = "%Y-%m-%d %H:%M:%S"  #global constant

def getInactivityValue(path):    # get inactivity_period
    inactiveFile = open(path, 'r')
    return int(inactiveFile.read())

def getLogData(path):        # get initial log file
    initialLogFile  = open(path, 'r')
    logList = initialLogFile.readlines()
    logList.pop(0)   # remove header from the data list
    initialLogFile.close()
    return logList

def getTimeDiff(op1,op2):
    return int((datetime.datetime.strptime(op2, timestampFormat) - datetime.datetime.strptime(op1, timestampFormat)).total_seconds())

def writeOutputContent(path):    # write output to file
    try:
        outputWriter = open(path, 'w')
    except:
        print('Supply a valid path')
        exit(1)
    return outputWriter


def getUserLogResults(logFilePath, inactivityPeriodFilePath, outputFilePath):

    activeIpList = []
    sortedIpList = []
    ipCollectDict = dict()

    inactivity_period = getInactivityValue(inactivityPeriodFilePath)
    logs = getLogData(logFilePath)
    writeToFile = writeOutputContent(outputFilePath)

    for log in logs:
        log = [x.strip() for x in log.split(',')]
        ip = log[0]
        initialStartTime = log[1]+' '+log[2]
        
        timestamp = datetime.datetime.strptime(initialStartTime, timestampFormat)
        currentTime = initialStartTime

        while sortedIpList:
            userIP = sortedIpList[0]

            if (timestamp - ipCollectDict[userIP]['sessionEndTime']).total_seconds() > inactivity_period:
                values = ipCollectDict.pop(userIP)
                sortedIpList.remove(userIP)
                activeIpList.remove(userIP)

                sessionStart = datetime.datetime.strftime(values['sessionStartTime'], timestampFormat)
                sessionEnd = datetime.datetime.strftime(values['sessionEndTime'], timestampFormat)
                writeToFile.write('%s,%s,%s,%d,%d\n' % (userIP, sessionStart, sessionEnd, getTimeDiff(sessionStart, sessionEnd) + 1,values['docsAccessed']))
            else:
                break

        if ip not in activeIpList:
            activeIpList.append(ip)
            ipCollectDict[ip] = {'sessionStartTime': timestamp, 'sessionEndTime': timestamp, 'docsAccessed': 1}
            sortedIpList.append(ip)

        else:
            ipCollectDict[ip]['sessionEndTime'] = timestamp
            ipCollectDict[ip]['docsAccessed'] += 1    # update document accessed count by 1
            sortedIpList.remove(ip)
            sortedIpList.append(ip)

    while len(activeIpList) > 0:  # write all remaining requests
        userIP = activeIpList.pop(0)
        values = ipCollectDict.pop(userIP)

        sessionStart = datetime.datetime.strftime(values['sessionStartTime'], timestampFormat)
        sessionEnd = datetime.datetime.strftime(values['sessionEndTime'], timestampFormat)
        writeToFile.write('%s,%s,%s,%d,%d\n' % (userIP, sessionStart, sessionEnd, getTimeDiff(sessionStart, sessionEnd) + 1, values['docsAccessed']))
        sortedIpList.remove(userIP)

    writeToFile.close()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Pass all required parameters: " + str(len(sys.argv)))
        exit(1)

    getUserLogResults(sys.argv[1], sys.argv[2], sys.argv[3])
