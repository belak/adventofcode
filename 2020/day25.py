card_pub, door_pub = list(map(int, open("day25-input").read().splitlines()))

def part1(card_pub, door_pub):
    card_priv = None
    for i in range(100000000):
        if pow(7, i, 20201227) == card_pub:
            card_priv = i
            break
    print(card_priv)

    # We only need to find one of the private keys for the encryption key
    # calculation, so there's no point in finding both.

    # door_priv = None
    # for i in range(100000000):
    #     if pow(7, i, 20201227) == door_pub:
    #         door_priv = i
    #         break
    # print(door_priv)

    return pow(door_pub, card_priv, 20201227)


def part2(card_pub, door_pub):
    return -1


print("part1:", part1(card_pub, door_pub))
print("part2:", part2(card_pub, door_pub))
