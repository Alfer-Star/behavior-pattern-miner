def getDivisionNameClassifier(event):
    return event['division'] +"_"+ event["concept:name"][:5]

def addDivisionClassifier(log, classifier):
    for trace in log:
        for event in trace:
            event[classifier] = getDivisionNameClassifier(event)


def addRessourceClassifier(log, classifier):
    index = 0
    readableRessDict = dict()
    for trace in log:
        for event in trace:
            ress = event['org:resource']
            if ress not in readableRessDict:
                readableRessDict[ress] = 'M'+ str(index)
                index += 1
            event[classifier] = readableRessDict[ress] +"_"+ event["concept:name"][:5]

def addDivisionLifecyleTransClassifier(log, classifier):
    for trace in log:
        for event in trace:
            event[classifier] = getDivisionNameClassifier(event) +'_'+ event["lifecycle:transition"]
