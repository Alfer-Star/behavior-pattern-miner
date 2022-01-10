import pm4py
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner

from pm4py.algo.discovery.inductive import parameters

from custom_cost_function import getCostFunctionParameter

import os

import json

customClassifierDivision = "customClassifierDivision"
customClassifierRessource = "customClassifierRessource"

def addDivisionLifecyleTransClassifier(log):
    for trace in log:
        for event in trace:
            event[customClassifierDivision] = event['division'] +"|"+ event["concept:name"] + event["lifecycle:transition"]

def addRessourceLifecyleTransClassifier(log):
    for trace in log:
        for event in trace:
            event[customClassifierRessource] = event['org:resource'] +"|"+ event["concept:name"] + event["lifecycle:transition"]

def generateAlignmentInFilteredParts(log, minValue, maxValue, net, initial_marking, final_marking):
        filtered_log = pm4py.filter_case_size(log, minValue, maxValue)

        parameters = getCostFunctionParameter(net)

        aligned_traces = alignments.apply_log(filtered_log, net, initial_marking, final_marking, parameters=parameters)

        f = open('output/aligned_traces_'+ str(minValue-1)+ '.json', 'w')
        json.dump(aligned_traces, f)
        f.close()


path = "../datasets/02_TestCompletedFFF_onlyTaskItems_simpleFilter.xes"
# path = "datasets/01_TestCompletedFFF_IDtoString_removeTransitionClassifier.xes"
log = xes_importer.apply(path)
log = pm4py.filter_case_size(log, 0, 300)

net, initial_marking, final_marking = pnml_importer.apply(os.path.join("../output/petri_net_full.pnml"))

minMaxList = [(1,70), (71,100), (101,130), (131,150), (151, 180), (181, 220), (221, 300)]
for minValue, maxValue in minMaxList: 
        print('Begin Stage:',minValue, maxValue)
        generateAlignmentInFilteredParts(log, minValue, maxValue, net, initial_marking, final_marking )
        print('End Stage:',minValue, maxValue)
