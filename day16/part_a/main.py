import click
import numpy as np
import bisect

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

    def get_start(self):
        return tuple(np.argwhere(self.maze == 'S')[0])

    def search(self):
        start = self.get_start()
        queue = [(0, [(start, (0, 1))])]
        min_score = np.inf
        while len(queue) > 0:
            path = queue.pop(0)
            score, path = path
            p, d = path[-1]
            if score > min_score:
                continue
            if self.maze[*p] == 'E' and score < min_score:
                min_score = score
                continue
            pf = p[0] + d[0], p[1] + d[1]
            dl = self.rotate_left(d)
            dr = self.rotate_right(d)
            pl = p[0] + dl[0], p[1] + dl[1]
            pr = p[0] + dr[0], p[1] + dr[1]
            if self.maze[*pf] != '#' and (pf, d) not in path:
                bisect.insort(queue, (score + 1, path + [(pf, d)]), key=lambda x: x[0])
            if self.maze[*pl] != '#' and (pl, dl) not in path:
                bisect.insort(queue, (score + 1001, path + [(pl, dl)]), key=lambda x: x[0])
            if self.maze[*pr] != '#' and (pl, dl) not in path:
                bisect.insort(queue, (score + 1001, path + [(pr, dr)]), key=lambda x: x[0])
            print(len(queue), min_score, queue[0][0], queue[-1][0])
        return min_score

    def print_unvisited(self, unvisited):
        for row in unvisited:
            print(''.join([str(x) for x in row]))

    def dijkstra(self):
        start = np.argwhere(self.maze == 'S')[0]
        end = np.argwhere(self.maze == 'E')[0]
        unvisited = np.full(self.maze.shape, 1)
        distances = np.full(self.maze.shape, np.inf)
        previous = np.full(self.maze.shape, None)
        previous = [list(row) for row in previous]
        distances[self.maze == 'S'] = 0
        previous[start[0]][start[1]] = (start[0], start[1] - 1)
        while unvisited[*end] == 1:
            p = min([x for x in np.argwhere(unvisited == 1)], key=lambda x: distances[*x])
            d = p[0] - previous[p[0]][p[1]][0], p[1] - previous[p[0]][p[1]][1]
            pf = p[0] + d[0], p[1] + d[1]
            dl = self.rotate_left(d)
            dr = self.rotate_right(d)
            pl = p[0] + dl[0], p[1] + dl[1]
            pr = p[0] + dr[0], p[1] + dr[1]
            if self.maze[*pf] != '#':
                distances[*pf] = distances[*p] + 1
                previous[pf[0]][pf[1]] = p
            if self.maze[*pl] != '#':
                distances[*pl] = distances[*p] + 1001
                previous[pl[0]][pl[1]] = p
            if self.maze[*pr] != '#':
                distances[*pr] = distances[*p] + 1001
                previous[pr[0]][pr[1]] = p
            unvisited[*p] = 0
        np.save('distances.npy', distances)
        return int(distances[*end])
                

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    maze = Maze(input_file)
    print(maze.dijkstra())

if __name__ == '__main__':
    main()
