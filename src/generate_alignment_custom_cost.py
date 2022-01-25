import pm4py
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner

from custom_cost_function import getCostFunctionParameter

from log_classifier_helper import addDivisionClassifier
from log_classifier_helper import addRessourceClassifier

import os
import json
import sys

assert sys.argv[1] == 'division' or sys.argv[1] == 'std' or sys.argv[1] == 'ressource' or len(
    sys.argv) == 1

std_classifier = "concept:name"
customClassifierDivision = "customClassifierDivision"
customClassifierRessource = "customClassifierRessource"

""" Eine Berechnung des gesamten Alignments ist Abbruch gefährdet auf der Windows 10 Power shell. Daher """

path = "../datasets/02_TestCompletedFFF_onlyTaskItems_simpleFilter.xes"
# path = "../datasets/01_TestCompletedFFF_IDtoString_removeTransitionClassifier.xes"
log = xes_importer.apply(path)
log = pm4py.filter_case_size(log, 0, 300)

if (sys.argv[1] == 'division'):
    print('choose Division Ansatz')
    netImportPath = "../output/petri_net_division_name.pnml"
    outputPath = '../output/custom_cost_alignment_division/aligned_traces_'
    classifier = customClassifierDivision
    addDivisionClassifier(log, classifier)
elif (sys.argv[1] == 'ressource'):
    print('choose Ressource Ansatz')
    netImportPath = "../output/petri_net_ress_name.pnml"
    outputPath = '../output/custom_cost_alignment_ressource/aligned_traces_'
    classifier = customClassifierRessource
    addRessourceClassifier(log, classifier)
else:
    netImportPath = "../output/petri_net_name.pnml"
    outputPath = '../output/custom_cost_alignment_name/aligned_traces_'
    classifier = std_classifier


net, initial_marking, final_marking = pnml_importer.apply(
    os.path.join(netImportPath))

minMaxList = [(1, 70), (71, 100), (101, 130), (131, 150),
              (151, 180), (181, 220), (221, 300)]
for minValue, maxValue in minMaxList:
    print('Begin Stage:', minValue, maxValue)
    filtered_log = pm4py.filter_case_size(log, minValue, maxValue)

    parameters = getCostFunctionParameter(net)
    if(classifier != None):
        parameters[alignments.Variants.VERSION_STATE_EQUATION_A_STAR.value.Parameters.ACTIVITY_KEY] = classifier
        parameters[inductive_miner.Variants.IMf.value.Parameters.ACTIVITY_KEY] = classifier
    aligned_traces = alignments.apply_log(
        filtered_log, net, initial_marking, final_marking, parameters=parameters)

    os.makedirs(os.path.dirname(
        outputPath + str(minValue-1) + '.json'), exist_ok=True)
    with open(os.path.join(outputPath + str(minValue-1) + '.json'), 'w') as f:
        json.dump(aligned_traces, f)
    print('End Stage:', minValue, maxValue)
