from itertools import combinations
import networkx as nx
from graph_generator import load_graph, generate_random_graph
from argparse import ArgumentParser
import time
import random

NMEC = 103600

random.seed(NMEC)

def exhaustive_search(G: nx.Graph):

    nodes = G.nodes
    n = G.number_of_nodes()
    max_cut_weight = 0

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
            n_sol += 1

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

def monte_carlo_random_cut(G: nx.Graph):
    # Inicializa o corte
    S1, S2 = set(), set()
    # Iteração sobre os vértices
    for i in G.nodes:
        # Adiciona o vértice ao corte com probabilidade 0.5
        if random.random() < 0.5:
            S1.add(i)
        else:
            S2.add(i)

    return tuple(S1), tuple(S2)
    
def random_node_choose_best_edge_cut(G: nx.Graph):
    # Copia o grafo
    G = G.copy()
    # Inicializa o corte
    S1, S2 = set(), set()
    # Randomiza a ordem dos vértices
    nodes = list(G.nodes)
    random.shuffle(nodes)
    # Iteração sobre os vértices
    for i in nodes:
        # Se o vértice i já estiver no corte, continue
        if i in S2:
            continue
        # Adiciona o vértice i a S1 e a S2 o vértice ligado a i com a aresta de maior peso
        S1.add(i)
        neighbors = list(G.neighbors(i))
        if len(neighbors) > 0:
            max_neighbor = max(neighbors, key=lambda x: G.get_edge_data(i, x).get('weight', 0))
            S2.add(max_neighbor)
            G.remove_node(max_neighbor)
        G.remove_node(i)

    return tuple(S1), tuple(S2)


def random_search(G: nx.Graph, max_tries = 100, max_time = float("inf"), random_cut_func=None):
    
    # Se o grafo não tiver arestas então não deve ser pesquisado
    if G.number_of_edges == 0:
        return 0, 0, 0
    max_tries = 2**G.number_of_nodes()//2*max_tries//100
    
    # Soluções testadas
    tested_sol = set()
    best_cut_weight = 0
    n_sol = 0
    n_oper = 0
    n_iter = 0
    start = time.perf_counter()

    # Iteração sobre o número de tentativas
    while n_iter < max_tries and time.perf_counter() - start < max_time:
        n_iter += 1
        # Gera um corte aleatório
        S1, S2 = random_cut_func(G)
        # Verifica se o corte já foi testado
        if S1 in tested_sol:
            continue
        # Calcula o peso do corte
        cut_weight = nx.cut_size(G, S1, S2, weight='weight')
        # Se o peso do corte for maior que o máximo, atualize o máximo
        if cut_weight > best_cut_weight:
            n_oper += 1
            best_cut_weight = cut_weight
        # Adiciona o corte ao conjunto de cortes testados
        tested_sol.add(S1)
        tested_sol.add(S2)
        n_sol += 1

    return best_cut_weight, n_sol, n_oper, n_iter

