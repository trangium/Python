import sys; args=sys.argv[1:]
from time import perf_counter

start = perf_counter()
with open(args[0]) as f:
    lines1 = [line.strip() for line in f]
with open(args[1]) as f:
    lines2 = [line.strip() for line in f]
with open(args[2]) as f:
    lines3 = [line.strip() for line in f]

def main():
    res1 = len(set(lines2)&set(lines1))
    print(f"#1: {res1}")

    seen = set()
    res2 = 0
    notedNums = set()
    heap = []
    for num in map(int, lines1):
        if num not in seen and len(seen)%100 == 99:
            res2 += num
        seen.add(num)


        heap.append(num)
        k = len(heap)-1
        while k:
            parent = (k-1)//2
            if heap[k] < heap[parent]:
                heap[k], heap[parent] = heap[parent], heap[k]
                k = parent
            else: break
        if not num%53:
            while True:
                minElem = heap[0]
                heap[0] = heap[-1]
                k = 0
                while 2*k+1 < len(heap):
                    if len(heap) > 2*k+2 and heap[2*k+2] < heap[2*k+1]:
                        if heap[k] <= heap[2*k+2]: break
                        heap[k], heap[2*k+2] = heap[2*k+2], heap[k]
                        k = 2*k+2
                    else:
                        if heap[k] <= heap[2*k+1]: break
                        heap[k], heap[2*k+1] = heap[2*k+1], heap[k]
                        k = 2*k+1
                if minElem not in notedNums:
                    notedNums.add(minElem)
                    break
    print(f"#2: {res2}")

    lineDict3 = {}
    for numStr in lines3:
        if numStr in lineDict3:
            lineDict3[numStr] += 1
        else:
            lineDict3[numStr] = 1
    res3 = 0
    for numStr in lines1:
        res3 += (numStr in lineDict3) and lineDict3[numStr]
    for numStr in lines2:
        res3 += (numStr in lineDict3) and lineDict3[numStr]
    print(f"#3: {res3}")

    lineInts1Map = map(int, lines1)
    lineInts1 = set(lineInts1Map)
    res4 = []
    for num in lineInts1:
        res4.append(num)
        if len(res4) == 10:
            break
    print(f"#4: {res4}")

    appearedOnce = set()
    appearedTwice = set()
    maxTwice = 0
    for numStr in lines2:
        if numStr in appearedOnce:
            num = int(numStr)
            appearedTwice.add(num)
            maxTwice = max(num, maxTwice)
        else:
            appearedOnce.add(numStr)
    res5 = []
    while len(res5) < 10:
        if maxTwice in appearedTwice:
            res5.append(maxTwice)
        maxTwice -= 1
    print(f"#5: {res5}")


            
    print(f"#6: {sum(notedNums)}")

    
    elapsedTime = perf_counter()-start
    print(f"Total time: {elapsedTime:.4f}s")


if __name__ == "__main__":
    main()

# Vincent Trang, pd.4, 2023
