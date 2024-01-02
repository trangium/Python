import sys; args=sys.argv[1:]
import re, random

BLOCKCHAR = "#"
OPENCHAR = "-"
PROTECTEDCHAR = "~"

# big test: 15x15 37 H0x4# v4x0# h1x12a
wordListFile = None
blockCount = None
boardHeight = None
boardWidth = None

wordsToPlace = [] # each elem is (word, x, y, dx, dy)

for arg in args:
    argl = arg.lower()
    if len(arg) > 4 and arg[-4:] == ".txt": # word list
        wordListFile = arg
    elif arg.isdigit(): # block count
        blockCount = int(arg)
    elif arg[0].isdigit(): # board size
        boardHeight, boardWidth = map(int, argl.split("x"))
    else:
        if argl[0] == "v": dx, dy = 0, 1
        else: dx, dy = 1, 0
        y, x = map(int, re.findall("\d+", argl))
        word = argl[re.search("\d+x\d+", argl).span()[1]:]
        wordsToPlace.append((word, x, y, dx, dy))

boardSize = boardWidth*boardHeight
board = [OPENCHAR for i in range(boardSize)]
for wordInfo in wordsToPlace:
    word, x, y, dx, dy = wordInfo
    for char in word:
        board[y*boardWidth+x] = char.upper()
        x += dx
        y += dy

def printBoard(board):
    boardCopy = board[:]
    while boardCopy:
        row, boardCopy = boardCopy[:boardWidth], boardCopy[boardWidth:]
        print(" ".join(row))
    print()

def getFinal(board, blockBoard):
    blockCopy = blockBoard[:]
    for index, char in enumerate(board):
        if char not in {BLOCKCHAR, OPENCHAR, PROTECTEDCHAR}:
            blockCopy[index] = board[index]
        if blockCopy[index] == PROTECTEDCHAR:
            blockCopy[index] = OPENCHAR
    return blockCopy

def printFinal(board, blockBoard):
    printBoard(getFinal(board, blockBoard))

def updateInd(board, pos, cell):
    board[pos] = cell
    board[boardSize-1-pos] = cell

def update(board, row, col, cell):
    updateInd(board, row*boardWidth+col, cell)

def get(board, row, col):
    return board[row*boardWidth+col]

def getRow(board, index):
    return board[index*boardWidth:(index+1)*boardWidth]

def getRowPad(board, index):
    return [BLOCKCHAR] + board[index*boardWidth:(index+1)*boardWidth] + [BLOCKCHAR]

def getCol(board, index):
    return board[index:boardSize:boardWidth]

def getColPad(board, index):
    return [BLOCKCHAR] + board[index:boardSize:boardWidth] + [BLOCKCHAR]

def fillRow(board, index):
    row = getRow(board, index) + [BLOCKCHAR]
    colIndex = 0
    recentBlockedCol = -1
    while colIndex < len(row):
        if row[colIndex] == BLOCKCHAR:
            if colIndex - recentBlockedCol <= 3:
                for col in range(recentBlockedCol+1, colIndex):
                    update(board, index, col, BLOCKCHAR)
            recentBlockedCol = colIndex
        if colIndex >= 1 and recentBlockedCol == colIndex-2 and row[colIndex-1] == PROTECTEDCHAR:
            update(board, index, colIndex, PROTECTEDCHAR)
        if colIndex >= 2 and recentBlockedCol == colIndex-3 and row[colIndex-1] == PROTECTEDCHAR:
            update(board, index, colIndex, PROTECTEDCHAR)
        colIndex += 1

def fillCol(board, index):
    col = getCol(board, index) + [BLOCKCHAR]
    rowIndex = 0
    recentBlockedRow = -1
    while rowIndex < len(col):
        if col[rowIndex] == BLOCKCHAR:
            if rowIndex - recentBlockedRow <= 3:
                for row in range(recentBlockedRow+1, rowIndex):
                    update(board, row, index, BLOCKCHAR)
            recentBlockedRow = rowIndex
        if rowIndex >= 1 and recentBlockedRow == rowIndex-2 and col[rowIndex-1] == PROTECTEDCHAR:
            update(board, rowIndex, index, PROTECTEDCHAR)
        if rowIndex >= 2 and recentBlockedRow == rowIndex-3 and col[rowIndex-1] == PROTECTEDCHAR:
            update(board, rowIndex, index, PROTECTEDCHAR)
        rowIndex += 1

def fillObvOnce(board):
    oldBoard = board[:]
    for i in range(boardWidth): fillCol(board, i)
    for j in range(boardHeight): fillRow(board, j)
    return (board != oldBoard)

def fillObv(blockBoard):
    while True:
        if not fillObvOnce(blockBoard): break

def findOpen(board, dx):
    for i in range(boardSize):
        pos = (i+dx)%boardSize
        if board[pos] == OPENCHAR:
            return pos

