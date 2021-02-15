import random

def lcs_bu(str1, str2):
    solutions = {}
    len1 = len(str1)
    len2 = len(str2)

    # Pre populate matrix
    for i in range(-1, len1):
        solutions[i, -1] = 0
    
    for j in range(-1, len2):
        solutions[-1, j] = 0

    for i in range(len1):
        for j in range(len2):
            if str1[i] == str2[j]:
                solutions[i, j] = 1 + solutions[i - 1, j - 1]
            else:
                solutions[i, j] = max(solutions[i - 1, j], solutions[i, j - 1])
    
    return solutions[len1 - 1, len2 - 1]

random.seed(1234)

def gen_string(n):
    s = [97 + random.randint(0, 26) for _ in range(n)]
    return "".join(map(chr, s))

s1 = gen_string(1000)
s2 = gen_string(1000)
l = lcs_bu(s1, s2)
print(l)
