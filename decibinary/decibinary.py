from bisect import bisect_right

dmax = 3000
digits = 10
powers = 20

v = {}
c = {}

def pre_compute():
    # Compute the number of duplicates for each value, number of digits.
    for i in range(dmax):
        v[i, 0] = int(i < digits)
        for j in range(1, powers):
            # Duplicates is sum of all shorter numbers duplicates for each digit.
            for k in range(digits):
                value = i - k * (1 << j)
                # Exit if using digit creates number larger than target value.
                if value < 0:
                    break
                v[i,j] = v.get((i, j), 0) + v[value, j - 1]

    # Calculate the absolute offset for the first duplicate of each number.
    for i in range(1, dmax):
        c[i] = v[i - 1, powers - 1] + c.get(i - 1, 0)

def decibinaryNumbers(x):
    # The decibinary to return.
    result = 0

    value = bisect_right(list(c.values()), x - 1)
    offset = (x - 1) - c[value]

    # Find each digit.
    for i in range(powers - 1, 0, -1):
        power = 1 << i
        
        # Find the digit which takes us closest to offset.
        for digit in range(digits):
            
            # Calculate value of remaining digits.
            v1 = value - digit * power

            # If index is less than duplicates for remainder we have our digit.
            if offset < v[v1, i - 1]:
                result += digit
                value -= power * digit
                break

            # Subtract number of duplicates for this digit from offset.
            offset -= v[v1, i - 1]

        result *= 10

    # Whatever is left must be the last digit.
    result += value
    # print(f"{x}:{result}:{l-c[0]}")

    return result

pre_compute()

while True:
    x = int(input("x: "))
    print(decibinaryNumbers(x))
