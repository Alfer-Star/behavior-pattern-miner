from src.conformance_with_alignment import sortLogAndModelMove

from src.casual_releation import calculateCR

from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.log.obj import EventLog
from pm4py.objects.log.obj import Trace

from tqdm import tqdm


event_identifier = 'event_identifier'
event_name = 'event_name'
event_ressource = 'event_ressource'

attributes = {event_identifier: 'cdb_process_id',
              event_name: "concept:name", event_ressource: "division"}


# Raw Instance Graph

def genInstanceGraph(trace: Trace, CR, attributeKeys: dict):
    """ Generates Nodes on Edge, in other words from Instace ordering Output """
    try:
        assert(event_name in attributeKeys and event_ressource in attributeKeys)
    except:
        print('attributes need event_identifier, event_name, event_ressource, event keys')
        return

    nodes = {event for event in trace}

    nameExist = set()
    for event in trace:
        label = event[event_ressource] + '_' + event[event_name]
        index = 0
        while(label in nameExist):
            index += 1
            if(index < 1):
                label = label + index
            label = label[:-1]+index
        nameExist.add(label)
        event['BP_label'] = label

    # Casual Relation erfüllt Instance Ordering Eigenschaft
    # dabei bedeutet depth 0, dass es sich um ein direkte nachfolge Beziehung mit keiner anderen Aktivität dazwischen handelt (InstanceOrdering).
    # TODO: CR sorgt, aktuell für gewaltige "Verbindungs Cluster"
    instanceOrdering = {(source, target) for (source, target, depth)
                        in CR if source in plainActivitysInGraph and target in plainActivitysInGraph and depth <= 0}

    edges = {(getBPActivityLabel(sourceEvent, orgaDict, considerLifecycle), getBPActivityLabel(targetEevent, orgaDict, considerLifecycle))
             for sourceEvent in trace for targetEevent in trace if (sourceEvent['concept.name'], targetEevent['concept.name']) in instanceOrdering}

    # Event Mapping, das letzte Auftreten ds events ist für die Aktivität hinterlegt hinterlegt

    return nodes, edges, nodeEventDict


# Reperatur
# Ansatz von Diamantini, C., Genga, L., and Potena, D. 2016. “Behavioral process mining for unstructured processes,” Journal of Intelligent Information Systems (47:1), pp. 5-32 (doi: 10.1007/s10844-016-0394-7)
def getNextEventOfAnotherActivity(trace, index, insertedEventName, nodeEventDict: dict):
    listOfEventsOfSameActivity = next(
        item for key, item in nodeEventDict.items() if key == insertedEventName)
    event = trace[index]
    return next(trace[i] for i in range(index+1, len(trace)) if trace[i] in listOfEventsOfSameActivity)


def repairInsertedEvent(edges_: set[tuple], insertedEventName, trace: Trace, index, nodeEventDict: dict, classifier="concept:name"):
    ''' Entferne alle kanten zwischen zwischen dem Inserted Event und anderen Events, weil irregulär eingefügt '''
    removingEdges = {(source, target) for (
        source, target) in edges_ if source == insertedEventName or target == insertedEventName}
    ''' Füge Event zwischen dem Event, welches nach den Inserted event aufgetreten ist und dessen Vorgänger '''
    eventAppearedAfter = getNextEventOfAnotherActivity(
        trace, index, nodeEventDict)
    aftereventLabel = next(
        key for key, eventList in nodeEventDict.items() if eventAppearedAfter in eventList)
    predecessorOfAfterEvent = {source for (source, target) in edges_
                               if target == aftereventLabel}
    addedEdges = {(source, insertedEventName) for source in predecessorOfAfterEvent}.union(
        {(insertedEventName, aftereventLabel)})
    try:
        assert(len(addedEdges) > 0)
    except:
        print("Keine Kanten für Insertion hinzugefügt!", insertedEventName)

    edges_ = edges_.difference(removingEdges).union(addedEdges)
    ''' Redundant die Kanten welche die Verbindung zwischen dem eventAppearedAfter und predecessorOfAfterEvent darstellen, 
        weil dieses aufgelöst und durch die INsertion ersetzt wurde'''
    redundEdges = {(source, target) for (source, target)
                   in edges_ if source in predecessorOfAfterEvent and target == aftereventLabel}
    edges_.difference_update(redundEdges)
    return edges_


def calculateDeletionCRNodes(correspondingCR, nonDeletionIndex, maxdepth, deletedEventHasCR):
    casualRelItems = set()
    depthIndex = -1
    while(deletedEventHasCR and len(casualRelItems) < 1):
        casualRelItems = {cr[nonDeletionIndex]
                          for cr in correspondingCR if cr[2] <= depthIndex}
        depthIndex += 1
        if(depthIndex > maxdepth):
            print('Repair break loop, after reached max deepness:' + str(maxdepth))
            break
    return casualRelItems


