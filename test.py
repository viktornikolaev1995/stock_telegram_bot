import re

string = 'https://www.investing.com/equities/apple-computer-inc-company-profile'

pattern = re.compile(r'(.+)-company-profile')

match = re.findall(pattern, string)
print(match)

a = {1, 5}
b = {33, 455, 55, 66}

a.add(*b)

print(a)