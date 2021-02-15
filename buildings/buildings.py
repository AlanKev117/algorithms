#!/bin/python3

import math
import os
import random
import re
import sys

from collections import deque

# Complete the largestRectangle function below.
def lr(h):
    n = len(h)
    h_with_i = [(h[i], i) for i in range(n)]
    h_with_i = sorted(h_with_i, key=lambda pair:pair[0])
    top_areas = [h_with_i[i][0] for i in range(n)]
    for i in range(n):
        for f in range(h_with_i[i][1] + 1, n):
            if h[f] < h_with_i[i][0]:
                break
            top_areas[i] += h_with_i[i][0]
        for b in range(h_with_i[i][1] - 1, -1, -1):
            if h[b] < h_with_i[i][0]:
                break
            top_areas[i] += h_with_i[i][0]
    return max(top_areas)
        




if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input())

    h = list(map(int, input().rstrip().split()))

    result = lr(h)

    print(str(result))
    #fptr.write(str(result) + '\n')

    #fptr.close()
