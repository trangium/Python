import sys; args=sys.argv[1:]
import re

BLOCKCHAR = "#"
OPENCHAR = "-"
PROTECTEDCHAR = "~"


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
currentBlockCount = 0
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

def printFinal(board, blockBoard):
    blockCopy = blockBoard[:]
    for index, char in enumerate(board):
        if char not in {BLOCKCHAR, OPENCHAR, PROTECTEDCHAR}:
            blockCopy[index] = board[index]
        if blockCopy[index] == PROTECTEDCHAR:
            blockCopy[index] = OPENCHAR
    printBoard(blockCopy)

def updateInd(board, pos, cell):
    global currentBlockCount
    if board[pos] == BLOCKCHAR: currentBlockCount -= 1
    board[pos] = cell
    if board[pos] == BLOCKCHAR: currentBlockCount += 1
    if board[boardSize-1-pos] == BLOCKCHAR: currentBlockCount -= 1
    board[boardSize-1-pos] = cell
    if board[boardSize-1-pos] == BLOCKCHAR: currentBlockCount += 1

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

def fillObv():
    while True:
        if not fillObvOnce(blockBoard): break

def findOpen(board, dx):
    for i in range(boardSize):
        pos = ((i+1) * dx)%boardSize
        if board[pos] == OPENCHAR:
            return pos

def isConnected(board):
    global boardCopy
    if currentBlockCount == boardSize: return True
    boardCopy = [OPENCHAR if (c != BLOCKCHAR) else BLOCKCHAR for c in board]
    connectHelper(boardCopy.index(OPENCHAR))
    return (OPENCHAR not in boardCopy)

def connectHelper(pos):
    global boardCopy
    if boardCopy[pos] != OPENCHAR: return
    boardCopy[pos] = BLOCKCHAR
    if pos >= boardWidth: connectHelper(pos-boardWidth)
    if pos < boardSize-boardWidth: connectHelper(pos+boardWidth)
    if pos%boardWidth: connectHelper(pos-1)
    if (pos+1)%boardWidth: connectHelper(pos+1)

# blockBoard filling
if blockCount == boardSize:
    blockBoard = [BLOCKCHAR for i in range(boardSize)]
    currentBlockCount = boardSize
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

dx = 1
while dx < boardSize:
    # store previous
    prevBoard = board[:]
    prevBlockBoard = blockBoard[:]
    initialBlockCount = currentBlockCount
    
    # do the filling
    fillObv()
    while currentBlockCount < blockCount:
        openPos = findOpen(blockBoard, dx)
        if openPos is None: break
        updateInd(blockBoard, openPos, BLOCKCHAR)
        fillObv()

    # check if it's valid
    if currentBlockCount == blockCount and isConnected(blockBoard): break
    else:
        board = prevBoard[:]
        blockBoard = prevBlockBoard[:]
        currentBlockCount = initialBlockCount
        dx += 1

printBoard(board)
printFinal(board, blockBoard)

# Vincent Trang, pd.4, 2023