def isConnected(board):
    global boardCopy
    boardCopy = board[:]
    if OPENCHAR not in boardCopy: return True
    boardCopy = [OPENCHAR if (c != BLOCKCHAR) else BLOCKCHAR for c in board]
    connectHelper(boardCopy.index(OPENCHAR))
    return (OPENCHAR not in boardCopy)

def neighbors(pos):
    if pos >= boardWidth: yield (pos-boardWidth)
    if pos < boardSize-boardWidth: yield (pos+boardWidth)
    if pos%boardWidth: yield (pos-1)
    if (pos+1)%boardWidth: yield (pos+1)

def connectHelper(pos):
    global boardCopy
    if boardCopy[pos] != OPENCHAR: return
    boardCopy[pos] = BLOCKCHAR
    for nbrPos in neighbors(pos):
        connectHelper(nbrPos)

def longestOpen(boardRow):
    record = 0
    current = 0
    for char in (boardRow + [BLOCKCHAR]):
        if char == OPENCHAR:
            current += 1
        elif char == BLOCKCHAR:
            record = max(record, current)
            current = 0
    return record

def goodness(row):
    count = 0
    counts = set()
    for cell in row:
        if cell == BLOCKCHAR:
            if count: counts.add(count)
            count = 0
        else:
            count += 1
    counts.add(count)
    good = 0
    for n in counts:
        if n <= 6: good += [0, 0, 0, 5, 3, 0, -9][n]
        else: good -= 6*(n-5)**2
    return good

def fullGoodness(board):
    if board.count(BLOCKCHAR) > blockCount or not isConnected(board): return -10000000
    good = 0
    for row in range(boardHeight):
        boardRow = board[(row*boardWidth):(row*boardWidth+boardWidth)]
        good += goodness(boardRow)
    for col in range(boardWidth):
        boardCol = board[col:boardSize:boardWidth]
        good += goodness(boardCol)
    return good

def weightedRand(board):
    nbrPenalty = 10
    openness = 1
    gamma = lambda x: 1 if x<13 else 100

    weightArray = [1.0 for i in range(boardSize)]
    for row in range(boardHeight):
        boardRow = board[(row*boardWidth):(row*boardWidth+boardWidth)]
        for col in range(boardWidth):
            boardCol = board[col:boardSize:boardWidth]
            currentGood = goodness(boardRow) + goodness(boardCol)
            boardRow[col] = BLOCKCHAR
            boardCol[row] = BLOCKCHAR
            nextGood = goodness(boardRow) + goodness(boardCol)
            weightArray[row*boardWidth+col] = max(1, (nextGood-currentGood))**0.6 if board[row*boardWidth+col] != BLOCKCHAR else 0
            
    return random.choices(range(boardSize), weights=weightArray)[0]

# blockBoard filling
if blockCount == boardSize:
    blockBoard = [BLOCKCHAR for i in range(boardSize)]
else: blockBoard = [OPENCHAR for i in range(boardSize)]
for i in range(boardSize):
    if board[i] == BLOCKCHAR: updateInd(blockBoard, i, BLOCKCHAR)
    elif board[i] != OPENCHAR: updateInd(blockBoard, i, PROTECTEDCHAR)

# middle cell
if boardSize%2 == 1:
    if blockCount%2 == 0:
        updateInd(blockBoard, boardSize//2, PROTECTEDCHAR)
    else:
        updateInd(blockBoard, boardSize//2, BLOCKCHAR)

def fillOnce(blockBoard):
    openPos = findOpen(blockBoard, weightedRand(blockBoard))
    if openPos is None: return
    updateInd(blockBoard, openPos, BLOCKCHAR)
    fillObv(blockBoard)

    
fillObv(blockBoard)
pareto = [(blockBoard, fullGoodness(blockBoard), blockBoard.count(BLOCKCHAR))]

for i in range(10*boardSize):
    nextBoard = random.choice(pareto)[0][:]
    fillOnce(nextBoard)
    nextGoodness = fullGoodness(nextBoard)
    nextBlocks = nextBoard.count(BLOCKCHAR)
    if nextBlocks > blockCount: continue
    nextOptimality = True
    for elem in pareto:
        if elem[1] <= nextGoodness and elem[2] == nextBlocks: # elem is strictly worse than the new board
            pareto.remove(elem)
        if elem[1] >= nextGoodness + boardSize/(50*random.random()) and elem[2] == nextBlocks: # elem is strictly better than the new board
            nextOptimality = False
    if nextOptimality: pareto.append((nextBoard, nextGoodness, nextBlocks))

for brd, score, blocks in pareto:
    if blocks == blockCount: break

printFinal(board, brd)
print(score, blocks, "\n\n")


# Vincent Trang, pd.4, 2023
