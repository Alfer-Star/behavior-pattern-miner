def genInstanceGraph(trace: Trace, CR, classifier="concept:name"):
    nodes = {event[classifier] for event in trace}
    nodeEventDict = dict()
    # Instance Ordering Eigenschaft angewendet, dabei bedeutet depth 0, 
    # dass es sich um ein direkte nachfolge Beziehung, mit keiner anderen Aktivität dazwischen, handelt.
    edges = {(source, target) for (source, target, depth)
             in CR if target in nodes and source in nodes and depth <= 0}
    # Event Mapping, das letzte Auftreten ds events ist für die Aktivität hinterlegt 
    nodeEventDict = {event[classifier]: event for event in trace}
    return nodes, edges, nodeEventDict

