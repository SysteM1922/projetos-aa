import itertools
import networkx as nx
from graph_generator import generate_random_graph
from argparse import ArgumentParser
import time

def exhaustive_search(G):

    nodes = G.nodes
    n = G.number_of_nodes()
    max_cut_weight = 0
    max_cut = None

    for i in range(n):
        for subset in itertools.combinations(nodes, i):
            cut_weight = nx.cut_size(G, subset, weight='weight')
            if cut_weight > max_cut_weight:
                max_cut_weight = cut_weight
                max_cut = subset

    return max_cut_weight, max_cut

def simple_greedy_search(G):
    # Simple Greedy Algorithm
    #nodes = sorted(G.nodes, key=lambda node: sum([G[node][neighbor]['weight'] for neighbor in G[node]]), reverse=True)
    nodes = G.nodes
    n = G.number_of_nodes()
    max_cut_weight = 0
    max_cut = None
    cut_weight = 0
    cut = set()
    for _ in range(n):
        for node in nodes:
            if node not in cut:
                cut.add(node)
                cut_weight = nx.cut_size(G, cut, weight='weight')
                if cut_weight > max_cut_weight:
                    max_cut_weight = cut_weight
                    max_cut = cut.copy()
                else:
                    cut.remove(node)
    return max_cut_weight, max_cut

def sg3_greedy_search(G):
    # Inicialização
    V = set(G.nodes)
    S1, S2 = set(), set()

    # Escolha a aresta de maior peso
    if len(G.edges) == 0:
        return S1, S2, 0
    max_weight_edge = max(G.edges(data=True), key=lambda x: x[2]['weight'])
    x, y = max_weight_edge[0], max_weight_edge[1]
    S1.add(x)
    S2.add(y)
    V.remove(x)
    V.remove(y)

    def get_edge_weight(graph, node1, node2):
        if graph.has_edge(node1, node2):
            edge_data = graph.get_edge_data(node1, node2)
            return edge_data.get('weight', 0)
        else:
            return 0
    
    scores = {}
    # Calcula os scores de cada vértice
    for i in V:
        scores[i] = 0
        for j in S1:
            scores[i] += get_edge_weight(G,i,j)
        for j in S2:
            scores[i] = abs(scores[i] - get_edge_weight(G,i,j))

    # Iteração sobre os demais vértices
    for _ in range(G.number_of_nodes() - 2):
        # Escolhe o vértice com maior score
        if len(scores) == 0:
            break
        i_max = max(scores, key=scores.get)
        # Se a aresta para S1 for maior, adicione i* a S2, caso contrário, adicione a S1
        if max(get_edge_weight(G,i_max,j) for j in S1) > max(get_edge_weight(G,i_max,j) for j in S2):
            S2.add(i_max)
        else:
            S1.add(i_max)
        del scores[i_max]
        for i in V:
            scores[i] = get_edge_weight(G,i,i_max)
        V.remove(i_max)

    return nx.cut_size(G, S1, S2, weight='weight'), S1

if __name__ == '__main__':
    
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-min_v', '--minimum_vertices', type=int, default=2, help='Minimum number of vertices')
    group.add_argument('-max_v', '--maximum_vertices', type=int, default=None, help='Maximum number of vertices')
    parser.add_argument('-p', '--percentage', type=int, default=4, help='1: 0.125,\n2: till 0.25,\n3: till 0.5, 4:\ntill 0.75')
    parser.add_argument('-e', '--exhaustive', action='store_true', help='Run exhaustive search')
    parser.add_argument('-g_s', '--simple_greedy', action='store_true', help='Run simple greedy search')
    parser.add_argument('-g_sg3', '--sg3_greedy', action='store_true', help='Run sg3 greedy search')
    args = parser.parse_args()

    for num_vertices in range(args.minimum_vertices, args.maximum_vertices+1):
        percentage = [0.125, 0.25, 0.5, 0.75][:args.percentage]
        for p in percentage:
            print(f'Graph with {num_vertices} vertices and {p} density')
            G=generate_random_graph(num_vertices, p)

            if args.exhaustive:
                start = time.perf_counter()
                print(exhaustive_search(G.copy()))
                end = time.perf_counter()
                print(f'Exhaustive elapsed time: {end-start}s\n')

            if args.simple_greedy:
                start = time.perf_counter()
                print(simple_greedy_search(G.copy()))
                end = time.perf_counter()
                print(f'Greedy elapsed time: {end-start}s\n')

            if args.sg3_greedy:
                start = time.perf_counter()
                print(sg3_greedy_search(G.copy()))
                end = time.perf_counter()
                print(f'Greedy elapsed time: {end-start}s\n')
