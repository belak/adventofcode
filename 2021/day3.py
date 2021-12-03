data = open('day3-input').read().splitlines()

combined = []
for _ in data[0]:
    combined.append({})

for line in data:
    for i, bit in enumerate(line):
        if bit not in combined[i]:
            combined[i][bit] = 0
        combined[i][bit] += 1

epsilon = ""
gamma = ""

for i in combined:
    #print(i)
    if i.get('0', 0) > i.get('1', 0):
        epsilon += '0'
        gamma += '1'
    else:
        epsilon += '1'
        gamma += '0'

print(int(epsilon, 2) * int(gamma, 2))

def bit_frequency_in_pos(data, pos):
    one = 0
    zero = 0
    for line in data:
        if line[pos] == '1':
            one += 1
        else:
            zero += 1

    if one > zero:
        return ('1', '0')
    elif zero > one:
        return ('0', '1')
    else:
        return ('1', '0')

oxygen_data = data.copy()
i = 0
while len(oxygen_data) > 1:
    most, _ = bit_frequency_in_pos(oxygen_data, i)
    oxygen_data = list(filter(lambda item: item[i] == most, oxygen_data))
    i += 1

carbon_data = data.copy()
i = 0
while len(carbon_data) > 1:
    _, least = bit_frequency_in_pos(carbon_data, i)
    carbon_data = list(filter(lambda item: item[i] == least, carbon_data))
    i += 1

print(int(oxygen_data[0], 2) * int(carbon_data[0], 2))
