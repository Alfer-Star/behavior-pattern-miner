import pm4py

from pm4py.objects.log.importer.xes import importer as xes_importer

from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

import sys

path = sys.argv[1]
outputFile = sys.argv[2]
do_filter = True
try:
    minimum = sys[3]
    maximum = sys[4]
except:
    do_filter = False

# python generate_petri_net.py ../datasets/Hospital_log.xes ../output/hospital_petrinet.pml Start 15:20 -16:49 (?) ca. 1h

log = xes_importer.apply(path)
if(do_filter):
    log = pm4py.filter_case_size(log, minimum, maximum)

parameters = dict()

variantIM = inductive_miner.Variants.IMf

print('starte PetriNet generation')
# Log
net, initial_marking, final_marking = inductive_miner.apply(
    log, variant=variantIM, parameters=parameters)
print('PetriNet generation  ended')
pnml_exporter.apply(net, initial_marking,
                    outputFile, final_marking=final_marking)
print('PetriNet exported')
