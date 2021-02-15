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

def find_balanced_forest(root, tree):
    stack = (root, None)
    #visited - visited nodes
    #visited_sums - sums that are currently visited
    #root complement sums complement sums (total_value - parent) on the way to the 
    #current node, the cardinality of root complement sums is increased when going
    #down the tree and decreased when going up the tree, it is okay to do that
    #because the sums are always unique in the root_complement_sums
    visited, visited_sums, root_complement_sums = set(), set(), set()
    min_result_value = math.inf

    while stack:
        selected_node = stack[0]

        if selected_node not in visited:
            visited.add(selected_node)

            #populate stack with children all at once:
            for child in tree[selected_node].children:
                stack = (child, stack)

            #this is a complement sum: TOTAL - current_sum
            #I need to calculate it while going down the tree so when I go up
            #I will use those values in the root_complement_sums to check for
            #existance
            selected_sum_comp = tree[root].sum - tree[selected_node].sum
            root_complement_sums.add(selected_sum_comp)

            # Yes, no bitwise shifts, I present what I want to get accomplished,
            # but I don't care how it is accomplished
            # tree[selected_node].sum * 3 >= tree[root].sum is checking that
            # that if the cut is made in selected subtree and the visited subtree 
            # (in case the comp or sum exists in the visited sums)
            # the remaining subtree sum is equal or less than the sums 
            # (which are equal) of the current and the visited subtrees
            # this is just part of the requirement - I can balance the remaining
            # tree only with 0 or positive elements
            if (
                    (tree[selected_node].sum * 2) in visited_sums or 
                    (tree[root].sum - tree[selected_node].sum * 2) in visited_sums
                ) and tree[selected_node].sum * 3 >= tree[root].sum:

                #get the candidate value and update min_result_value if it's less
                candidate_value = tree[selected_node].sum * 3 - tree[root].sum
                min_result_value = min(min_result_value, candidate_value)
        else:
            # This is a case where two even halfs are found.
            if (tree[selected_node].sum * 2) == tree[root].sum:
                candidate_value = tree[selected_node].sum
                # In this case a balanced forest is these two halfs + a new node as
                # a separate tree with the same value as the half of the existing 
                # tree sum
                min_result_value = min(min_result_value, candidate_value)

            # check visited sums and root complements
            # root complements are the sums on the way from root to the selected
            # nodes taken from it's parents of if we have a tree
            #          (1)
            #        / |  \
            #      /   |   \
            #     /    |    \
            #   (2)   (3)   (4)
            #   / \    |    /\
            # (5)(6) (7)  (8)(9)
            # 
            # 
            # If I am at the node 8, I have the {TOTAL - (8).sum, TOTAL - (4).sum }
            # If I am at the node 9, I have the {TOTAL - (9).sum, TOTAL - (4).sum }
            # If I am at the node 2, I have the {TOTAL - (2).sum }
            if (
                    (
                        tree[selected_node].sum in visited_sums or
                        tree[selected_node].sum in root_complement_sums
                    ) and tree[selected_node].sum * 3 >= tree[root].sum
               ):
                # candidate split:
                candidate_value = tree[selected_node].sum * 3 - tree[root].sum
                min_result_value = min(min_result_value, candidate_value)
            
            selected_sum_comp = tree[root].sum - tree[selected_node].sum
            if selected_sum_comp % 2 == 0:
                #I am not trying to impress anyone with bitwise shifts here:
                selected_sum_comp_half = selected_sum_comp // 2
                if selected_sum_comp_half > tree[selected_node].sum and (
                        selected_sum_comp_half in visited_sums or
                        selected_sum_comp_half in root_complement_sums
                    ):
                    #same candidate value
                    candidate_value = selected_sum_comp_half - tree[selected_node].sum 
                    min_result_value = min(min_result_value, candidate_value)

            #remove selected complement from root while going up the tree
            root_complement_sums.remove(selected_sum_comp)
            #added to the visited sums while going up the tree
            visited_sums.add(tree[selected_node].sum)

            #stack pop:
            stack = stack[-1]

    if min_result_value == math.inf:
        min_result_value = -1
    return min_result_value

def balancedForest(c, edges):
    tree, root = get_tree(get_graph(c, edges))
    return find_balanced_forest(root, tree)

result = balancedForest([1,1,1], [[1,2], [2,3]])

print(result)
