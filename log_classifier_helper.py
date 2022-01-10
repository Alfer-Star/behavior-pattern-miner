def getDivisionNameClassifier(event):
    return event['division'] +"_"+ event["concept:name"][:5]

def addDivisionClassifier(log, classifier):
    for trace in log:
        for event in trace:
            event[classifier] = getDivisionNameClassifier(event)

def addDivisionLifecyleTransClassifier(log, classifier):
    for trace in log:
        for event in trace:
            event[classifier] = getDivisionNameClassifier(event) +'_'+ event["lifecycle:transition"]
