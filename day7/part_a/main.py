import click

def evaluate(value, equation):
    if len(equation) == 2:
        return (equation[0] * equation[1] == value) or (equation[0] + equation[1] == value)
    return evaluate(value - equation[0], equation[1:]) or evaluate(value / equation[0], equation[1:])

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
        if evaluate(pair[0], list(reversed(pair[1]))):
            result += pair[0]
    print(result)

if __name__ == '__main__':
    main()
