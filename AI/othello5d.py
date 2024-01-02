import sys; args=sys.argv[1:]
import random, time

DIRECTIONS = [-9, -8, -7, -1, 1, 7, 8, 9]
TOKENINVERSE = {"o":"x", "x":"o"}
TOKENSCALE = {"x":1, "o":-1, "": 1}
ROWRANGES = [(i, i+8, 1) for i in range(0, 64, 8)] + \
            [(i, i+64, 8) for i in range(8)] + \
            [(i, 64-8*i, 9) for i in range(8)] + \
            [(i, 64, 9) for i in range(8, 64, 8)] + \
            [(i, 8*i+1, 7) for i in range(8)] + \
            [(i, 63, 7) for i in range(7, 64, 8)]
POSTYPE = [0, 1, 2, 3, 3, 2, 1, 0,
           1, 4, 5, 6, 6, 5, 4, 1,
           2, 5, 7, 8, 8, 7, 5, 2,
           3, 6, 8, 9, 9, 8, 6, 3,
           3, 6, 8, 9, 9, 8, 6, 3,
           2, 5, 7, 8, 8, 7, 5, 2,
           1, 4, 5, 6, 6, 5, 4, 1,
           0, 1, 2, 3, 3, 2, 1, 0]

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

def quickPossibleMoves(board, mover, dotSet):
    acc = []
    for pos in dotSet:
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

def makeMove(board, pos, mover, dotSet):
    newBoard = boardOnMove(board, pos, mover)
    oppMoves = quickPossibleMoves(newBoard, TOKENINVERSE[mover], dotSet)
    newDots = dotSet - {pos}
    if oppMoves: return newBoard, TOKENINVERSE[mover], oppMoves, dotSet
    yourMoves = quickPossibleMoves(newBoard, mover, dotSet)
    if yourMoves:
        return newBoard, mover, yourMoves, dotSet
    return newBoard, "", yourMoves, set()

cache = {}
cacheHits = 0
cacheMisses = 0

def negamaxHelper(board, mover, possibleMoves, dotSet, lowerBound, upperBound):
    global cacheHits, cacheMisses
    # returns list [score, lastMove, last2Move, last3Move, ...]
    if (board, mover) in cache:
        cacheHits += 1
        return cache[(board, mover)]
    cacheMisses += 1
    if not mover: return [board.count("x") - board.count("o")]
    enemyToken = TOKENINVERSE[mover]
    bestSoFar = [-65*TOKENSCALE[mover]]
    for pos in possibleMoves:
        moveInfo = makeMove(board, pos, mover, dotSet)
        if moveInfo[1] == mover: mm = negamaxHelper(*moveInfo, -65, 65)
        elif mover == "x": mm = negamaxHelper(*moveInfo, bestSoFar[0], 65)
        else: mm = negamaxHelper(*moveInfo, -65, bestSoFar[0])
        if (mm[0] - bestSoFar[0])*TOKENSCALE[mover] > 0:
            bestSoFar = mm + [pos]
            if not (lowerBound < mm[0] < upperBound): return bestSoFar 
    cache[(board, mover)] = bestSoFar
    return bestSoFar

def negamax(board, mover):
    mm = negamaxHelper(board, mover, getPossibleMoves(board, mover), {i for i in range(64) if board[i] == "."}, -65, 65)[:]
    mm[0] *= TOKENSCALE[mover]
    return mm


# If we're on the top level, and we encounter any list that's better than what we've found before, PRINT IT.
# If we have duplicate calls, DON'T REPEAT COMPUTATION.
# If you're at level 2 or 3 and you're about to time out, PRINT A LIST and GUESS the last (first) indices. Set a cache!


def getSafeSpots(board, mover):
    acc = set()
    for (startPos, direc) in [(0, 1), (0, 8), (7, -1), (7, 8), (56, -8), (56, 1), (63, -8), (63, -1)]:
        pos = startPos
        steps = 0
        switch = False
        while (board[pos] == mover and switch == False) or (board[pos] == TOKENINVERSE[mover] and switch == True) :
            pos += direc
            steps += 1
            if steps == 7: break
            if board[pos] == TOKENINVERSE[mover]: switch = True
        if board[pos] == ".":
            acc.add(pos)
    return acc

