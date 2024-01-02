import sys; args=sys.argv[1:]
import time

# Performance: Q2 = 0.0001s
ALPHABET = "123456"
SIZE = 6
FULLSIZE = 24

# creating the lookup tables
LINES = [{0,1,2,6,7,8}, {2,3,4,8,9,10}, {5,6,7,12,13,14}, {7,8,9,14,15,16},
         {9,10,11,16,17,18}, {13,14,15,19,20,21}, {15,16,17,21,22,23}]
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
    
    print("",result[0:5])
    print(result[5:12])
    print(result[12:19])
    print("",result[19:24])
    
    print("\nTime: ", round(finish-start, 4), "seconds")

if __name__ == "__main__":
    main()
    
# Vincent Trang, pd.4, 2023
