import sys; args=sys.argv[1:]
import time # Performance: 18s on PC, 23s on grader

with open(args[0]) as f:
    lines = [line.strip() for line in f]

def setGlobals(pzl):
    global ALPHABETSET, ALPHABET, SIZE, NBRLOOKUP, CONSTRAINTSETS, ITERLOOKUP, CONSTRMEMBERS
    
    ALPHABETSET = set(pzl) - {"."}
    if len(ALPHABETSET)**2 < len(pzl): ALPHABETSET.add(min(set("123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")-ALPHABETSET))
    ALPHABET = "".join(sorted(list(ALPHABETSET)))
        
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
    CONSTRMEMBERS = [{idx for idx,cset in enumerate(CONSTRAINTSETS) if j in cset} for j in range(SIZE**2)]
    NBRLOOKUP = [{pos for ln in CONSTRAINTSETS if i in ln for pos in ln if pos != i} for i in range(SIZE**2)]
    ITERLOOKUP = [[i for i in range(j, SIZE**2)] + [i for i in range(0, j)] for j in range(SIZE**2)]

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
        
def getCandidatesTable(pzl):
    # candidatesTable[position] is a set of all chars that could go in that spot
    candidatesTable = [set() for i in range(SIZE**2)]
    for testIndex in range(SIZE**2): 
        if pzl[testIndex] == ".":
            ruledOut = set()
            for pos in NBRLOOKUP[testIndex]:
                if pzl[pos] != ".":
                    ruledOut.add(pzl[pos])
            candidatesTable[testIndex] = ALPHABETSET - ruledOut
    return candidatesTable

def getHiddenCounts(pzl, candidatesTable):
    # hiddenCounts[char][constraintIdx] = number of places to put char in that constraint set
    #                                   = SIZE+1 if already filled
    hiddenCounts = {character:[SIZE+1 for i in range(len(CONSTRAINTSETS))] for character in ALPHABET}
    for constraintIdx, constraintSet in enumerate(CONSTRAINTSETS):
        for character in ALPHABET:
            numPositions = SIZE
            for position in constraintSet:
                if pzl[position] == character:
                    numPositions = -1
                    break
                elif pzl[position] != "." or character not in candidatesTable[position]:
                    numPositions -= 1
            if numPositions >= 0:
                hiddenCounts[character][constraintIdx] = numPositions
    return hiddenCounts
                
def updateTables(mainIndex, mainChar, candidatesTable, hiddenCounts):
    for nbr in NBRLOOKUP[mainIndex]:
        if mainChar in candidatesTable[nbr]:
            candidatesTable[nbr].remove(mainChar)
            for constrIdx in CONSTRMEMBERS[nbr]:
                hiddenCounts[mainChar][constrIdx] -= 1

    for char in candidatesTable[mainIndex]:
        for constrIdx in CONSTRMEMBERS[mainIndex]:
            hiddenCounts[char][constrIdx] -= 1
            
    candidatesTable[mainIndex] = set()
    for constrIdx in CONSTRMEMBERS[mainIndex]:
        hiddenCounts[mainChar][constrIdx] = SIZE+1
        
def bruteHelper(pzl, dotsLeft, prevIndex):
    exhaustiveSet = []
    candidatesTable = getCandidatesTable(pzl)
    hiddenCounts = getHiddenCounts(pzl, candidatesTable)

    while True:
        if dotsLeft == 0: return pzl
        index = -1
        uniqueNext = False


        # find the best index to bifuricate on the value of a single cell
        minBranch = SIZE
        for testIndex in ITERLOOKUP[prevIndex]:
            if pzl[testIndex] == ".":
                if len(candidatesTable[testIndex]) < minBranch:
                    minBranch = len(candidatesTable[testIndex])
                    index = testIndex
                    if minBranch <= 1: break

        # find the best constraint set to bifuricate on the position of a value
        bestSet = set()
        bestCharacter = ""
        if minBranch > 1:
            for character, ctList in hiddenCounts.items():
                for constraintIdx, numPositions in enumerate(ctList):
                    if numPositions < minBranch:
                        bestCharacter, setIdx = character, constraintIdx
                        minBranch = numPositions
                        bestSet = CONSTRAINTSETS[setIdx]
                        break
                    if minBranch <= 1: break
                if minBranch <= 1: break

        if minBranch == 0: return ""

        choices = []  # (index, char)
        if bestCharacter:
            for idxChoice in bestSet:
                if pzl[idxChoice] == "." and bestCharacter in candidatesTable[idxChoice]:
                    choices.append((idxChoice, bestCharacter))
        else:
            for character in ALPHABET:
                if character in candidatesTable[index]:
                    choices.append((index, character))

        mainIndex, mainChar = choices.pop()
        for index, character in choices:
            bF = bruteHelper(pzl[:index] + character + pzl[(index+1):], dotsLeft-1, index)
            if bF: return bF

        # Applying the main choice! Update the candidates table here
        pzl = pzl[:mainIndex] + mainChar + pzl[(mainIndex+1):]
        updateTables(mainIndex, mainChar, candidatesTable, hiddenCounts)
                    
        dotsLeft -= 1
        prevIndex = mainIndex
            
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
