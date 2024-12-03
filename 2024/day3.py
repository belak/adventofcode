import re

data = [line for line in open('./input-3').readlines()]

MUL_RE = re.compile(r'mul\((\d+),(\d+)\)')
FULL_RE = re.compile(r'(do)\(\)|(don\'t)\(\)|mul\((\d+),(\d+)\)')

total = 0
total2 = 0
enabled = True
for line in data:
    for (a, b) in MUL_RE.findall(line):
        total += int(a) * int(b)

    for (do, do_not, a, b) in FULL_RE.findall(line):
        if do == "do":
            enabled = True
        elif do_not == "don't":
            enabled = False
        elif enabled:
            total2 += int(a) * int(b)

print(total)
print(total2)
