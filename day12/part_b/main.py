import click
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
import matplotlib.pyplot as plt


def floodfill(data, result, letter, counter, pos):
    if pos[0] < 0 or pos[1] < 0 or pos[0] >= data.shape[0] or pos[1] >= data.shape[1]:
        return
    if data[*pos] != letter:
        return
    if result[*pos] != 0:
        return
    result[*pos] = counter
    floodfill(data, result, letter, counter, (pos[0] - 1, pos[1]))
    floodfill(data, result, letter, counter, (pos[0] + 1, pos[1]))
    floodfill(data, result, letter, counter, (pos[0], pos[1] - 1))
    floodfill(data, result, letter, counter, (pos[0], pos[1] + 1))


def count_borders(data):
    data = np.pad(data, 1)
    line_counter = 0
    for row1, row2 in zip(data[:-1], data[1:]):
        inside_line = (0, 0)
        for i in range(row1.shape[0]):
            if (row1[i] == 0 and row2[i] != 0):
                if inside_line == (0, 0) or inside_line == (1, 0):
                    inside_line = (0, 1)
                    line_counter += 1
            elif (row1[i] != 0 and row2[i] == 0):
                if inside_line == (0, 0) or inside_line == (0, 1):
                    inside_line = (1, 0)
                    line_counter += 1
            elif (row1[i] == 0 and row2[i] == 0) or (row1[i] == 1 and row2[i] == 1):
                if inside_line in [(0, 1), (1, 0)]:
                    inside_line = (0, 0)
    return line_counter

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    with open(input_file, 'r') as fd:
        data = []
        for line in fd:
            data.append(list(line.strip()))
        data = np.array(data)
        derived = np.zeros(data.shape)
        counter = 0
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if derived[row, col] == 0:
                    counter += 1
                    floodfill(data, derived, data[row][col], counter, (row, col))
        result = 0
        for area in np.unique(derived):
            a = np.count_nonzero(derived == area)
            patch = np.zeros(derived.shape)
            patch[derived == area] = 1
            print(area, a, count_borders(patch), count_borders(patch.T))
            result += (count_borders(patch) + count_borders(patch.T)) * a
    print(result)            

if __name__ == '__main__':
    main()
