up = 0
down = 0

total = 0
count = 0

basement = None

with open('input/day1') as f:
    while True:
        c = f.read(1)
        if not c:
            break
        
        if c == '(':
            up += 1
            total += 1
        elif c == ')':
            down += 1
            total -= 1

        if total == -1 and basement is None:
            basement = up + down

print(up-down)
print(basement)
