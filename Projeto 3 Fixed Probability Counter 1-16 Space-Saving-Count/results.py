import csv
import matplotlib.pyplot as plt

def load_file(file_name: str):
    with open(file_name, newline='') as csvfile:
        csvfile.readline()
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        data = []
        for row in reader:
            data.append((row[0], int(row[1])))
        return data

def load_file_1(file_name: str):
    with open(file_name, newline='') as csvfile:
        csvfile.readline()
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        data = []
        for row in reader:
            data.append((row[0], int(row[1])))
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if letter not in [row[0] for row in data]:
                data.append((letter, 0))
        sorted_data = sorted(data, key=lambda x: x[0])
        total_letters = sum([row[1] for row in sorted_data])
        #sorted_data = [(row[0], row[1] / total_letters) for row in sorted_data]
        return sorted_data

def precision(exact, approx):
    wrong = 0
    for idx in range(len(exact)):
        if idx > len(approx)-1 or exact[idx][0] != approx[idx][0]:
            wrong += 1

    return 1 - (wrong / len(exact))

def precision_1(exact, approx):
    wrong = 0
    for idx in range(len(approx)):
        if idx > len(approx)-1 or exact[idx][0] != approx[idx][0]:
            wrong += 1

    return 1 - (wrong / len(approx))

def abs_error(exact, approx):
    return abs(exact - approx)

def rel_error(exact, approx):
    return abs(exact - approx) / exact
    
