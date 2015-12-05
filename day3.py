from collections import defaultdict, namedtuple

class Actor:
    def __init__(self):
        self.x = 0
        self.y = 0

def gen_present_map(actor_count):
    count = 0
    data = defaultdict(lambda: 0)
    actors = []
    for _ in range(actor_count):
        actors.append(Actor())

    with open('input/day3') as f:
        while True:
            c = f.read(1)
            if not c:
                break

            a = count%len(actors)

            if c == '^':
                actors[a].y += 1
            elif c == '>':
                actors[a].x += 1
            elif c == 'v':
                actors[a].y -= 1
            elif c == '<':
                actors[a].x -= 1

            data['%dx%d' % (actors[a].x, actors[a].y)] += 1
            count += 1

    return data

print('santa alone:', len(gen_present_map(1)))
print('santa with robot:', len(gen_present_map(2)))
