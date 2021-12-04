import numpy

data = open("day4-input").read().split("\n\n")

numbers = map(int, data[0].split(","))
boards = [
    numpy.array(list(list(map(int, line.split())) for line in board.splitlines()))
    for board in data[1:]
]

def board_complete(board):
    return 0 in board.sum(axis=0) or 0 in board.sum(axis=1)

def mark_number(boards, number):
    complete = []
    incomplete = []

    for idx in range(len(boards)):
        board = numpy.where(boards[idx] == number, 0, boards[idx])

        if board_complete(board):
            complete.append(board)
        else:
            incomplete.append(board)

    return complete, incomplete

# NOTE: We really want the scores of completed boards - the first one is part 1,
# the last one is part 2.
incomplete = boards
for number in numbers:
    complete, incomplete = mark_number(incomplete, number)
    for board in complete:
        print(board.sum() * number)
