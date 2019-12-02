answer1 = 0
for l in open('input/day8'):
    l = l.strip()
    answer1 += len(l) - len(eval(l))

print(answer1)

answer2 = 0
for l in open('input/day8'):
    l = l.strip()
    answer2 += l.count('\\') + l.count('"') + 2

print(answer2)
