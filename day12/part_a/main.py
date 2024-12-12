import click
import numpy as np

def perimeter(data, pos):
    neighbours = 0
    w = (pos[0] - 1, pos[1])
    if w[0] >= 0 and data[*w] == data[*pos]:
        neighbours += 1
    e = (pos[0] + 1, pos[1])
    if e[0] < data.shape[0] and data[*e] == data[*pos]:
        neighbours += 1
    n = (pos[0], pos[1] - 1)
    if n[1] >= 0 and data[*n] == data[*pos]:
        neighbours += 1
    s = (pos[0], pos[1] + 1)
    if s[1] < data.shape[1] and data[*s] == data[*pos]:
        neighbours += 1
    return 4 - neighbours

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
                print(derived)

if __name__ == '__main__':
    main()
