#include <bits/stdc++.h>
using namespace std;

unordered_map<int, unordered_set<int>> &
get_graph(vector<vector<int>> & edges) {
    unordered_map<int, unordered_set<int>> graph;
    for (vector<int> edge : edges) {
        int node_a = edge[0] - 1, node_b = edge[1] - 1; 
        graph[node_a] = graph.find(node_a) != graph.end() ? graph[node_a] : unordered_set<int>();
        graph[node_b] = graph.find(node_b) != graph.end() ? graph[node_b] : unordered_set<int>();
        graph[node_a].insert(node_b);
        graph[node_b].insert(node_a);
    }
    return graph;
}

tuple<unordered_map<int, int>, unordered_set<int>, int>
get_tree(unordered_map<int, unordered_set<int>> & graph) {
    queue<int> leaves_q;
    unordered_set<int> nodes;
    for (auto node_neighbors : graph) {
        if (node_neighbors.second.size() == 1) {
            leaves_q.push(node_neighbors.first);
        }
        nodes.insert(node_neighbors.first);
    }
    unordered_map<int, int> tree;
    while (graph.size() > 2) {
        int q_len = leaves_q.size();
        for (int i = 0; i < q_len; i++) {
            int leaf = leaves_q.front();
            leaves_q.pop();
            for (int neighbor : graph[leaf]) {
                graph[neighbor].erase(leaf);
                tree[leaf] = neighbor;
                if (graph[neighbor].size() == 1){
                    leaves_q.push(neighbor);
                }
            }
            graph.erase(leaf);
        }
    }
    vector<int> left_nodes;
    for (auto node_neighbors: graph) left_nodes.push_back(node_neighbors.first);
    int root;
    if (left_nodes.size() == 2) {
        root = left_nodes[1];
        tree[left_nodes[0]] = root;
    }
    else {
        root = left_nodes[0];
    }
    return make_tuple(tree, nodes, root);;
}

tuple<unordered_map<int, long>, unordered_map<int, unordered_set<int>>>
get_sums_and_children(unordered_map<int, int> tree, unordered_set<int> nodes, int root, vector<int> c) {
    unordered_map<int, long> sums;
    unordered_map<int, unordered_set<int>> children;
    for (int node : nodes) {
        int aux = node;
        while (true) { // aux != root
            try {
                // For sums
                sums[aux] = ((sums.find(aux) != sums.end()) ? sums[aux] : 0) + c[node];
                // For children
                children[aux] = ((children.find(aux) != children.end()) ? children[aux] : unordered_set<int>());
                if (node != aux) {
                    children[aux].insert(node);
                }
                aux = tree[aux];
            } catch (out_of_range oor) { // aux == root -> root not in tree
                break;
            }
        }  
    }
    return make_tuple(sums, children);
}

long balancedForest(vector<int> c, vector<vector<int>> edges) {
    auto tree_components = get_tree(get_graph(edges));
    unordered_map<int, int> tree = get<0>(tree_components);
    unordered_set<int> nodes = get<1>(tree_components);
    int root = get<2>(tree_components);
    auto sums_and_children = get_sums_and_children(tree, nodes, root, c);
    unordered_map<int, long> sums = get<0>(sums_and_children);
    unordered_map<int, unordered_set<int>> children = get<1>(sums_and_children);
    long val = LONG_MAX;
    vector<vector<int>> checked(c.size(), vector<int>(c.size(), 0));
    for (auto n1: children[root]) {
        map<int, long> valid_sum;
        valid_sum[n1] = sums[n1];
        valid_sum[root] = sums[root] - sums[n1];
        int node_lo = valid_sum[n1] < valid_sum[root] ? n1 : root;
        int node_hi = valid_sum[n1] < valid_sum[root] ? root : n1;
        if (valid_sum[node_hi] == valid_sum[node_lo]){
            val = min(val, valid_sum[node_lo]);
            continue;
        }
        long goal_sum, new_node_val;
        unordered_set<int> curr_children;
        if (valid_sum[node_hi] < 2 * valid_sum[node_lo]) {
            goal_sum = valid_sum[node_lo];
            new_node_val = 2 * valid_sum[node_lo] - valid_sum[node_hi];
            if (node_hi == n1) {
                curr_children = children[n1];
            }
            else {
                curr_children.clear();
                copy_if(
                    children[root].begin(),
                    children[root].end(), 
                    inserter(curr_children, curr_children.end()), 
                    [&children, n1] (int node) { return (children[n1].find(node) == children[n1].end() || node != n1); }
                );
            }
        }
        else if (valid_sum[node_hi] > 2 * valid_sum[node_lo]){
            if (valid_sum[node_hi] % 2 == 0){
                goal_sum = valid_sum[node_hi] / 2;
                new_node_val = goal_sum - valid_sum[node_lo];
                if (node_hi == n1) {
                    curr_children = children[n1];
                }
                else{
                    curr_children.clear();
                    copy_if(
                        children[root].begin(),
                        children[root].end(), 
                        inserter(curr_children, curr_children.end()), 
                        [&children, n1] (int node) { return (children[n1].find(node) == children[n1].end() || node != n1); }
                    );
                }
            }
            else {
                continue;
            }
        }
        else { // valid_sum[node_hi] == 2 * valid_sum[node_lo]
            goal_sum = valid_sum[node_hi] / 2;
            new_node_val = 0;  // goal_sum - valid_sum[node_lo]
            if (node_hi == n1) {
                curr_children = children[n1];
            }
            else {
                curr_children.clear();
                copy_if(
                    children[root].begin(),
                    children[root].end(), 
                    inserter(curr_children, curr_children.end()), 
                    [&children, n1] (int node) { return (children[n1].find(node) == children[n1].end() || node != n1); }
                );
            }
        }  
        for (auto n2 :curr_children){
            if (!checked[n2][n1]) {
                checked[n1][n2] = 1;
                long sum_bottom = sums[n2];
                long sum_top = valid_sum[node_hi] - sum_bottom;
                if (sum_top == goal_sum or sum_bottom == goal_sum) {
                    val = min(val, new_node_val);
                    break;
                }
            }
        }
    }
    return val != LONG_MAX ? val : -1;
}
