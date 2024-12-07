import click

def concatenate(x1, x2):
    return int(str(x1) + str(x2))

def evaluate(value, equation, result):
    if len(equation) == 0:
        return value == result
    return (evaluate(value, equation[1:], result * equation[0]) or
            evaluate(value, equation[1:], result + equation[0]) or
            evaluate(value, equation[1:], concatenate(result, equation[0])))

@click.command()
@click.option('-i', '--input_file', help='Input data file')
def main(input_file):
    data = []
    with open(input_file, 'r') as fd:
        for line in fd:
            line = line.strip()
            value, equation = line.split(':')
            value = int(value.strip())
            equation = equation.strip()
            equation = [int(x) for x in equation.split(' ')]
            data.append((value, equation))
    result = 0
    for pair in data:
        if evaluate(pair[0], pair[1][1:], pair[1][0]):
            print(pair)
            result += pair[0]
    print(result)

if __name__ == '__main__':
    main()
