import re

YEAR_REGEX = re.compile(r"^\d\d\d\d$")
PID_REGEX = re.compile(r"^\d\d\d\d\d\d\d\d\d$")
HAIR_REGEX = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")
HEIGHT_REGEX = re.compile(r"^(\d+)(cm|in)")

EYE_COLORS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

lines = open("day4-input").read().split("\n\n")

data = []
for line in lines:
    cur = {}

    for item in line.split():
        key, val = item.split(":", 2)
        cur[key] = val

    data.append(cur)


def validate_year(raw_val, min_val, max_val):
    if raw_val is None:
        return False

    if YEAR_REGEX.match(raw_val) is None:
        return False

    val = int(raw_val)
    if not (min_val <= val <= max_val):
        return False

    return True


def validate_hgt(val):
    if val is None:
        return False

    hgt_match = HEIGHT_REGEX.match(val)
    if hgt_match is None:
        return False
    if hgt_match.group(2) == "cm" and not (150 <= int(hgt_match.group(1)) <= 193):
        return False
    if hgt_match.group(2) == "in" and not (59 <= int(hgt_match.group(1)) <= 76):
        return False

    return True


def validate_hcl(val):
    if val is None:
        return False

    if HAIR_REGEX.match(val) is None:
        return False

    return True


def validate_ecl(val):
    return val in EYE_COLORS


def validate_pid(val):
    if val is None:
        return False

    if PID_REGEX.match(val) is None:
        return False

    return True


def validate_cid(val):
    return True


# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)
# cid (Country ID)


validators = {
    "byr": lambda val: validate_year(val, 1920, 2002),
    "iyr": lambda val: validate_year(val, 2010, 2020),
    "eyr": lambda val: validate_year(val, 2020, 2030),
    "hgt": validate_hgt,
    "hcl": validate_hcl,
    "ecl": validate_ecl,
    "pid": validate_pid,
    #'cid': validate_cid,
}


def validate_part2_item(item):
    for key, validator in validators.items():
        if not validator(item.get(key)):
            return False

    return True


def validate_part1_item(item):
    for key in validators.keys():
        if item.get(key) is None:
            return False

    return True


def part1(data):
    count = 0
    for item in data:
        if validate_part1_item(item):
            count += 1

    return count


def part2(data):
    count = 0
    for item in data:
        if validate_part2_item(item):
            count += 1

    return count


print(part1(data))
print(part2(data))
