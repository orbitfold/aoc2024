import click
import numpy as np
import fractions

def is_whole(f, eps):
    return abs(f - round(f)) < abs(eps)

def draw_line(x1, x2, y1, y2):
    x1 = fractions.Fraction(x1)
    x2 = fractions.Fraction(x2)
    y1 = fractions.Fraction(y1)
    y2 = fractions.Fraction(y2)
    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1
    return lambda x: m * x + c

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
                line_equation = draw_line(a1[1], a2[1], a1[0], a2[0])
                for col in range(data.shape[1]):
                    row = line_equation(col)
                    anode = row, col
                    if anode[0] >= 0 and anode[1] >= 0 and anode[0] < data.shape[0] and anode[1] < data.shape[1] and anode[0].denominator == 1 and anode[1].denominator == 1:
                        antinodes[anode[0].numerator, anode[1].numerator] = '#'
    result = np.array(antinodes)
    result[data != '.'] = data[data != '.']
    for line in result:
        print(''.join(line))
    print(np.count_nonzero(antinodes == '#'))
            
if __name__ == '__main__':
    main()
