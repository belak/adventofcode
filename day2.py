total = 0
total_ribbon = 0

with open('input/day2') as f:
    while True:
        line = f.readline()
        if not line:
            break

        l, w, h = line.split('x')
        l, w, h = int(l), int(w), int(h)

        sides = [l*w, l*h, w*h]
        small = min(sides)

        #print('sides:', sides)
        #print('smallest side area:', small)
        #print('sum of sides:', sum(sides))

        ribbon_sides = [2*(l+w), 2*(l+h), 2*(w+h)]
        total_ribbon += min(ribbon_sides) + l*w*h

        total += (sum(sides) * 2 + small)

print('Wrapping paper needed:', total)
print('Ribbon needed:', total_ribbon)
