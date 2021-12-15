from adventlib import load_list

data = load_list("day6-input")

timers = [data.count(i) for i in range(9)]

for i in range(256):
    # Day 1 asks for the answer after 80 days, but it's the same formula.
    if i == 80:
        print(sum(timers))

    zero_timers = timers.pop(0)
    timers.append(zero_timers)
    timers[6] += zero_timers

print(sum(timers))
