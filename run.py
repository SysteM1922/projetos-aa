from itertools import combinations
import networkx as nx
from graph_generator import generate_random_graph
from argparse import ArgumentParser
import time

def exhaustive_search(G):

    nodes = G.nodes
    n = G.number_of_nodes()
    max_cut_weight = 0
    max_cut = None

    n_sol = 0
    n_oper = 0

    # Iteração sobre os subconjuntos de vértices
    for i in range(n):
        # Combinações de i vértices
        for subset in combinations(nodes, i):
            # Calcula o peso do corte para o subconjunto
            cut_weight = nx.cut_size(G, subset, weight='weight')
            # Se o peso do corte for maior que o máximo, atualize o máximo
            n_oper += 1
            if cut_weight > max_cut_weight:
                max_cut_weight = cut_weight
                max_cut = subset
            n_sol += 1

    return max_cut_weight, n_sol, n_oper

def simple_greedy_search(G, sort=False):

    nodes = G.nodes

    if sort:
        # Ordena os vértices pelo peso das arestas incidentes em ordem decrescente
        nodes = sorted(nodes, key=lambda x: sum([G.get_edge_data(x, y).get('weight', 0) for y in G.adj[x]]), reverse=True)

    max_cut_weight = 0
    max_cut = None
    cut_weight = 0
    cut = set()
    n_sol = 0
    n_oper = 0

    # Iteração sobre os vértices
    for node in nodes:
        # Se o vértice não estiver no corte, adicione-o e calcule o peso do corte
        if node not in cut:
            cut.add(node)
            cut_weight = nx.cut_size(G, cut, weight='weight')
            # Se o peso do corte for maior que o máximo, atualize o máximo
            n_oper += 1
            n_sol += 1
            if cut_weight > max_cut_weight:
                max_cut_weight = cut_weight
                max_cut = cut.copy()
            # Se o peso do corte for menor que o máximo, remova o vértice do corte
            else:
                cut.remove(node)
        n_oper += 1

    return max_cut_weight, n_sol, n_oper

def sg3_greedy_search(G):
    V = set(G.nodes)
    S1, S2 = set(), set()

    n_sol = 0
    n_oper = 1

    # Se o grafo for vazio, retorne o corte vazio
    if len(G.edges) == 0:
        return 0, n_sol, n_oper
    
    # Calcula a aresta de maior peso
    max_weight_edge = max(G.edges(data=True), key=lambda x: x[2]['weight'])
    x, y = max_weight_edge[0], max_weight_edge[1]

    # Adiciona os vértices da aresta ao corte
    S1.add(x)
    S2.add(y)

    # Remove os vértices da aresta do conjunto de vértices
    V.remove(x)
    V.remove(y)

    # Função para obter o peso da aresta entre dois vértices, retorna 0 se não existir
    def get_edge_weight(graph, node1, node2):
        if graph.has_edge(node1, node2):
            edge_data = graph.get_edge_data(node1, node2)
            return edge_data.get('weight', 0)
        else:
            return 0
    
    scores = {}
    # Calcula os scores de cada vértice
    # O score é o módulo da diferença entre a soma dos pesos das arestas de um vértice i para os vértices de S1 e S2
    for i in V:
        scores[i] = 0
        for j in S1:
            scores[i] += get_edge_weight(G,i,j)
            n_oper += 1
        for j in S2:
            scores[i] = abs(scores[i] - get_edge_weight(G,i,j))
            n_oper += 1

    # Iteração sobre os vértices restantes
    for _ in range(G.number_of_nodes() - 2):
        # Se não houver mais vértices para avaliar, pare
        if len(scores) == 0:
            n_oper += 1
            break
        # Obtenha o vértice com maior score
        i_max = max(scores, key=scores.get)
        # Se a aresta para S1 for maior, adicione i_max a S2, caso contrário, adicione a S1
        n_sol += 1
        n_oper += len(S1) + len(S2)
        if max(get_edge_weight(G,i_max,j) for j in S1) > max(get_edge_weight(G,i_max,j) for j in S2):
            S2.add(i_max)
        else:
            S1.add(i_max)
        n_oper += 1
        # Remova o vértice do conjunto de vértices
        del scores[i_max]
        # Atualize os scores dos vértices restantes
        for i in V:
            scores[i] = get_edge_weight(G,i,i_max)
            n_oper += 1
        # Remova o vértice do conjunto de vértices
        V.remove(i_max)

    # Retorne o peso do corte e o corte
    return nx.cut_size(G, S1, S2, weight='weight'), n_sol, n_oper

if __name__ == '__main__':
    
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-min_v', '--minimum_vertices', type=int, default=2, help='Minimum number of vertices')
    group.add_argument('-max_v', '--maximum_vertices', type=int, default=None, help='Maximum number of vertices')
    parser.add_argument('-p', '--percentage', type=int, default=4, help='1: 0.125,\n2: till 0.25,\n3: till 0.5, 4:\ntill 0.75')
    parser.add_argument('-e_s', '--exhaustive', action='store_true', help='Run exhaustive search')
    parser.add_argument('-g_s', '--simple_greedy', action='store_true', help='Run simple greedy search')
    parser.add_argument('-g_s_sorted', '--simple_greedy_sorted', action='store_true', help='Run simple greedy search with sorted nodes')
    parser.add_argument('-g_sg3', '--sg3_greedy', action='store_true', help='Run sg3 greedy search')
    args = parser.parse_args()

    lst = []
    lst2 = []

    for num_vertices in range(args.minimum_vertices, args.maximum_vertices+1):
        percentage = [0.125, 0.25, 0.5, 0.75][:args.percentage]
        for p in percentage:
            print("\033[93m {}\033[00m" .format(f'Graph with {num_vertices} vertices and {p} density'))
            G=generate_random_graph(num_vertices, p)

            if args.exhaustive:
                start = time.perf_counter()
                result = exhaustive_search(G.copy())
                print("\t",result[0])
                end = time.perf_counter()
                print("\033[92m {}\033[00m".format(f'\tExhaustive elapsed time: {end-start}s\n'))
                #lst.append([num_vertices, p, end-start, result[0], result[1], result[2]])

            if args.simple_greedy:
                start = time.perf_counter()
                result = simple_greedy_search(G.copy())
                print("\t",result[0])
                end = time.perf_counter()
                print("\033[92m {}\033[00m".format(f'\tGreedy Simple elapsed time: {end-start}s\n'))
                #lst.append([num_vertices, p, end-start, result[0], result[1], result[2]])

            if args.simple_greedy_sorted:
                start = time.perf_counter()
                result = simple_greedy_search(G.copy(), sort=True)
                print("\t",result[0])
                end = time.perf_counter()
                print("\033[92m {}\033[00m".format(f'\tGreedy Sorted elapsed time: {end-start}s\n'))
                #lst.append([num_vertices, p, end-start, result[0], result[1], result[2]])
                #lst2.append([num_vertices, p, end-start, result[0], result[1], result[2]])

            if args.sg3_greedy:
                start = time.perf_counter()
                result = sg3_greedy_search(G.copy())
                print("\t",result[0])
                end = time.perf_counter()
                print("\033[92m {}\033[00m".format(f'\tGreedy SG3 elapsed time: {end-start}s\n'))
                #lst.append([num_vertices, p, end-start, result[0], result[1], result[2]])

with open('results.csv', 'w') as f:
    f.write("num_vertices,edge_ratio,elapsed_time,weight,n_sol,n_oper\n")
    for item in lst:
        f.write("%s\n" % ",".join(map(str, item)))