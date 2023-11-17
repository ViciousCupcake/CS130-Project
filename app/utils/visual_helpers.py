# Helpers that include all visualization tools
import networkx as nx
import matplotlib.pyplot as plt

def visualize_relations(relations, filepath):
    """
    Visualize the relations(mapping) as a graph.

    :param relations: Relations between attributes in a table
    :return: None
    """

    G = nx.MultiDiGraph()

    for attribute1, relation, attribute2 in relations:
        G.add_node(attribute1)
        G.add_node(attribute2)
        G.add_edge(attribute1, attribute2, label=relation)

    pos = nx.spring_layout(G, k=0.15, iterations=20)

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='skyblue', alpha=0.9,
            labels={node: node for node in G.nodes()})
    
    edge_labels = dict([((u, v,), d['label'])
                        for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5)

    plt.axis('off')
    plt.savefig(filepath, format='PNG')
    plt.close()
