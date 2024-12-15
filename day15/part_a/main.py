import click
import numpy as np

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

def move(maze, position, direction):
    new_position = (position[0] + direction[0],
                    position[1] + direction[1])
    if maze[*new_position] == '#':
        return position
    if maze[*new_position] == '.':
        return new_position
    if maze[*new_position] == 'O':
        p = tuple(new_position)
        while maze[*p] == 'O':
            p = p[0] + direction[0], p[1] + direction[1]
        if maze[*p] == '.':
            while p != new_position:
                maze[*p] = 'O'
                p = p[0] - direction[0], p[1] - direction[1]
            maze[*p] = '.'
            return new_position
        else:
            return position

def gps(maze):
    os = np.argwhere(maze == 'O')
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
    directions = ''.join(directions.strip().split('\n'))
    position = np.argwhere(maze == '@')[0]
    maze[*position] = '.'
    for direction in directions:
        direction = translate_direction(direction)
        position = move(maze, position, direction)
        print(maze)
    print(gps(maze))
    breakpoint()

if __name__ == '__main__':
    main()
