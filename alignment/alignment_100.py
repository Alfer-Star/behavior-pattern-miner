import pm4py
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner

import os

import json

variantIM = inductive_miner.Variants.IMf

path = "../datasets/02_TestCompletedFFF_onlyTaskItems_simpleFilter.xes"
# path = "datasets/01_TestCompletedFFF_IDtoString_removeTransitionClassifier.xes"
log = xes_importer.apply(path)
log = pm4py.filter_case_size(log, 0, 300)
filtered_log = pm4py.filter_case_size(log, 101, 130)

net, initial_marking, final_marking = inductive_miner.apply(log,variant=variantIM)

aligned_traces = alignments.apply_log(filtered_log, net, initial_marking, final_marking)

f = open('output/aligned_traces_100.json', 'w')
json_string = json.dump(aligned_traces, f)
f.close()