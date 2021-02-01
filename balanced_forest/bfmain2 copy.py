#!/bin/python3

import math
import os
import random
import re
import sys


from collections import deque


class TreeNode:
    def __init__(self, nsum):
        self.sum = nsum
        self.children = set()
        self.degree = 0


def get_graph(c, edges):
    graph = {i: TreeNode(c[i]) for i in range(len(c))}
    for edge in edges:
        node_a, node_b = edge[0] - 1, edge[1] - 1
        graph[node_a].children.add(node_b)
        graph[node_b].children.add(node_a)
    for node in graph:
        graph[node].degree = len(graph[node].children)
    return graph


def get_root(graph):

    q = deque()

    # First enqueue all leaf nodes in queue
    for node in graph:
        if graph[node].degree == 1:
            q.append(node)

    # loop until total vertex remains less than 2
    nodes = len(graph)
    while nodes > 2:
        for _ in range(len(q)):
            leaf = q.popleft()
            nodes -= 1

            # for each neighbour, decrease its degree and
            # if it become leaf, insert into queue
            for neighbor in graph[leaf].children:
                graph[neighbor].degree -= 1
                if graph[neighbor].degree == 1:
                    q.append(neighbor)

    # Nodes in q are posible roots for min height tree, we take first.
    return q[0]


def get_tree(graph, root):
    stack = [root]
    parents = set()
    
    while len(stack) > 0:
        parent = stack[-1]
        if parent not in parents:
            parents.add(parent)
            for child in graph[parent].children:
                graph[child].children.remove(parent)
                stack.append(child)
        else: # backtracking
            graph[parent].sum += sum(map(lambda node: node.sum, graph[parent].children))
            stack.pop()
    return graph


def balancedForest(c, edges):
    graph = get_graph(c, edges)
    root = get_root(graph)
    tree = get_tree(graph, root)
    
    result = float("inf")
    q1 = deque(tree[root].children)
    q2 = deque()
    checked = {}
    while len(q1) > 0:
        n1 = q1.popleft()
        q1.extend(tree[n1].children)

        if tree[n1].sum < tree[root].sum - tree[n1].sum:
            node_lo, node_hi = n1, root
            valid_sum_lo, valid_sum_hi = tree[n1].sum, tree[root].sum - tree[n1].sum
        else:
            node_lo, node_hi = root, n1
            valid_sum_lo, valid_sum_hi = tree[root].sum - \
                tree[n1].sum, tree[n1].sum

        if valid_sum_hi == valid_sum_lo:
            result = min(result, valid_sum_lo)
            continue
        if valid_sum_hi <= 2 * valid_sum_lo:
            goal_sum = valid_sum_lo
            new_node_val = 2 * valid_sum_lo - valid_sum_hi
        elif valid_sum_hi % 2 == 0:
            goal_sum = valid_sum_hi // 2
            new_node_val = goal_sum - valid_sum_lo
        else:
            continue

        q2.extend(tree[node_hi].children)
        while len(q2) > 0:
            n2 = q2.popleft()
            if n2 == node_lo:
                continue
            q2.extend(tree[n2].children)
            if (n2, n1) not in checked:
                checked[n1, n2] = True
                sum_bottom = tree[n2].sum
                sum_top = valid_sum_hi - sum_bottom
                if sum_top == goal_sum or sum_bottom == goal_sum:
                    result = min(result, new_node_val)
                    break
    return result if result != float("inf") else -1


result = balancedForest([1, 1, 1], [[1, 2], [2, 3]])

print(result)
