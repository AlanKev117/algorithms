from fenwick_tree import FenwickTree

"""
Given an array arr of n integers, the sorted_sums function returns a new array of
the same length (n). In the i-th position in contains the following sum:

    sorted_sums[i] = 1*s[0] + 2*s[1] + ... + (i + 1)*s[i]

where s is the sorted version of arr[:i]

"""

def sorted_sums(arr):
    # n*log(n)
    sorted_arr = sorted(arr)
    arr_len = len(arr)
    
    # n
    index_of = {item: [] for item in sorted_arr}
    for i in range(arr_len):
        index_of[sorted_arr[i]].append(i)

    # n
    values_ft = FenwickTree([0 for _ in range(arr_len)])
    indexes_ft = FenwickTree([0 for _ in range(arr_len)])

    # 1
    prev_sum = 0
    sums = []

    # n
    for i, item in enumerate(arr):

        # log(n)
        sorted_index = index_of[item].pop()
        values_ft.update(sorted_index, item)
        indexes_ft.update(sorted_index, 1)
        
        # log(n)
        shifted_interval_sum = values_ft.query_range(sorted_index + 1, arr_len - 1)
        index_of_new_item = indexes_ft.query(sorted_index)
        current_sum = prev_sum + index_of_new_item * item + shifted_interval_sum

        # 1
        sums.append(current_sum)
        prev_sum = current_sum
    
    # Total: n*log(n)
    return sums

print(sorted_sums([9,2,12,5,2]))

