data = open('day4-input').read().split('\n\n')

numbers = map(int, data[0].split(','))
boards = []

for board in data[1:]:
    boards.append([list(map(int, line.split())) for line in board.splitlines()])

def board_complete(board):
    # Check rows
    for line in board:
        if line.count(None) == len(line):
            return True

    # Check cols
    for x in range(len(board[0])):
        valid = True
        for line in board:
            if line[x] != None:
                valid = False
                break

        if valid:
            return True

    return False

def total_board(board):
    return sum([sum(filter(lambda x: x is not None, line)) for line in board])

def mark_number(boards, number):
    complete = None

    for idx in range(len(boards)):
        boards[idx] = [
            list(map(lambda x: x if x != number else None, line)) for line in boards[idx]
        ]

        board = boards[idx]

        if board_complete(board):
            complete = board

    if complete is not None:
        total = total_board(complete)
        return boards, number * total

    return boards, None

def mark_number2(boards, number):
    for idx in range(len(boards)):
        boards[idx] = [
            list(map(lambda x: x if x != number else None, line)) for line in boards[idx]
        ]

    return boards, [board for board in boards if not board_complete(board)]

for number in numbers:
    boards, x = mark_number(boards, number)
    if x is not None:
        print(x)
        break

for number in numbers:
    all_boards, boards = mark_number2(boards, number)
    if len(all_boards) == 1 and len(boards) == 0:
        print(total_board(all_boards[0]) * number)
        break
