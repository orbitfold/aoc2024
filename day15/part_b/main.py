import click
import numpy as np

def print_maze(maze, position):
    maze = np.array(maze)
    maze[*position] = '@'
    for row in maze:
        print(''.join(row))

def upscale_maze(maze):
    new_maze = np.zeros((maze.shape[0], maze.shape[1] * 2)).astype('<U1')
    for row in range(maze.shape[0]):
        for col in range(maze.shape[1]):
            if maze[row][col] == '.':
                new_maze[row][2 * col] = '.'
                new_maze[row][2 * col + 1] = '.'
            if maze[row][col] == 'O':
                new_maze[row][2 * col] = '['
                new_maze[row][2 * col + 1] = ']'
            if maze[row][col] == '#':
                new_maze[row][2 * col] = '#'
                new_maze[row][2 * col + 1] = '#'
            if maze[row][col] == '@':
                new_maze[row][2 * col] = '@'
                new_maze[row][2 * col + 1] = '.'
    return new_maze

def mark_pushes(maze, pushes, position, direction):
    if maze[*position] == '[':
        if pushes[*position] == 0:
            pushes[*position] = direction[0]
            mark_pushes(maze, pushes, (position[0], position[1] + 1), direction)
            mark_pushes(maze, pushes, (position[0] + direction[0], position[1]), direction)
        else:
            return
    elif maze[*position] == ']':
        if pushes[*position] == 0:
            pushes[*position] = direction[0]
            mark_pushes(maze, pushes, (position[0], position[1] - 1), direction)
            mark_pushes(maze, pushes, (position[0] + direction[0], position[1]), direction)
        else:
            return
    elif maze[*position] == '.':
        return
    elif maze[*position] == '#':
        raise RuntimeError

def commit_pushes(maze, pushes):
    new_maze = np.zeros((maze.shape[0], maze.shape[1])).astype('<U1')
    for position in np.argwhere(pushes != 0):
        new_maze[int(position[0] + pushes[*position]), position[1]] = maze[*position]
        maze[*position] = '.'
    maze[new_maze != '0'] = new_maze[new_maze != '0']

def push_horizontal(maze, position, direction):
    position = tuple(position)
    p = tuple(position)
    while maze[*p] in ['[', ']']:
        p = p[0], p[1] + direction[1]
    if maze[*p] == '#':
        raise RuntimeError
    if maze[*p] == '.':
        while p != position:
            maze[*p] = maze[p[0], p[1] - direction[1]]
            p = p[0], p[1] - direction[1]
        maze[*p] = '.'

def move(maze, position, direction):
    new_position = position[0] + direction[0], position[1] + direction[1]
    if maze[*new_position] == '.':
        return new_position
    elif maze[*new_position] == '#':
        return position
    elif direction[1] == 0:
        pushes = np.zeros(maze.shape)
        try:
            mark_pushes(maze, pushes, new_position, direction)
            commit_pushes(maze, pushes)
            return new_position
        except RuntimeError:
            return position
    elif direction[0] == 0:
        try:
            push_horizontal(maze, new_position, direction)
            return new_position
        except RuntimeError:
            return position

def translate_direction(d):
    if d == '>':
        return (0, 1)
    elif d == '<':
        return (0, -1)
    elif d == '^':
        return (-1, 0)
    elif d == 'v':
        return (1, 0)
    else:
        raise RuntimeError

def gps(maze):
    os = np.argwhere(maze == '[')
    result = 0
    for o in os:
        result += 100 * o[0] + o[1]
    return result

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    with open(input_file, 'r') as fd:
        data = fd.read()
        maze, directions = data.split('\n\n')
    maze = np.array([list(line.strip()) for line in maze.split('\n')])
    maze = upscale_maze(maze)
    directions = ''.join(directions.strip().split('\n'))
    position = np.argwhere(maze == '@')[0]
    maze[*position] = '.'
    for direction in directions:
        direction = translate_direction(direction)
        position = move(maze, position, direction)
    print(gps(maze))

if __name__ == '__main__':
    main()
