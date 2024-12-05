import click

def check_update(ordering_before, ordering_after, update):
    for i, nr in enumerate(update):
        if i > 1:
            for other_page in update[:i]:
                try:
                    if other_page not in ordering_after[nr]:
                        return False
                except KeyError:
                    pass
        if i < len(update) - 1:
            for other_page in update[i + 1:]:
                try:
                    if other_page not in ordering_before[nr]:
                        return False
                except KeyError:
                    pass
    return True

def get_middle(update):
    return update[int((len(update) - 1) / 2)]

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    ordering_before = {}
    ordering_after = {}
    updates = []
    with open(input_file, 'r') as fd:
        data = fd.readlines()
        i = data.index('\n')
        section1 = data[:i]
        section2 = data[i + 1:]
        for rule in section1:
            rule = rule.strip().split('|')
            rule[0] = int(rule[0])
            rule[1] = int(rule[1])
            try:
                ordering_before[rule[0]].append(rule[1])
            except KeyError:
                ordering_before[rule[0]] = [rule[1]]
            try:
                ordering_after[rule[1]].append(rule[0])
            except KeyError:
                ordering_after[rule[1]] = [rule[0]]
        for update in section2:
            update = update.strip().split(',')
            update = [int(x) for x in update]
            updates.append(update)
    result = 0
    for update in updates:
        if check_update(ordering_before, ordering_after, update):
            print(update)
            result += get_middle(update)
    print(result)

if __name__ == '__main__':
    main()
