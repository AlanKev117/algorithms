class Heap:

    def __init__(self, arr, heap_type="max"):
        # Define comparators
        def bigger(a, b):
            return a > b

        def less(a, b):
            return a < b

        # Assign comparator
        self.compare = bigger if heap_type == "max" else less if heap_type == "min" else None
        assert self.compare != None, "Heap type not supported"

        # Heapify array
        self.heapify(arr)

    def heapify(self, arr):
        # Initialize heap as a copy of the array
        self.heap = [*arr]

        # Get the middle of the heap
        middle = max(0, len(arr) // 2 - 1)

        # Loop from first non-leaf (middle) down to zero.
        for i in range(middle, -1, -1):
            self.sink(i)

    def sink(self, pos):
        # Copy of sink position
        i = pos

        # Get heap size
        n = len(self.heap)

        # Loop while value in i cannot longer be sunk.
        while True:
            # Indexes
            prior = i
            left = 2 * i + 1
            right = 2 * i + 2

            # Update prior
            if left < n and self.compare(self.heap[left], self.heap[prior]):
                prior = left
            if right < n and self.compare(self.heap[right], self.heap[prior]):
                prior = right

            if prior == i:
                break

            # Swap current item with possibly updated priorer one.
            self.heap[prior], self.heap[i] = self.heap[i], self.heap[prior]

            # Go deeper (sink)
            i = prior

    def swim(self, pos):
        # Bounds valdation
        assert 0 <= pos < len(self.heap), "Swim position out of heap bounds"

        # Parent and child initial values
        child = pos
        parent = (pos - 1) // 2

        # Swimming of the child
        while child > 0 and self.compare(self.heap[child], self.heap[parent]):
            self.heap[child], self.heap[parent] = self.heap[parent], self.heap[child]
            child = parent
            parent = (parent - 1) // 2

    def pop(self):
        trash = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.sink(0)
        return trash

    def push(self, item):
        self.heap.append(item)
        self.swim(len(self.heap) - 1)


arr = [3, 9, 2, 1, 4, 5]

heap = Heap(arr, "max")
print(heap.heap)

heap.push(20)
print(heap.heap)

print(heap.pop())
print(heap.heap)
