data = list(map(int, open("day6-input").read().split(',')))

timers = data.copy()

for i in range(80):
    # Step
    for i in range(len(timers)):
        if timers[i] == 0:
            timers.append(8)
            timers[i] = 7
        timers[i] -= 1

print(len(timers))

timers = {i: 0 for i in range(9)}
for item in data:
    timers[item] += 1

for i in range(256):
    zero_timers = timers[0]

    for j in range(8):
        timers[j] = timers[j+1]

    timers[6] += zero_timers
    timers[8] = zero_timers

print(sum(timers.values()))
