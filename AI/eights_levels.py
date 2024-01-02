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
    
def solve(start, goal=None):
    #if not isSolvable(start, goal):
    #    return []
    depths = []
    visited = {start: None}
    if start == goal:
        return [start]
    currentLayer = {start}
    while currentLayer:
        depths.append(len(currentLayer))
        nextLayer = set()
        for pzl in currentLayer:
            for nextPzl in neighbors(pzl):
                if nextPzl not in visited:
                    visited[nextPzl] = pzl
                    nextLayer.add(nextPzl)
                #if nextPzl == goal:
                #    return findPath(start, goal, visited)
        currentLayer = nextLayer
    return depths

def main():
    startTime = time.time()

    setDimensions(9)

    PUZZLE = "12_456783"
    print(PUZZLE)
    solution = solve(PUZZLE)
    print(solution)

    print("Time: "+"{:.3g}".format(time.time()-startTime)+"s")
    
if __name__ == "__main__":
    main()

#12_456783
# Vincent Trang, pd.4, 2023
