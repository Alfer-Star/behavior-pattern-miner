import networkx as nx
import matplotlib.pyplot as plt

def transformToNetworkxGraph(instanceGraph: tuple[set, set, dict]):
    nodes, edges, eventDict = instanceGraph

    G = nx.DiGraph() # empty Graph
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

    plt.rcParams['figure.figsize'] = [100, 40] # Größe
    return plt