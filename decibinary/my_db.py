from collections import OrderedDict

counts = {}
cmax = 100000

def decimal_of(x):
    decimal = 0
    x_c = x
    i = 0
    while x_c > 0:
        decimal += (x_c % 10) * (1 << i)
        x_c //= 10
        i += 1
    return decimal

d = OrderedDict()

n = 3
for i in range(10 ** n):
    dec = decimal_of(i)
    d[dec] = d.get(dec, 0) + 1

vals = list(d.values())
print(vals[0:2 ** n])
print(sum(vals[0:2**n]))