import pm4py
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.log.importer.xes import importer as xes_importer

import os

import json

path = "datasets/02_TestCompletedFFF_onlyTaskItems_simpleFilter.xes"
# path = "datasets/01_TestCompletedFFF_IDtoString_removeTransitionClassifier.xes"
log = xes_importer.apply(path)

net, initial_marking, final_marking = pnml_importer.apply(os.path.join("output/petri_net_full.pnml"))

aligned_traces = alignments.apply_log(log, net, initial_marking, final_marking)

f = open('output/aligned_traces.json', 'w')
json_string = json.dump(aligned_traces, f)
f.close()