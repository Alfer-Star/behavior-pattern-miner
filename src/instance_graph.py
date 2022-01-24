from src.conformance_with_alignment import sortLogAndModelMove

from src.casual_releation import calculateCR

from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.log.obj import EventLog
from pm4py.objects.log.obj import Trace

from tqdm import tqdm


# Raw Instnace Graph
def genInstanceGraph(trace: Trace, CR, classifier="concept:name"):
    """ Generates Nodes on Edge, in other words from Instace ordering Output """
    nodes = {event[classifier] for event in trace}
    nodeEventDict = dict()
    # Instance Ordering Eigenschaft angewendet, dabei bedeutet depth 0, dass es sich um ein direkte nachfolge Beziehung, mit keiner anderen Aktivität dazwischen, handelt.
    edges = {(source, target) for (source, target, depth)
             in CR if target in nodes and source in nodes and depth == 0}
    # Event Mapping, das letzte Auftreten ds events ist für die Activität hinterlegt hinterlegt
    # TODO: ist noch nicht ausgereift.
    nodeEventDict = {event[classifier]: event for event in trace}
    return nodes, edges, nodeEventDict


# Reperatur
# Ansatz von Diamantini, C., Genga, L., and Potena, D. 2016. “Behavioral process mining for unstructured processes,” Journal of Intelligent Information Systems (47:1), pp. 5-32 (doi: 10.1007/s10844-016-0394-7)

def repairInsertedEvent(edges_: set[tuple], insertedEventName, trace: Trace, index, classifier="concept:name"):
    ''' Entferne alle kanten zwischen zwischen dem Inserted Event und anderen Events, weil irregulär eingefügt '''
    removingEdges = {(source, target) for (
        source, target) in edges_ if source == insertedEventName or target == insertedEventName}
    ''' Füge Event zwischen dem Event, welches nach den Inserted event aufgetreten ist und dessen Vorgänger '''
    eventAppearedAfter = trace[index + 1]
    aftereventLabel = eventAppearedAfter[classifier]
    predecessorOfAfterEvent = {source for (
        source, target) in edges_ if target == aftereventLabel}
    addedEdges = {(source, insertedEventName) for source in predecessorOfAfterEvent}.union(
        {(insertedEventName, aftereventLabel)})
    try:
        assert(len(addedEdges) > 0)
    except:
        print("Keine Kanten für Insertion hinzugefügt!", insertedEventName)

    edges_ = edges_.difference(removingEdges).union(addedEdges)
    ''' Redundant die Kanten welche die Verbindung zwischen dem eventAppearedAfter und predecessorOfAfterEvent darstellen, weil dieses aufgelöst und durch die INsertion ersetzt'''
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
    correspondingPreCR = {cr for cr in CR if cr[1]==deletionEventName and cr[0] in nodes }
    {cr[0] for cr in correspondingPreCR if cr[2] == 0}
    depthIndex = 1
    while(casualPredecessor and casualPredecessor):
        casualPredecessor = {cr[0] for cr in correspondingPreCR if cr[2] == depthIndex}
        depthIndex += 1
        if(depthIndex < maxdepth):
            print('Repair break loop, after '+ str(maxdepth)+ ' failed iterations')
            break

    correspondingSucCR = {cr for cr in CR  if cr[0]== deletionEventName and cr[1] in nodes}
    casualSuccessor = {cr[1] for cr in correspondingSucCR if cr[2]<= 0}
    depthIndex = 1
    while(deletedEventHasCR and casualPredecessor):
        casualPredecessor = {cr[1] for cr in correspondingSucCR if cr[2]<= depthIndex}
        depthIndex += 1
        if(depthIndex < maxdepth):
            print('Repair break loop, after '+ str(maxdepth)+ ' failed iterations')
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
    ## redunEdges = {(source,target) for (source,target) in edges_ if source in predecessorOfAfterEvent and target == aftereventLabel}
    return edges_


def buildInstanceGraphFromTrace(trace: Trace, variantAlignment, cr, classifier="concept:name"):
    nodes, edges, nodeEventDict = genInstanceGraph(trace, cr, classifier)
    print(trace.attributes['variant'])
    print('nodes', len(nodes))
    print('Anzahl Edges InstanceGraph build:', len(edges))
    print('Anzahl Edges InstanceGraph build:', len(edges))
    insertedActivities, deletedActivities = sortLogAndModelMove(
        variantAlignment['alignment'])
    maxdepth = max(cr, key=lambda cr: cr[2])[2]
    edges_ = edges
    for index, event in enumerate(trace):
        # TODO: handle Silent Transition
        if(event[classifier] in insertedActivities):
            edges_ = repairInsertedEvent(
                edges_, event[classifier], trace, index, classifier)
        elif(event[classifier] in deletedActivities):
            edges_ = repairDeletionEvent(
                nodes, edges_, event[classifier], cr, maxdepth)
    return (nodes, edges_, nodeEventDict)


def buildingInstanceGraphsFromLog(eventLog: EventLog, net: PetriNet, variantAlignmentDict, classifier="concept:name"):
    cr = calculateCR(net)
    instanceGraphDict = dict()
    # with tqdm(total=len(eventLog)) as pbar:
    for trace in eventLog:
        variant = trace.attributes['variant']
        variantAlignment = variantAlignmentDict[variant]
        repairedInstanceGraph = buildInstanceGraphFromTrace(
            trace, variantAlignment, cr, classifier)
        instanceGraphDict[variant] = repairedInstanceGraph
        # print('Anzahl Edges Repaired InstanceGraph build:', len(repairedInstanceGraph[1]))
        # pbar.update(1)
    return instanceGraphDict
