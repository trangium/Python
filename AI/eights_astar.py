import sys; args=sys.argv[1:]
import time, random

width = None
height = None
OPTIMIZE = 12/16 # 0 = completely greedy, 1 = surely optimal, 9/16 = submitted to the grader
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

def findCompactPath(start, goal, visited):
    path = ""
    while goal != start:
        prevPos = visited[goal]
        path = {-width:"U", -1:"L", 1:"R", width:"D"}[goal.index("_") - prevPos.index("_")] + path
        goal = prevPos
    return path

def h(pzl):
    dist = 0
    for idx, val in enumerate(pzl):
        if val != "_":
            dist += distanceTable[val][idx]
    return dist
            
    
def solve(start, goal):
    if not isSolvable(start, goal):
        return "X"
    visited = {start: None}
    if start == goal:
        return "G"
    unparsed = [(h(start), start, 0)]
    while unparsed:
        nextLayer = set()
        pzlData = unparsed[0]
        remove_min(unparsed)
        pzl = pzlData[1]
        for nextPzl in neighbors(pzl):
            if nextPzl not in visited:
                visited[nextPzl] = pzl
                insert(unparsed, (h(nextPzl)+OPTIMIZE*(pzlData[2]+1), nextPzl, pzlData[2]+1))
            if nextPzl == goal:
                return findCompactPath(start, goal, visited)
    return "X"

def main():
    global distanceTable
    startTime = time.perf_counter()
    goal = pzlInput[0]
    setDimensions(len(goal))
    distanceTable = {val:DISTANCES[idx] for idx, val in enumerate(goal) if val != "_"}
    print("Optimization factor: ", int(OPTIMIZE*16), "/16", sep="")
    for pzl in pzlInput:
        prevTime = time.perf_counter()
        solution = solve(pzl, goal)
        solutionTime = -prevTime+time.perf_counter()
        print(pzl, "path", solution)
        print("Length: ",len(solution),"\tTime:",f"{solutionTime:.4g}")
    
if __name__ == "__main__":
    main()

# Vincent Trang, pd.4, 2023
