def valid1(code):
    doubles = False
    last_c = ""
    for c in str(code):
        if c < last_c:
            return False
        if c == last_c:
            doubles = True
        else:
            last_c = c

    return doubles

def valid2(code):
    doubles = False
    last_c = ""
    last_count = 1
    for c in str(code):
        if c < last_c:
            return False
        if c == last_c:
            last_count = last_count + 1
        else:
            if last_count == 2:
                doubles = True
            last_count = 1
            last_c = c

    if last_count == 2:
        doubles = True

    return doubles

def valid_codes(start, end, valid_function):
    count = 0
    for code in range(start, end + 1):
        if valid_function(code):
            count = count + 1

    return count

assert valid1(122345) == True
assert valid1(111123) == True
assert valid1(135679) == False
assert valid1(111111) == True
assert valid1(223450) == False
assert valid1(123789) == False

assert valid2(112233) == True
assert valid2(123444) == False
assert valid2(111122) == True

print(valid_codes(165432, 707912, valid1))
print(valid_codes(165432, 707912, valid2))
