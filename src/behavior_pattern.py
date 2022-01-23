from src.subgraph_mining import getSubGraphs
from src.subgraph_mining import formatToSubdueGraphShema
from src.subgraph_mining import writeSubDueInputFile

import subprocess
from tqdm import tqdm


def calcBehaviorPattern(instanceGraphsDict, k):
    """ 
        Uses Subdue 5.5.2 modified MDL Programm 
        Writes two output Files, which serve as input Graph files
        Modifikations: 
        1. Calculation of ExternalEdgeBits for compressedDL removed, because of Error
        2. changed Value output from Compresssion index to inverse
    
     """    
    behaviorPattern = list()
    subdieOutputFilePath = 'output/output-subdue'
    g2Path = 'output/input-g2-mdl.g'

    ## Create g2: Subgraph
    subdueOutputFile = open(subdieOutputFilePath, 'r')
    inputFile = open(g2Path, 'w')
    inputFile.write('')
    inputFile.close()
    inputFile = open(g2Path, 'a')
    subdue_output_Lines = subdueOutputFile.readlines()
    passedFirstSubgraph = False
    for line in tqdm(subdue_output_Lines):
        if(not passedFirstSubgraph and line.startswith('S')):
            passedFirstSubgraph = True
        elif(not line.startswith('S')):
            inputFile.write(line)
        else:
            inputFile.close()
            if checkSubgraphBehaviorPattern(instanceGraphsDict, g2Path,k):
                behaviorPattern.append(getSubGraphs(g2Path))
            ## prepare for next Subgraph 
            inputFile = open(g2Path, 'w')
            inputFile.write('')
            inputFile.close()
            inputFile = open(g2Path, 'a')
    inputFile.close()

    return behaviorPattern

def checkSubgraphBehaviorPattern(instanceGraphsDict: dict, filePathWithSubgraph: str, k: int)-> bool: 
    g1Path = 'output/input-g1-mdl'
    for variant,instanceGraph in instanceGraphsDict.items():
        ## Create g1: graph
        subdueGraphNodes, subdueGraphEdges = formatToSubdueGraphShema(instanceGraph[0], instanceGraph[1])
        file = open(g1Path+'.g', 'w')
        file.write('')
        file.close()
        writeSubDueInputFile(variant, subdueGraphNodes, subdueGraphEdges, g1Path, '')

        output =subprocess.check_output(['/home/adrian/Schreibtisch/behavior-pattern-miner/subdue-5.2.2/bin/mdl_custom', '/home/adrian/Schreibtisch/behavior-pattern-miner/' + filePathWithSubgraph, '/home/adrian/Schreibtisch/behavior-pattern-miner/' + g1Path + '.g'])
        compressionValue = float(output.decode('utf-8').rstrip().split('\n')[-1].split(' ')[-1])
        if 1/compressionValue > k:
            return True
    return False