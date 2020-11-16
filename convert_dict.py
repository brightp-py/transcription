import json

with open("cmu_dictionary.txt", 'r') as f:
    lines = f.read().split('\n')

d = {}

for line in lines:
    a, b = line.split('\t', 1)

    a = a.split('(')[0]
    b = b.replace("ER", "R")

    if b not in d:
        d[b] = []
    
    d[b].append(a)

    if len(d[b]) > 1:
        print(d[b])

with open("cmu.json", 'w') as f:
    json.dump(d, f)