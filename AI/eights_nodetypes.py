import sys; args=sys.argv[1:]
import time, random

BAND = 6
width = None
height = None
TESTING_AMOUNT = 500

def printSolution(solution):
    for i in range(0, len(solution), BAND):
        printBand(solution[i:i+BAND])
        print()

def printBand(solution):
    for sectionIndex in range(0, width*height, width):
        for pzl in solution:
            print(pzl[sectionIndex:sectionIndex+width], end=" ")
        print()

def setDimensions(tileCt):
    global width, height
    height = int(tileCt**0.5)
    while tileCt%height:
        height -= 1
    width = tileCt // height

def parity(start, goal):
    if start == goal:
        return True
    else:
        for pos in range(len(goal)):
            if start[pos] != goal[pos]:
                break
        return not parity(start, swapChars(goal, pos, goal.index(start[pos])))

def isSolvable(start, goal):
    holeParity = "".join(str((i+j)%2) for i in range(height) for j in range(width))
    return parity(start, goal) == (holeParity[start.index("_")] == holeParity[goal.index("_")])
    
def swapChars(string, index1, index2):
    return "".join(string[index2] if x==index1 else string[x] if x!=index2 else string[index1] for x in range(len(string)))

def neighbors(pzl):
    holePos = pzl.index("_")
    neighborList = []
    if holePos >= width:
        neighborList.append(swapChars(pzl, holePos, holePos-width))
    if holePos < width*height-width:
        neighborList.append(swapChars(pzl, holePos, holePos+width))
    if holePos%width:
        neighborList.append(swapChars(pzl, holePos, holePos-1))
    if (holePos+1)%width:
        neighborList.append(swapChars(pzl, holePos, holePos+1))
    return neighborList

def findPath(start, goal, visited):
    path = [goal]
    while goal != start:
        prevPos = visited[goal]
        path = [prevPos] + path
        goal = prevPos
    return path

totalChildren = 0
totalParents = 0

def solve(start, goal):
    global totalChildren, totalParents
    pcDict = {}
    if not isSolvable(start, goal):
        return []
    visited = {start: None}
    if start == goal:
        return [start]
    currentLayer = {start}
    while currentLayer:
        nextLayer = set()
        for pzl in currentLayer:
            parents = 0
            children = 0
            for nextPzl in neighbors(pzl):
                if nextPzl not in visited: # new neighbor
                    visited[nextPzl] = pzl
                    nextLayer.add(nextPzl)
                    children += 1
                    totalChildren += 1
                elif nextPzl in nextLayer: # found already, but as a child
                    children += 1
                    totalChildren += 1
                else:
                    parents += 1
                    totalParents += 1
                if nextPzl == goal:
                    pass # return findPath(start, goal, visited)
            if (parents, children) in pcDict:
                pcDict[(parents, children)] += 1
            else:
                pcDict[(parents, children)] = 1
        currentLayer = nextLayer
    return pcDict

def main():
    startTime = time.time()
    if len(args):
        start = args[0]
        goal = args[1] if len(args)>1 else "".join(sorted(args[0].replace("_","")))+"_"
        setDimensions(len(start))

        solution = solve(start, goal)
        for k, v in solution.items():
            print (f"Parents: {k[0]}, Children: {k[1]}, Count: {v}")
        
    else:
        possibleCt = 0
        pathLenSum = 0
        setDimensions(9)
        for n in range(TESTING_AMOUNT):
            solution = solve("".join(random.sample("12345678_",9)), "".join(random.sample("12345678_",9)))
            if solution:
                possibleCt += 1
                pathLenSum += len(solution)-1
        print("Puzzles attempted:", TESTING_AMOUNT)
        print("Number of impossible puzzles:", TESTING_AMOUNT-possibleCt)
        print("Average depth of solvable puzzles:", round(pathLenSum/possibleCt, 3))
    print("Time: "+"{:.3g}".format(time.time()-startTime)+"s")
    
if __name__ == "__main__":
    main()

# Vincent Trang, pd.4, 2023
