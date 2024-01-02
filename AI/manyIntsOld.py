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
    prevTime = perf_counter()
    print(f"#0: Read files; {(prevTime-start):.3g}s")

    res1 = len(set(lines2)&set(lines1))
    print(f"#1: {res1}; {(-prevTime+(prevTime:=perf_counter())):.3g}s")

    seen = set()
    res2 = 0
    for num in lines1:
        if num not in seen and len(seen)%100 == 99:
            res2 += int(num)
        seen.add(num)
    print(f"#2: {res2}; {(-prevTime+(prevTime:=perf_counter())):.3g}s")

    lineset3 = set(lines3)
    res3 = 0
    for num in lines1:
        res3 += (num in lineset3)
    for num in lines2:
        res3 += (num in lineset3)
    print(f"#3: {res3}; {(-prevTime+(prevTime:=perf_counter())):.3g}s")

    lineInts1Map = map(int, lines1)
    lineInts1 = set(lineInts1Map)
    res4 = []
    for num in lineInts1:
        res4.append(num)
        if len(res4) == 10:
            break
    print(f"#4: {res4}; {(-prevTime+(prevTime:=perf_counter())):.3g}s")

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
    print(f"#5: {res5}; {(-prevTime+(prevTime:=perf_counter())):.3g}s")
    
    def heap_up(heap, k):
        if k:
            parent = (k-1)//2
            if heap[k] < heap[parent]:
                heap[k], heap[parent] = heap[parent], heap[k]
                heap_up(heap, parent)

    def insert(heap, elem):
        heap.append(elem)
        heap_up(heap, len(heap)-1)

    def heap_down(heap):
        k = 0
        while 2*k+1 < len(heap):
            if len(heap) > 2*k+2 and heap[2*k+2] < heap[2*k+1]:
                if heap[k] <= heap[2*k+2]: return
                heap[k], heap[2*k+2] = heap[2*k+2], heap[k]
                k = 2*k+2
            else:
                if heap[k] <= heap[2*k+1]: return
                heap[k], heap[2*k+1] = heap[2*k+1], heap[k]
                k = 2*k+1

    def remove_min(heap):
        heap[0] = heap[-1]
        heap.pop()
        heap_down(heap)

    def heapify(heap):
        for i in range(1, len(heap)):
            heap_up(heap, i)

    notedNums = set()
    heap = []
    for num in map(int, lines1):
        insert(heap, num)
        if not num%53:
            while True:
                minElem = heap[0]
                remove_min(heap)
                if minElem not in notedNums:
                    notedNums.add(minElem)
                    break
            
    print(f"#6: {sum(notedNums)}; {(-prevTime+(prevTime:=perf_counter())):.3g}s")

    
    elapsedTime = perf_counter()-start
    print(f"Total time: {elapsedTime:.3g}s")


if __name__ == "__main__":
    main()

# Vincent Trang, pd.4, 2023
