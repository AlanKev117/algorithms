class UnionFind:
    def __init__(self, size):
        assert size > 0, "Union Find size must be larger than zero"
        self.sets_sizes = [1 for i in range(size)]
        self.graph = [i for i in range(size)]

    def find(self, item):
        # Initialize aux node variable
        node = item

        # Check for self link (root node)
        while node != self.graph[node]:
            node = self.graph[node]
        root = node

        # Path compression for nodes in path from item to root.
        node = item
        while node != root:
            parent = self.graph[node]
            self.graph[node] = root
            node = parent

        return root

    def unify(self, item_1, item_2):
        # Roots of sets of each item
        root_1, root_2 = self.find(item_1), self.find(item_2)

        # Abort if they belong to same set
        if root_1 == root_2:
            return

        # Sort roots according to its sets sizes
        root_of_smaller, root_of_larger = sorted(
            [root_1, root_2],
            key=lambda r: self.sets_sizes[r])

        # Update set_size of larger set and root of smaller one.
        self.sets_sizes[root_of_larger] += self.sets_sizes[root_of_smaller]
        self.sets_sizes[root_of_smaller] = 0
        self.graph[root_of_smaller] = root_of_larger

uf = UnionFind(9)
uf.unify(2, 5)
uf.unify(3, 6)
uf.unify(1, 8)
uf.unify(1, 4)
uf.unify(4, 7)
uf.unify(0, 1)
print(uf.graph)
print(uf.sets_sizes)