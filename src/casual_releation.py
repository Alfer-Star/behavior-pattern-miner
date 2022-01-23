
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.obj import PetriNet
import pm4py

from tqdm import tqdm

import json

import os

def calculateCR(net):
    CR = set()
    for trans in tqdm(net.transitions):
        if(trans.label != None):
            addCasualPredecessorForTransition(CR, trans, trans)
    return CR

def addCasualPredecessorForTransition(CR: set, casualPredecessor: PetriNet.Transition, casualSuccessor: PetriNet.Transition, maxdepth = -1):
    """ 
    Recursion startet bei Depth -2 und CP = CS 
    Endet sobald die Transition bzw. Place erreicht ist ohne eingehende Kanten
    Depth ist der Wert wie viele Aktivitäten zwischen dem Casual Predecessor und dem Casual Successor
    Starts at -1 (Übespringt sich selbst als predecessor)), -1 is an self-loop, 0 fullFills an instanceOrdering characteristic    """
    predecessorList = [(casualPredecessor,-1)]
    transition_durchlaufen = set()
    while(predecessorList):
        tupleInList = predecessorList.pop(0)
        casualPredecessor = tupleInList[0]
        depth = tupleInList[1]
        ## To prevent to deep, spart Zeit
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
        # TODO: loop in loop detection
        ##print(casualPredecessor.label, depth)
        # add cr if not silent trans and 
        if(casualPredecessor.label != None and depth >-1):
            CR.add((casualPredecessor.label, casualSuccessor.label, depth))
        for inArc in casualPredecessor.in_arcs:
            predPlace = inArc.source
            for placeInArc in predPlace.in_arcs: ## abort, if place no in_arcs
                nextPC = placeInArc.source
                if(nextPC not in transition_durchlaufen):
                    transition_durchlaufen.add(nextPC)
                    predecessorList.append((nextPC, depth +1))

def computeCasualRelAsJSON(net, filename='output/CasualRelation.json'):
    CR = list(calculateCR(net))
    f = open(filename, 'w')
    json.dump(CR, f)
    f.close()