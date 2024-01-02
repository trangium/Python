import sys; args=sys.argv[1:]
import time # Performance: 0.2 to 1.2 seconds on PC

with open(args[0]) as f:
    lines = [line.strip() for line in f]

SIZE = -1
def setGlobals(pzl):
    global ALPHABETSET, ALPHABET, SIZE, SIZESQRD, NBRLOOKUP, CONSTRAINTSETS, ITERLOOKUP, CONSTRMEMBERS

    oldSize = SIZE
    ALPHABETSET = set(pzl) - {"."}
    while len(ALPHABETSET)**2 < len(pzl): ALPHABETSET.add(min(set("123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")-ALPHABETSET))
    ALPHABET = "".join(sorted(list(ALPHABETSET)))
    SIZE = len(ALPHABET)
    SIZESQRD = SIZE**2
    if oldSize != SIZE:
        BOX_Y = int(SIZE**0.5)
        while SIZE%BOX_Y:
            BOX_Y -= 1
        BOX_X = SIZE // BOX_Y

        # creating the lookup tables
        rows = [set(range(SIZE*i, SIZE*(i+1))) for i in range(SIZE)]
        cols = [set(range(i, SIZESQRD, SIZE)) for i in range(SIZE)]
        boxes = []
        for startingRow in range(0, SIZE, BOX_Y):
            for startingCol in range(0, SIZE, BOX_X):
                boxes.append([y*SIZE+x for x in range(startingCol, startingCol+BOX_X) for y in range(startingRow, startingRow+BOX_Y)])
        CONSTRAINTSETS = rows + cols + boxes
        CONSTRMEMBERS = [{idx for idx,cset in enumerate(CONSTRAINTSETS) if j in cset} for j in range(SIZESQRD)]
        NBRLOOKUP = [{pos for ln in CONSTRAINTSETS if i in ln for pos in ln if pos != i} for i in range(SIZESQRD)]
        ITERLOOKUP = [[i for i in range(j, SIZESQRD)] + [i for i in range(0, j)] for j in range(SIZESQRD)]

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
    candidatesTable = [set() for i in range(SIZESQRD)]
    for testIndex in range(SIZESQRD): 
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
                
def updateTables(mainIndex, mainChar, candidatesTable, hiddenCounts, singles, hiddens):
    for nbr in NBRLOOKUP[mainIndex]:
        if mainChar in candidatesTable[nbr]:
            candidatesTable[nbr].remove(mainChar)
            if len(candidatesTable[nbr]) == 1:
                singles.add(nbr)
            for constrIdx in CONSTRMEMBERS[nbr]:
                hiddenCounts[mainChar][constrIdx] -= 1
                if hiddenCounts[mainChar][constrIdx] == 1: hiddens.add((constrIdx, mainChar))

    for char in candidatesTable[mainIndex]:
        for constrIdx in CONSTRMEMBERS[mainIndex]:
            hiddenCounts[char][constrIdx] -= 1
            if hiddenCounts[char][constrIdx] == 1: hiddens.add((constrIdx, char))
            
    candidatesTable[mainIndex] = set()
    for constrIdx in CONSTRMEMBERS[mainIndex]:
        hiddenCounts[mainChar][constrIdx] = SIZE+1
        if (constrIdx, mainChar) in hiddens:
            hiddens.remove((constrIdx, mainChar))
        
def bruteHelper(pzl, dotsLeft, prevIndex, candidatesTable, hiddenCounts, singles, hiddens):
    exhaustiveSet = []

    while True:
        if dotsLeft == 0: return pzl
        index = -1
        uniqueNext = False


        # find the best index to bifuricate on the value of a single cell
        minBranch = SIZESQRD
        if singles:
            index = singles.pop()
            minBranch = len(candidatesTable[index])
        elif not hiddens:
            for testIndex in ITERLOOKUP[prevIndex]:
                if pzl[testIndex] == ".":
                    if len(candidatesTable[testIndex]) < minBranch:
                        minBranch = len(candidatesTable[testIndex])
                        index = testIndex
                        if minBranch <= 2: break

        # find the best constraint set to bifuricate on the position of a value
        bestSet = set()
        bestCharacter = ""
        if minBranch > 1 and hiddens:
            setIdx, bestCharacter = hiddens.pop()
            minBranch = hiddenCounts[bestCharacter][setIdx]
            bestSet = CONSTRAINTSETS[setIdx]
        elif minBranch > 2:
            for character, ctList in hiddenCounts.items():
                for constraintIdx, numPositions in enumerate(ctList):
                    if numPositions < minBranch:
                        bestCharacter, setIdx = character, constraintIdx
                        minBranch = numPositions
                        bestSet = CONSTRAINTSETS[setIdx]
                        break
                    if minBranch <= 2: break
                if minBranch <= 2: break

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
            newCandidatesTable = [{*cSet} for cSet in candidatesTable]
            newHiddenCounts = {char:[*cts] for char,cts in hiddenCounts.items()}
            newPzl = pzl[:index] + character + pzl[(index+1):]
            newSingles = {i for i in singles}
            newHiddens = {i for i in hiddens}
            updateTables(index, character, newCandidatesTable, newHiddenCounts, newSingles, newHiddens)
            bF = bruteHelper(newPzl, dotsLeft-1, index, newCandidatesTable, newHiddenCounts, newSingles, newHiddens)
            if bF: return bF

        # Applying the main choice! Update the candidates table here
        pzl = pzl[:mainIndex] + mainChar + pzl[(mainIndex+1):]
        updateTables(mainIndex, mainChar, candidatesTable, hiddenCounts, singles, hiddens)
                    
        dotsLeft -= 1
        prevIndex = mainIndex
            
def bruteForce(pzl):
    for idx, val in enumerate(pzl):
        if val != ".":
            if val not in ALPHABET or not isValid(pzl, idx, val):
                return ""
    if "." not in pzl: return pzl
    candidatesTable = getCandidatesTable(pzl)
    hiddenCounts = getHiddenCounts(pzl, candidatesTable)
    return bruteHelper(pzl, pzl.count("."), 0, candidatesTable, hiddenCounts, {i for i in range(SIZESQRD) if len(candidatesTable[i]) == 1}, {(constrIdx, char) for constrIdx in range(len(CONSTRAINTSETS)) for char in ALPHABET if hiddenCounts[char][constrIdx] == 1})

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
