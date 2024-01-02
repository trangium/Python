import sys; args=sys.argv[1:]
import time

BAND = 6
width = None
height = None

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

def isPossible(start, goal):
    holeParity = "".join(str((i+j)%2) for i in range(height) for j in range(width))
    return parity(start, goal) == (holeParity[start.index("_")] == holeParity[goal.index("_")])
    
def swapChars(string, index1, index2):
    return "".join([string[index2] if x==index1 else string[index1] if x==index2 else string[x] for x in range(len(string))])

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

def findPath(start, goal, midPzl, visited, endTable):
    path = [midPzl]
    pzl = midPzl
    while pzl != start:
        prevPos = visited[pzl]
        path = [prevPos] + path
        pzl = prevPos
    pzl = midPzl
    while pzl != goal:
        nextPos = endTable[pzl]
        path.append(nextPos)
        pzl = nextPos
    return path
    
def solve(start, goal):
    if not isPossible(start, goal):
        return []
    visited = {start: None}
    endTable = {goal: None} #
    if start == goal:
        return [start]
    currentLayer = {start}
    goalLayer = {goal} #
    while currentLayer:
        nextLayer = set()
        backLayer = set()
        for pzl in currentLayer:
            for nextPzl in neighbors(pzl):
                if nextPzl not in visited:
                    visited[nextPzl] = pzl
                    nextLayer.add(nextPzl)
                if nextPzl in endTable:
                    return findPath(start, goal, nextPzl, visited, endTable)
        for pzl in goalLayer: #
            for prevPzl in neighbors(pzl):
                if prevPzl not in endTable:
                    endTable[prevPzl] = pzl
                    backLayer.add(prevPzl)
                if prevPzl in visited:
                    return findPath(start, goal, prevPzl, visited, endTable)
        currentLayer = nextLayer
        goalLayer = backLayer
    return [] # should never reach this line unless puzzle has height 1

def main():
    startTime = time.time()
    start = args[0]
    goal = args[1] if len(args)>1 else "".join(sorted(args[0].replace("_","")))+"_"
    setDimensions(len(start))

    solution = solve(start, goal)

    if solution:
        printSolution(solution)
        print("Steps:",len(solution)-1)
    else:
        printSolution([start])
        print("Steps: -1")
    print("Time: "+"{:.3g}".format(time.time()-startTime)+"s")
    
if __name__ == "__main__":
    main()

# Vincent Trang, pd.4, 2023
