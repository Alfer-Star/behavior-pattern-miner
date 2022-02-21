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
        """ Warne, dass die keine Kanten zur Reparatur hinzugefügt werden können! """
    addingEdges = {(source, target)
                   for source in casualPredecessor for target in casualSuccessor}
    edges_.update(addingEdges)
    # Es werden keine Redundante Kanten durch den Deleletion repair hinzugefügt
    return edges_