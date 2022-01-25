def getDivisionNameClassifier(event):
    return event['division'] + "_" + event["concept:name"]

def addDivisionClassifier(log, classifier):
    for trace in log:
        for event in trace:
            event[classifier] = getDivisionNameClassifier(event)

def getDivisionNameCutClassifier(event, maxchars =10):
    return event['division'] + "_" + event["concept:name"][:maxchars].strip()

def addDivisionClassifierNoDuplicate(log, classifier, maxchars = 10):
    createdSynonym = dict()
    for trace in log:
        for event in trace:
            synonym = getDivisionNameCutClassifier(event, maxchars)
            if(synonym in createdSynonym):
                if(event["concept:name"] == createdSynonym[synonym]):
                     event[classifier] = synonym
                else: 
                    index = 2 # faengt bei 2 an, weil 1 würde keine Nummer tragen!
                    while(synonym + str(index) in createdSynonym):
                        if(event["concept:name"] == createdSynonym[synonym]):
                            event[classifier] = synonym + str(index)
                        else:
                            index += 1
                    # fall while Schleife bricht, ab weil für diesen Index gibt es kein duplikat => füge also hinzu 
                    if(synonym + str(index) not in createdSynonym):
                        createdSynonym[synonym] = event["concept:name"]
                        event[classifier] = synonym + str(index)
            else:
                createdSynonym[synonym] = event["concept:name"]
                event[classifier] = synonym


def addRessourceClassifier(log, classifier):
    index = 0
    readableRessDict = dict()
    for trace in log:
        for event in trace:
            ress = event['org:resource']
            if ress not in readableRessDict:
                readableRessDict[ress] = 'M' + str(index)
                index += 1
            event[classifier] = readableRessDict[ress] + \
                "_" + event["concept:name"]


def addDivisionLifecyleTransClassifier(log, classifier):
    for trace in log:
        for event in trace:
            event[classifier] = getDivisionNameClassifier(
                event) + '_' + event["lifecycle:transition"]
