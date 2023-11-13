import random
import networkx as nx
import matplotlib.pyplot as plt

NMEC = 103600

random.seed(NMEC)

def generate_random_graph(num_vertices, p):
    G = nx.gnp_random_graph(num_vertices, p, seed=NMEC, directed=False)
    for (u, v) in G.edges():
        G[u][v]['weight'] = random.randint(1, 100)
        
    nx.write_gml(G, f'graphs/graph_{num_vertices}_{p}.gml')

def plot_graph(G, save=False, name=None):
    nx.draw(G, with_labels=True, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G), edge_labels=edge_labels)
    if save:
        plt.savefig(f'{name}.png')
    plt.show()
    plt.clf()

def load_graph(filename):
    G = nx.read_gml(filename)
    return G

def main():
    
    for num_vertices in range(2, 257):
        percentage = [0.125, 0.25, 0.5, 0.75]
        print(f'Generating graphs with {num_vertices} vertices')
        for p in percentage:
            generate_random_graph(num_vertices, p)
    
    #G = load_graph('graphs/graph_256_0.75.gml')
    #plot_graph(G)

if __name__ == '__main__':
    main()







