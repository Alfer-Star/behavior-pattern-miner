import pm4py
from pm4py.objects.log.obj import EventLog

import json

def mapAlignmentAndLog(log: EventLog, alignmentList):
    """ 
        Das log und Alignment sollten zusammengehörig sein, 
        d.h. das alignment in Position i entspricht dem trace auf Position i im log
    """
    alignmentLogMapping = dict()
    for index in range(len(log)):
        variantStr = log[index].attributes['variant']
        alignment = alignmentList[index]
        alignmentLogMapping[variantStr] = alignment
    return alignmentLogMapping

def loadAlignment(log: EventLog, folderPath = 'output/custom_cost_alignment_name_classifier/'):
    """ Load prepared Alignment from previous generated Output"""
    filtered_log_0 = pm4py.filter_case_size(log, 0, 70)
    filtered_log_70 = pm4py.filter_case_size(log, 71, 100)
    filtered_log_100 = pm4py.filter_case_size(log, 101, 130)
    filtered_log_130 = pm4py.filter_case_size(log, 131, 150)
    filtered_log_150 = pm4py.filter_case_size(log, 151, 180)
    filtered_log_180 = pm4py.filter_case_size(log, 181, 220)
    filtered_log_220 = pm4py.filter_case_size(log, 221, 300)

    filtered_logs = (filtered_log_0, filtered_log_70, filtered_log_100, filtered_log_130, filtered_log_150, filtered_log_180, filtered_log_220)
    fileindexes = (0,70,100,130,150,180,220)

    alignmentLogMapping = dict()
    for i in range(len(fileindexes)):
        logOfFile = filtered_logs[i]
        filename = folderPath+'aligned_traces_'+str(fileindexes[i])
        f = open(filename+'.json','r')
        alignmentList = json.load(f)
        f.close()

        if(len(logOfFile)!=len(alignmentList)):
            print('aligned list sind ungleich lang: ' + str(filename))
        else: 
            # concat dict from https://stackoverflow.com/a/26853961, but overwrites values from first dict if same key, like dict.update()
            alignmentLogMapping = alignmentLogMapping | mapAlignmentAndLog(logOfFile, alignmentList)

    ## lade mapping als dict aus varaint und alignmenten
    return alignmentLogMapping


def getTracePerVariant(log: EventLog, variant:str):
    for trace in log:
        if trace.attributes['variant']==variant:
            return trace


def printAlignment(alignmentLogMapping: dict, log = None):
    for key, item in alignmentLogMapping.items():
            print(key)
            if log != None:
                getTracePerVariant(log, key)
            print(item)
            print("__________________________________________________________________________")
## print all Alignments
# printAlignment(alignmentLogMapping)

## print all Alignments with her trace
## printAlignment(alignmentLogMapping, log)

## Alignment Helper
def sortLogAndModelMove(alignment: list):
    """ Return modelMoves, logMoves; filtert silent Transition """
    modelMoves = set()
    logMoves = set()
    for x in alignment:
        # check is model move and no silent trans => d
        if (x[0]=='>>' and x[1] != None):
            modelMoves.add(x[1])
        # check is log move and no silent trans
        elif (x[1]=='>>' and x[0] != None):
            logMoves.add(x[0])
    return modelMoves, logMoves

def sortLogAndModelMoveWithSilent(alignment: list):
    """ Return modelMoves, logMoves; filtert silent Transition """
    modelMoves = set()
    logMoves = set()
    for x in alignment:
        # check is model move
        if (x[0]=='>>'):
            modelMoves.add(x[1])
        # check is log move
        elif (x[1]=='>>'):
            logMoves.add(x[0])
    return modelMoves, logMoves

def printEvaluationAlignment(log: EventLog, alignmentDict: dict, key: str):
    """ key : variant string """
    traceVaraintDict = {trace.attributes['variant']:trace for trace in log} 
    item = alignmentDict[key]
    alignment = item['alignment']
    lenAlign = len(alignment)
    lenTrace = len(traceVaraintDict[key])
    modelMoves, logMoves = sortLogAndModelMove(alignment)
    modelmSil, LogmSil = sortLogAndModelMoveWithSilent(alignment)
    lenModelMoves = len(modelMoves)
    lenlogMoves = len(logMoves)
    # fitness.append(item['fitness'])
    anteilAlign= (lenModelMoves +lenlogMoves) / lenAlign
    anteilTrace = (lenModelMoves +lenlogMoves) / lenTrace
    # anteileIR.append(anteilTrace)
    print(key + ' Trace | Alignments: ' + str(lenTrace) + '|' + str(lenAlign))
    print('irregular Traces (ohne Silent): ' + str(lenModelMoves+lenlogMoves ))
    print('Fitness: ' + str(item['fitness']))
    print('irregular Traces Anteil From Trace: ' + str(anteilTrace))
    print('irregular Traces Anteil From Alignemt: ' + str(anteilAlign))
    print('ModelMoves:' + str(lenModelMoves))
    print('ModelMovesSil:' + str(len(modelmSil)-lenModelMoves))
    print('LogMoves:' + str(lenlogMoves))
    print('LogMovesSil:' + str(len(LogmSil)-lenlogMoves))
    print('______________________')