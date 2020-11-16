import json

with open("wordlist.txt", 'r') as f:
    lines = f.read().split('\n')

to_write = {}

for line in lines:
    if line == "":
        continue
    a, b = line.split('\t')[1:]
    to_write[a.lower()] = float(b)

with open("freq.json", 'w') as f:
    json.dump(to_write, f)