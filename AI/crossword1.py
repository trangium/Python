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

board = [OPENCHAR for i in range(boardWidth*boardHeight)]
for wordInfo in wordsToPlace:
    word, x, y, dx, dy = wordInfo
    for char in word:
        board[y*boardWidth+x] = char
        x += dx
        y += dy

boardCopy = board
while boardCopy:
    row, boardCopy = boardCopy[:boardWidth], boardCopy[boardWidth:]
    print(" ".join(row).upper())
        
        

# Vincent Trang, pd.4, 2023
