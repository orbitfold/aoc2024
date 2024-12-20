import click
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

class Board:
    def __init__(self, data):
        self.board = data
        self.start = tuple(np.argwhere(self.board == 'S')[0])
        self.end = tuple(np.argwhere(self.board == 'E')[0])

    def h(self, p):
        return abs(self.end[0] - p[0]) + abs(self.end[1] - p[1])

    def get_neighbours(self, p):
        neighbours = [(p[0] + 1, p[1]), (p[0] - 1, p[1]),
                      (p[0], p[1] + 1), (p[0], p[1] - 1)]
        neighbours = [n for n in neighbours
                      if n[0] >= 0 and
                      n[1] >= 0 and
                      n[0] < self.board.shape[0] and
                      n[1] < self.board.shape[1] and
                      self.board[*n] != '#']
        return neighbours

    def show_path(self, path):
        b = np.zeros(self.board.shape)
        b[self.board == '#'] = 1
        for p in path:
            b[*p] = 2
        b[*self.start] = 3
        b[*self.end] = 4
        plt.imshow(b)
        plt.show()

    def show_time(self):
        b = np.zeros(self.board.shape)
        for t in self.time:
            b[*t] = self.time[t]
        plt.imshow(b)
        plt.show()

    def reconstruct_path(self, current, came_from):
        path = [current]
        while True:
            try:
                current = came_from[current]
                path = [current] + path
            except KeyError:
                return path

    def a_star(self):
        open_set = [self.start]
        came_from = {}
        gscore = defaultdict(lambda: np.inf)
        gscore[self.start] = 0
        fscore = defaultdict(lambda: np.inf)
        fscore[self.start] = self.h(self.start)
        while len(open_set) > 0:
            current = min(open_set, key=lambda p: fscore[p])
            if current == self.end:
                return self.reconstruct_path(current, came_from)
            open_set.remove(current)
            for neighbour in self.get_neighbours(current):
                tentative_gscore = gscore[current] + 1
                if tentative_gscore < gscore[neighbour]:
                    came_from[neighbour] = current
                    gscore[neighbour] = tentative_gscore
                    fscore[neighbour] = tentative_gscore + self.h(neighbour)
                    if neighbour not in open_set:
                        open_set.append(neighbour)
        return False

    def modified_boards(self, p):
        neighbours = [(p[0] + 1, p[1]), (p[0] - 1, p[1]),
                      (p[0], p[1] + 1), (p[0], p[1] - 1)]
        for n in neighbours:
            new_board = np.array(self.board)
            if n[0] >= 0 and n[1] >= 0 and n[0] < self.board.shape[0] and n[1] < self.board.shape[1] and new_board[*n] == '#':
                new_board[*n] = '.'
                yield Board(new_board)

    def after(self, time):
        path = [self.start]
        while time > 0:
            neighbours = self.get_neighbours(path[-1])
            for neighbour in neighbours:
                if neighbour not in path:
                    path.append(neighbour)
            time -= 1
        return path[-1]

    def find_close_points(self, current, path):
        possibilities = [current]
        for _ in range(2):
            new_possibilities = []
            for p in possibilities:
                neighbours = [(p[0] + 1, p[1]), (p[0] - 1, p[1]),
                              (p[0], p[1] + 1), (p[0], p[1] - 1)]
                for n in neighbours:
                    if n not in new_possibilities:
                        new_possibilities.append(n)
                possibilities = new_possibilities
        possibilities = [p for p in possibilities if p in path]
        return possibilities

    def diff_after(self, path, time):
        possibilities = self.find_close_points(path[time], path)
        new_paths = []
        diffs = [path.index(possibility) - time - 2 for possibility in possibilities]
        return [d for d in diffs if d > 0]

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    with open(input_file, 'r') as fd:
        data = [list(row) for row in fd.read().strip().split('\n')]
        data = np.array(data)
    board = Board(data)
    path = board.a_star()
    result = defaultdict(lambda: 0)
    for time in range(len(path) - 1):
        diffs = board.diff_after(path, time)
        for diff in diffs:
            result[diff] += 1
    r = 0
    for t in result:
        if t >= 100:
            r += result[t]
    print(r)
    #for p in path:
    #    print(board.find_close_points(p, path))
    #board.show_path(path)
    #print(board.after(10))
    #path = board.a_star()
    #length = len(path) - 1
    #print(len(path))
    #result = defaultdict(lambda: 0)
    #for start_time in range(length):
    #    after = board.after(start_time)
    #    diffs = []
    #    for new_board in board.modified_boards(after):
    #        shortest = new_board.a_star()
    #        new_length = len(shortest) - 1
    #        diffs.append(length - new_length)
    #    result[max(diffs)] += 1
    #print(result)
        
    #length = board.time[board.end]
    #result = defaultdict(lambda: 0)
    #for cheat_start in range(length + 10):
    #    path = board.a_star(cheat_start=cheat_start)
    #    print(length - board.time[board.end])
    #    #result[length - len(path) + 1] += 1
    #print(result)
    #board.show_path(path)

if __name__ == '__main__':
    main()
