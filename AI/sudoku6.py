import sys; args=sys.argv[1:]
import time # Performance: 32s on grader

with open(args[0]) as f:
    lines = [line.strip() for line in f]

def setGlobals(pzl):
    global ALPHABET, SIZE, NBRLOOKUP, CONSTRAINTSETS
    
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

def getExhaustiveSet(pzl, dotsLeft, prevIndex):
    exhaustiveSet = []
    candidates = {i:bytearray(SIZE**2) for i in ALPHABET} # candidates[char][position] is 0 if [char] can be at [position], else 1

    while True:
        if dotsLeft == 0: return [(pzl, 0, 0)]
        minBranch = SIZE
        index = -1
        uniqueNext = False
        
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
                        return exhaustiveSet
                    if branches == 1:
                        uniqueNext = True
                        break
                if uniqueNext:
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
                        return exhaustiveSet
                    if numPossibilities == 1:
                        uniqueNext = True
                        break
                if uniqueNext:
                    break

        choices = []  # (index, char)
        if bestCharacter:
            for idxChoice in bestSet:
                if pzl[idxChoice] == "." and not candidates[bestCharacter][idxChoice]:
                    choices.append((idxChoice, bestCharacter))
        else:
            for character in ALPHABET:
                if not candidates[character][index]:
                    choices.append((index, character))

        mainIndex, mainChar = choices.pop()
        for index, character in choices:
            exhaustiveSet.append((pzl[:index] + character + pzl[(index+1):], dotsLeft-1, index))

        # Applying the main choice! TODO: Update the constraint set here. This will make it WAY more efficient.
        pzl = pzl[:mainIndex] + mainChar + pzl[(mainIndex+1):]
        dotsLeft -= 1
        prevIndex = mainIndex
    
def bruteHelper(pzl, dotsLeft, prevIndex):
    if dotsLeft == 0: return pzl
    for subPzl, dotsLeft, prevIndex in getExhaustiveSet(pzl, dotsLeft, prevIndex):
        bF = bruteHelper(subPzl, dotsLeft, prevIndex)
        if bF: return bF
    return ""
            
def bruteForce(pzl):
    for idx, val in enumerate(pzl):
        if val != ".":
            if val not in ALPHABET or not isValid(pzl, idx, val):
                return ""
    if "." not in pzl: return pzl
    return bruteHelper(pzl, pzl.count("."), 0)

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
    print(round(time.perf_counter()-absoluteStart, 4),"s total for ",len(lines)," puzzles\n\n", sep="")

def timing(startingPzl=0, endingPzl=None):
    absoluteStart = time.perf_counter()
    for idx,inp in enumerate(lines[startingPzl:endingPzl]):
        setGlobals(inp)
        bruteForce(inp)
    print(round(time.perf_counter()-absoluteStart, 4),"s total for ",len(lines)," puzzles\n\n", sep="")

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
