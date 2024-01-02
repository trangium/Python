print("loading...\n")

with open("words_alpha.txt") as f:
    words = [line.strip() for line in f]

with open("words_freq.txt") as f:
    freqs = [((a:=line.strip().split("\t"))[0], int(a[1])) for line in f]

import random, time, collections



cnt = collections.Counter()
def subs(word):
    ya = set()
    for i in range(len(word)):
        for j in range(len(word)):
            if 0 < j-i <= 4:
                ya.add(word[i:j])
    return ya

for word, freq in freqs:
    for sub in subs(word):
        cnt[sub] += freq**(1/3)
L = cnt.most_common(len(cnt))

def suggest(sub):
    return [k for k,v in freqs if sub.upper() in k]

def main():
    start = time.time()
    letters = set("abcdefghijklmnopqrstuvwxyz")
    guesses = 0 # includes guessed words and skips
    skips = 0
    indexHM = 0
    while letters:
        index = random.randint(83, 2082)
        indexHM += 1/index
        guesses += 1
        pr = L[index]
        print("\n"+pr[0].lower(),"\tindex:", index, "\t", "".join(sorted(letters)))
        while pr[0] not in (a:=input()).upper() or a not in words or a == pr[0].lower():
            if not a:
                print(suggest(pr[0])[:12])
                skips += 1
                break
            else:
                print("--")
        for char in a:
            letters = letters - {char}
    print("\nWords:", guesses)
    print("Skips:", skips)
    print("Difficulty:", round(diff:=(guesses/indexHM)))
    print("Time: ", round(elapsed:=(time.time()-start), 2))
    print("\nScore:", round(guesses+2*skips+((32805/32768)**(-diff)), 3))

if __name__ == "__main__":
    main()
