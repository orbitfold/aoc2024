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

    def find_close_points(self, current, path):
        points = []
        for point in path:
            d = abs(point[0] - current[0]) + abs(point[1] - current[1])
            if d <= 20:
                if point != current:
                    points.append(point)
        return points

    def find_savings(self, path, time):
        others = self.find_close_points(path[time], path)
        result = defaultdict(lambda: 0)
        for other in others:
            d = abs(other[0] - path[time][0]) + abs(other[1] - path[time][1])
            diff = path.index(other) - time - d
            if diff > 0:
                result[(path[time], other)] = diff
        return result

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    with open(input_file, 'r') as fd:
        data = [list(row) for row in fd.read().strip().split('\n')]
        data = np.array(data)
    board = Board(data)
    path = board.a_star()
    #print(board.find_savings(path, 0))
    result = defaultdict(set)
    for time in range(len(path)):
        savings = board.find_savings(path, time)
        for k in savings:
            result[savings[k]].add(k)
        print(len(path), time)
    #print(result)
    result_summary = defaultdict(lambda: 0)
    for k in result:
        if k >= 100:
            result_summary[k] = len(result[k])
    print(result_summary)
    r = 0
    for k in result_summary:
        r += result_summary[k]
    print(r)

if __name__ == '__main__':
    main()
