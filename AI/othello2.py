import sys; args=sys.argv[1:]

DIRECTIONS = [-9, -8, -7, -1, 1, 7, 8, 9]
TOKENINVERSE = {"o":"x", "x":"o"}

def isValidDirection(board, mover, pos, direction):
    seenOppTokens = False
    pos += direction
    if {pos%8, (pos-direction)%8} == {0, 7}: return False
    while 0 <= pos < 64:
        if board[pos] == ".": return False
        elif board[pos] == mover: return seenOppTokens
        else: seenOppTokens = True
        pos += direction
        if {pos%8, (pos-direction)%8} == {0, 7}: return False
    return False

def isValidMove(board, mover, pos):
    if board[pos] != ".": return False
    for d in DIRECTIONS:
        if isValidDirection(board, mover, pos, d): return True
    return False

def getPossibleMoves(board, mover):
    acc = []
    for pos in range(64):
        if isValidMove(board, mover, pos):
            acc.append(pos)
    return acc

def boardOnMove(board, movePos, mover):
    flipTokens = set()
    for direction in DIRECTIONS:
        potentialFlips = set()
        pos = movePos + direction
        if {pos%8, (pos-direction)%8} == {0, 7}: continue
        while 0 <= pos < 64:
            if board[pos] == ".": break
            elif board[pos] == mover:
                flipTokens |= potentialFlips
                break
            else: potentialFlips.add(pos)
            pos += direction
            if {pos%8, (pos-direction)%8} == {0, 7}: break
    return "".join((mover if idx == movePos else TOKENINVERSE[val] if idx in flipTokens else val) for idx, val in enumerate(board))

def showBoard(board, possibleMoves, mover):
    for idx, char in enumerate(board):
        if idx in possibleMoves: print("*", end="")
        else: print(char, end="")
        if idx%8 == 7: print()
    print()
    print(board, end="  ")
    print(board.count("x"), "/", board.count("o"), sep="")
    if not possibleMoves: print("No moves possible")
    else: print("Possible moves for "+mover, end=": ")
    print(str(possibleMoves).replace("[", "").replace("]", ""))
    
def main():
    revArgs = [i for i in args[::-1] if i]
    if not revArgs or len(revArgs[-1]) != 64: revArgs.append('.'*27 + "ox......xo" + '.'*27)
    board = revArgs[-1].lower()
    revArgs.pop()
    if not revArgs or revArgs[-1] not in "XxOo": revArgs.append("o" if board.count(".")%2 else "x")
    mover = revArgs[-1].lower()
    revArgs.pop()
    moveStack = list(filter(lambda x: (x >= 0), map(lambda moveStr: ("abcdefgh".find(moveStr[0].lower())+8*int(moveStr[1])-8 if moveStr[0].lower() in "abcdefgh" else int(moveStr)), revArgs)))

    while True:
        possibleMoves = getPossibleMoves(board, mover)
        if not possibleMoves:
            mover = TOKENINVERSE[mover]
            possibleMoves = getPossibleMoves(board, mover)
        showBoard(board, possibleMoves, mover)
        if not moveStack: break
        print("\n"+mover,"plays to",moveStack[-1])
        board = boardOnMove(board, moveStack.pop(), mover)
        mover = TOKENINVERSE[mover]


if __name__ == "__main__":
    main()
    
# Vincent Trang, pd.4, 2023