if __name__ == '__main__':
    
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-min_v', '--minimum_vertices', type=int, default=2, help='Minimum number of vertices')
    group.add_argument('-max_v', '--maximum_vertices', type=int, default=None, help='Maximum number of vertices')
    parser.add_argument('-p', '--percentage', type=int, default=4, help='1: 0.125,\n2: till 0.25,\n3: till 0.5, 4:\ntill 0.75')
    parser.add_argument('-e_s', '--exhaustive', action='store_true', help='Run exhaustive search')
    parser.add_argument('-g_sg3', '--sg3_greedy', action='store_true', help='Run sg3 greedy search')
    parser.add_argument('-m_c', '--monte_carlo_random', action='store_true', help='Run monte carlo random search')
    parser.add_argument('-b_e', '--random_node_choose_best_edge', action='store_true', help='Run random node choose best edge search')
    parser.add_argument('-max_time', '--max_time', type=float, default=float("inf"), help='Maximum time to run the random algorithms')
    parser.add_argument('-max_tries', '--max_tries', type=float, default=100, help='Percentage of max number of tries to run the random algorithms')
    args = parser.parse_args()

    if 0 > args.max_tries > 100:
        # inform that max_tries can't be greater than 100
        print("max_tries must be between 0%\\ and 100%")
        exit(0)

    lst = []
    lst2 = []
    lst3 = []

    """for num_vertices in range(args.minimum_vertices, args.maximum_vertices+1):
        percentage = [0.125, 0.25, 0.5, 0.75][:args.percentage]
        for p in percentage:
            print("\033[93m {}\033[00m" .format(f'Graph with {num_vertices} vertices and {p} density'))
            G=load_graph(f"graphs/graph_{num_vertices}_{p}.gml")
            #G=generate_random_graph(num_vertices, p)

            if args.exhaustive:
                start = time.perf_counter()
                result = exhaustive_search(G.copy())
                print("\t",result[0])
                end = time.perf_counter()
                print("\033[92m {}\033[00m".format(f'\tExhaustive elapsed time: {end-start}s\n'))
                lst.append([num_vertices, p, end-start, result[0], result[1], result[2], result[1]])

            if args.sg3_greedy:
                start = time.perf_counter()
                result = sg3_greedy_search(G.copy())
                print("\t",result[0])
                end = time.perf_counter()
                print("\033[92m {}\033[00m".format(f'\tGreedy SG3 elapsed time: {end-start}s\n'))
                lst.append([num_vertices, p, end-start, result[0], result[1], result[2], result[1]])

            if args.monte_carlo_random:
                start = time.perf_counter()
                result = random_search(G.copy(), max_tries=args.max_tries, max_time=args.max_time, random_cut_func=monte_carlo_random_cut)
                print("\t",result[0])
                end = time.perf_counter()
                print("\033[92m {}\033[00m".format(f'\tMonte Carlo Random elapsed time: {end-start}s\n'))
                lst2.append([num_vertices, p, end-start, result[0], result[1], result[2], result[3]])

            if args.random_node_choose_best_edge:
                start = time.perf_counter()
                result = random_search(G.copy(), max_tries=args.max_tries, max_time=args.max_time, random_cut_func=random_node_choose_best_edge_cut)
                print("\t",result[0])
                end = time.perf_counter()
                print("\033[92m {}\033[00m".format(f'\tRandom Node Choose Best Edge elapsed time: {end-start}s\n'))
                lst3.append([num_vertices, p, end-start, result[0], result[1], result[2], result[3]])"""

    G=load_graph(f"graphs/SW10000EWD.gml")

    if args.sg3_greedy:
        start = time.perf_counter()
        result = sg3_greedy_search(G.copy())
        print("\t",result[0])
        end = time.perf_counter()
        print("\033[92m {}\033[00m".format(f'\tGreedy SG3 elapsed time: {end-start}s\n'))
        lst.append([G.number_of_nodes(), 0, end-start, result[0], result[1], result[2], result[1]])

    if args.monte_carlo_random:
        start = time.perf_counter()
        result = random_search(G.copy(), max_tries=args.max_tries, max_time=args.max_time, random_cut_func=monte_carlo_random_cut)
        print("\t",result[0])
        end = time.perf_counter()
        print("\033[92m {}\033[00m".format(f'\tMonte Carlo Random elapsed time: {end-start}s\n'))
        lst2.append([G.number_of_nodes(), 0, end-start, result[0], result[1], result[2], result[3]])

    if args.random_node_choose_best_edge:
        start = time.perf_counter()
        result = random_search(G.copy(), max_tries=args.max_tries, max_time=args.max_time, random_cut_func=random_node_choose_best_edge_cut)
        print("\t",result[0])
        end = time.perf_counter()
        print("\033[92m {}\033[00m".format(f'\tRandom Node Choose Best Edge elapsed time: {end-start}s\n'))
        lst3.append([G.number_of_nodes(), 0, end-start, result[0], result[1], result[2], result[3]])


with open('results.csv', 'w') as f:
    f.write("num_vertices,edge_ratio,elapsed_time,weight,n_sol,n_oper,n_iter\n")
    for item in lst:
        f.write("%s\n" % ",".join(map(str, item)))

with open('results2.csv', 'w') as f:
    f.write("num_vertices,edge_ratio,elapsed_time,weight,n_sol,n_oper,n_iter\n")
    for item in lst2:
        f.write("%s\n" % ",".join(map(str, item)))

with open('results3.csv', 'w') as f:
    f.write("num_vertices,edge_ratio,elapsed_time,weight,n_sol,n_oper,n_iter\n")
    for item in lst3:
        f.write("%s\n" % ",".join(map(str, item)))