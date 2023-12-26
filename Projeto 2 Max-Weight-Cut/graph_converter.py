import networkx as nx

lines = []
nr_nodes = 0
with open("SW10000EWD.txt", "r") as f:
    f.readline()
    f.readline()
    nr_nodes = int(f.readline())
    f.readline()
    lines = f.readlines()

G = nx.Graph()
for line in lines:
    line = line.split()
    G.add_edge(int(line[0]), int(line[1]), weight=float(line[2]))

# save graph
nx.write_gml(G, f'graphs/SW10000EWD.gml')