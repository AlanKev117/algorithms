from collections import deque


# Complete the riddle function below.
def riddle(arr):
    N = len(arr)
    result = [-1] * N
    span = [-1] * N

    values = []  # Stack
    indexes = [] # Stack
    indexes.append(-1) # Aux most left index, not 0.

    # How many greater or equal items exist to the left before one smaller appears
    # Store in span.
    for i in range(N):
        # Pop items as long as they are greater or equal than the current one.
        while len(values) > 0 and values[-1] >= arr[i]:
            values.pop()
            indexes.pop()
        # Store the distance from this item (i) to the previous smaller (indexes.peak())
        span[i] = i - indexes[-1] - 1
        # push items as long as they are greater than the peak of the stack
        values.append(arr[i])
        indexes.append(i)

    values.clear() # Reset stack
    indexes.clear() # Reset stack
    indexes.append(N) # Aux most right index, not N - 1.
    # How many greater or equal items exist to the right before one smaller appears
    # Add to values in span.
    for i in range(N-1, -1, -1):
        # Pop items as long as they are greater or equal than the current one.
        while len(values) > 0 and values[-1] >= arr[i]:
            values.pop()
            indexes.pop()
        # Store the distance from this item (i) to the previous smaller (indexes.peak())
        span[i] += indexes[-1] - i - 1
        # push items as long as they are greater than the peak of the stack
        values.append(arr[i])
        indexes.append(i)

    # Result acts as a hash table whose indexes (keys) are the sizes of the windows
    # the values are equivalent max([arr[i] for i in range(N) if span[i] == key])
    # but calculed linearly as follows
    for i in range(N):
        result[span[i]] = max(result[span[i]], arr[i])

    # There might be some gaps in result. We propagate the smallest value to right.
    for i in range(N - 2, -1, -1):
        result[i] = max(result[i], result[i + 1])

    return result



print(riddle([6, 7, 9, 2, 1, 8, 4, 4]))
