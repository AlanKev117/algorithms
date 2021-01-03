from math import log2, ceil


class SegmentTree:

    def __init__(self, arr):
        # Get the length of the original array.
        self.n = len(arr)
        # Define inner segment tree as an array twice as big as the original.
        self.st = [None] * self.n + arr
        for i in range(self.n - 1, 0, -1):
            self.st[i] = self.st[2*i] + self.st[2*i+1]

    def update(self, pos, val):
        node = self.n + pos
        prev_val = self.st[node]
        delta = val - prev_val
        while node:
            self.st[node] += delta
            node //= 2

    def query(self, begin, end):
        res = 0
        b = begin + self.n
        e = end + self.n
        while (b < e):

            if b & 1:
                res += self.st[b]
                b += 1

            if e & 1:
                e -= 1
                res += self.st[e]

            b //= 2
            e //= 2

        return res

arr = [1,2,3,4,5,6,23,3,12,2]
st = SegmentTree(arr)
sum = st.query(3, 8)
print(sum)