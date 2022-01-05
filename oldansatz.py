## alter Ansatz

def getTuplesWithEvent(ev: Event, arcs):
    arcsList = set()
    #print(arcs)
    for arc in arcs:
        #print(type(arc))
        """ if(arc == ev['concept:name'] or arc== ev['concept:name']):
            print('YAY')
            arcsList.add(arc) """
    return arcsList
    
def checkCasualRelation(ev1: Event, ev2:Event, net: PetriNet)-> bool:
    tuple = (ev1['concept:name'], ev2['concept:name'])
    ## print(tuple)
    ## TODO: wie machen wir hier die Vergleich: greife auf die CasualRelation Eigenschaft zu
    arcList = getTuplesWithEvent(ev1, net.arcs)
    arcList2 = getTuplesWithEvent(ev1, arcList)
    hasRelation = len(arcList2)>0
    ## hasRelation = tuple in net.arcs
    if(hasRelation):
        print('YAY Treffer')
        print(tuple)
    return hasRelation

from collections.abc import Sequence
def getInstanceOrdering(trace: Trace, net: PetriNet)->Sequence[tuple]:
    instanceOrderingSet = set()
    for idx, event in enumerate(trace):
        nextIndex = idx+1
        ##print(trace)
        if(nextIndex > len(trace)-1):
            print("For break")
            break
        event2 = trace[nextIndex]
        hasCasualRelation = False

        while(not hasCasualRelation):
            if(nextIndex > len(trace)-1):
                print("while break")
                break
            event2 = trace[nextIndex]
            hasCasualRelation = checkCasualRelation(event, event2, net)
            nextIndex = nextIndex+1

        if (hasCasualRelation):
            instanceOrderingSet.add((event, event2))

    return instanceOrderingSet