from pm4py.objects.log.obj import Trace

from instance_graph_new import BP_NODE_LABEL

from tqdm import tqdm


# Reperatur
# Ansatz von Diamantini, C., Genga, L., and Potena, D. 2016. “Behavioral process mining for unstructured processes,” Journal of Intelligent Information Systems (47:1), pp. 5-32 (doi: 10.1007/s10844-016-0394-7)

def repairInsertedEvent(edges_: set[tuple], insertedEventName, trace: Trace, index, classifier="concept:name"):
    ''' Entferne alle kanten zwischen zwischen dem Inserted Event und anderen Events, weil irregulär eingefügt '''
    removingEdges = {(source, target) for (
        source, target) in edges_ if source == insertedEventName or target == insertedEventName}
    ''' Füge Event zwischen dem Event, welches nach den Inserted event aufgetreten ist und dessen Vorgänger '''
    eventAppearedAfterLabel = None
    for i in range(index + 1, len(trace)):
        eventLabel = trace[i][classifier]
        if trace[i][classifier] != insertedEventName:
            eventAppearedAfterLabel = eventLabel
            break
    predecessorOfAfterEvent = {source for (
        source, target) in edges_ if target == eventAppearedAfterLabel}
    addedEdges = {(source, insertedEventName) for source in predecessorOfAfterEvent}.union(
        {(insertedEventName, eventAppearedAfterLabel)})
    try:
        assert(len(addedEdges) > 0)
    except:
        print("Keine Kanten für Insertion hinzugefügt!", insertedEventName)

    edges_ = edges_.difference(removingEdges).union(addedEdges)
    ''' Redundant die Kanten welche die Verbindung zwischen dem eventAppearedAfter und predecessorOfAfterEvent darstellen, weil dieses aufgelöst und durch die INsertion ersetzt'''
    redundEdges = {(source, target) for (source, target)
                   in edges_ if source in predecessorOfAfterEvent and target == eventAppearedAfterLabel}
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


def repairDeletionEvent(nodes: set, edges_: set[tuple], nodelAbelEventDict: dict, deletionEvent, CR, maxdepth=1000):
    deletionActivityName = deletionEvent['concept:name']
    deletionBPLabel = deletionEvent['concept:name']
    deletedEventHasCR = any(
        {cr[0] == deletionActivityName or cr[1] == deletionActivityName for cr in CR})
    if(not deletedEventHasCR):
        print("Not deletedEventHasCR: No deletion Add!", deletionActivityName)
        return edges_
    # cs where CasualPredecessor in Nodes and smallest depth (nearest predecessor)
    correspondingPreCR = {
        cr for cr in CR if cr[1] == deletionActivityName and cr[0] in nodes}
    casualPredecessor = calculateDeletionCRNodes(
        correspondingPreCR, 0, maxdepth, deletedEventHasCR)

    # cs where CasualSuccessor in Nodes and smallest depth (nearest successor )
    correspondingSucCR = {
        cr for cr in CR if cr[0] == deletionActivityName and cr[1] in nodes}
    casualSuccessor = calculateDeletionCRNodes(
        correspondingSucCR, 1, maxdepth, deletedEventHasCR)
    try:
        assert(len(casualSuccessor) > 0 and len(casualPredecessor) > 0)
    except:
        print("Kann keine Kanten für deletion hinzufügen!", deletionActivityName)
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
