import click
import sympy
from sympy import Symbol
from sympy.solvers import solve

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    with open(input_file, 'r') as fd:
        data = fd.read()
        puzzle_input = []
        for machine in data.split('\n\n'):
            machine_specs = machine.split('\n')
            button_a = [int(x.strip()[1:]) for x in machine_specs[0].split(':')[1].strip().split(',')]
            button_b = [int(x.strip()[1:]) for x in machine_specs[1].split(':')[1].strip().split(',')]
            prize = [int(x.strip()[2:]) for x in machine_specs[2].split(':')[1].strip().split(',')]
            puzzle_input.append({'a': button_a, 'b': button_b, 'prize': prize})
    a = Symbol('a')
    b = Symbol('b')
    result = 0
    for machine in puzzle_input:
        solution = solve([a * machine['a'][0] + b * machine['b'][0] - machine['prize'][0],
                          a * machine['a'][1] + b * machine['b'][1] - machine['prize'][1]])
        if solution[a].denominator == 1 and solution[b].denominator == 1 and solution[a] <= 100 and solution[b] <= 100:
            result += 3 * solution[a]
            result += solution[b]
    print(result)

if __name__ == '__main__':
    main()
