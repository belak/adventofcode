data = [list(map(int, line.split(' '))) for line in open('./input-2').readlines()]

total = 0
total2 = 0

def check_report(report):
    # If we check the report against the sorted and reverse-sorted lists we can
    # ensure it's either all ascending or decending.
    report_sorted = list(sorted(report))
    report_reversed = list(reversed(report_sorted))

    if report != report_sorted and report != report_reversed:
        return False

    prev = report[0]

    for curr in report[1:]:
        diff = abs(curr - prev)
        if diff < 1 or diff > 3:
            return False

        prev = curr

    return True

for (idx, report) in enumerate(data):
    if check_report(report):
        total += 1
        total2 += 1
        continue

    possible_reports = [
        check_report(report[:i] + report[i+1:])
        for i in range(len(report))
    ]
    if any(possible_reports):
        total2 += 1

print(total)
print(total2)
