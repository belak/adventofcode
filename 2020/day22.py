players = open("day22-input").read().split("\n\n")
p1 = list(map(int, players[0].splitlines()[1:]))
p2 = list(map(int, players[1].splitlines()[1:]))


def part1(p1, p2):
    while len(p1) != 0 and len(p2) != 0:
        p1_card, p1 = p1[0], p1[1:]
        p2_card, p2 = p2[0], p2[1:]

        if p1_card > p2_card:
            p1 += [p1_card, p2_card]
        elif p2_card > p1_card:
            p2 += [p2_card, p1_card]
        else:
            raise Exception("cards equal")

    if len(p1) > 0:
        winner = p1
    else:
        winner = p2

    winner.reverse()

    return sum(map(lambda item: item[0] * item[1], enumerate(winner, start=1)))

    # return -1


def run_game(p1, p2):
    previous_rounds = set()
    while len(p1) != 0 and len(p2) != 0:
        cur_round_cards = (tuple(p1), tuple(p2))
        if cur_round_cards in previous_rounds:
            return "p1", p1
        previous_rounds.add(cur_round_cards)

        p1_card, p1 = p1[0], p1[1:]
        p2_card, p2 = p2[0], p2[1:]

        if len(p1) >= p1_card and len(p2) >= p2_card:
            winner_name, _ = run_game(p1[:p1_card], p2[:p2_card])
        else:
            if p1_card > p2_card:
                winner_name = 'p1'
            elif p2_card > p1_card:
                winner_name = 'p2'
            else:
                raise Exception("cards equal")

        if winner_name == 'p1':
            p1 += [p1_card, p2_card]
        elif winner_name == 'p2':
            p2 += [p2_card, p1_card]
        else:
            raise Exception("unknown winner")

    if len(p1) > 0:
        winner_name = 'p1'
        winner = p1
    else:
        winner_name = 'p2'
        winner = p2

    return winner_name, winner


def part2(p1, p2):
    _, winner = run_game(p1, p2)
    winner.reverse()
    return sum(map(lambda item: item[0] * item[1], enumerate(winner, start=1)))


print("part1:", part1(p1, p2))
print("part2:", part2(p1, p2))
