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
    # Variables
    tree, root = get_tree(get_graph(c, edges))
    #print(tree)
    #print(root)
    #return 0
    stack = [root]
    visited, visited_sums, complement_sums = set(), set(), set()
    result = float("inf")

    while len(stack) > 0:
        # Selected node
        node = stack.pop()

        if node not in visited:
            visited.add(node)
            # Push node's children onto stack.
            for child in tree[node].children:
                stack.append(child)
            # Add the sum of the rest of the tree without the subtree whose root is node
            complement_sum = tree[root].sum - tree[node].sum
            complement_sums.add(complement_sum)

            if ((tree[node].sum * 2) in visited_sums or
                    (tree[root].sum - tree[node].sum * 2) in visited_sums) and \
                    tree[node].sum * 3 >= tree[root].sum:
                result = min(result, tree[node].sum * 3 - tree[root].sum)
        else:
            # Two equals subtrees
            if tree[node].sum * 2 == tree[root].sum:
                result = min(result, tree[node].sum)

            if (tree[node].sum in visited_sums or
                    tree[node].sum in complement_sums) and \
                    tree[node].sum * 3 >= tree[root].sum:
                result = min(result, tree[node].sum * 3 - tree[root].sum)

            complement_sum = tree[root].sum - tree[node].sum
            if complement_sum % 2 == 0:
                half_complement_sum = complement_sum // 2
                if half_complement_sum > tree[node].sum and (
                    half_complement_sum in visited_sums or
                    half_complement_sum in complement_sums
                ):
                    result = min(result, half_complement_sum - tree[node].sum)

            complement_sums.remove(complement_sum)
            visited_sums.add(tree[node].sum)

            stack.pop()

    return result if result != float("inf") else -1


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
result = balancedForest(c, edges)
# result = balancedForest((1, 2, 2, 1, 1),
                        # ((1, 2), (1, 3), (3, 5), (1, 4)))
print(result)
