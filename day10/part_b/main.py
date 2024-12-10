import click
import numpy as np

def evaluate(pos, data, elevation):
    if (pos[0] < 0 or pos[1] < 0 or pos[0] >= data.shape[0] or pos[1] >= data.shape[1]):
        return 0
    if data[*pos] != elevation + 1:
        return 0
    if data[*pos] == 9:
        return 1
    return (evaluate((pos[0] - 1, pos[1]), data, data[*pos]) +
            evaluate((pos[0] + 1, pos[1]), data, data[*pos]) +
            evaluate((pos[0], pos[1] - 1), data, data[*pos]) +
            evaluate((pos[0], pos[1] + 1), data, data[*pos]))

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    data = []
    with open(input_file, 'r') as fd:
        for line in fd:
            data.append([int(x) for x in list(line.strip())])
    data = np.array(data)
    result = 0
    for trailhead in np.argwhere(data == 0):
        score = evaluate(trailhead, data, -1)
        result += score
    print(result)

if __name__ == '__main__':
    main()
