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
    ''' Redundant die Kanten welche die Verbindung zwischen dem eventAppearedAfter und 
    predecessorOfAfterEvent darstellen, weil dieses aufgelöst und durch die INsertion ersetzt'''
    redundEdges = {(source, target) for (source, target)
                   in edges_ if source in predecessorOfAfterEvent and target == aftereventLabel}
    edges_.difference_update(redundEdges)
    return edges_