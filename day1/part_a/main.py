import click
import numpy as np
import operator

@click.command()
@click.option('-i', '--input-file', help='Input data')
def main(input_file):
    pairs = []
    with open(input_file) as fd:
        for line in fd:
            pair = line.split()
            pair[0] = int(pair[0].strip())
            pair[1] = int(pair[1].strip())
            pairs.append(pair)
    pairs = np.array(pairs)
    col1 = np.sort(pairs[:,0])
    col2 = np.sort(pairs[:,1])
    print(np.abs(col1 - col2).sum())
    
    

if __name__ == '__main__':
    main()
