#!/bin/python3

import math
import os
import random
import re
import sys


from collections import deque


class TreeNode:
    def __init__(self):
        self.sum = 0
        self.children = set()
        self.degree = 0

    def __repr__(self):
        return f"<sum: {self.sum}, children:{self.children}, degree:{self.degree}>"


def get_graph(c, edges):
    graph = {i: TreeNode() for i in range(len(c))}
    for edge in edges:
        node_a, node_b = edge[0] - 1, edge[1] - 1
        graph[node_a].sum = c[node_a]
        graph[node_a].children.add(node_b)
        graph[node_b].sum = c[node_b]
        graph[node_b].children.add(node_a)
    for node in graph:
        graph[node].degree = len(graph[node].children)
    return graph


def get_tree(graph):
    leaves = [node for node in graph if len(graph[node].children) == 1]
    q = deque(leaves)
    visited = set()
    nodes = set(graph.keys())
    while len(nodes) > 2:
        for _ in range(len(q)):
            leaf = q.popleft()
            visited.add(leaf)
            to_erase = None
            for neighbor in graph[leaf].children:
                if neighbor in visited:
                    continue
                graph[neighbor].degree -= 1
                graph[neighbor].sum += graph[leaf].sum
                to_erase = neighbor
                if graph[neighbor].degree == 1:
                    q.append(neighbor)
            graph[leaf].children.remove(to_erase)
            nodes.remove(leaf)  # del graph[leaf]
    left_nodes = list(nodes)
    if len(left_nodes) == 2:
        root = left_nodes[1]
        graph[left_nodes[0]].children.remove(root)
    else:
        root = left_nodes[0]
    return graph, root


def balancedForest(c, edges):
    tree, root = get_tree(get_graph(c, edges))
    val = float("inf")
    q = deque(tree[root].children)
    checked = {}
    while len(q) > 0:
        n1 = q.popleft()
        q.extend(tree[n1].children)
        valid_sum = {n1: tree[n1].sum, root: tree[root].sum - tree[n1].sum}
        node_lo, node_hi = sorted(valid_sum, key=lambda k: valid_sum[k])
        if valid_sum[node_hi] == valid_sum[node_lo]:
            val = min(val, valid_sum[node_lo])
            continue
        if valid_sum[node_hi] <= 2 * valid_sum[node_lo]:
            goal_sum = valid_sum[node_lo]
            new_node_val = 2 * valid_sum[node_lo] - valid_sum[node_hi]
        elif valid_sum[node_hi] > 2 * valid_sum[node_lo]:
            if valid_sum[node_hi] % 2 == 0:
                goal_sum = valid_sum[node_hi] // 2
                new_node_val = goal_sum - valid_sum[node_lo]
            else:
                continue
        q2 = deque(tree[node_hi].children)
        while len(q2) > 0:
            n2 = q2.popleft()
            if (n2 == node_lo):
                continue
            q2.extend(tree[n2].children)
            if (n2, n1) not in checked:
                checked[n1, n2] = True
                sum_bottom = tree[n2].sum
                sum_top = valid_sum[node_hi] - sum_bottom
                if sum_top == goal_sum or sum_bottom == goal_sum:
                    val = min(val, new_node_val)
                    break
    return val if val != float("inf") else -1

# if __name__ == '__main__':

#     q = int(input())

#     for q_itr in range(q):
#         n = int(input())

#         c = list(map(int, input().rstrip().split()))

#         edges = []

#         for _ in range(n - 1):
#             edges.append(list(map(int, input().rstrip().split())))

#         result = balancedForest(c, edges)


#         print(result)
c = [1, 3, 4, 4]
edges = [[1, 2], [1, 3], [1, 4]]
result = balancedForest((1, 2, 2, 1, 1),
                        ((1, 2), (1, 3), (3, 5), (1, 4)))
# result = balancedForest((1, 2, 2, 1, 1),
# ((1, 2), (1, 3), (3, 5), (1, 4)))
print(result)
