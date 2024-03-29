
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.obj import PetriNet
import pm4py

from tqdm import tqdm

import json


def calculateCR(net):
    CR = set()
    for trans in tqdm(net.transitions):
        if(trans.label != None):
            addCasualPredecessorForTransition(CR, trans)
    return CR


def addCasualPredecessorForTransition(CR: set, casualSuccessor: PetriNet.Transition, maxdepth=-1):
    """ 
    Recursion startet bei Depth -1 und CP = CS 
    Endet sobald die Transition bzw. Place erreicht ist ohne eingehende Kanten
    Depth ist Anzahl echten Aktivitäten auf dem Weg zwischen dem Casual Predecessor und dem Casual Successor
    Starts at -1 (Übespringt sich selbst als predecessor)), -1 is an self-loop, 0 fullFills an instanceOrdering characteristic    
    maxDepth = -1: keine Maximale Tiefe"""
    predecessorList = [(casualSuccessor, -1)]
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
                CR.add((casualPredecessor.label, casualSuccessor.label, -1))
                continue
            # ignore loop, which are not self loops, abort to prevent endless recursion
            elif(depth != -1):
                #print('ignore n-Loop')
                continue
        # add cr if not silent trans and
        depthSummand = 0  # 1 or 0; is 1 if new CR added, i.e. cp is no silent Trans
        if(casualPredecessor.label != None and depth > -1):
            CR.add((casualPredecessor.label, casualSuccessor.label, depth))
            depthSummand = 1
        elif(depth == -1):
            depthSummand = 1
        for inArc in casualPredecessor.in_arcs:
            predPlace = inArc.source
            for placeInArc in predPlace.in_arcs:  # abort, if place no in_arcs
                nextPC = placeInArc.source
                if(nextPC not in transition_durchlaufen):
                    # alle bis auf die Initiale Transistion, werden aufgezeichent, es sei den es exitiert ein self Loop
                    transition_durchlaufen.add(nextPC)
                    predecessorList.append((nextPC, depth + depthSummand))
                # TODO: else check if duplicate has an lower depth!


def computeCasualRelAsJSON(net, filename='output/CasualRelation.json'):
    CR = list(calculateCR(net))
    f = open(filename, 'w')
    json.dump(CR, f)
    f.close()
