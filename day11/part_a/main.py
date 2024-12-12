import click

def transform(nr):
    str_nr = str(nr)
    if nr == 0:
        return [1]
    if len(str_nr) % 2 == 0:
        mid = len(str_nr) // 2
        return [int(str_nr[:mid]), int(str_nr[mid:])]
    return [nr * 2024]

def blink(lst):
    result = []
    for nr in lst:
        result += transform(nr)
    return result

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    with open(input_file, 'r') as fd:
        data = [int(x) for x in fd.read().strip().split()]
    for _ in range(25):
        data = blink(data)
        print(data)
    print(len(data))

if __name__ == '__main__':
    main()
