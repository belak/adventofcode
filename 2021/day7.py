from adventlib import load_list


data = load_list("day7-input")

min_crab = min(data)
max_crab = max(data)

min_total = 9999999
min_part2_total = 99999999

for x in range(min_crab, max_crab + 1):
    total = 0
    part2_total = 0

    for crab in data:
        crab_total = abs(crab - x)

        # These are triangular numbers, so there's a constant-time calculation
        # for it: https://www.mathsisfun.com/algebra/triangular-numbers.html
        part2_crab_total = int(crab_total * (crab_total + 1) / 2)

        total += crab_total
        part2_total += part2_crab_total

    if total < min_total:
        min_total = total

    if part2_total < min_part2_total:
        min_part2_total = part2_total

print(min_total)
print(min_part2_total)
