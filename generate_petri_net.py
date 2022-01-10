import pm4py

from pm4py.objects.log.importer.xes import importer as xes_importer

from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

from log_classifier_helper import addDivisionClassifier

path = "datasets/02_TestCompletedFFF_onlyTaskItems_simpleFilter.xes"

log = xes_importer.apply(path)
log = pm4py.filter_case_size(log, 0, 300)

customClassifierDivision = "customClassifierDivision"

variantIM = inductive_miner.Variants.IMf
parameters = {inductive_miner.Variants.IMf.value.Parameters.ACTIVITY_KEY: customClassifierDivision}
addDivisionClassifier(log, customClassifierDivision)
print('starte PetriNet generation')
# Log
net, initial_marking, final_marking = inductive_miner.apply(log,variant=variantIM, parameters=parameters)
pnml_exporter.apply(net, initial_marking, "output/petri_net_full.pnml", final_marking=final_marking) 
print('PetriNet generation  ended')
