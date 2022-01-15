import pm4py
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner

from alignment_custom_cost.custom_cost_function import getCostFunctionParameter

from log_classifier_helper import addDivisionClassifier
from log_classifier_helper import addRessourceClassifier


import os

import json

std_classifier = "concept:name"
customClassifierDivision = "customClassifierDivision"
customClassifierRessource = "customClassifierRessource"

importPathDivision = "output/petri_net_division_name.pnml"
importPathName = "output/petri_net_name.pnml"
importPathRessource = "output/petri_net_ress_name.pnml"

""" Eine Berechnung des gesamten Alignments ist Abbruch gefährdet auf schwachen Systemen. Daher """

def generateAlignmentInFilteredParts(log, minValue, maxValue, net, initial_marking, final_marking, classifier = None):
    filtered_log = pm4py.filter_case_size(log, minValue, maxValue)

    parameters = getCostFunctionParameter(net)
    if(classifier != None):
        parameters[alignments.Variants.VERSION_STATE_EQUATION_A_STAR.value.Parameters.ACTIVITY_KEY] = customClassifierDivision
        parameters[inductive_miner.Variants.IMf.value.Parameters.ACTIVITY_KEY] = customClassifierDivision
    aligned_traces = alignments.apply_log(filtered_log, net, initial_marking, final_marking, parameters=parameters)

    f = open('output/custom_cost_alignment/aligned_traces_'+ str(minValue-1)+ '.json', 'w')
    json.dump(aligned_traces, f)
    f.close()

def generateAlignments(netImportPath, classifier="concept:name"):
    std_classifier = "concept:name"
    customClassifierDivision = "customClassifierDivision"
    customClassifierRessource = "customClassifierRessource"
    path = "datasets/02_TestCompletedFFF_onlyTaskItems_simpleFilter.xes"
    # path = "datasets/01_TestCompletedFFF_IDtoString_removeTransitionClassifier.xes"
    log = xes_importer.apply(path)
    log = pm4py.filter_case_size(log, 0, 300)

    if(classifier == customClassifierDivision):
        addDivisionClassifier(log, classifier)
    elif (classifier == customClassifierRessource):
        addRessourceClassifier(log, classifier)
    else:
        classifier = None

    net, initial_marking, final_marking = pnml_importer.apply(os.path.join("output/petri_net_division_name.pnml"))

    minMaxList = [(1,70), (71,100), (101,130), (131,150), (151, 180), (181, 220), (221, 300)]
    for minValue, maxValue in minMaxList: 
            print('Begin Stage:',minValue, maxValue)
            generateAlignmentInFilteredParts(log, minValue, maxValue, net, initial_marking, final_marking, classifier )
            print('End Stage:', minValue, maxValue)


generateAlignments(customClassifierRessource)