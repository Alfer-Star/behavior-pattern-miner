import pm4py

from pm4py.objects.log.importer.xes import importer as xes_importer

from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

from log_classifier_helper import addDivisionClassifier
from log_classifier_helper import addRessourceClassifier

path = "datasets/02_TestCompletedFFF_onlyTaskItems_simpleFilter.xes"

log = xes_importer.apply(path)
log = pm4py.filter_case_size(log, 0, 300)

std_classifier = "concept:name"
customClassifierDivision = "customClassifierDivision"
customClassifierRessource = "customClassifierRessource"

importPathDivision = "output/petri_net_division_name.pnml"
importPathName = "output/petri_net_name.pnml"
importPathRessource = "output/petri_net_ress_name.pnml"

variantIM = inductive_miner.Variants.IMf
parameters = {inductive_miner.Variants.IMf.value.Parameters.ACTIVITY_KEY: customClassifierRessource}
## addDivisionClassifier(log, customClassifierDivision)
addRessourceClassifier(log, customClassifierRessource)
print('starte PetriNet generation')
# Log
net, initial_marking, final_marking = inductive_miner.apply(log,variant=variantIM, parameters=parameters)
pnml_exporter.apply(net, initial_marking, "output/petri_net_ress_name.pnml", final_marking=final_marking) 
print('PetriNet generation  ended')
