import sys; args=sys.argv[1:]
import time

# Performance: Q3 = 3.5s to verify no solution
ALPHABET = "1234567"
SIZE = 7
FULLSIZE = 24

# creating the lookup tables
hexes = [{0,1,2,6,7,8}, {2,3,4,8,9,10}, {5,6,7,12,13,14}, {7,8,9,14,15,16},
         {9,10,11,16,17,18}, {13,14,15,19,20,21}, {15,16,17,21,22,23}]
rows = [{0,1,2,3,4}, {5,6,7,8,9,10,11}, {12,13,14,15,16,17,18}, {19,20,21,22,23},
        {1,0,6,5,12}, {3,2,8,7,14,13,19}, {4,10,9,16,15,21,20}, {11,18,17,23,22},
        {5,12,13,19,20}, {0,6,7,14,15,21,22}, {1,2,8,9,16,17,23}, {3,4,10,11,18}]
LINES = hexes + rows
LINELOOKUP = [{pos for ln in LINES if i in ln for pos in ln if pos != i} for i in range(SIZE**2)]

def isValid(pzl, index, choice):
    for pos in LINELOOKUP[index]:
        if pzl[pos] == choice:
            return False
    return True
    
def bruteHelper(pzl, index):
    while pzl[index] != ".":
        index += 1
        if index == FULLSIZE:
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
    inp = (args[0]+("."*FULLSIZE))[:FULLSIZE]
    print(inp, "\n")
    
    start = time.perf_counter()
    result = bruteForce(inp)
    finish = time.perf_counter()

    if result:    
        print("",result[0:5])
        print(result[5:12])
        print(result[12:19])
        print("",result[19:24])
    else:
        print("No solution")
    
    print("\nTime: ", round(finish-start, 4), "seconds")

if __name__ == "__main__":
    main()
    
# Vincent Trang, pd.4, 2023
