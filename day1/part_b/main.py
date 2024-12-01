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
    col1 = pairs[:,0]
    col2 = pairs[:,1]
    def count_instances(x):
        return np.count_nonzero(col2 == x)
    vfunc = np.vectorize(count_instances)
    print((col1 * vfunc(col1)).sum())
    

if __name__ == '__main__':
    main()
