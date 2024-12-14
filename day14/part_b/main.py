import click
import matplotlib.pyplot as plt
import numpy as np

def tree_test(data):
    center = data[40:60][:,40:60]
    if center.sum() / (center.shape[0] * center.shape[1]) > 0.2:
        return True
    else:
        return False

def get_quadrant(p, width, height):
    if 0 <= p[0] < width // 2 and 0 <= p[1] < height // 2:
        return 0
    elif 0 <= p[0] < width // 2 and height // 2 < p[1] <= height:
        return 2
    elif width // 2 < p[0] <= width and 0 <= p[1] < height // 2:
        return 1
    elif width // 2 < p[0] <= width and height // 2 < p[1] <= height:
        return 3
    else:
        return None
    
    
@click.command()
@click.option('-i', '--input-file', help='Input data file')
@click.option('-w', '--width', help='Area width')
@click.option('-h', '--height', help='Area height')
def main(input_file, width, height):
    width = int(width)
    height = int(height)
    puzzle_input = []
    with open(input_file, 'r') as fd:
        for line in fd:
            p, v = line.strip().split(' ')
            p = [int(x) for x in p[2:].split(',')]
            v = [int(x) for x in v[2:].split(',')]
            puzzle_input.append({'p': p, 'v': v})
    result = [0, 0, 0, 0]
    for seconds in range(10000):
        positions = []
        board = np.zeros((height, width))
        for robot in puzzle_input:
            end_pos = ((robot['p'][0] + seconds * robot['v'][0]) % width,
                       (robot['p'][1] + seconds * robot['v'][1]) % height)
            positions.append(end_pos)
        for position in positions:
            board[position[1]][position[0]] = 1
        if tree_test(board):
            print(seconds)
            plt.imshow(board)
            plt.show()
            
            

if __name__ == '__main__':
    main()
