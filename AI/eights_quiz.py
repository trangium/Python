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

def good(s1, s2):
    return s1=="_" or s2=="_" or abs(int(s1)-int(s2)) != 1

goodPuzzles = [[] for i in range(31)]
badPuzzles = [[] for i in range(32)]

def solve(start):
    visited = {start: None}
    currentLayer = {start}
    depth = 0
    while currentLayer:
        nextLayer = set()
        for pzl in currentLayer:
            if pzl[0] != start[0] and pzl[1] != start[1] and pzl[2] != start[2] and pzl[3] != start[3] and pzl[4] != start[4] and pzl[5] != start[5] and pzl[6] != start[6] and pzl[7] != start[7] and pzl[8] != start[8]:
                goodPuzzles[depth] = pzl
            else:
                badPuzzles[depth] = pzl
            # determine if the puzzle satisfies no 2 tiles differing by 1
            for nextPzl in neighbors(pzl):
                if nextPzl not in visited:
                    visited[nextPzl] = pzl
                    nextLayer.add(nextPzl)
        currentLayer = nextLayer
        depth += 1
    return []

def main():
    startTime = time.time()
    start = "12345678_"
    # goal = args[1] if len(args)>1 else "".join(sorted(args[0].replace("_","")))+"_"
    setDimensions(len(start))

    solution = solve(start)


    print("Time: "+"{:.3g}".format(time.time()-startTime)+"s")
    
if __name__ == "__main__":
    main()

# Vincent Trang, pd.4, 2023
