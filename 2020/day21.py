from collections import namedtuple

Item = namedtuple('Item', ('ingredients', 'allergens'))

lines = open("day21-input").read().splitlines()
data = []
for line in lines:
    ingredients, allergens = line.split(' (contains ')
    data.append(Item(set(ingredients.split(' ')), set(allergens[:-1].split(', '))))


# We use these in multiple places so pre-calculate them.
all_allergens = set()
all_ingredients = set()
for item in data:
    all_allergens = all_allergens.union(item.allergens)
    all_ingredients = all_ingredients.union(item.ingredients)


def build_allergen_map(data):
    allergen_map = {}

    # Every allergen can only be in one item, so we build a map containing all
    # possible allergens mapped to which ingredients they could be in.
    for allergen in all_allergens:
        # We start with all ingredients. For every item on the menu, if it
        # contains the allergen, we need to see which items intersect with the
        # previously determined possible items.
        possible = all_ingredients.copy()
        for item in data:
            if allergen in item.allergens:
                possible = possible.intersection(item.ingredients)

        allergen_map[allergen] = possible

    return allergen_map


def part1(data):
    allergen_map = build_allergen_map(data)

    # Combine all the possible allergens to find which items are maybe
    # allergens.
    maybe_allergens = set()
    for possible in allergen_map.values():
        maybe_allergens = maybe_allergens.union(possible)

    # Subtract ingredients which might have allergens from all ingredients to
    # find everything that's not an allergen.
    not_allergens = all_ingredients.difference(maybe_allergens)

    # Total up how many items in each set intersect with ingredients which
    # definitely aren't allergens.
    total = 0
    for item in data:
        total += len(item.ingredients.intersection(not_allergens))

    return total


def part2(data):
    allergen_map = build_allergen_map(data)

    # Find which allergens are found in which ingredients by finding which
    # allergens have only 1 possible ingredient and removing that ingredient
    # from all the other allergens.
    found = {}
    while len(allergen_map) > 0:
        # Find which allergens only have 1 ingredient.
        tmp = []
        for allergen, possible in allergen_map.items():
            if len(possible) == 1:
                found[allergen] = next(iter(possible))
                tmp += [allergen]

        # If there were no changes, this is an error.
        if len(tmp) == 0:
            return -1

        # Remove this item from the allergen map and remove this ingredient from
        # all the other allergen_map items.
        for item in tmp:
            del allergen_map[item]
            for possible in allergen_map.values():
                possible.discard(found[item])

    allergens = list(found.keys())
    allergens.sort()

    return ','.join(map(lambda key: found[key], allergens))


print("part1:", part1(data))
print("part2:", part2(data))
