import sys; args=sys.argv[1:]
import time
    
def doJump(string, source, jumpee, target):
    return "".join([("." if (x==source or x==jumpee) else "1" if x==target else string[x]) for x in range(len(string))])

fsJumps = [(0, 1, 3), (1, 3, 6), (3, 6, 10), (6, 10, 15),
                  (2, 4, 7), (4, 7, 11), (7, 11, 16), (5, 8, 12), (8, 12, 17), (9, 13, 18)]
horizJumps = [(3, 4, 5), (6, 7, 8), (7, 8, 9), (10, 11, 12), (11, 12, 13), (12, 13, 14),
                  (15, 16, 17), (16, 17, 18), (17, 18, 19), (18, 19, 20)]
bsJumps = [(6, 11, 17), (3, 7, 12), (7, 12, 18), (1, 4, 8), (4, 8, 13), (8, 13, 19),
                  (0, 2, 5), (2, 5, 9), (5, 9, 14), (9, 14, 20)]
ascendingJumps = fsJumps + bsJumps + horizJumps
descendingJumps = [(z, y, x) for (x, y, z) in ascendingJumps]
possibleJumps = ascendingJumps + descendingJumps

def neighbors(pzl):
    neighborList = []
    for source, jumpee, target in possibleJumps:
        if pzl[source] == "1" and pzl[jumpee] == "1" and pzl[target] == ".":
            neighborList.append(doJump(pzl, source, jumpee, target))
    return neighborList

def getMove(prevPzl, postPzl):
    inv = []
    for idx in range(21):
        if prevPzl[idx] != postPzl[idx]:
            inv.append(idx)
    inv.sort()
    move = tuple(inv)
    mType = "-"
    if move in fsJumps:
        mType = "/"
    if move in bsJumps:
        mType = "\\"
    return str(inv[1])+mType

def findPath(start, goal, visited):
    path = []
    while goal != start:
        prevPos = visited[goal]
        path = [getMove(prevPos, goal)] + path
        goal = prevPos
    return path

def isSolved(pzl):
    return pzl.count("1")==1 and pzl.find("1") != initialHole # lenient
    #return pzl.count("1")==1 and pzl.find("1") == initialHole # strict

def solve(start):
    visited = {start: None}
    if isSolved(start):
        return [start]
    currentLayer = [start]
    for pzl in currentLayer:
        for nextPzl in neighbors(pzl):
            if nextPzl not in visited:
                visited[nextPzl] = pzl
                currentLayer.append(nextPzl)
            if isSolved(nextPzl):
                return findPath(start, nextPzl, visited)
    return []

def main():
    global initialHole
    startTime = time.time()
    start = args[0]
    initialHole = start.index(".")

    print(start)
    solution = solve(start)

    if solution:
        for step in solution:
            print(step, end=" ")
    else:
        print([start])
    print("\n\nTime: "+"{:.4g}".format(time.time()-startTime)+"s")
    
if __name__ == "__main__":
    main()

# Vincent Trang, pd.4, 2023
