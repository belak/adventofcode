lines = [
    int(line)
    for line in open('input').read().splitlines()
]

def compute(lines):
    for line1 in lines:
        for line2 in lines:
            if line1 + line2 == 2020:
                return line1 * line2

def compute2(lines):
    for line1 in lines:
        for line2 in lines:
            for line3 in lines:
                if line1 + line2 + line3 == 2020:
                    return line1 * line2 * line3

print(compute(lines))
print(compute2(lines))
