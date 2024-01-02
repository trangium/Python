import sys; args=sys.argv[1:]
import time # Performance: 50s on grader

with open(args[0]) as f:
    lines = [line.strip() for line in f]

def setGlobals(pzl):
    global ALPHABET, SIZE, NBRLOOKUP, CONSTRAINTSETS, NONNBRLOOKUP
    
    ALPHABET = set(pzl) - {"."}
    if len(ALPHABET)**2 < len(pzl): ALPHABET.add(min(set("123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")-ALPHABET))
    ALPHABET = "".join(sorted(list(ALPHABET)))
        
    SIZE = len(ALPHABET)
    BOX_Y = int(SIZE**0.5)
    while SIZE%BOX_Y:
        BOX_Y -= 1
    BOX_X = SIZE // BOX_Y

    # creating the lookup tables
    rows = [set(range(SIZE*i, SIZE*(i+1))) for i in range(SIZE)]
    cols = [set(range(i, SIZE**2, SIZE)) for i in range(SIZE)]
    boxes = []
    for startingRow in range(0, SIZE, BOX_Y):
        for startingCol in range(0, SIZE, BOX_X):
            boxes.append([y*SIZE+x for x in range(startingCol, startingCol+BOX_X) for y in range(startingRow, startingRow+BOX_Y)])
    CONSTRAINTSETS = rows + cols + boxes
    NBRLOOKUP = [{pos for ln in CONSTRAINTSETS if i in ln for pos in ln if pos != i} for i in range(SIZE**2)]
    NONNBRLOOKUP = [[i for i in range(SIZE**2) if i not in NBRLOOKUP[j]] for j in range(SIZE**2)]

def isValid(pzl, index, choice):
    for pos in NBRLOOKUP[index]:
        if pzl[pos] == choice:
            return False
    return True

def getInvalids(pzl, index):
    seen = set()
    for pos in NBRLOOKUP[index]:
        if pzl[pos] != ".":
            seen.add(pzl[pos])
    return SIZE-len(seen)
    
def bruteHelper(pzl, dotsLeft):
    if dotsLeft == 0: return pzl
    minBranch = SIZE
    index = -1

    candidates = {i:bytearray(SIZE**2) for i in ALPHABET} # candidates[char][position] is 0 if [char] can be at [position], else 1

    # find the best cell to bifuricate on an n-single
    for testIndex in range(SIZE**2): 
        if pzl[testIndex] == ".":
            seen = set()
            for pos in NBRLOOKUP[testIndex]:
                if pzl[pos] != ".":
                    seen.add(pzl[pos])
                    candidates[pzl[pos]][testIndex] = 1
            branches = SIZE-len(seen)
            if branches < minBranch:
                minBranch = branches
                index = testIndex
                if branches == 0:
                    return ""
                if branches == 1:
                    break

    bestSet = set()
    bestCharacter = ""
    if minBranch > 1:
        # find candidates for h-singles
        
        for constraintSet in CONSTRAINTSETS:
            for character in ALPHABET:
                numPossibilities = SIZE
                for position in constraintSet:
                    if pzl[position] == character:
                        numPossibilities = SIZE
                        break
                    elif pzl[position] != ".": numPossibilities -= 1
                    else: numPossibilities -= candidates[character][position]
                if numPossibilities < minBranch:
                    bestSet = constraintSet
                    bestCharacter = character
                if numPossibilities == 0:
                    return ""
                if numPossibilities == 1:
                    break

    if bestCharacter:
        for idxChoice in bestSet:
            if pzl[idxChoice] == "." and not candidates[bestCharacter][idxChoice]:
                subPzl = pzl[:idxChoice] + bestCharacter + pzl[(idxChoice+1):]
                bF = bruteHelper(subPzl, dotsLeft-1)
                if bF: return bF
    else:
        for character in ALPHABET:
            if not candidates[character][index]:
                subPzl = pzl[:index] + character + pzl[(index+1):]
                bF = bruteHelper(subPzl, dotsLeft-1)
                if bF: return bF
    return ""

def bruteForce(pzl):
    for idx, val in enumerate(pzl):
        if val != ".":
            if val not in ALPHABET or not isValid(pzl, idx, val):
                return ""
    if "." not in pzl: return pzl
    return bruteHelper(pzl, pzl.count("."))

def main():
    absoluteStart = time.perf_counter()
    for idx,inp in enumerate(lines):
        numHeader = str(idx+1)+": "
        print(numHeader, end="")
        print(inp)
        start = time.perf_counter()

        setGlobals(inp)
        result = bruteForce(inp)
        
        finish = time.perf_counter()
        print(" "*len(numHeader),end="")
        print(result,end=" ")
        checksum = sum(ord(i)-ord(min(result.replace(".",""))) for i in result)
        print(checksum, end=" ")
        print(round(finish-start, 4), "s\n\n", sep="")
    print(round(time.perf_counter()-absoluteStart, 4), "s total for 128 puzzles\n\n", sep="")

def printSudoku(string):
    for idx,char in enumerate(string):
        delim = ""
        if (idx+1)%3 == 0: delim = " "
        if (idx+1)%9 == 0: delim = "\n"
        if (idx+1)%27 == 0: delim = "\n"+" "*11+"\n"
        print(char, end=delim)

if __name__ == "__main__":
    main()
    
# Vincent Trang, pd.4, 2023
