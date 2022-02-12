from src.conformance_with_alignment import sortLogAndModelMove

from src.casual_releation import calculateCR

from src.instance_graph_repair import repairDeletionEvent
from src.instance_graph_repair import repairInsertedEvent

from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.log.obj import EventLog
from pm4py.objects.log.obj import Trace


# Raw Instnace Graph
def genInstanceGraph(trace: Trace, CR, classifier="concept:name"):
    """ Generates Nodes on Edge, in other words from Instace ordering Output """
    nodes = {event[classifier] for event in trace}
    nodeEventDict = dict()
    # Instance Ordering Eigenschaft angewendet, dabei bedeutet depth 0, dass es sich um ein direkte nachfolge Beziehung, mit keiner anderen Aktivität dazwischen, handelt.
    edges = {(source, target) for (source, target, depth)
             in CR if target in nodes and source in nodes and depth <= 0}
    # Event Mapping, das letzte Auftreten ds events ist für die Activität hinterlegt hinterlegt
    # TODO: ist noch nicht ausgereift.
    nodeEventDict = {event[classifier]: event for event in trace}
    return nodes, edges, nodeEventDict


def buildInstanceGraphFromTrace(trace: Trace, variantAlignment, cr, classifier="concept:name"):
    nodes, edges, nodeEventDict = genInstanceGraph(trace, cr, classifier)
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
