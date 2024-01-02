import random

comb = {"1":"2", "2":"1", "3":"3", "6":"6", "t":"t", "T":"T"}
grow = {"1":"3", "2":"3", "3":"6", "6":"t", "t":"T", "T":"X"}

def leftH(x):
    if not x: return ""
    if x[0] == ".": return x[1:]
    if len(x) >= 2 and comb[x[0]] == x[1]: return grow[x[0]]+x[2:]
    return x[0] + leftH(x[1:])

def left(x, nextTile):
    c = leftH(x)
    if len(c) == 4: return c
    return c + nextTile

def right(x, nextTile):
    return left(x[::-1], nextTile)[::-1]

def sim(start, goal, bagTag, shuffle=True):
    bag = list(bagTag)
    acc = ""
    if shuffle: random.shuffle(bag)
    else: bag.reverse()
    while bag:
        nt = bag.pop()
        if random.random() < 0.5:
            start = left(start, nt)
            acc += "L"
        else:
            start = right(start, nt)
            acc += "R"
        acc += " " + start + " "
    if start == goal:
        return acc
    return False

def largeSim(start, goal, bag, shuffle=True):
    ct = 0
    for i in range(50000):
        ct += bool(sim(start, goal, bag, shuffle))

    return ct
