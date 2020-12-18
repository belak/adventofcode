def get_input():
    data = open("day7-input").read().splitlines()

    ret = {}

    for item in data:
        key, inner = item.removesuffix(".").split(" bags contain ")

        ret[key] = {}

        if "no other" in inner:
            continue

        for bag in inner.split(", "):
            count, name = (
                bag.removesuffix("s").removesuffix(" bag").split(" ", maxsplit=1)
            )
            ret[key][name] = int(count)

    return ret


lines = get_input()


def handle_bags(data):
    cur_set = set(["shiny gold"])
    last_len = -1

    while True:
        if len(cur_set) == last_len:
            break

        last_len = len(cur_set)

        for search in list(cur_set):
            for key, val in data.items():
                if search in val:
                    cur_set.add(key)

    cur_set.remove("shiny gold")

    return cur_set


def calculate_depth(data, name):
    count = 1

    contained_bags = data[name]
    for bag, num in contained_bags.items():
        inner_count = calculate_depth(data, bag)

        count += num * inner_count

    return count


def part1(data):
    return len(handle_bags(data))


def part2(data):
    return calculate_depth(data, "shiny gold") - 1


print(part1(lines))
print(part2(lines))
