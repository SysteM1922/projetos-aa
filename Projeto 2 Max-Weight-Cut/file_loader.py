import csv
import matplotlib.pyplot as plt

def load_file(file_name):
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None)
        data = []
        for row in reader:
            # remove all empty strings
            row = list(filter(None, row))
            # convert all strings to floats
            data.append([int(row[0]), float(row[1]), float(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6])])
    return data

def write_file(file_name, data):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["num_vertices","edge_ratio","elapsed_time","weight","n_sol","n_oper","n_iter"])
        for row in data:
            writer.writerow(row)

if __name__ == '__main__':
    
    #data_es = load_file('results_es.csv')
    data_mc = load_file('results2.csv')
    data_sg3 = load_file('results_sg3.csv')
    data_be = load_file('results3.csv')


    # plot a graphic with the number of solutions tested per 0.75 density graphs with one line for each algorithm
    plt.figure()
    plt.title('Number of iteractions vs Number of vertices')
    plt.xlabel('Number of vertices')
    plt.ylabel('Number of iteractions')
    plt.grid(True)
    plt.yscale('linear')
    plt.plot([i[0] for i in data_mc if i[1] == 0], [i[6] for i in data_mc if i[1] == 0], label='Monte Carlo')
    plt.plot([i[0] for i in data_be if i[1] == 0], [i[6] for i in data_be if i[1] == 0], label='NAMA')
    plt.legend()
    plt.savefig('iteractions_x_graphs_m_c_sg3_075.png')
    plt.show()
    plt.clf()
    """
   
    with open('results.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None)
        columns = []
        for row in reader:
            row = list(filter(None, row))
            columns.append([float(el) for el in row])

    plt.figure()
    plt.title('Max Weight Cut Update % per graph')
    plt.xlabel('Graph #')
    plt.ylabel('Percentage of max number of solutions')
    plt.grid(True)
    plt.yscale('linear')
    # each list in columns list is the list of percentages for each graph
    # make a dispersion map for every graph
    for i in range(len(columns)):
        plt.scatter([i for _ in range(len(columns[i]))], columns[i])
    plt.savefig('solutions_x_graphs.png')
    plt.show()
    plt.clf()

    n_equals = 0
    size = len(data_es)
    for i in range(len(data_es)):
        if data_es[i][3] == data_mc[i][3]:
            n_equals += 1
    print(f'Number of times that the max cut weight was the same: {n_equals} ({n_equals/size*100}%)')


    # plot a graphic with the max cut weight per vertice of each algorithm with one line for each algorithm for density 0.75
    plt.figure()
    plt.title('Number of vertices vs Max cut weight for edge ratio 0.75')
    plt.xlabel('Number of vertices')
    plt.ylabel('Max cut weight')
    plt.grid(True)
    plt.yscale('linear')
    plt.plot([i[0] for i in data_es if i[1] == 0.75], [i[3] for i in data_es if i[1] == 0.75], label='Greedy SG3')
    plt.plot([i[0] for i in data_be if i[1] == 0.75], [i[3] for i in data_be if i[1] == 0.75], label='NAMA')
    #plt.plot([i[0] for i in data_sg3], [i[5] for i in data_sg3], label='Greedy SG3')
    plt.legend()
    plt.savefig('weight_x_vertices_e_s_b_e_075.png')
    plt.show()
    plt.clf()


    percentage = [0.125, 0.25, 0.5, 0.75]
    # plot a graphic with the vertices and the time with one line for each density
    plt.figure()
    plt.title('Time taken vs Number of vertices')
    plt.xlabel('Number of vertices')
    plt.ylabel('Time taken (s)')
    plt.grid(True)
    plt.yscale('linear')
    for p in percentage:
        plt.plot([i[0] for i in data_mc if i[1] == p], [i[2] for i in data_mc if i[1] == p], label=f'edge ratio {p}')
    plt.legend()
    plt.savefig('time_x_vertices.png')
    plt.show()
    plt.clf()

    # plot a graphic with the vertices and the number of iterations with one line for each density
    plt.title('Number of solutions tested vs Number of vertices')
    plt.xlabel('Number of vertices')
    plt.ylabel('Number of solutions tested')
    plt.grid(True)
    plt.yscale('linear')
    for p in percentage:
        plt.plot([i[0] for i in lst if i[1] == p], [i[4] for i in lst if i[1] == p], label=f'edge ratio {p}')
    plt.legend()
    plt.savefig('solutions_x_vertices.png')
    plt.show()
    plt.clf()
    
    # plot a graphic with the vertices and the number of basic operations with one line for each density
    plt.title('Number of basic operations vs Number of vertices')
    plt.xlabel('Number of vertices')
    plt.ylabel('Number of basic operations')
    plt.grid(True)
    plt.yscale('log')
    for p in percentage:
        plt.plot([i[0] for i in lst if i[1] == p], [i[5] for i in lst if i[1] == p], label=f'edge ratio {p}')
    plt.legend()
    plt.savefig('operations_x_vertices.png')
    plt.show()
    plt.clf()
    
    # plot a graphic per density with the max_cut_weight per vertice of each algorithm with one line for each algorithm
    for p in percentage:
        plt.title(f'Max cut weight vs Number of vertices for edge ratio {p}')
        plt.xlabel('Number of vertices')
        plt.ylabel('Max cut weight')
        plt.grid(True)
        plt.yscale('linear')
        plt.plot([i[0] for i in lst if i[1] == p], [i[3] for i in lst if i[1] == p], label='Greedy Simple')
        plt.plot([i[0] for i in lst2 if i[1] == p], [i[3] for i in lst2 if i[1] == p], label='Greedy Sorted')
        plt.legend()
        plt.savefig(f'max_cut_weight_x_vertices_{p}.png')
        plt.show()
        plt.clf()
    
    # plot a graphic per density 0.75 with the time per vertice of each algorithm with one line for each algorithm
    plt.title(f'Time taken vs Number of vertices for edge ratio 0.75')
    plt.xlabel('Number of vertices')
    plt.ylabel('Time taken (s)')
    plt.grid(True)
    plt.yscale('linear')
    plt.plot([i[0] for i in lst if i[1] == 0.75], [i[2] for i in lst if i[1] == 0.75], label='Greedy Simple')
    plt.plot([i[0] for i in lst2 if i[1] == 0.75], [i[2] for i in lst2 if i[1] == 0.75], label='Greedy Sorted')
    plt.legend()
    plt.savefig(f'time_x_vertices_0.75.png')
    plt.show()
    plt.clf()
    
    # compare the number of times that gredy_simple algorithms found the max cut weight for each density
    max_gredy_simple = 0
    max_gredy_sorted = 0
    for p in percentage:
        print(f'edge ratio {p}')
        for i in range(len(lst)):
            if lst[i][1] == p:
                if lst[i][3] > lst2[i][3]:
                    max_gredy_simple += 1
                elif lst[i][3] < lst2[i][3]:
                    max_gredy_sorted += 1
        print(f'Greedy Simple: {max_gredy_simple}')
        print(f'Greedy Sorted: {max_gredy_sorted}')
        max_gredy_simple = 0
        max_gredy_sorted = 0
    """
        