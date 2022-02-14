from src.conformance_with_alignment import sortLogAndModelMove

from src.casual_releation import calculateCR

from src.instance_graph_repair import repairDeletionEvent
from src.instance_graph_repair import repairInsertedEvent

from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.log.obj import EventLog
from pm4py.objects.log.obj import Trace

from tqdm import tqdm

BP_NODE_LABEL = 'BPNodeLabel'
GEN_IG_ORGA_PARAMETER = 'orgaDict'


def createOrgaUnitDict(log: EventLog, ressPrefix='M'):
    orgaUnitDict = dict()
    index = 0
    for trace in log:
        for event in trace:
            orgaUnit = event['org:resource']
            if(orgaUnit not in orgaUnitDict):
                orgaUnitDict[orgaUnit] = ressPrefix+index
                index += 1


def getBPActivityLabel(event, orgaDict):
    return orgaDict(event['org:resource'])+event['concept:name']


# Raw Instnace Graph


def genInstanceGraph(trace: Trace, CR, orgaDict: dict, classifier="concept:name", **kwargs):
    """ Generates Node for Every event and add edges if between Events instance ordering fullfilled """
    nodes = set()
    edges = set()
    nodeLabelEventDict = dict()

    prevEvent = trace[0]
    for event in trace:
        label = getBPActivityLabel(event, orgaDict)

        # vermeide gleiche label bei unterschiedlichen Events
        index = 1
        newlabel = label
        while(newlabel in nodes):
            newlabel = label + index
            index += 1
        label = newlabel

        event[BP_NODE_LABEL] = label
        nodeLabelEventDict[label] = event
        nodes.add(label)

        # Casual Relation, die Instance Ordering Eigenschaft erfüllt
        # dabei bedeutet depth 0, dass es sich um ein direkte nachfolge Beziehung mit keiner anderen Aktivität dazwischen handelt (InstanceOrdering).
        plainActivitysInGraph = {event['concept:name'] for event in trace}
        instanceOrdering = {(source, target) for (source, target, depth)
                            in CR if source in plainActivitysInGraph and target in plainActivitysInGraph and depth <= 0}

        if(event == prevEvent):  # Case
            continue
        elif((prevEvent[classifier], event[classifier]) in instanceOrdering):
            edges.add((prevEvent[BP_NODE_LABEL], label))

        prevEvent = event

    return nodes, edges, nodeLabelEventDict


def buildInstanceGraphFromTrace(trace: Trace, alignmentList: list, cr, orgaDict: dict, classifier="concept:name"):
    nodes, edges, nodeEventDict = genInstanceGraph(
        trace, cr, orgaDict, classifier)
    """ print(trace.attributes['variant'])
    print('nodes', len(nodes))
    print('Anzahl Edges InstanceGraph build:', len(edges)) """
    filter(lambda alignment: None not in alignment, alignmentList)
    maxdepth = max(cr, key=lambda cr: cr[2])[2]
    edges_ = edges
    assert(len(trace) == len(alignmentList))
    for index, event in enumerate(trace):
        assert(event[classifier] in [
               alignmentList[index][0], alignmentList[index][1]])
        if(alignmentList[index][0] == '>>'):
            edges_ = repairInsertedEvent(
                edges_, event[BP_NODE_LABEL], trace, index, classifier)
        if(alignmentList[index][1] == '>>'):
            edges_ = repairDeletionEvent(
                nodes, edges_, nodeEventDict, event, cr, maxdepth)
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
