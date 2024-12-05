import click

def get_middle(update):
    return update[int((len(update) - 1) / 2)]

def get_before(ordering_after, update):
    nr = update[0]
    before = []
    for other_page in update[1:]:
        try:
            if other_page in ordering_after[nr]:
                before.append(other_page)
        except KeyError:
            pass
    return before

def get_after(ordering_before, update):
    nr = update[0]
    after = []
    for other_page in update[1:]:
        try:
            if other_page in ordering_before[nr]:
                after.append(other_page)
        except KeyError:
            pass
    return after

def order_update(ordering_before, ordering_after, update):
    if len(update) < 2:
        return update
    return (order_update(ordering_before, ordering_after, get_before(ordering_after, update)) +
            [update[0]] +
            order_update(ordering_before, ordering_after, get_after(ordering_before, update)))

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
        if not check_update(ordering_before, ordering_after, update):
            new_update = order_update(ordering_before, ordering_after, update)
            print(new_update)
            result += get_middle(new_update)
    print(result)

if __name__ == '__main__':
    main()
