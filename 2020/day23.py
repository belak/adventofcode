cups = list(map(int, open("day23-input").read().strip()))


class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

    def __str__(self):
        ret = f"{self.val}"

        target_val = self.val
        cur = self.next

        while cur.val != target_val:
            ret += f"{cur.val}"
            cur = cur.next

        return ret


def run_cups(cups, iterations, mode=1):
    max_val = max(cups)
    min_val = min(cups)

    # Build both a lookup table (by value) and a circular buffer.
    lookup = {val: Node(val) for val in cups}
    for i, cup_val in enumerate(cups):
        cur_cup = lookup[cup_val]
        next_cup_val = cups[(i + 1) % len(cups)]
        next_cup = lookup[next_cup_val]
        cur_cup.next = next_cup

    # Start with the cup at index 0.
    cur = lookup[cups[0]]

    for move_num in range(1, iterations + 1):
        target = cur.val

        # Grab a reference to the next item
        pickup = cur.next

        # Remove the items which were picked up from the list
        cur.next = cur.next.next.next.next

        while target in [cur.val, pickup.val, pickup.next.val, pickup.next.next.val]:
            target -= 1
            if target < min_val:
                target = max_val

        # Append the cups that we picked up to the target location.
        loc = lookup[target]
        pickup.next.next.next = loc.next
        loc.next = pickup

        # Iterate
        cur = cur.next

    return lookup


def part1(cups):
    lookup = run_cups(cups, 100)
    return str(lookup[1])[1:]


def part2(cups):
    max_val = max(cups)
    extra_cups = list(range(max_val + 1, 1000001))
    lookup = run_cups(cups + extra_cups, 10000000)
    return lookup[1].next.val * lookup[1].next.next.val


print("part1:", part1(cups))
print("part2:", part2(cups))
