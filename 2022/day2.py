from adventlib import AOC

# There's probably a better way to do this, but this is where my brain went.
#
# These are essentially lookup tables - wins mean "if we play key and they play
# value, we win". The _rev variants are inverted, so "if they play key and we
# play val, we win".
wins = {"X": "C", "Y": "A", "Z": "B"}
wins_rev = {v: k for k, v in wins.items()}
ties = {"X": "A", "Y": "B", "Z": "C"}
ties_rev = {v: k for k, v in ties.items()}
losses = {"X": "B", "Y": "C", "Z": "A"}
losses_rev = {v: k for k, v in losses.items()}
scores = {"X": 1, "Y": 2, "Z": 3}


class Day2(AOC):
    def process_input(self, raw_data):
        return [line.split(" ") for line in raw_data.strip().split("\n")]

    def part1(self):
        score = 0
        for val in self.data:
            them = val[0]
            us = val[1]
            score += scores[us]
            if wins[us] == them:
                score += 6
            elif losses[us] == them:
                score += 0
            else:
                score += 3
        return score

    def part2(self):
        score = 0
        for val in self.data:
            them = val[0]
            goal = val[1]

            if goal == "X":  # Lose
                us = losses_rev[them]
            elif goal == "Y":  # Draw
                us = ties_rev[them]
            elif goal == "Z":  # Win
                us = wins_rev[them]
            else:
                raise Exception("unknown goal")

            score += scores[us]
            if wins[us] == them:
                score += 6
            elif losses[us] == them:
                score += 0
            else:
                score += 3
        return score


if __name__ == "__main__":
    aoc = Day2()
    aoc.run()
