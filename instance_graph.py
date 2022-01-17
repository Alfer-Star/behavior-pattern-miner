from conformance_with_alignment import sortLogAndModelMove

from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.log.obj import EventLog
from pm4py.objects.log.obj import Trace

## CR und Instance Ordering

def getTransitionsConnectedPerNodesFromPetriNet(net: PetriNet):
    """ returns tuples of Transitions, which are connected per node, 
    Transitions with incoming arc to node are the source:  tuple position 0
    Transitions with incoming arc to node are the source:  tuple position 0 """
    arcedTrans = list()
    # Transition == Event or activity
    places = net.places
    for place in places:
        for arc_in in place.in_arcs:
            for arc_out in place.out_arcs:
                arcedTrans.append((arc_in.source, arc_out.target))
    return arcedTrans

def getInstanceOrdering(net: PetriNet):
    InstanceOrdering = set()
    # net (Petri net) represents CR Relation
    # tuples of Transitions, which are connected per node => instance Ordering Property
    # Instance Ordering Eigenschaft, da CR Eigenschaft erfüllt und keine CR dazwischen (laut Modell)!
    orderingList = getTransitionsConnectedPerNodesFromPetriNet(net)
   
    # Map Transitions in orderList to their activity Name (Transition label)
    # Map silent Transition, where Label None to there name in PetriNet
    for ordering in orderingList:
        transitionLabel = ordering[0].label # source eventname
        if transitionLabel == None: # silentTransistion in source
            transitionLabel = ordering[0].name
        transitionFollowerLabel = ordering[1].label # target eventname
        if transitionFollowerLabel == None: # silentTransistion in target
            transitionFollowerLabel = ordering[1].name
        
        tuple = (transitionLabel, transitionFollowerLabel)
        InstanceOrdering.add(tuple)  
    return InstanceOrdering


silent_transition_substrings = {'skip', 'init_log', 'tauJoin', 'tauSplit'}
## any(substring in x[1] for substring in silent_transistion)


## Raw INstnace Graph
def genInstanceGraph(trace: Trace, InstanceOrdering, classifier="concept:name"):
    """ Generates Nodes on Edge, in other words from Instace ordering Output """
    nodes = {event[classifier] for event in trace}
    nodeEventDict = dict()
    edges = {(source, target) for (source, target) in InstanceOrdering if target in nodes and source in nodes}

    silent_transition_substrings = {'skip', 'init_log', 'tauJoin', 'tauSplit'}
    isSilentTransistion = lambda node: any([substring in node for substring in silent_transition_substrings])
    silentEdges ={(source, target) for (source, target) in InstanceOrdering if target in nodes and isSilentTransistion(source) or source in nodes and isSilentTransistion(source)}
    edges.update(silentEdges)
    
    silentNodes = { node for edge in silentEdges for node in edge if node not in nodes}
    nodes.update(silentNodes)
    # Event Mapping
    nodeEventDict = {event[classifier]: event for event in trace}
    return nodes, edges, nodeEventDict


#Reperatur
## Ansatz von Diamantini, C., Genga, L., and Potena, D. 2016. “Behavioral process mining for unstructured processes,” Journal of Intelligent Information Systems (47:1), pp. 5-32 (doi: 10.1007/s10844-016-0394-7)

def repairInsertedEvent(edges_:set[tuple], evenDict:dict, insertedEventName, trace:Trace, index, classifier="concept:name"):
    ''' Entferne alle kanten zwischen zwischen dem Inserted Event und anderen Events, weil irregulär eingefügt '''
    removingEdges = {(source,target) for (source,target) in edges_ if source == insertedEventName or target == insertedEventName}

    ''' Füge Event zwischen dem Event, welches nach den Inserted event aufgetreten ist und dessen Vorgänger '''
    eventAppearedAfter = trace[index + 1]
    aftereventLabel = eventAppearedAfter[classifier]
    predecessorOfAfterEvent = {source for (source,target) in edges_ if target == aftereventLabel}
    addedEdges = {(source, insertedEventName) for source in predecessorOfAfterEvent}.union({(insertedEventName, aftereventLabel)})

    edges_ = edges_.difference(removingEdges).union(addedEdges)
    ''' Redundant die Kanten welche die Verbindung zwischen dem eventAppearedAfter und predecessorOfAfterEvent darstellen, weil dieses aufgelöst und durch die INsertion ersetzt'''
    redundEdges = {(source,target) for (source,target) in edges_ if source in predecessorOfAfterEvent and target == aftereventLabel}
    edges_.difference_update(redundEdges)
    return edges_

def repairDeletionEvent(nodes: set, edges_:set[tuple], deletionEventName, instanceOrdering):
    casualSuccessor = {source for source in nodes if (source, deletionEventName) in instanceOrdering}
    casualPredecessor = {target for target in nodes if (deletionEventName, target) in instanceOrdering}
    try:
        assert(len(casualSuccessor)>0 and len(casualPredecessor)>0)
    except:
        print("Kann keine Kanten für deletion hinzufügen!", deletionEventName)
        print('casualSuccessor: '+ str(len(casualSuccessor)))
        print('casualSuccessor: '+ str(len(casualPredecessor)))
    addingEdges = {(source, target) for source in casualSuccessor for target in casualPredecessor}
    edges_.update(addingEdges)
    ## kp ob redundante ecken entstehen können
    ## redunEdges = {(source,target) for (source,target) in edges_ if source in predecessorOfAfterEvent and target == aftereventLabel}
    return edges_

def buildInstanceGraphFromTrace(trace: Trace, variantAlignment, instanceOrdering, classifier="concept:name"):
    nodes, edges, nodeEventDict = genInstanceGraph(trace, instanceOrdering, classifier)
    print(trace.attributes['variant'])
    print('nodes', len(nodes))
    print( 'Anzahl Edges InstanceGraph build:', len(edges))
    insertedActivities, deletedActivities =sortLogAndModelMove(variantAlignment['alignment'])
    edges_ = edges
    for index, event in enumerate(trace):
        if(event[classifier] in insertedActivities):
            edges_= repairInsertedEvent(edges_, nodeEventDict,event[classifier], trace, index, classifier)
        elif(event[classifier] in deletedActivities):
            edges_ = repairDeletionEvent(nodes, edges_, event[classifier], instanceOrdering)
    return (nodes, edges_, nodeEventDict)

def buildingInstanceGraphsFromLog(eventLog: EventLog, net: PetriNet, variantAlignmentDict, classifier="concept:name"):
    instanceOrdering = getInstanceOrdering(net)
    instanceGraphDict = dict()
    for trace in eventLog:
        variant = trace.attributes['variant']
        variantAlignment = variantAlignmentDict[variant]
        repairedInstanceGraph = buildInstanceGraphFromTrace(trace, variantAlignment,instanceOrdering, classifier)
        instanceGraphDict[variant] = repairedInstanceGraph
        print('Anzahl Edges Repaired InstanceGraph build:', len(repairedInstanceGraph[1]))
    return instanceGraphDict