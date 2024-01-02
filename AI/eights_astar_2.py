import sys; args=sys.argv[1:]
import time, random

width = None
height = None
DISTANCES = [[0,1,2,3,1,2,3,4,2,3,4,5,3,4,5,6],[1,0,1,2,2,1,2,3,3,2,3,4,4,3,4,5],[2,1,0,1,3,2,1,2,4,3,2,3,5,4,3,4],[3,2,1,0,4,3,2,1,5,4,3,2,6,5,4,3],
             [1,2,3,4,0,1,2,3,1,2,3,4,2,3,4,5],[2,1,2,3,1,0,1,2,2,1,2,3,3,2,3,4],[3,2,1,2,2,1,0,1,3,2,1,2,4,3,2,3],[4,3,2,1,3,2,1,0,4,3,2,1,5,4,3,2],
             [2,3,4,5,1,2,3,4,0,1,2,3,1,2,3,4],[3,2,3,4,2,1,2,3,1,0,1,2,2,1,2,3],[4,3,2,3,3,2,1,2,2,1,0,1,3,2,1,2],[5,4,3,2,4,3,2,1,3,2,1,0,4,3,2,1],
             [3,4,5,6,2,3,4,5,1,2,3,4,0,1,2,3],[4,3,4,5,3,2,3,4,2,1,2,3,1,0,1,2],[5,4,3,4,4,3,2,3,3,2,1,2,2,1,0,1],[6,5,4,3,5,4,3,2,4,3,2,1,3,2,1,0]]
distanceTable = {}

with open(args[0]) as f:
    pzlInput = [line.strip() for line in f]

def heap_up(heap, k):
    if k:
        parent = (k-1)//2
        if heap[k] < heap[parent]:
            heap[k], heap[parent] = heap[parent], heap[k]
            heap_up(heap, parent)

def insert(heap, elem):
    heap.append(elem)
    heap_up(heap, len(heap)-1)

def heap_down(heap):
    k = 0
    while 2*k+1 < len(heap):
        if len(heap) > 2*k+2 and heap[2*k+2] < heap[2*k+1]:
            if heap[k] <= heap[2*k+2]: return
            heap[k], heap[2*k+2] = heap[2*k+2], heap[k]
            k = 2*k+2
        else:
            if heap[k] <= heap[2*k+1]: return
            heap[k], heap[2*k+1] = heap[2*k+1], heap[k]
            k = 2*k+1

def remove_min(heap):
    heap[0] = heap[-1]
    heap.pop()
    heap_down(heap)

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

def findCompactPath(start, goal, visited):
    path = ""
    holePos = goal.index("_")
    while goal != start:
        path = (visited[goal]) + path
        
        if visited[goal] == "U":
            newPos = holePos+width
        if visited[goal] == "D":
            newPos = holePos-width
        if visited[goal] == "L":
            newPos = holePos+1
        if visited[goal] == "R":
            newPos = holePos-1
        goal = swapChars(goal, holePos, newPos)
        
        holePos = newPos
    return path

def h(pzl):
    dist = 0
    for idx, val in enumerate(pzl):
        if val != "_":
            dist += distanceTable[val][idx]
    return dist
            

def processNbr(openSet, min_f, pzl, holePos, posFrom, direc):
    nbr = swapChars(pzl, holePos, posFrom)
    newF = min_f - distanceTable[nbr[holePos]][posFrom] + distanceTable[nbr[holePos]][holePos] + 1
    openSet[newF].append((nbr, direc))

def aStar(root, goal):
    if not isSolvable(root, goal): return "X"
    openSet = [[] for i in range(160)] # create an openSet with root
    openSet[h(root)].append((root, None))
    min_f = h(root)
    closedSet = {} # create an empty closedSet

    while True:
        while not openSet[min_f]:
            min_f += 1
        pzl, direc = openSet[min_f].pop()
        if pzl in closedSet: continue
        closedSet[pzl] = direc
        if pzl == goal: return findCompactPath(root, goal, closedSet)
        
        holePos = pzl.index("_")
        if holePos >= width and direc != "D":
            processNbr(openSet, min_f, pzl, holePos, holePos-width, "U")
        if holePos < width*height-width and direc != "U":
            processNbr(openSet, min_f, pzl, holePos, holePos+width, "D")
        if holePos%width and direc != "R":
            processNbr(openSet, min_f, pzl, holePos, holePos-1, "L")
        if (holePos+1)%width and direc != "L":
            processNbr(openSet, min_f, pzl, holePos, holePos+1, "R")

def main():
    global distanceTable
    startTime = time.perf_counter()
    goal = pzlInput[0]
    setDimensions(len(goal))
    distanceTable = {val:DISTANCES[idx] for idx, val in enumerate(goal) if val != "_"}
    for pzl in pzlInput:
        prevTime = time.perf_counter()
        solution = aStar(pzl, goal)
        solutionTime = -prevTime+time.perf_counter()
        print(pzl, "path", solution)
        print("Length: ",len(solution),"\tTime:",f"{solutionTime:.4g}", "\t cumulative: " ,f"{((time.perf_counter())-startTime):.4g}")


if __name__ == "__main__":
    main()
        

# Vincent Trang, pd.4, 2023
