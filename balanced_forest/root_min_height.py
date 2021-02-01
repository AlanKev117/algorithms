from collections import deque


def rootForMinimumHeight(tree):

    q = deque()

    # First enqueue all leaf nodes in queue
    for node in tree:
        if tree[node].degree == 1:
            q.append(node)

    # loop until total vertex remains less than 2
    nodes = len(tree)
    while nodes > 2:
        for _ in range(len(q)):
            leaf = q.popleft()
            nodes -= 1

            # for each neighbour, decrease its degree and
            # if it become leaf, insert into queue
            for neighbor in tree[leaf].children:
                tree[neighbor].degree -= 1
                if tree[neighbor].degree == 1:
                    q.append(neighbor)

    # Nodes in q are posible root for min height
    return q[0]
