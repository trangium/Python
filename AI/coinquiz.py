##
### slow
##def change(n, coinLst):
##    if n == 0: return 1
##    if not coinLst: return 0
##    if n < 0: return 0
##    return change(n, coinLst[1:]) + change(n-coinLst[0], coinLst)
import sys
sys.setrecursionlimit(100005)
lookup = {}
# fast
def fastChange(n, coinLst):
    coinTup = tuple(coinLst)
    if (n, coinTup) in lookup: return lookup[(n, coinTup)]
    if n == 0: ret = 1
    elif not coinLst or n < 0: ret = 0
    else: ret = fastChange(n, coinLst[1:]) + fastChange(n-coinLst[0], coinLst)
    lookup[(n, coinTup)] = ret
    return ret

def smartChange(n):
    acc = 0
    for i in range(0, n+5, 5):
        acc += fastChange(i, [100, 50, 25, 10, 5])
    return acc

print(smartChange(10000))
