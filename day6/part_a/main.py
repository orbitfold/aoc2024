import click
import numpy as np

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    data = []
    with open(input_file, 'r') as fd:
        for line in fd:
            data.append(list(line.strip()))
    data = np.array(data)
    row, col = np.argwhere(data == '^')[0]
    data[row][col] = 'X'
    direction = '^'
    while True:
        if direction == '^':
            if row - 1 < 0:
                data[row][col] = 'X'
                break
            elif data[row - 1][col] == '#':
                direction = '>'
            else:
                data[row][col] = 'X'
                row -= 1
        elif direction == '>':
            if col + 1 >= data.shape[1]:
                data[row][col] = 'X'
                break
            elif data[row][col + 1] == '#':
                direction = 'v'
            else:
                data[row][col] = 'X'
                col += 1
        elif direction == '<':
            if col - 1 < 0:
                data[row][col] = 'X'
                break
            elif data[row][col - 1] == '#':
                direction = '^'
            else:
                data[row][col] = 'X'
                col -= 1
        elif direction == 'v':
            if row + 1 >= data.shape[0]:
                data[row][col] = 'X'
                break
            elif data[row + 1][col] == '#':
                direction = '<'
            else:
                data[row][col] = 'X'
                row += 1
    print(data)
    print(np.count_nonzero(data == 'X'))

if __name__ == '__main__':
    main()
