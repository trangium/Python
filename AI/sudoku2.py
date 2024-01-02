import sys; args=sys.argv[1:]
import time

with open(args[0]) as f:
    lines = [line.strip() for line in f]

def setGlobals(pzl):
    global ALPHABET, SIZE, LINELOOKUP
    
    ALPHABET = "".join(set(pzl) - {"."})
    if len(ALPHABET)**2 < len(pzl): ALPHABET += min(set("123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")-set(ALPHABET))
        
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
    LINES = rows + cols + boxes
    LINELOOKUP = [{pos for ln in LINES if i in ln for pos in ln if pos != i} for i in range(SIZE**2)]

def isValid(pzl, index, choice):
    for pos in LINELOOKUP[index]:
        if pzl[pos] == choice:
            return False
    return True
    
def bruteHelper(pzl, index):
    while pzl[index] != ".":
        index += 1
        if index == SIZE**2:
            return pzl
    for choice in ALPHABET:
        if isValid(pzl, index, choice):
            subPzl = pzl[:index] + choice + pzl[(index+1):]
            bF = bruteHelper(subPzl, index)
            if bF: return bF
    return ""

def bruteForce(pzl):
    for idx, val in enumerate(pzl):
        if val != ".":
            if val not in ALPHABET or not isValid(pzl, idx, val):
                return ""
    if "." not in pzl: return pzl
    return bruteHelper(pzl, 0)

def main():
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
        checksum = sum(ord(i)-ord(min(inp.replace(".",""))) for i in result)
        print(checksum, end=" ")
        print(round(finish-start, 4), "s\n\n", sep="")

if __name__ == "__main__":
    main()
    
# Vincent Trang, pd.4, 2023
