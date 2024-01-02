import sys; args=sys.argv[1:]
import time, random

width = None
height = None
DISTANCES = [[0,1,2,3,1,2,3,4,2,3,4,5,3,4,5,6],[1,0,1,2,2,1,2,3,3,2,3,4,4,3,4,5],[2,1,0,1,3,2,1,2,4,3,2,3,5,4,3,4],[3,2,1,0,4,3,2,1,5,4,3,2,6,5,4,3],
             [1,2,3,4,0,1,2,3,1,2,3,4,2,3,4,5],[2,1,2,3,1,0,1,2,2,1,2,3,3,2,3,4],[3,2,1,2,2,1,0,1,3,2,1,2,4,3,2,3],[4,3,2,1,3,2,1,0,4,3,2,1,5,4,3,2],
             [2,3,4,5,1,2,3,4,0,1,2,3,1,2,3,4],[3,2,3,4,2,1,2,3,1,0,1,2,2,1,2,3],[4,3,2,3,3,2,1,2,2,1,0,1,3,2,1,2],[5,4,3,2,4,3,2,1,3,2,1,0,4,3,2,1],
             [3,4,5,6,2,3,4,5,1,2,3,4,0,1,2,3],[4,3,4,5,3,2,3,4,2,1,2,3,1,0,1,2],[5,4,3,4,4,3,2,3,3,2,1,2,2,1,0,1],[6,5,4,3,5,4,3,2,4,3,2,1,3,2,1,0]]
distanceTable = {}
UNDERSCORE = 95 # ord("_")

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
    return parity(start, goal) == (holeParity[start.index(UNDERSCORE)] == holeParity[goal.index(UNDERSCORE)])
    
def swapChars(string, index1, index2):
    return bytes(string[index2] if x==index1 else string[x] if x!=index2 else string[index1] for x in range(len(string)))

def findCompactPath(start, goal, visited):
    path = ""
    holePos = goal.index(UNDERSCORE)
    while goal != start:
        if visited[goal] == 0:
            path = "U" + path
            newPos = holePos+width
        if visited[goal] == 2:
            path = "D" + path
            newPos = holePos-width
        if visited[goal] == 3:
            path = "L" + path
            newPos = holePos+1
        if visited[goal] == 1:
            path = "R" + path
            newPos = holePos-1
        goal = swapChars(goal, holePos, newPos)
        
        holePos = newPos
    return path if path else "G"

def h(pzl):
    dist = 0
    for idx, val in enumerate(pzl):
        if val != UNDERSCORE:
            dist += distanceTable[val][idx]
    return dist
            

def processNbr(openSet, min_f, pzl, holePos, posFrom, direc):
    nbr = swapChars(pzl, holePos, posFrom)
    newF = min_f - distanceTable[nbr[holePos]][posFrom] + distanceTable[nbr[holePos]][holePos] + 1
    openSet[newF].append((nbr, direc))

def aStar(root, goal):
    if not isSolvable(root, goal): return "X"
    openSet = [[] for i in range(160)] # each index contains all (pzl, f) in openSet with f = index
    openSet[h(root)].append((root, None))
    min_f = h(root)
    closedSet = {} # empty dict with key = pzl, val = most recent direction of hole movement

    while True:
        while not openSet[min_f]:
            min_f += 1
        pzl, direc = openSet[min_f].pop()
        if pzl in closedSet: continue
        closedSet[pzl] = direc # 0 = up, 1 = right, 2 = down, 3 = left
        if pzl == goal: return findCompactPath(root, goal, closedSet)
        
        holePos = pzl.index(UNDERSCORE)
        if direc != 2 and holePos >= width:
            processNbr(openSet, min_f, pzl, holePos, holePos-width, 0)
        if direc != 0 and holePos < width*height-width:
            processNbr(openSet, min_f, pzl, holePos, holePos+width, 2)
        if direc != 1 and holePos%width:
            processNbr(openSet, min_f, pzl, holePos, holePos-1, 3)
        if direc != 3 and (holePos+1)%width:
            processNbr(openSet, min_f, pzl, holePos, holePos+1, 1)

def main():
    global distanceTable
    startTime = time.perf_counter()
    goal = bytes(pzlInput[0], "utf-8") # puzzles are represented as a bytes[16] object 
    setDimensions(len(goal))
    distanceTable = {val:DISTANCES[idx] for idx, val in enumerate(goal) if val != "_"}
    for pzl in pzlInput:
        prevTime = time.perf_counter()
        solution = aStar(bytes(pzl, "utf-8"), goal)
        solutionTime = -prevTime+time.perf_counter()
        print(pzl, "path", solution)
        print("Length: ",len(solution),"\tTime:",f"{solutionTime:.4g}", "\t cumulative: " ,f"{((time.perf_counter())-startTime):.4g}")


if __name__ == "__main__":
    main()
        

# Vincent Trang, pd.4, 2023
