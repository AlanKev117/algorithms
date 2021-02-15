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


def get_tree(graph):
    leaves = [node for node in graph if graph[node].degree == 1]
    q = deque(leaves)
    visited = set()
    nodes = set(graph.keys())
    while len(nodes) > 2:
        for _ in range(len(q)):
            leaf = q.popleft()
            visited.add(leaf)
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
        root = left_nodes[0]
        no_root = left_nodes[1]
        graph[no_root].children.remove(root)
        graph[root].sum += graph[no_root].sum
    else:
        root = left_nodes[0]
    return graph, root


def balancedForest(c, edges):
    tree, root = get_tree(get_graph(c, edges))
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
            valid_sum_lo, valid_sum_hi = tree[root].sum - tree[n1].sum, tree[n1].sum
        
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

result = balancedForest([1,1,1], [[1,2], [2,3]])

print(result)
