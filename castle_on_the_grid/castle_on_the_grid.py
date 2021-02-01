from collections import deque

'''
10
.X..XX...X
X.........
.X.......X
..........
........X.
.X...XXX..
.....X..XX
.....X.X..
..........
.....X..XX
9 1 9 6
'''


def neighbors(g, x, y):
    i = x - 1
    while i >= 0 and g[i][y] != "X":  # Go top while possible
        yield (i, y)  # Return next top neighbor if it exists
        i -= 1

    i = y + 1
    while i < len(g[0]) and g[x][i] != "X":  # Go right while possible
        yield (x, i)  # Return right neighbor if it exists
        i += 1

    i = x + 1
    while i < len(g) and g[i][y] != "X":  # Go bottom while possible
        yield (i, y)  # Return bottom neighbor if it exists
        i += 1

    i = y - 1
    while i >= 0 and g[x][i] != "X":  # Go left while possible
        yield (x, i)  # Return left neighbor if it exists
        i -= 1


def BFS(G, start, goal):
    Q = deque()
    discovered = {}
    track = {}
    discovered[start] = True
    Q.append(start)
    while len(Q) > 0:
        cell = Q.popleft()
        if cell == goal:
            return track
        for neighbor in neighbors(G, *cell):
            if neighbor not in discovered:
                discovered[neighbor] = True
                Q.append(neighbor)
                track[neighbor] = cell


def minimumMoves(grid, startX, startY, goalX, goalY):
    start = (startX, startY)
    goal = (goalX, goalY)
    track = BFS(grid, start, goal)
    cell = goal
    moves = 0
    while cell != start:
        cell = track[cell]
        moves += 1
    return moves


if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input())

    grid = []

    for _ in range(n):
        grid_item = input()
        grid.append(grid_item)

    startXStartY = input().split()

    startX = int(startXStartY[0])

    startY = int(startXStartY[1])

    goalX = int(startXStartY[2])

    goalY = int(startXStartY[3])

    result = minimumMoves(grid, startX, startY, goalX, goalY)

    print(str(result))

    # fptr.close()
