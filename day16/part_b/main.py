import click
import numpy as np
import bisect
import matplotlib.pyplot as plt

#MIN_SCORE = 7036
#MIN_SCORE = 11048
MIN_SCORE = 143580

class Maze:
    def __init__(self, input_file):
        import sys
        sys.setrecursionlimit(1500)
        data = []
        with open(input_file, 'r') as fd:
            for line in fd:
                data.append(list(line.strip()))
        self.maze = np.array(data)

    def rotate_right(self, d):
        if d == (1, 0):
            return (0, 1)
        elif d == (0, 1):
            return (-1, 0)
        elif d == (-1, 0):
            return (0, -1)
        elif d == (0, -1):
            return (1, 0)

    def rotate_left(self, d):
        return self.rotate_right(self.rotate_right(self.rotate_right(d)))

    def print(self):
        for row in self.maze:
            print(''.join(row))

    def print_examined(self, examined):
        for row in examined:
            print(''.join([str(int(x)) for x in row]))

    def get_start(self):
        return tuple(np.argwhere(self.maze == 'S')[0])


    def search(self):
        start = self.get_start()
        queue = [(0, [(start, (0, 1))])]
        min_score = np.inf
        result = []
        old_score = 0
        distances = np.load('distances.npy')
        examined = np.zeros(self.maze.shape)
        while len(queue) > 0:
            path = queue.pop(0)
            score, path = path
            p, d = path[-1]
            examined[*p] = 1
            if score > distances[*p] + 1001 or score > MIN_SCORE:
                continue
            if self.maze[*p] == 'E' and score == MIN_SCORE:
                result.append(path)
                continue
            pf = p[0] + d[0], p[1] + d[1]
            dl = self.rotate_left(d)
            dr = self.rotate_right(d)
            pl = p[0] + dl[0], p[1] + dl[1]
            pr = p[0] + dr[0], p[1] + dr[1]
            if self.maze[*pf] != '#' and (pf, d) not in path:
                queue.append((score + 1, path + [(pf, d)]))
            if self.maze[*pl] != '#' and (pl, dl) not in path:
                queue.append((score + 1001, path + [(pl, dl)]))
            if self.maze[*pr] != '#' and (pl, dl) not in path:
                queue.append((score + 1001, path + [(pr, dr)]))
            new_score = examined.sum() / (examined.shape[0] * examined.shape[1])
            if new_score > old_score:
                print(len(queue), new_score, len(result))
                self.print_examined(examined)
                old_score = new_score
        return result

    def count_tiles(self, paths):
        result = set()
        for path in paths:
            for tile in path:
                result.add(tile[0])
        return result

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    maze = Maze(input_file)
    result = maze.search()
    print("DONE!")
    print(len(maze.count_tiles(result)))

if __name__ == '__main__':
    main()
