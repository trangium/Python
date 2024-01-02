import sys; args=sys.argv[1:]
import time

STATS = {"auto-reject":0}
def updateStats(name):
    global STATS
    STATS[name] = STATS[name]+1

def placeable(gridState, gridPos, blockX, blockY, dX, dY):
    for x in range(0, blockX*dX, dX):
        for y in range(0, blockY*dY, dY):
            if gridState[gridPos+x+y*gridX] == "#":
                return False
    return True

def placeOnGrid(gridState, gridPos, blockX, blockY, dX, dY):
    return "".join("#" if idx%gridX in range(gridPos%gridX, gridPos%gridX+blockX*dX, dX) and idx//gridX in range(gridPos//gridX, gridPos//gridX+blockY*dY, dY) else c for idx, c in enumerate(gridState))

def getChoices(gridState, unplacedBlocks):
    # printGrid(gridState)
    minBranch = gridX*gridY
    bestPos = -1
    bestChoices = []
    for gridPos in range(gridX*gridY):
        if gridState[gridPos] == ".":
            leftFilled = (gridState[gridPos-1] == "#")
            rightFilled = (gridState[gridPos+1] == "#")
            dX = -1 if rightFilled else 1 if leftFilled else 0
            topFilled = (gridState[gridPos-gridX] == "#")
            bottomFilled = (gridState[gridPos+gridX] == "#")
            dY = -1 if bottomFilled else 1 if topFilled else 0
            if dX and dY:
                choices = []
                for blockX, blockY in set(unplacedBlocks):
                    if placeable(gridState, gridPos, blockX, blockY, dX, dY):
                        choices.append((blockX, blockY))
                    if blockX != blockY and placeable(gridState, gridPos, blockY, blockX, dX, dY):
                        choices.append((blockY, blockX))
                # print(gridPos, dX, dY, len(choices))
                if len(choices) < minBranch:
                    minBranch = len(choices)
                    bestPos = gridPos
                    bestChoices = choices
                    bestdX = dX
                    bestdY = dY
    return bestPos, bestChoices, bestdX, bestdY


visited = {} # gridState : prevState
def bruteForce(pzlData):
    # pzlData = gridState (str), unplacedBlocks (tuple of 2-tuples)
    gridState, unplacedBlocks = pzlData
    if not unplacedBlocks: return getSolution(pzlData)
    bestPos, bestChoices, bestdX, bestdY = getChoices(gridState, unplacedBlocks)
    for blockX, blockY in bestChoices:
        newGridState = placeOnGrid(gridState, bestPos, blockX, blockY, bestdX, bestdY)
        blockIdx = unplacedBlocks.index((min(blockX, blockY), max(blockX, blockY)))
        newUnplacedBlocks = unplacedBlocks[:blockIdx] + unplacedBlocks[blockIdx+1:]
        newPzlData = (newGridState, newUnplacedBlocks)
        if newPzlData not in visited:
            visited[newPzlData] = pzlData
            if len(visited) in [25, 50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 51200]:
                print("visited:", len(visited), "  |  rejects:", STATS["auto-reject"])
            r = bruteForce(newPzlData)
            if r: return r
        else:
            updateStats("auto-reject")
    return False

def getSolution(pzlData):
    solution = []
    while pzlData in visited:
        # print()
        # printGrid(pzlData[0])
        topLeft = 0
        while pzlData[0][topLeft] == visited[pzlData][0][topLeft]: topLeft += 1
        bottomRight = gridX*gridY-1
        while pzlData[0][bottomRight] == visited[pzlData][0][bottomRight]: bottomRight -= 1
        blockX, blockY = ((bottomRight-topLeft) // gridX + 1, (bottomRight-topLeft) % gridX + 1)
        solution.append((topLeft, str(blockX)+"x"+str(blockY)))
        pzlData = visited[pzlData]
    return [block for pos, block in sorted(solution)]
        
def main():
    global gridX, gridY
    blockDimens = []
    for arg in args:
        exhaust = arg
        res = ""
        while exhaust:
            res += exhaust[0]
            exhaust = exhaust[1:]
            if res[-1] not in "0123456789":
                blockDimens.append(int(res[:-1]))
                res = ""
        if res: blockDimens.append(int(res))
    blocks = []
    totalArea = 0
    for i in range(0, len(blockDimens), 2):
        bX, bY = blockDimens[i], blockDimens[i+1]
        if i:
            totalArea += bX*bY
            blocks.append(tuple(sorted((bX, bY))))
        else:
            gridY, gridX = bX, bY
    while totalArea < gridX*gridY:
        blocks.append((1, 1))
        totalArea += 1
    print(gridY, "by", gridX)
    gridX += 2 # padding
    gridY += 2 # padding
    emptyPzl = "".join("#" if (x==0 or x==gridX-1 or y==0 or y==gridY-1) else "." for y in range(gridY) for x in range(gridX))
    pzlData = (emptyPzl, tuple(sorted(blocks, reverse=True)))
    print(pzlData[1])
    solution = bruteForce(pzlData)
    if solution: print("Decomposition:", " ".join(solution))
    else: print("No Solution")
    print("len(visited) =", len(visited))

def printGrid(grid):
    while grid:
        print(grid[:gridX])
        grid = grid[gridX:]

if __name__ == "__main__":
    main()
    
# Vincent Trang, pd.4, 2023
