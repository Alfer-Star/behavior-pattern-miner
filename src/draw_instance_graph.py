import graphviz
import networkx as nx
import matplotlib.pyplot as plt

from tqdm import tqdm

# ============ Networkx ==========


def transformToNetworkxGraph(instanceGraph: tuple[set, set, dict]):
    nodes, edges, eventDict = instanceGraph

    G = nx.DiGraph()  # empty Graph
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    return G


def drawInstanceGraph(instanceGraph: tuple[set, set, dict, set], trace=None):
    G = transformToNetworkxGraph(instanceGraph)

    # Layout
    # pos = nx.multipartite_layout(G) ## layers of straight lines: https://networkx.org/documentation/stable/reference/drawing.html?highlight=layout#module-networkx.drawing.layout)
    # zwo straight lines
    #top = nx.bipartite.sets(G)[0]
    ##pos = nx.bipartite_layout(G, top)
    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, edge_color='black')
    nx.draw_networkx_labels(G, pos)

    plt.rcParams['figure.figsize'] = [100, 40]  # Größe
    return plt


def drawInstanceMultipleIGraphs(instanceGraphs: dict, folderPath='output/graphs/'):
    with tqdm(total=len(instanceGraphs)) as pbar:
        for key, iGraph in instanceGraphs.items():
            plot = drawInstanceGraph(iGraph)
            plot.savefig(folderPath+key+'.png')
            plot.close('all')
            pbar.update(1)


# ================ GraphViz =================
# https://graphviz.readthedocs.io/en/stable/manual.html


def createGraphVizGraph(IG: tuple[set, set[tuple], dict], graphName: str):
    dot = graphviz.Digraph(graphName, comment='Instance Graph', format='svg')
    for node in IG[0]:
        identifier = node
        label = node
        dot.node(identifier, label)
    dot.edges(IG[1])
    return dot


def drawInstanceGraphViz(instanceGraphs: dict, folderPath='output/graphs/', view=False):
    with tqdm(total=len(instanceGraphs)) as pbar:
        for key, ig in instanceGraphs.items():
            dot = createGraphVizGraph(ig, key)
            dot.render(directory=folderPath, view=view)
            pbar.update(1)
