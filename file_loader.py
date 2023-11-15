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
            data.append([int(row[0]), float(row[1]), float(row[2]), int(row[3]), int(row[4]), int(row[5])])
    return data

def write_file(file_name, data):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["num_vertices","edge_ratio","elapsed_time","weight","n_sol","n_oper"])
        for row in data:
            writer.writerow(row)

if __name__ == '__main__':
    
    lst = load_file('results/results_sg3.csv')

    percentage = [0.125, 0.25, 0.5, 0.75]

    # plot a graphic with the vertices and the time with one line for each density
    plt.figure()
    plt.title('Time taken vs Number of vertices')
    plt.xlabel('Number of vertices')
    plt.ylabel('Time taken (s)')
    plt.grid(True)
    plt.yscale('linear')
    for p in percentage:
        plt.plot([i[0] for i in lst if i[1] == p], [i[2] for i in lst if i[1] == p], label=f'edge ratio {p}')
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
    """
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
        