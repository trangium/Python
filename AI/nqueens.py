import sys; args=sys.argv[1:]
import time

# Performance: 7x7 = 0.43 seconds, 8x8 = 2 minutes 46 seconds
ALPHABET = "1234567"
SIZE = len(ALPHABET)

# creating the lookup tables
rows = [set(range(SIZE*i, SIZE*(i+1))) for i in range(SIZE)]
cols = [set(range(i, SIZE**2, SIZE)) for i in range(SIZE)]
diag1 = [set(range(0, SIZE**2, SIZE+1))]
diag2 = [set(range(SIZE-1, SIZE**2-1, SIZE-1))]
LINES = rows + cols + diag1 + diag2
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
    args.append("")
    inp = (args[0]+("."*SIZE**2))[:SIZE**2]
    print(inp, "\n")
    
    start = time.perf_counter()
    result = bruteForce(inp)
    finish = time.perf_counter()
    if not result:
        print("No solution")
    while result:
        print(result[:SIZE])
        result = result[SIZE:]
    
    print("\nTime: ", round(finish-start, 4), "seconds")

if __name__ == "__main__":
    main()
    
# Vincent Trang, pd.4, 2023
