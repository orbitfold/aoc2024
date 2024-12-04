import click
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def check_arr(arr):
    return arr[0] == 'M'

@click.command()
@click.option('-i', '--input-file', help='Input file')
def main(input_file):
    with open(input_file, 'r') as fd:
        data = fd.read()
    data = data.split()
    data = [list(l) for l in data]
    data = np.array(data)
    result = 0
    for i in range(1, data.shape[0] - 1):
        for j in range(1, data.shape[1] - 1):
            if data[i][j] == 'A':
                if data[i - 1][j - 1] == 'M' and data[i + 1][j + 1] == 'S':
                    if (data[i - 1][j + 1] == 'M' and data[i + 1][j - 1] == 'S') or (data[i - 1][j + 1] == 'S' and data[i + 1][j - 1] == 'M'):
                        result += 1
                elif data[i - 1][j - 1] == 'S' and data[i + 1][j + 1] == 'M':
                    if (data[i - 1][j + 1] == 'M' and data[i + 1][j - 1] == 'S') or (data[i - 1][j + 1] == 'S' and data[i + 1][j - 1] == 'M'):
                        result += 1
    print(result)
                
        
if __name__ == '__main__':
    main()
