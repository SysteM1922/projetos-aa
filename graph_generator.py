import random
import networkx as nx
import matplotlib.pyplot as plt
from argparse import ArgumentParser

NMEC = 103600

random.seed(NMEC)

def generate_random_graph(num_vertices, p):
    G = nx.fast_gnp_random_graph(num_vertices, p, seed=NMEC, directed=False)
    for (u, v) in G.edges():
        G[u][v]['weight'] = random.randint(1, 100)
        
    return G

def save_graph(G, name):
    nx.write_gml(G, f'graphs/{name}.gml')

def plot_graph(G, save=False, name=None):
    pos = nx.spring_layout(G)
    nx.draw(G, pos=pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    if save:
        plt.savefig(f'{name}.png')
    plt.show()
    plt.clf()

def load_graph(filename):
    return nx.read_gml(filename)

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-min_v', '--minimum_vertices', type=int, default=2, help='Minimum number of vertices')
    parser.add_argument('-max_v', '--maximum_vertices', type=int, default=None, help='Maximum number of vertices')
    parser.add_argument('-p', '--percentage', type=int, default=4, help='1: 0.125,\n2: till 0.25,\n3: till 0.5, 4:\ntill 0.75')
    parser.add_argument('-s', '--save', action='store_true', help='Save graph')
    parser.add_argument('-n', '--name', type=str, default=None, help='Name of the graph to load')
    parser.add_argument('-l', '--load', action='store_true', help='Load graph')
    args = parser.parse_args()

    if args.load and args.name:
        G = load_graph(f'graphs/{args.name}.gml')
        plot_graph(G, save=args.save, name=args.name)

    elif args.maximum_vertices:
        for num_vertices in range(args.minimum_vertices, args.maximum_vertices+1):
            percentage = [0.125, 0.25, 0.5, 0.75][:args.percentage]
            print(f'Generating graphs with {num_vertices} vertices')
            for p in percentage:
                G=generate_random_graph(num_vertices, p)
                if args.save:
                    save_graph(G, f'graph_{num_vertices}_{p}')








