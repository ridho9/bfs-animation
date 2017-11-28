import sys
import os
import queue
import draw


def load_maze(filename):
    with open(filename) as f:
        nrow, ncol = map(int, f.readline().split())
        maze = []
        for i in range(nrow):
            maze.append(list(f.readline().strip()))

    return maze, nrow, ncol


def matrix_index(matrix, coordinate):
    return matrix[coordinate[0]][coordinate[1]]


def gmi(matrix, coordinate, value):
    matrix[coordinate[0]][coordinate[1]] = value


def is_inside(coordinate, nrow, ncol):
    return (0 <= coordinate[0] < nrow) and (0 <= coordinate[1] < ncol)


def process_maze(maze, nrow, ncol):
    # find start coordinate and end coordinate
    for i in range(nrow):
        for j in range(ncol):
            if maze[i][j].lower() == 's':
                start = (i, j)
    try:
        print("Start \t: {}".format(start))
    except UnboundLocalError:
        print("No start symbol found")
        sys.exit(1)

    for i in range(nrow):
        for j in range(ncol):
            if maze[i][j].lower() == 'f':
                finish = (i, j)
    try:
        print("Finish \t: {}".format(finish))
    except UnboundLocalError:
        print("No finish symbol found")
        sys.exit(1)

    visited = []
    dist = []
    for i in range(nrow):
        visited.append([False] * ncol)
        dist.append([-1] * ncol)
    gmi(dist, start, 0)

    bfs = queue.Queue()
    bfs.put(start)

    found = False

    fc = 0
    draw.draw_state(maze, visited, dist, [], None)\
        .save("r/{}{num:06d}.png".format(sys.argv[1], num=fc))
    fc += 1

    while not bfs.empty():
        current = bfs.get()
        if matrix_index(visited, current):
            continue
        if current == finish:
            found = True
            break

        gmi(visited, current, True)

        draw.draw_state(maze, visited, dist, [], current)\
            .save("r/{}{num:06d}.png".format(sys.argv[1], num=fc))
        fc += 1

        # update and put adjacent
        adj = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for a in adj:
            point = (a[0] + current[0], a[1] + current[1])
            if (not is_inside(point, nrow, ncol))\
                    or (matrix_index(maze, point) == '#')\
                    or (matrix_index(visited, point)):
                continue
            gmi(dist, point, matrix_index(dist, current) + 1)
            bfs.put(point)

    try:
        assert found
    except AssertionError:
        print("No solution found")
        sys.exit(1)

    backtrack = [finish]
    draw.draw_state(maze, visited, dist, backtrack, None)\
        .save("r/{}{num:06d}.png".format(sys.argv[1], num=fc))
    fc += 1

    while backtrack[-1] != start:
        current = backtrack[-1]
        adj = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for a in adj:
            point = (a[0] + current[0], a[1] + current[1])
            if (not is_inside(point, nrow, ncol))\
                    or (matrix_index(dist, current) - matrix_index(dist,
                        point) != 1):
                continue
            backtrack.append(point)
            draw.draw_state(maze, visited, dist, backtrack, None)\
                .save("r/{}{num:06d}.png".format(sys.argv[1], num=fc))
            fc += 1
            break

    return maze, visited, dist, backtrack


if __name__ == "__main__":
    if(len(sys.argv) == 1):
        print("Usage : python3 main.py [maze file]")
        sys.exit(1)

    os.system("mkdir r")

    maze, nrow, ncol = load_maze(sys.argv[1])
    maze, visited, dist, backtrack = process_maze(maze, nrow, ncol)

    print("Finished, creating GIF...")

    os.system("convert -delay 30 -loop 0 -layers Optimize"
              " -fuzz 10% r/{0}* {0}.gif".format(sys.argv[1]))
    os.system("rm -rf r")

    print("Saved result to {}.gif".format(sys.argv[1]))
