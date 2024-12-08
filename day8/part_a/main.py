import click
import numpy as np
from bresenham import bresenham

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    data = []
    with open(input_file, 'r') as fd:
        for line in fd:
            data.append(list(line.strip()))
    data = np.array(data)
    antinodes = np.full(data.shape, '.')
    unique = np.unique(data)
    unique = unique[unique != '.']
    counter = 0
    for antenna in unique:
        locations = np.argwhere(data == antenna)
        if locations.shape[0] < 2:
            continue
        for i, a1 in enumerate(locations):
            for a2 in locations[i + 1:]:
                d_row = abs(a1[0] - a2[0])
                d_col = abs(a1[1] - a2[1])
                min_row = min(a1[0], a2[0])
                max_row = max(a1[0], a2[0])
                min_col = min(a1[1], a2[1])
                max_col = max(a1[1], a2[1])
                if (a1[0] <= a2[0] and a1[1] <= a2[1]) or (a1[0] >= a2[0] and a1[1] >= a2[1]):
                    anode1 = min_row - d_row, min_col - d_col
                    anode2 = max_row + d_row, max_col + d_col
                else:
                    anode1 = min_row - d_row, max_col + d_col
                    anode2 = max_row + d_row, min_col - d_col
                if anode1[0] >= 0 and anode1[0] < data.shape[0] and anode1[1] >= 0 and anode1[1] < data.shape[1]:
                    antinodes[anode1] = '#'
                if anode2[0] >= 0 and anode2[0] < data.shape[0] and anode2[1] >= 0 and anode2[1] < data.shape[1]:
                    antinodes[anode2] = '#'
                print(antenna, a1, a2, d_row, d_col, anode1, anode2)
    print(antinodes)
    print(np.count_nonzero(antinodes == '#'))
            
if __name__ == '__main__':
    main()
