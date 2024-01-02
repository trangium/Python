import itertools
numerator = 0
denominator = 0
p = itertools.product([False, True], repeat=25)

a = 0
for c in p:
    a += 1
    if all(sum(c[i:i+5])==3 for i in range(0, 25, 5)):
        denominator += 1
        if all(sum(c[i:i+25:5])==3 for i in range(5)):
            numerator += 1
    if not a%12345: print(a)

print(numerator)
print(denominator)
