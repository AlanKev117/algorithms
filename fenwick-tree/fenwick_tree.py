class FenwickTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.ft = [0] + arr
        for i in range(1 , self.n + 1):
            range_end_index = i + (i & -i)
            if range_end_index <= self.n:
                self.ft[range_end_index] += self.ft[i]

    def update(self, pos, val):
        p = pos + 1
        while p <= self.n:
            self.ft[p] += val
            p += (p & -p)

    def query(self, end):
        e = end + 1
        res = 0
        while e > 0:
            res += self.ft[e]
            e -= (e & -e)
        return res

    def query_range(self, begin, end):
        return self.query(end) - self.query(begin - 1)

def main():
    arr = [1,2,3,4]
    ft = FenwickTree(arr)
    print(ft.ft)
    print(ft.query(3))
    print(ft.update(0, 5))
    print(ft.ft)
    print(ft.query_range(0, 3))

if __name__ == "__main__":
    main()
