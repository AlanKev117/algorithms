#!/bin/python3

import math
import os
import random
import re
import sys

from collections import deque


def get_graph(edges):
    graph = {}
    for edge in edges:
        node_a, node_b = edge[0] - 1, edge[1] - 1
        graph[node_a] = graph.get(node_a, set())
        graph[node_b] = graph.get(node_b, set())
        graph[node_a].add(node_b)
        graph[node_b].add(node_a)
    return graph


def get_tree(graph):
    leaves = [node for node in graph if len(graph[node]) == 1]
    q = deque(leaves)
    tree = {}
    nodes = set(graph.keys())
    while len(graph) > 2:
        for _ in range(len(q)):
            leaf = q.popleft()
            for neighbor in graph[leaf]:
                graph[neighbor].remove(leaf)
                tree[leaf] = neighbor
                if len(graph[neighbor]) == 1:
                    q.append(neighbor)
            del graph[leaf]
    left_nodes = list(graph.keys())
    if len(left_nodes) == 2:
        root = left_nodes[1]
        tree[left_nodes[0]] = root
    else:
        root = left_nodes[0]
    return tree, nodes, root

def get_sums_and_children(tree, nodes, root, c):
    sums = {}
    children = {}
    for node in nodes:
        aux = node
        while True:  # aux != root
            try:
                # For sums
                sums[aux] = sums.get(aux, 0) + c[node]
                # For children
                children[aux] = children.get(aux, set())
                if node != aux:
                    children[aux].add(node)
                aux = tree[aux]
            except KeyError:  # aux == root -> root not in tree
                break
    return sums, children

def balancedForest(c, edges):
    tree, nodes, root = get_tree(get_graph(edges))
    sums, children = get_sums_and_children(tree, nodes, root, c)
    val = float("inf")
    checked = {}
    for n1 in children[root]:
        valid_sum = {n1: sums[n1], root: sums[root] - sums[n1]}
        node_lo, node_hi = sorted(valid_sum, key=lambda k: valid_sum[k])
        if valid_sum[node_hi] == valid_sum[node_lo]:
            val = min(val, valid_sum[node_lo])
            continue
        if valid_sum[node_hi] <= 2 * valid_sum[node_lo]:
            goal_sum = valid_sum[node_lo]
            new_node_val = 2 * valid_sum[node_lo] - valid_sum[node_hi]
            if node_hi == n1:
                curr_children = children[n1]
            else:
                curr_children = children[root] - children[n1].union([n1])
        elif valid_sum[node_hi] > 2 * valid_sum[node_lo]:
            if valid_sum[node_hi] % 2 == 0:
                goal_sum = valid_sum[node_hi] // 2
                new_node_val = goal_sum - valid_sum[node_lo]
                if node_hi == n1:
                    curr_children = children[n1]
                else:
                    curr_children = children[root] - children[n1].union([n1])
            else:
                continue

        for n2 in curr_children:
            if (n2, n1) not in checked:
                checked[n1, n2] = True
                sum_bottom = sums[n2]
                sum_top = valid_sum[node_hi] - sum_bottom
                if sum_top == goal_sum or sum_bottom == goal_sum:
                    val = min(val, new_node_val)
                    break
    return val if val != float("inf") else -1


if __name__ == '__main__':
    with open("input05.txt", "r") as file:
        q = int(file.readline())
        for q_itr in range(q):
            n = int(file.readline())

            c = list(map(int, file.readline().rstrip().split()))

            edges = []

            for _ in range(n - 1):
                edges.append(list(map(int, file.readline().rstrip().split())))

            result = balancedForest(c, edges)

            print(result)
