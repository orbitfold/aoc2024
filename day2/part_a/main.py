import click
import numpy as np

def is_safe(lst):
    arr = np.array(lst)
    if not ((np.diff(arr) < 0).all() or (np.diff(arr) > 0).all()):
        return False
    if (np.abs(np.diff(arr)) < 1).any() or (np.abs(np.diff(arr)) > 3).any():
        return False
    return True
    
    

@click.command()
@click.option('-i', '--input-file', help='Input data')
def main(input_file):
    puzzle_input = []
    with open(input_file) as fd:
        for line in fd:
            puzzle_input.append([int(x) for x in line.strip().split()])
    counter = 0
    for lst in puzzle_input:
        if is_safe(lst):
            counter += 1
    print(counter)

if __name__ == '__main__':
    main()
