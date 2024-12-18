import click
import numpy as np

class Board:
    def __init__(self, data, size, nbytes):
        self.board = np.full((size, size), '.')
        self.data = data
        for i in range(nbytes):
            self.board[*data[i]] = '#'
        self.counter = nbytes

    def add_byte(self, byte):
        self.board[*byte] = '#'

    def check_p(self, p):
        return p[0] >= 0 and p[1] >= 0 and p[0] < self.board.shape[0] and p[1] < self.board.shape[1]

    def dijkstra(self, start, end):
        unvisited = np.full(self.board.shape, 1)
        distances = np.full(self.board.shape, np.inf)
        distances[*start] = 0
        while unvisited[*end] == 1:
            p = min([x for x in np.argwhere(unvisited == 1)], key=lambda x: distances[*x])
            candidates = [(p[0] + 1, p[1]), (p[0] - 1, p[1]),
                          (p[0], p[1] + 1), (p[0], p[1] - 1)]
            candidates = [p for p in candidates if self.check_p(p) and self.board[*p] != '#']
            if len(candidates) == 0:
                return np.inf
            for candidate in candidates:
                distances[*candidate] = distances[*p] + 1
            unvisited[*p] = 0
        return int(distances[*end])

    def print(self):
        for row in self.board:
            print(''.join(row))

def binsearch(data, start, end, size, a, b):
    if a == b:
        return data[a - 1]
    full = len(data)
    mid = a + int((b - a) / 2)
    board = Board(data, size, mid)
    result = board.dijkstra(start, end)
    print(result, a, b)
    if result == np.inf:
        return binsearch(data, start, end, size, a, mid)
    else:
        return binsearch(data, start, end, size, mid + 1, b)

@click.command()
@click.option('-i', '--input-file', help='Input data file')
@click.option('-s', '--size', help='Board size')
@click.option('-n', '--nbytes', help='Number of bytes')
def main(input_file, size, nbytes):
    with open(input_file, 'r') as fd:
        data = []
        for line in fd:
            line = line.strip().split(',')
            data.append((int(line[1]), int(line[0])))
        print(data)
        print(len(data))
        board = Board(data, int(size), int(nbytes))
        board.print()
        print(binsearch(data, (0, 0), (int(size) - 1, int(size) - 1), int(size), 0, len(data)))

if __name__ == '__main__':
    main()