import pm4py

from pm4py.objects.log.importer.xes import importer as xes_importer

from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

from log_classifier_helper import addDivisionClassifier
from log_classifier_helper import addDivisionClassifierNoDuplicate
from log_classifier_helper import addRessourceClassifier

import sys

assert sys.argv[1] == 'division' or sys.argv[1] == 'std' or sys.argv[1] == 'ressource' or int(
    sys.argv[2]) or len(sys.argv) == 1

std_classifier = "concept:name"
customClassifierDivision = "customClassifierDivision"
customClassifierRessource = "customClassifierRessource"

importPathDivision = "../output/petri_net_division_name.pnml"
importPathName = "../output/petri_net_name.pnml"
importPathRessource = "../output/petri_net_ress_name.pnml"


path = "../datasets/02_TestCompletedFFF_onlyTaskItems_simpleFilter.xes"

log = xes_importer.apply(path)
log = pm4py.filter_case_size(log, 0, 300)


if (sys.argv[1] == 'division'):
    print('choose Division Ansatz')
    outputFile = importPathDivision
    if(int(sys.argv[2])):
        addDivisionClassifierNoDuplicate(
            log, customClassifierDivision, int(sys.argv[2]))
    else:
        addDivisionClassifier(log, customClassifierDivision)
    parameters = {
        inductive_miner.Variants.IMf.value.Parameters.ACTIVITY_KEY: customClassifierDivision}
elif (sys.argv[1] == 'ressource'):
    print('choose Ressource Ansatz')
    outputFile = importPathRessource
    addRessourceClassifier(log, customClassifierRessource)
    parameters = {
        inductive_miner.Variants.IMf.value.Parameters.ACTIVITY_KEY: customClassifierRessource}
else:
    print('choose Standard Ansatz')
    parameters = None
    outputFile = importPathName

variantIM = inductive_miner.Variants.IMf

print('starte PetriNet generation')
# Log
net, initial_marking, final_marking = inductive_miner.apply(
    log, variant=variantIM, parameters=parameters)
print('PetriNet generation  ended')
pnml_exporter.apply(net, initial_marking,
                    outputFile, final_marking=final_marking)
print('PetriNet generation  ended')


# Ist Transition in Trace
# Achtung eine Aktivität hat mehrere Events (start,, complete ect.), d.h. es tritt in trace mehrfach auf
# TODO: Eine Aktivität kann mehrfach auftreten, und von jemanden andern durchgeführt werden, wie behandeln wir diesen Fall?
# Aktuell erscheine mehrfach auftretende Aktivitäten dadurch erscheinen, dass sie im Pnetz drin ist. Was unsere CR Grundlage ist.
# Das reicht aus, weil wir die Instance ordering nur auf Basis der CR bemessen.
# die delted und inserted Aktivitäten bekommen wird bei der Reparatur aus. später heraus
# Sollen wir diese Fälle unterscheiden, indem wir den Namen und die
""" for trans in net.transitions:
    transLabel = str(trans.label) # eventname der aktuellen iteration
    isTransInTrace = lambda event: transLabel == event[customClassifierDivision]
    filteredItems = list(filter(isTransInTrace , trace))
    # prüfe Aktivität im PNetz auftaucht; theoretisch unnötig Petri Netz aus eventlog generiert
    if(len(filteredItems)>0):
        print('Is part', len(filteredItems))
        # print(transLabel + 'is Part of Trace')
    else:
        print('Is Not Part of Trace: ', len(transLabel)
        #print('Is Not Part of Trace: ', transLabel) """


# Print Einsicht PetriNet

""" place = net.places
print(place)
print(place.name)

arc = place.in_arcs[0]
print(arc.source.name, arc.source.label) """

""" # sind initial marker in places 
print(initial_marking)
print(final_marking)
places = net.places
for place in places:
    if place == final_marking or place == initial_marking:
      print('yes')
 """
""" places = net.places
for place in places:
  print("\nPLACE: "+place.name)
  for arc in place.in_arcs:
    print(arc.source.name, arc.source.label) """

""" print(net.arcs)
print(net.places)
print(net.transitions) """
""" print(net.places)
print(net.transitions) """

""" for trans in net.transitions:
    print(trans.label, trans.name) """

""" # stille Transitionen
transList = list()
for trans in net.transitions:
    if (trans.label == None):
        transList.append(trans)
print(len(transList)) """

# print(net.arcs[0].name)
