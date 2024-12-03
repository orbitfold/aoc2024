import click
import re

def parse_mul(expr):
    pair = expr[4:-1]
    pair = pair.split(',')
    pair[0] = int(pair[0])
    pair[1] = int(pair[1])
    return pair[0] * pair[1]

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    with open(input_file, 'r') as fd:
        data = fd.read()
    matches = re.findall(r'mul\([0-9]+,[0-9]+\)', data)
    result = 0
    for match in matches:
        result += parse_mul(match)
    print(result)

if __name__ == '__main__':
    main()
