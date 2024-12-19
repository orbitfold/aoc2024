import click
import functools

@functools.cache
def check(stripes, towel):
    if towel == '':
        return True
    else:
        candidates = [stripe for stripe in stripes if towel.startswith(stripe)]
        if len(candidates) == 0:
            return False
        else:
            return any([check(stripes, towel[len(stripe):]) for stripe in candidates])

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    with open(input_file, 'r') as fd:
        stripes, towels = fd.read().split('\n\n')
        stripes = [s.strip() for s in stripes.strip().split(',')]
        towels = [t.strip() for t in towels.strip().split('\n')]
    counter = 0
    for towel in towels:
        if check(tuple(stripes), towel):
            counter += 1
    print(counter)
    

if __name__ == '__main__':
    main()
