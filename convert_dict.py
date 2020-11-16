import json

with open("cmu_dictionary.txt", 'r') as f:
    lines = f.read().split('\n')

with open("symbol.json", 'r') as f:
    SYMBOL = json.load(f)

def syllabalize(word):
    
    word = word.split(' ')
    i = 0

    while i < len(word):
        a = {
            "o": [],
            "n": [],
            "c": []
        }

        j = i

        # print("+", ' '.join(a["n"] + [word[i]]))

        while i < len(word) and ' '.join(a["o"] + [word[i]]) in SYMBOL["onset"].values():
            a["o"].append(word[i])
            i += 1
        
        while i < len(word) and ' '.join(a["n"] + [word[i]]) in SYMBOL["nucleus"].values():
            a["n"].append(word[i])
            i += 1
        
        while i < len(word) and ' '.join(a["c"] + [word[i]]) in SYMBOL["coda"].values():
            a["c"].append(word[i])
            i += 1
        
        if j == i:
            print()
            print(word)
            print(word[i])
            print(a)
            break
            
        if not len(a["n"]):
            if a["o"][-1] in "SLZRTD":
                a["n"] = a["o"][-1]
                del a["o"][-1]
        
        for p in a:
            a[p] = ' '.join(a[p])
        
        yield a

d = {}
bad = 0

for line in lines:
    try:
        a, b = line.split('\t', 1)
    except Exception:
        print(line)
        continue

    a = a.split('(')[0]
    b = b.replace("ER", "R")
    b = b.replace("DH", "TH")
    b = b.replace("HH W", "W")
    b = b.replace("L V TH", "L F TH")
    b = b.replace("D TH", "T TH")

    for syl in syllabalize(b):
        if syl["n"] == '':
            print(b)
            print(syl)
            bad += 1

    if b not in d:
        d[b] = []
    
    d[b].append(a)

print("BAD:", bad)

with open("cmu.json", 'w') as f:
    json.dump(d, f)