import click
import numpy as np

def count_xmas(l):
    l = ''.join(l)
    return l.count('XMAS') + l.count('SAMX')

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    with open(input_file, 'r') as fd:
        data = fd.read()
    data = data.split()
    data = [list(l) for l in data]
    data = np.array(data)
    rows, cols = data.shape
    result = 0
    for line in data:
        result += count_xmas(line)
    for line in data.T:
        result += count_xmas(line)
    for offset in range(-rows + 1, cols):
        diagonal = data.diagonal(offset=offset)
        print(diagonal)
        result += count_xmas(diagonal)
    for offset in range(-rows + 1, cols):
        diagonal = np.fliplr(data).diagonal(offset=offset)
        print(diagonal)
        result += count_xmas(diagonal)
    print(result)
    
if __name__ == '__main__':
    main()