def moveScore(board, mover, pos, dotCt=60):
    penalty = 0
    if pos in getSafeSpots(board, mover): penalty -= 128000 # "corner"
    if POSTYPE[pos] == 2: penalty -= 1 # two away from edge
    if POSTYPE[pos] == 4: penalty += 1 # diagonal from edge
    if POSTYPE[pos] == 5: penalty -= 1 # knight's move away from edge
    newBoard = boardOnMove(board, pos, mover)

    oppMoves = getPossibleMoves(newBoard, TOKENINVERSE[mover])
    safeSpots = getSafeSpots(newBoard, TOKENINVERSE[mover])
    for pos in oppMoves:
        if pos in safeSpots:
            penalty += 5000
        elif POSTYPE[pos] == 1: penalty -= 2
    return -len(oppMoves) - penalty*(dotCt >= 11)


def quickMove(board, mover):
    global cache
    dotCt = board.count(".")
    if dotCt < 11:
        return negamax(board, mover)[-1]
    possibleMoves = getPossibleMoves(board, mover)
    prefMove = max(possibleMoves, key=(lambda pos: (moveScore(board, mover, pos, dotCt), pos)))
    return prefMove

def testRand(count=500):
    startTime = time.perf_counter()
    yourTokens = 0
    oppTokens = 0
    for i in range(count):
        board = '.'*27 + "ox......xo" + '.'*27
        yourMover = "x" if i%2 else "o"
        mover = "x" # always x
        while True:
            possibleMoves = getPossibleMoves(board, mover)
            if not possibleMoves:
                mover = TOKENINVERSE[mover]
                possibleMoves = getPossibleMoves(board, mover)
                if not possibleMoves: break
            if mover == yourMover:
                prefMove = quickMove(board, mover)
            else:
                prefMove = random.choice(list(possibleMoves))
            board = boardOnMove(board, prefMove, mover)
            mover = TOKENINVERSE[mover]
        yourTokens += board.count(yourMover)
        oppTokens += board.count(TOKENINVERSE[yourMover])
        if (i and not (i+1)%10) or (i == count):
            print(f"{100 * yourTokens / (yourTokens + oppTokens):.2f}%  ",i+1,"/",count,sep="")
    print(f"\nTime: {time.perf_counter()-startTime:.2f}s")

def showBoard(board, possibleMoves, mover, recentMove=-1):
    for idx, char in enumerate(board):
        if idx in possibleMoves: print("*", end="")
        elif idx == recentMove: print(char.upper(), end="")
        else: print(char, end="")
        if idx%8 == 7: print()
    print()
    print(board, end="  ")
    print(board.count("x"), "/", board.count("o"), sep="")
    if not possibleMoves: print("No moves possible")
    else: print("Possible moves for "+mover, end=": ")
    print(str(sorted(possibleMoves)).replace("[", "").replace("]", ""))
    
def main():
    board = '.'*27 + "ox......xo" + '.'*27
    mover = None
    moveStack = []
    for arg in args[::-1]:
        if arg in "XxOo": mover = arg
        # elif len(arg) <= 2: moveStack.append("abcdefgh".find(arg[0].lower())+8*int(arg[1])-8 if arg[0].lower() in "abcdefgh" else int(arg))
        elif len(arg) == 64 and ("." in arg or "x" in arg.lower() or "o" in arg.lower()): board = arg.lower()
        else:
            condensed = arg
            while condensed:
                moveStr = condensed[-2:]
                condensed = condensed[:-2]
                moveStack.append(int(moveStr.replace("_","")))
    moveStack = [i for i in moveStack if i >= 0]

    if mover is None: mover = "o" if board.count(".")%2 else "x"

    recentMove = -1
    while True:
        possibleMoves = getPossibleMoves(board, mover)
        if not possibleMoves:
            mover = TOKENINVERSE[mover]
            possibleMoves = getPossibleMoves(board, mover)
        showBoard(board, possibleMoves, mover, recentMove)
        if not moveStack: break
        print("\n"+mover,"plays to",moveStack[-1])
        recentMove = moveStack[-1]
        board = boardOnMove(board, moveStack.pop(), mover)
        mover = TOKENINVERSE[mover]

    if possibleMoves:
        prefMove = quickMove(board, mover)
        print(f"My preferred move is: {prefMove}")

    if board.count(".") < 11:
        mm = negamax(board, mover)
        print(f"Min score: {mm[0]}; move sequence: {mm[1:]}")

if __name__ == "__main__":
    main()
    
# Vincent Trang, pd.4, 2023
