def three_vowels(line):
    count = 0
    vowels = ['a', 'e', 'i', 'o', 'u']
    for vowel in vowels:
        count += line.count(vowel)

    if count < 3:
        return False

    return True

def double_letters(line):
    letters = ['aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz']
    for l in letters:
        if l in line:
            return True

    return False

def magic_strings(line):
    magic = ['ab', 'cd', 'pq', 'xy']
    for m in magic:
        if m in line:
            return False

    return True

matchers = [three_vowels, double_letters, magic_strings]

total = 0
naughty = 0

with open('input/day5') as f:
    for line in f:
        for matcher in matchers:
            if not matcher(line):
                naughty += 1
                break

        total += 1

print('naughty:', naughty)
print('nice:', total-naughty)

def double_str(line):
    for i, c in enumerate(line):
        if i > len(line)-2:
            break

        if line.count('{}{}'.format(c, line[i+1])) >= 2:
            return True

    return False

def sandwich(line):
    for i, c in enumerate(line):
        if i > len(line)-3:
            break

        if c == line[i+2]:
            return True

    return False

matchers = [double_str, sandwich]

total = 0
naughty = 0

with open('input/day5') as f:
    for line in f:
        for matcher in matchers:
            if not matcher(line):
                naughty += 1
                break

        total += 1

print('naughty:', naughty)
print('nice:', total-naughty)
