data = open("day16-input").read().split('\n\n')
limits = {}
my_ticket = list(map(int, data[1].splitlines()[1].split(',')))
nearby = [list(map(int, line.split(','))) for line in data[2].splitlines()[1:]]

for limit in data[0].splitlines():
    name, desc = limit.split(': ')
    limits[name] = list(map(lambda x: list(map(int, x.split('-'))), desc.split(' or ')))


def is_valid(limit, value):
    first = limit[0]
    second = limit[1]

    if (first[0] <= value <= first[1]) or (second[0] <= value <= second[1]):
        return True

    return False


def value_error_rate(limits, value):
    for limit in limits.values():
        if is_valid(limit, value):
            return 0

    return value


def ticket_error_rate(limits, ticket):
    error_rate = 0
    for value in ticket:
        error_rate += value_error_rate(limits, value)
    return error_rate


def part1(limits, my_ticket, nearby):
    error_rate = 0

    count = 0

    for ticket in nearby:
        tmp = ticket_error_rate(limits, ticket)
        if tmp == 0:
            count += 1

        error_rate += ticket_error_rate(limits, ticket)

    print(len(nearby))
    print(count)

    return error_rate


def part2(limits, my_ticket, nearby):
    # Filter out any ticket with an error rate of > 0
    nearby = [
        ticket for ticket in nearby
        if ticket_error_rate(limits, ticket) == 0
    ]

    print(len(nearby))

    # Start with an empty possible set for all positions
    leftover_limits = [set() for x in my_ticket]

    # For all possible keys
    for key in limits.keys():
        # Loop through all fields it could be in
        for i in range(len(my_ticket)):
            valid = True

            # If this limit at this position is valid for all tickets, add it to
            # the possible values.
            if not is_valid(limits[key], my_ticket[i]):
                valid = False

            for ticket in nearby:
                if not is_valid(limits[key], ticket[i]):
                    valid = False
                    break

            if valid:
                leftover_limits[i].add(key)

    limit_keys = {}
    #print(leftover_limits)

    while True:
        print(leftover_limits)

        changed = False
        tmp = []

        # For every possible ticket field, if there's only 1 possible limit we
        # know that's the right one.
        for i, item in enumerate(leftover_limits):
            if len(item) == 1:
                key = item.pop()
                limit_keys[key] = i
                tmp += [key]
                changed = True

        print('Removing', tmp)

        for item in leftover_limits:
            for limit in tmp:
                item.discard(limit)

        if not changed:
            break

    print(leftover_limits)

    print(limit_keys)

    ret = 1
    for key, loc in limit_keys.items():
        if not key.startswith('departure'):
            continue

        ret *= my_ticket[loc]

    return ret


print('part1:', part1(limits, my_ticket, nearby))
print('part2:', part2(limits, my_ticket, nearby))