"""
    correspondingPreCR = {
        cr for cr in CR if cr[1]==deletionEventName and cr[0] in nodes }
    {cr[0] for cr in correspondingPreCR if cr[2] == 0}
    depthIndex = 1
    while(casualPredecessor and casualPredecessor):
        casualPredecessor = {cr[0]
            for cr in correspondingPreCR if cr[2] == depthIndex}
        depthIndex += 1
        if(depthIndex < maxdepth):
            print('Repair break loop, after '+ \
                  str(maxdepth)+ ' failed iterations')
            break

    correspondingSucCR = {
        cr for cr in CR  if cr[0]== deletionEventName and cr[1] in nodes}
    casualSuccessor = {cr[1] for cr in correspondingSucCR if cr[2]<= 0}
    depthIndex = 1
    while(deletedEventHasCR and casualPredecessor):
        casualPredecessor = {cr[1]
            for cr in correspondingSucCR if cr[2]<= depthIndex}
        depthIndex += 1
        if(depthIndex < maxdepth):
            print('Repair break loop, after '+ \
                  str(maxdepth)+ ' failed iterations')
            break

 """


def repairDeletionEvent(nodes: set, edges_: set[tuple], deletionEventName, CR, maxdepth=1000):
    deletedEventHasCR = any(
        {cr[0] == deletionEventName or cr[1] == deletionEventName for cr in CR})
    if(not deletedEventHasCR):
        print("Not deletedEventHasCR: No deletion Add!", deletionEventName)
        return edges_
    # cs where CasualPredecessor in Nodes and smallest depth (nearest predecessor)
    correspondingPreCR = {
        cr for cr in CR if cr[1] == deletionEventName and cr[0] in nodes}
    casualPredecessor = calculateDeletionCRNodes(
        correspondingPreCR, 0, maxdepth, deletedEventHasCR)

    # cs where CasualSuccessor in Nodes and smallest depth (nearest successor )
    correspondingSucCR = {
        cr for cr in CR if cr[0] == deletionEventName and cr[1] in nodes}
    casualSuccessor = calculateDeletionCRNodes(
        correspondingSucCR, 1, maxdepth, deletedEventHasCR)
    try:
        assert(len(casualSuccessor) > 0 and len(casualPredecessor) > 0)
    except:
        print("Kann keine Kanten für deletion hinzufügen!", deletionEventName)
        print('correspondingPreCR', str(len(correspondingPreCR)))
        print('correspondingSucCR', str(len(correspondingSucCR)))
        print('casualSuccessor: ' + str(len(casualSuccessor)))
        print('casualPredecessor: ' + str(len(casualPredecessor)))
    addingEdges = {(source, target)
                   for source in casualPredecessor for target in casualSuccessor}
    edges_.update(addingEdges)
    # kp ob redundante ecken entstehen können
    # redunEdges = {(source,target) for (source,target) in edges_ if source in predecessorOfAfterEvent and target == aftereventLabel}
    return edges_


def buildInstanceGraphFromTrace(trace: Trace, variantAlignment, cr, orgaDict: dict, classifier="concept:name"):
    nodes, edges, nodeEventDict = genInstanceGraph(
        trace, cr, orgaDict, classifier)
    print(trace.attributes['variant'])
    print('nodes', len(nodes))
    print('Anzahl Edges InstanceGraph build:', len(edges))
    insertedActivities, deletedActivities = sortLogAndModelMove(
        variantAlignment['alignment'])
    maxdepth = max(cr, key=lambda cr: cr[2])[2]
    edges_ = edges
    for index, event in enumerate(trace):
        # Did find out
        if(event[classifier] in insertedActivities):
            edges_ = repairInsertedEvent(
                edges_, event[classifier], trace, index, classifier)
        if(event[classifier] in deletedActivities):
            edges_ = repairDeletionEvent(
                nodes, edges_, event[classifier], cr, maxdepth)
    return (nodes, edges_, nodeEventDict)


def buildingInstanceGraphsFromLog(eventLog: EventLog, net: PetriNet, variantAlignmentDict, classifier="concept:name"):
    cr = calculateCR(net)
    orgaDict = createOrgaUnitDict(eventLog)
    instanceGraphDict = dict()
    # with tqdm(total=len(eventLog)) as pbar:
    for trace in eventLog:
        variant = trace.attributes['variant']
        variantAlignment = variantAlignmentDict[variant]
        repairedInstanceGraph = buildInstanceGraphFromTrace(
            trace, variantAlignment, cr, orgaDict, classifier)
        instanceGraphDict[variant] = repairedInstanceGraph
        # print('Anzahl Edges Repaired InstanceGraph build:', len(repairedInstanceGraph[1]))
        # pbar.update(1)
    return instanceGraphDict
