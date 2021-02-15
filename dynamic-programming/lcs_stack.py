import random

def lcs(str1, str2):
    solutions = {}
    solution_stack = [(0,0)]
    while len(solution_stack) > 0:
        
        i, j = solution_stack[-1]

        if (i, j) in solutions:
            solved_node = solution_stack.pop()
            children_stack.append(solved_node)
            continue
        
        if i == len(str1) or j == len(str2):
            solutions[i, j] = 0
            solution_stack.pop()
            continue

        if str1[i] == str2[j]:
            if (i + 1, j + 1) not in solutions:
                solution_stack.append((i + 1, j + 1))
            else:
                solutions[i, j] = 1 + solutions[i + 1, j + 1]
                solution_stack.pop()
            continue
        
        if str1[i] != str2[j]:
            if (i + 1, j) not in solutions:
                solution_stack.append((i + 1, j))
            elif (i, j + 1) not in solutions:
                solution_stack.append((i, j + 1))
            else:
                solutions[i, j] = max(solutions[i + 1, j], solutions[i, j + 1])
                solution_stack.pop()
        
    return solutions[0, 0]

random.seed(1234)

def gen_string(n):
    s = [97 + random.randint(0, 26) for _ in range(n)]
    return "".join(map(chr, s))

s1 = gen_string(1000)
s2 = gen_string(1000)
l = lcs(s1, s2)
print(l)