import click

def iterate(number, n):
    for _ in range(n):
        number = (number ^ (number * 64)) % 16777216
        number = (number ^ (number // 32)) % 16777216
        number = (number ^ (number * 2048)) % 16777216
    return number

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    with open(input_file, 'r') as fd:
        initial_numbers = [int(x.strip()) for x in fd.read().strip().split('\n')]
    print(initial_numbers)
    result = []
    for number in initial_numbers:
        result.append(iterate(number, 2000))
    print(sum(result))

if __name__ == '__main__':
    main()
