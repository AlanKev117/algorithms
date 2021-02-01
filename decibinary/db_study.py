dp = {}

def f(d,s):
    if (d,s) not in dp:
        if d == 0 and s == 0:
            dp[d,s] = 1
        elif d == 0 and s != 0:
            dp[d,s] = 0
        elif s < 0:
            dp[d,s] = 0
        else:
            dp[d,s] = sum([f(d-1, s-i*2**(d-1)) for i in range(10)])
    return dp[d,s]

for d in range(20):
    r = []
    for s in range(20):
        r.append(f(d,s))
    print(f"d = {d} ", r)