data = [list(map(int, line.split("   "))) for line in open("./input-1").readlines()]

data1 = [line[0] for line in data]
data2 = [line[1] for line in data]
data1.sort()
data2.sort()

total = 0

for i, d1 in enumerate(data1):
    d2 = data2[i]
    total += abs(d1 - d2)

print(total)

total2 = 0
data2counter = {}
for d2 in data2:
    data2counter[d2] = data2counter.get(d2, 0) + 1

for i, d1 in enumerate(data1):
    total2 += d1 * data2counter.get(d1, 0)

print(total2)
