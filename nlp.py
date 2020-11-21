import json, math

with open("cmu.json", 'r') as f:
    CMU = json.load(f)

findWord = lambda x : CMU[x] if x in CMU else None

def interpretSound(sounds):

    possibilities = [[[], []]]

    for sound in sounds.split(' '):
        np = []
        for p in possibilities:
            if words := findWord(' '.join(p[0] + [sound])):
                np.append([[], p[1] + [words]])
            np.append([p[0] + [sound], p[1]])
        possibilities = np[:]
    
    return [p[1] for p in possibilities if not len(p[0])]

pos = interpretSound("W AY IH Z HH IY G R IY K")
print(pos)

for p in pos:
    toprint = []
    total = 0
    count = 1
    for w in p:
        likely = max(w, key = lambda x : w[x])
        toprint.append(likely)
        total += (w[likely] / 10000) ** 2
        count += 1 / count
    count -= 1
    print(' '.join(toprint), total / count)