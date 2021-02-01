factorials = {}
def factorial(f):
    if f in factorials:
        return factorials[f]
    
    if f < 2:
        factorials[f] = 1
    else:
        factorials[f] =  f * factorial(f - 1)
    
    return factorials[f]
    
def linear_result(x, y, z):
    return 3*x+2*y+z  

def stepPerms(n):
    three_max = n // 3
    two_max = n // 2
    one_max = n
    total_perms = 0
    n_fact = factorial(n)
    for i in range(three_max+1):
        for j in range(two_max+1):
            for k in range(one_max+1):
                if linear_result(i,j,k) == n:
                    total_perms += factorial(i+j+k) / (factorial(i) * factorial(j) * factorial(k))
    return total_perms
