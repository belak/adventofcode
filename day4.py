import hashlib

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

key = file_get_contents('input/day4').strip()

def find_suffix_for_prefix(key, prefix):
    x = 0
    while True:
        h = hashlib.md5()
        h.update('{}{}'.format(key, x).encode('ascii'))
        data = h.hexdigest()
        if data.startswith(prefix):
            break

        x += 1

    return x

print('00000:', find_suffix_for_prefix(key, '00000'))
print('000000:', find_suffix_for_prefix(key, '000000'))
