import re

data = [line for line in open("./input-4").readlines()]

total = 0
total2 = 0

allowed_words = ["XMAS", "SAMX"]

for i in range(len(data)):
    for j in range(len(data[i])):
        # Horizontal
        try:
            check = data[i][j] + data[i][j + 1] + data[i][j + 2] + data[i][j + 3]
            if check in allowed_words:
                total += 1
        except IndexError:
            pass

        # Vertical
        try:
            check = data[i][j] + data[i + 1][j] + data[i + 2][j] + data[i + 3][j]
            if check in allowed_words:
                total += 1
        except IndexError:
            pass

        # Diagonal
        try:
            check = (
                data[i][j]
                + data[i + 1][j + 1]
                + data[i + 2][j + 2]
                + data[i + 3][j + 3]
            )
            if check in allowed_words:
                total += 1
        except IndexError:
            pass

        try:
            check = (
                data[i][j]
                + data[i + 1][j - 1]
                + data[i + 2][j - 2]
                + data[i + 3][j - 3]
            )
            if check in allowed_words:
                total += 1
        except IndexError:
            pass

allowed_diags = ["MAS", "SAM"]

for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j] != "A":
            continue

        if i == 0 or i == len(data) - 1:
            continue

        if j == 0 or j == len(data[i]) - 1:
            continue

        d1 = data[i - 1][j - 1] + data[i][j] + data[i + 1][j + 1]
        d2 = data[i - 1][j + 1] + data[i][j] + data[i + 1][j - 1]
        if d1 in allowed_diags and d2 in allowed_diags:
            total2 += 1

print(total)
print(total2)
