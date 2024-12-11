import click
import functools

@functools.cache
def rtransform(nr, depth):
    if depth == 0:
        return 1
    elif nr == 0:
        return rtransform(1, depth - 1)
    else:
        str_nr = str(nr)
        if len(str_nr) % 2 == 0:
            mid = len(str_nr) // 2
            return rtransform(int(str_nr[:mid]), depth - 1) + rtransform(int(str_nr[mid:]), depth - 1)
        else:
            return rtransform(nr * 2024, depth - 1)

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    with open(input_file, 'r') as fd:
        data = [int(x) for x in fd.read().strip().split()]
    result = 0
    for nr in data:
        result += rtransform(nr, 75)
    print(result)

if __name__ == '__main__':
    main()
