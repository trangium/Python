import sys; args=sys.argv[1:]

DIRECTIONS = [-9, -8, -7, -1, 1, 7, 8, 9]

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

def showBoard(board, possibleMoves):
    for idx, char in enumerate(board):
        if idx in possibleMoves: print("*", end="")
        else: print(char, end="")
        if idx%8 == 7: print()
    
def main():
    global args
    if not args or len(args[0]) == 1: args = ['.'*27 + "ox......xo" + '.'*27]
    if len(args) == 1: args += ("o" if args[0].count(".")%2 else "x")
    board = args[0].lower()
    mover = args[1].lower()
    possibleMoves = getPossibleMoves(board, mover)
    if not possibleMoves:
        print("No moves possible")
        return
    showBoard(board, possibleMoves)
    print()
    print(board, end="  ")
    print(board.count("x"), "/", board.count("o"), sep="")
    print("Possible moves for "+mover, end=": ")
    print(str(possibleMoves).replace("[", "").replace("]", ""))

if __name__ == "__main__":
    main()
    
# Vincent Trang, pd.4, 2023