def main():

    """
    book1 = load_file_1('results/results1_e.csv')
    book2 = load_file_1('results/results2_e.csv')
    book3 = load_file_1('results/results3_e.csv')
    # graphic with the frequency of each letter in every book
    plt.title('Absolute Frequency of each letter in every book (Exact Counter)')
    plt.xlabel('Letter')
    plt.ylabel('Absolute Frequency')
    plt.plot([row[0] for row in book1], [row[1] for row in book1], label='Spanish', marker='o')
    plt.plot([row[0] for row in book2], [row[1] for row in book2], label='Portuguese', marker='o')
    plt.plot([row[0] for row in book3], [row[1] for row in book3], label='English', marker='o')
    plt.legend()
    plt.savefig('letters_absolute_frequency_exact.png')
    """
    
    """
    book1_e = load_file('results/results1_e.csv')
    book1_1 = load_file('results/results1_1.csv')
    book1_10 = load_file('results/results1_10.csv')
    book1_100 = load_file('results/results1_100.csv')

    book2_e = load_file('results/results2_e.csv')
    book2_1 = load_file('results/results2_1.csv')
    book2_10 = load_file('results/results2_10.csv')
    book2_100 = load_file('results/results2_100.csv')

    book3_e = load_file('results/results3_e.csv')
    book3_1 = load_file('results/results3_1.csv')
    book3_10 = load_file('results/results3_10.csv')
    book3_100 = load_file('results/results3_100.csv')

    with open('results.csv', 'w') as f:
        print("|{:35s}|{:10s}|{:>10s}|{:>15s}|{:>15s}|{:>15s}|{:>15s}|{:>15s}|{:>15s}|".format("Book", "Counter", "Precision", "Max Abs Error", "Min Abs Error", "Avg Abs Error", "Max Rel Error", "Min Rel Error", "Avg Rel Error"))
        f.write("Book,Counter,Precision,Max Abs Error,Min Abs Error,Avg Abs Error,Max Rel Error,Min Rel Error,Avg Rel Error\n")
        for book in [("La venganza de Don Mendo", book1_e, book1_1, book1_10, book1_100),
                     ("O Mysterio da Estrada de Cintra", book2_e, book2_1, book2_10, book2_100),
                     ("The Tragedy of Romeo and Juliet", book3_e, book3_1, book3_10, book3_100)]:

            abs_errors = [abs_error(book[1][idx][1], book[2][idx][1] if idx < len(book[2]) else 0) for idx in range(len(book[1]))]
            rel_errors = [rel_error(book[1][idx][1], book[2][idx][1] if idx < len(book[2]) else 0) for idx in range(len(book[1]))]
            print("|{:35s}|{:10s}|{:10.2f}|{:15.1f}|{:15.1f}|{:15.2f}|{:15.5f}|{:15.5f}|{:15.5f}|".format(book[0], "Approx 1", precision(book[1], book[2]), max(abs_errors), min(abs_errors), sum(abs_errors) / len(abs_errors), max(rel_errors), min(rel_errors), sum(rel_errors) / len(rel_errors)))
            f.write("{},{},{},{},{},{},{},{},{}\n".format(book[0], "Approx 1", precision(book[1], book[2]), max(abs_errors), min(abs_errors), sum(abs_errors) / len(abs_errors), max(rel_errors), min(rel_errors), sum(rel_errors) / len(rel_errors)))
            abs_errors = [abs_error(book[1][idx][1], book[3][idx][1]//10 if idx < len(book[3]) else 0) for idx in range(len(book[1]))]
            rel_errors = [rel_error(book[1][idx][1], book[3][idx][1]/10 if idx < len(book[3]) else 0) for idx in range(len(book[1]))]
            print("|{:35s}|{:10s}|{:10.2f}|{:15.1f}|{:15.1f}|{:15.2f}|{:15.5f}|{:15.5f}|{:15.5f}|".format(book[0], "Approx 10", precision(book[1], book[3]), max(abs_errors), min(abs_errors), sum(abs_errors) / len(abs_errors), max(rel_errors), min(rel_errors), sum(rel_errors) / len(rel_errors)))
            f.write("{},{},{},{},{},{},{},{},{}\n".format(book[0], "Approx 10", precision(book[1], book[3]), max(abs_errors), min(abs_errors), sum(abs_errors) / len(abs_errors), max(rel_errors), min(rel_errors), sum(rel_errors) / len(rel_errors)))
            abs_errors = [abs_error(book[1][idx][1], book[4][idx][1]//100 if idx < len(book[4]) else 0) for idx in range(len(book[1]))]
            rel_errors = [rel_error(book[1][idx][1], book[4][idx][1]/100 if idx < len(book[4]) else 0) for idx in range(len(book[1]))]
            print("|{:35s}|{:10s}|{:10.2f}|{:15.1f}|{:15.1f}|{:15.2f}|{:15.5f}|{:15.5f}|{:15.5f}|".format(book[0], "Approx 100", precision(book[1], book[4]), max(abs_errors), min(abs_errors), sum(abs_errors) / len(abs_errors), max(rel_errors), min(rel_errors), sum(rel_errors) / len(rel_errors)))
            f.write("{},{},{},{},{},{},{},{},{}\n".format(book[0], "Approx 100", precision(book[1], book[4]), max(abs_errors), min(abs_errors), sum(abs_errors) / len(abs_errors), max(rel_errors), min(rel_errors), sum(rel_errors) / len(rel_errors)))
    """

    book1_e = load_file('results/results1_e.csv')
    book1_ds_3 = load_file('results/results1_ds_3.csv')
    book1_ds_5 = load_file('results/results1_ds_5.csv')
    book1_ds_10 = load_file('results/results1_ds_10.csv')

    book2_e = load_file('results/results2_e.csv')
    book2_ds_3 = load_file('results/results2_ds_3.csv')
    book2_ds_5 = load_file('results/results2_ds_5.csv')
    book2_ds_10 = load_file('results/results2_ds_10.csv')

    book3_e = load_file('results/results3_e.csv')
    book3_ds_3 = load_file('results/results3_ds_3.csv')
    book3_ds_5 = load_file('results/results3_ds_5.csv')
    book3_ds_10 = load_file('results/results3_ds_10.csv')

    with open('results.csv', 'w') as f:
        print("|{:35s}|{:20s}|{:>10s}|{:>15s}|{:>15s}|{:>15s}|{:>15s}|{:>15s}|{:>15s}|".format("Book", "Counter", "Precision", "Max Abs Error", "Min Abs Error", "Avg Abs Error", "Max Rel Error", "Min Rel Error", "Avg Rel Error"))
        f.write("Book,Counter,Precision,Max Abs Error,Min Abs Error,Avg Abs Error,Max Rel Error,Min Rel Error,Avg Rel Error\n")
        for book in [("La venganza de Don Mendo", book1_e, book1_ds_3, book1_ds_5, book1_ds_10),
                     ("O Mysterio da Estrada de Cintra", book2_e, book2_ds_3, book2_ds_5, book2_ds_10),
                     ("The Tragedy of Romeo and Juliet", book3_e, book3_ds_3, book3_ds_5, book3_ds_10)]:

            abs_errors = [abs_error(book[1][idx][1], book[2][idx][1] if idx < len(book[2]) else 0) for idx in range(len(book[1]))]
            rel_errors = [rel_error(book[1][idx][1], book[2][idx][1] if idx < len(book[2]) else 0) for idx in range(len(book[1]))]
            print("|{:35s}|{:20s}|{:10.2f}|{:15.1f}|{:15.1f}|{:15.2f}|{:15.5f}|{:15.5f}|{:15.5f}|".format(book[0], "Metwally et Al. 3", precision_1(book[1], book[2]), max(abs_errors), min(abs_errors), sum(abs_errors) / len(abs_errors), max(rel_errors), min(rel_errors), sum(rel_errors) / len(rel_errors)))
            f.write("{},{},{},{},{},{},{},{},{}\n".format(book[0], "Metwally et Al. 3", precision_1(book[1], book[2]), max(abs_errors), min(abs_errors), sum(abs_errors) / len(abs_errors), max(rel_errors), min(rel_errors), sum(rel_errors) / len(rel_errors)))
            abs_errors = [abs_error(book[1][idx][1], book[3][idx][1] if idx < len(book[3]) else 0) for idx in range(len(book[1]))]
            rel_errors = [rel_error(book[1][idx][1], book[3][idx][1] if idx < len(book[3]) else 0) for idx in range(len(book[1]))]
            print("|{:35s}|{:20s}|{:10.2f}|{:15.1f}|{:15.1f}|{:15.2f}|{:15.5f}|{:15.5f}|{:15.5f}|".format(book[0], "Metwally et Al. 5", precision_1(book[1], book[3]), max(abs_errors), min(abs_errors), sum(abs_errors) / len(abs_errors), max(rel_errors), min(rel_errors), sum(rel_errors) / len(rel_errors)))
            f.write("{},{},{},{},{},{},{},{},{}\n".format(book[0], "Metwally et Al. 5", precision_1(book[1], book[3]), max(abs_errors), min(abs_errors), sum(abs_errors) / len(abs_errors), max(rel_errors), min(rel_errors), sum(rel_errors) / len(rel_errors)))
            abs_errors = [abs_error(book[1][idx][1], book[4][idx][1] if idx < len(book[4]) else 0) for idx in range(len(book[1]))]
            rel_errors = [rel_error(book[1][idx][1], book[4][idx][1] if idx < len(book[4]) else 0) for idx in range(len(book[1]))]
            print("|{:35s}|{:20s}|{:10.2f}|{:15.1f}|{:15.1f}|{:15.2f}|{:15.5f}|{:15.5f}|{:15.5f}|".format(book[0], "Metwally et Al. 10", precision_1(book[1], book[4]), max(abs_errors), min(abs_errors), sum(abs_errors) / len(abs_errors), max(rel_errors), min(rel_errors), sum(rel_errors) / len(rel_errors)))
            f.write("{},{},{},{},{},{},{},{},{}\n".format(book[0], "Metwally et Al. 10", precision_1(book[1], book[4]), max(abs_errors), min(abs_errors), sum(abs_errors) / len(abs_errors), max(rel_errors), min(rel_errors), sum(rel_errors) / len(rel_errors)))

    """
    book1_e = load_file('results/results3_e.csv')

    with open('results.csv', 'w') as f:
        sorted_by_letter = sorted(book1_e, key=lambda x: x[0])
        for book in sorted_by_letter:
            f.write("{}\n".format(book[1]))
    """

if __name__ == '__main__':
    main()