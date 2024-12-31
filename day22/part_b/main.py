import click
from collections import defaultdict

def iterate(number, n):
    previous = number
    for _ in range(n):
        number = (number ^ (number * 64)) % 16777216
        number = (number ^ (number // 32)) % 16777216
        number = (number ^ (number * 2048)) % 16777216
        yield (number % 10) - (previous % 10), number % 10
        previous = number

def gather_sequences(lst, sequence_set):
    encountered = set()
    for x1, x2, x3, x4 in zip(lst[:-3], lst[1:-2], lst[2:-1], lst[3:]):
        candidate = (x1[0], x2[0], x3[0], x4[0])
        if candidate not in encountered:
            sequence_set[candidate].append(x4[1])
            encountered.add(candidate)

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    with open(input_file, 'r') as fd:
        initial_numbers = [int(x.strip()) for x in fd.read().strip().split('\n')]
    print(initial_numbers)
    result = []
    sequences = defaultdict(list)
    for number in initial_numbers:
        lst = list(iterate(number, 2000))
        gather_sequences(lst, sequences)
    best = max(sequences, key=lambda k: sum(sequences[k]))
    print(best)
    print(sum(sequences[best]))

if __name__ == '__main__':
    main()
