from itertools import count
from functools import reduce

lines = open("day13-input").read().splitlines()

target = int(lines[0])
lines = [int(line) if line != "x" else -1 for line in lines[1].split(",")]


def part1(target, data):
    max_ts_id = -1
    max_ts = 9999999999999
    for item in data:
        ts = item * (target // item + 1)
        if ts < max_ts:
            max_ts_id = item
            max_ts = ts

    return max_ts_id * (max_ts - target)


def part2(target, data):
    # The goal is to reduce all values down to one. We do this by starting at
    # what are essentially "identity" values and walking through the algorithm
    # with each value. This can alternatively be done by starting with cur and
    # step both set to data[0] (as well as iterating from index 1 in the list).
    #
    # For each offset/value combination, we find the point where the following
    # formula is evenly divisible by the target value. When that's found, we
    # update both cur and step.
    #
    # ```
    # (cur + i * step + offset)
    # ```
    #
    # Finally, we continue processing until there are no more values in the
    # list.

    cur = 1
    step = 1

    for offset, val in enumerate(data):
        # Skip timestamps where the schedule doesn't matter.
        if val == -1:
            continue

        # Loop through all starting points (cur + (i * step)) and check if this
        # offset/value combo is valid. If yes, we can reduce and move on,
        # otherwise continue looping.
        #
        # Cleverer people than me have used count(cur, step) (and resetting cur
        # to the current count) because that's exactly what this does without as
        # much code. I'm leaving this in its current form because this is how I
        # wrote it and it works.
        #
        # Essentially, all of this block can be shortened to this:
        #
        # ```
        # cur = next(p for p in count(cur, step) if (p + offset) % val == 0)
        # ```
        for i in count(1):
            if (cur + (i * step) + offset) % val == 0:
                cur += i * step
                break

        # My first attempt used cur and step as the same value, but this isn't
        # valid. I thought this would work because we can validly start with
        # data[0] as both cur and step. Unfortunately, we need to use the
        # product of all processed values up to this point as the step.
        #
        # My second attempt stored all completed values and multiplied them
        # together every time.
        #
        # This final version just keeps the running total of all the multiplied
        # values.
        step *= val

    return cur


print("part1:", part1(target, list(filter(lambda x: x != -1, lines))))
print("part2:", part2(target, lines))
