import click
import networkx as nx

@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    graph = nx.Graph()
    with open(input_file, 'r') as fd:
        for line in fd:
            c1, c2 = line.strip().split('-')
            graph.add_edge(c1, c2)
    cliques = nx.enumerate_all_cliques(graph)
    biggest = max(cliques, key=lambda c: len(c))
    biggest = sorted(biggest)
    print(",".join(biggest))

if __name__ == '__main__':
    main()
