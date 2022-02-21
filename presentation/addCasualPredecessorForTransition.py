def addCasualPredecessorForTransition(CR: set, casualPredecessor: PetriNet.Transition, casualSuccessor: PetriNet.Transition, maxdepth=-1):
    """ 
    Recursion startet bei Depth -1 und CP = CS 
    Endet sobald die Transition bzw. Place erreicht ist ohne eingehende Kanten
    Depth ist Anzahl echten Aktivitäten auf dem Weg zwischen dem Casual Predecessor und dem Casual Successor
    Starts at -1 (Übespringt sich selbst als predecessor)), -1 is an self-loop, 0 fullFills an instanceOrdering characteristic    
    maxDepth = -1: keine Maximale Tiefe"""
    predecessorList = [(casualPredecessor, -1)]
    transition_durchlaufen = set()
    while(predecessorList):
        tupleInList = predecessorList.pop(0)
        casualPredecessor = tupleInList[0]
        depth = tupleInList[1]
        # To prevent going to deep, spart Zeit
        if(maxdepth != -1 and depth > maxdepth):
            continue
        if (casualPredecessor == casualSuccessor):
            if(depth == 0):
                #print('self Loop')
                CR.add((casualPredecessor.label, casualSuccessor.label, depth-1))
                continue
            # ignore loop, which are not self loops, abort to prevent endless recursion
            elif(depth > 0):
                #print('ignore n-Loop')
                continue
        # add cr if not silent trans and
        depthSummand = 0  # 1 or 0; is 1 if new CR added, i.e. cp is no silent Trans
        if(casualPredecessor.label != None and depth > -1):
            CR.add((casualPredecessor.label, casualSuccessor.label, depth))
            depthSummand = 1
        elif(depth < 0):
            depthSummand = 1
        for inArc in casualPredecessor.in_arcs:
            predPlace = inArc.source
            for placeInArc in predPlace.in_arcs:  # abort, if place no in_arcs
                nextPC = placeInArc.source
                if(nextPC not in transition_durchlaufen):
                    transition_durchlaufen.add(nextPC)
                    predecessorList.append((nextPC, depth + depthSummand))