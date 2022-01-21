import subprocess

def formatToSubdueGraphShema(nodes: set, edges: set):
    """ 
    Formats my Graph shema into Sudbue 5.2.2 redable shema
    source subdue-5.2.2/docs/Usermanual_1.5
    #### Knoten
    v # label  
    #: is a unique vertex ID for the graph   
    label: is any string or real number.  
    Strings containing white-space or the comment character (see below) must be surrounded by double-quotes.   
    Knoten IDs for a graph must start at 1 and increase by 1 schrittweise aufeinanderfolgend.  
    It should also be noted that there must be at least one vertex defined before any edges are defined.

    #### Kanten
    e vertex 1 # vertex 2 # label  
    d vertex 1 # vertex 2 # label  
    u vertex 1 # vertex 2 # label   
    vertex 1 # and vertex 2 # are the vertex ID's for the source vertex and the target vertex respectively  
    label: is any string or real number. Strings containing white-space or the comment 
    character (see below) must be surrounded by double-quotes.   
    Edges beginning with “e” are assumed directed unless the option “-undirected” is specified at the command line (see next section), in which 
    case all “e” edges become undirected. Edges beginning with “d” are always directed, and edges beginning with “u” are always undirected.
    """
    subdueGraphNodesDict = dict()
    subdueGraphNodes = list()
    subdueGraphEdges = list()
    nodes = list(nodes)
    for index in range(len(nodes)):
        graphIndex = index +1
        subdueGraphNodesDict[nodes[index]] = graphIndex
        # replace " in strings because it used in fileFormat 
        subdueGraphNodes.append('v ' + str(graphIndex)+ ' "' + nodes[index].replace('"',"'")  + '"')
    for edge in edges:
        source = str(subdueGraphNodesDict[edge[0]])
        target = str(subdueGraphNodesDict[edge[1]])
        subdueGraphEdges.append('d '+ source + ' ' + target + ' ""' )
    
    return subdueGraphNodes, subdueGraphEdges

def writeSubDueInputFile(variant, subdueGraphNodes, subdueGraphEdges, filepath: str, example = 'XP'):
    """ Appends Output from getSubdueGraph to .g file"""
    f = open(filepath+".g", "a")
    f.write('%' +variant+'%' + "\n")
    f.write(example + "\n")
    for nodestr in subdueGraphNodes:
        f.write(nodestr + "\n")
    f.write("\n")
    for edgestr in subdueGraphEdges:
        f.write(edgestr + "\n")
    f.write("\n")
    f.write("\n")
    f.close()

def computeSubgraphsFromInstanceGraphs(instanceGraphsDict: dict, filepath = 'output/subdueGraphs'):

    # overwrite bestehenden Inhalt
    f = open(filepath+".g", "w")
    f.write("")
    f.close()

    # create SubDueGraph
    for key, instanceGraph in instanceGraphsDict.items():
        subdueGraphNodes, subdueGraphEdges = formatToSubdueGraphShema(instanceGraph[0], instanceGraph[1])
        writeSubDueInputFile(key, subdueGraphNodes, subdueGraphEdges, filepath)
    
    # subrpocesss to call bash commands, from here: https://unix.stackexchange.com/questions/190495/how-to-execute-a-bash-command-in-a-python-script
    outputFilePath = 'output/output-subdue'
    subprocess.check_output(['/home/adrian/Schreibtisch/behavior-pattern-miner/subdue-5.2.2/bin/subdue','-eval','1', '-iterations', '0', '-overlap', '-out', outputFilePath, '/home/adrian/Schreibtisch/behavior-pattern-miner/output/subdueGraphs.g'])
    
    return outputFilePath


def getSubGraphs(filepath = 'output/output-subdue')->list:
    """ 
    Verarbeitet Subdue 5.2.2 Subgraph FileOutput zurück in my graph Format
    return subgraphes 
    """
    file = open(filepath, 'r')
    subdue_output = file.readlines()
    file.close()

    subgraphs = list()
    currentGraphNodesDict = dict()
    currentGraphNodes = set()
    currentGraphEdges = set()
    firstCall = True
    for line in subdue_output:
        # Start neuen Subgraph
        if(not firstCall and line.startswith('S')):
            firstCall = False
            subgraphs.append((currentGraphNodes,currentGraphEdges))
            currentGraphNodes = set()
            currentGraphEdges = set()
        # füge Knoten hinzu
        elif(line.startswith('v')):
            lineStringList=line.split()
            nodeName = lineStringList[2].replace("'",'"') # Replace ' back to " 
            currentGraphNodesDict[lineStringList[1]] = nodeName
            currentGraphNodes = nodeName
        # Füge Kante hinzu
        elif line.startswith('d') or line.startswith('e') or line.startswith('u'):
            lineStringList=line.split()
            currentGraphEdges.add((currentGraphNodesDict[lineStringList[1]],currentGraphNodesDict[lineStringList[2]]))
    
    return subgraphs






