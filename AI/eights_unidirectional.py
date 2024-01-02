import sys; args=sys.argv[1:]
import time

BAND = 6
width = 3
height = 3

def printSolution(solution):
    for i in range(0, len(solution), BAND):
        printBand(solution[i:i+BAND])
        print()

def printBand(solution):
    for sectionIndex in range(0, width*height, width):
        for pzl in solution:
            print(pzl[sectionIndex:sectionIndex+width], end=" ")
        print()

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

def findPath(start, goal, visited):
    path = [goal]
    while goal != start:
        prevPos = visited[goal]
        path = [prevPos] + path
        goal = prevPos
    return path
    
def solve(start, goal):
    visited = {start: None}
    if start == goal:
        return [start]
    currentLayer = {start}
    while currentLayer:
        nextLayer = set()
        for pzl in currentLayer:
            for nextPzl in neighbors(pzl):
                if nextPzl not in visited:
                    visited[nextPzl] = pzl
                    nextLayer.add(nextPzl)
                if nextPzl == goal:
                    return findPath(start, goal, visited)
        currentLayer = nextLayer
    return []

def main():
    startTime = time.time()
    start = args[0]
    goal = args[1] if len(args)>1 else "12345678_"

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
