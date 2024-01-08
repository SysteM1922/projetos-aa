from argparse import ArgumentParser
import random
from collections import Counter
import time

PROBABILITY = 1/16

def read_file(file):
    with open(file, 'r') as f:
        return "".join(f.readlines())

def exact_counter(file, k):
    return Counter(read_file(file)).most_common(k)

def approximate_counter(file, k, runs):
    counter = Counter()
    stream = read_file(file)
    for _ in range(runs):
        for letter in stream:
            if random.random() < PROBABILITY:
                counter[letter] += 1

    return counter.most_common(k)

def space_saving_counter(file, k):
    counter = Counter()
    stream = read_file(file)
    for letter in stream:
        if letter in counter:
            counter[letter] += 1
        elif len(counter) < k:
            counter[letter] = 1
        else:
            min_letter = min(counter, key=counter.get)
            counter[letter] = counter[min_letter] + 1
            del counter[min_letter]

    return counter.most_common(k)

if __name__ == '__main__':
    
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', help='File to be read')
    parser.add_argument('-n', '--number', help='Most n frequent letters', type=int, default=26)
    parser.add_argument('-e', '--exact', action='store_true', help='Run the exact counter')
    parser.add_argument('-a', '--approximate', action='store_true', help='Run the approximate counter')
    parser.add_argument('-ds', '--data_stream', action='store_true', help='Run the data stream counter')
    parser.add_argument('-k', '--k', help='Number of runs to execute the approximate counter', type=int, default=1)
    args = parser.parse_args()

    results = None
    if args.exact:
        start = time.perf_counter()
        results = exact_counter(args.file, args.number)
        end = time.perf_counter()
        print(f'Exact counter took {end - start} seconds')
    elif args.approximate:
        start = time.perf_counter()
        results = approximate_counter(args.file, args.number, args.k)
        end = time.perf_counter()
        print(f'Approximate counter took {end - start} seconds')
    elif args.data_stream:
        start = time.perf_counter()
        results = space_saving_counter(args.file, args.number)
        end = time.perf_counter()
        print(f'Data stream counter took {end - start} seconds')
    else:
        exit('You must choose between exact and approximate counters')

    with open('results.csv', 'w') as f:
        # print the n most frequent letters
        print(f'The {args.number} most frequent letters are:')
        f.write(f'letter,count')
        for letter, count in results:
            print(f'{letter}: {count}')
            f.write(f'\n{letter},{count}')
