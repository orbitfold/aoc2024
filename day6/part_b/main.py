import click
import numpy as np
import numba

def next_position(data, row, col, direction, path):
    if direction == '^':
        if row - 1 < 0:
            return 'end'
        else:
            if data[row - 1][col] == '#':
                new_pos = (row, col, '>')
            else:
                new_pos = (row - 1, col, direction)
    elif direction == '>':
        if col + 1 >= data.shape[1]:
            return 'end'
        else:
            if data[row][col + 1] == '#':
                new_pos = (row, col, 'v')
            else:
                new_pos = (row, col + 1, direction)
    elif direction == '<':
        if col - 1 < 0:
            return 'end'
        else:
            if data[row][col - 1] == '#':
                new_pos = (row, col, '^')
            else:
                new_pos = (row, col - 1, direction)
    elif direction == 'v':
        if row + 1 >= data.shape[0]:
            return 'end'
        else:
            if data[row + 1][col] == '#':
                new_pos = (row, col, '<')
            else:
                new_pos = (row + 1, col, direction)
    if new_pos in path:
        return 'loop'
    else:
        return new_pos

def simulate_walk(data, row, col, direction):
    path = [(row, col, direction)]
    path_set = set([])
    new_position = next_position(data, row, col, direction, path_set)
    while new_position not in ('loop', 'end'):
        path.append(new_position)
        path_set.add(new_position)
        new_position = next_position(data, new_position[0], new_position[1], new_position[2], path_set)
    return path, new_position

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    data = []
    with open(input_file, 'r') as fd:
        for line in fd:
            data.append(list(line.strip()))
    data = np.array(data)
    row, col = np.argwhere(data == '^')[0]
    direction = '^'
    path, ending = simulate_walk(data, row, col, direction)
    counter = 0
    unique_positions = []
    for position in path:
        p = (position[0], position[1])
        if p not in unique_positions:
            unique_positions.append(p)
    for i, position in enumerate(unique_positions):
        new_data = np.array(data)
        new_data[position[0]][position[1]] = '#'
        path, ending = simulate_walk(new_data, row, col, '^')
        if ending == 'loop':
            counter += 1
    print(counter)

if __name__ == '__main__':
    main()
